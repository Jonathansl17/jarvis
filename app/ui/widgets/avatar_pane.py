"""Hosts the animated procedural penguin avatar (§7 of the design spec)."""

import customtkinter as ctk
from PIL import Image

from app.emotion.protocol import Emotion
from app.ui.avatar.animator import AvatarAnimator
from app.ui.avatar.expressions import Expression, resolve_expression
from app.ui.avatar.renderer import render_pose
from app.ui.avatar.spec import POSES, AvatarState

_AVATAR_SIZE_PX = (200, 200)

_FrameKey = tuple[AvatarState, int, Emotion | None]


class AvatarPane(ctk.CTkLabel):
    """A `CTkLabel` that shows the avatar's current animated frame."""

    def __init__(self, master: ctk.CTkBaseClass, **kwargs: object) -> None:
        super().__init__(master, text="", **kwargs)
        self._image_cache: dict[_FrameKey, Image.Image] = {}
        self._animator = AvatarAnimator(
            schedule=self.after, render=self._render_frame, on_frame=self._show_frame
        )
        self._animator.set_state(AvatarState.IDLE)

    def set_state(self, state: AvatarState) -> None:
        """Switch the avatar's behavioral state (idle/listening/thinking/speaking)."""
        self._animator.set_state(state)

    def set_emotion(self, emotion: Emotion | None) -> None:
        """Update the emotion overlaid on the avatar's current state."""
        self._animator.set_emotion(emotion)

    def destroy(self) -> None:
        """Stop the animation timer before the widget is torn down."""
        self._animator.stop()
        super().destroy()

    def _render_frame(self, state: AvatarState, frame_index: int, emotion: Emotion | None) -> Image.Image:
        """Render (or reuse a cached render of) one `(state, frame, emotion)` combo."""
        key = (state, frame_index, emotion)
        cached = self._image_cache.get(key)
        if cached is not None:
            return cached
        pose = POSES[state][frame_index]
        expression: Expression | None = resolve_expression(emotion) if emotion is not None else None
        image = render_pose(pose, expression, _AVATAR_SIZE_PX)
        self._image_cache[key] = image
        return image

    def _show_frame(self, image: Image.Image) -> None:
        """Wrap a rendered frame as a `CTkImage` and display it."""
        self.configure(image=ctk.CTkImage(light_image=image, dark_image=image, size=_AVATAR_SIZE_PX))
