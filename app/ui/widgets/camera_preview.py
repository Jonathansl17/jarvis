"""Hosts the camera card's video feed and emotion-word label (§8).

Implemented as a `CTkFrame` rather than a bare `CTkLabel` (a deviation from
the architecture plan's sketch) because §8 requires two stacked elements —
the video image and, 8px below it, the emotion-word label — which a single
label cannot host; `update_sample`/`show_disabled` keep the plan's method
contract.
"""

import customtkinter as ctk
from PIL import Image

from app.emotion.protocol import Emotion
from app.emotion.spanish_labels import EMOTION_LABELS_ES, NO_FACE_TEXT
from app.ui import strings, theme
from app.ui.camera_render import VIDEO_HEIGHT_PX, VIDEO_WIDTH_PX, render_camera_frame
from app.ui.theme import Fonts
from app.workers.camera_worker import CameraSample

_VIDEO_EMOTION_GAP_PX = 8


class CameraPreview(ctk.CTkFrame):
    """Shows a mirrored, cropped webcam feed plus the detected emotion word."""

    def __init__(self, master: ctk.CTkBaseClass, fonts: Fonts, **kwargs: object) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._video_label = ctk.CTkLabel(
            self,
            text="",
            fg_color=theme.COLOR_BG_CARD_ELEVATED,
            width=VIDEO_WIDTH_PX,
            height=VIDEO_HEIGHT_PX,
        )
        self._video_label.pack()
        self._emotion_label = ctk.CTkLabel(
            self, text=strings.CAMERA_DISABLED_LABEL, font=fonts.emotion_word, text_color=theme.COLOR_TEXT_SECONDARY
        )
        self._emotion_label.pack(pady=(_VIDEO_EMOTION_GAP_PX, 0))

    def show_disabled(self) -> None:
        """Clear the video image and show the disabled placeholder text."""
        self._video_label.configure(image=None)
        self._emotion_label.configure(text=strings.CAMERA_DISABLED_LABEL, text_color=theme.COLOR_TEXT_SECONDARY)

    def update_sample(self, sample: CameraSample | None) -> None:
        """Render the sampled frame and update the emotion-word label."""
        if sample is None:
            return
        self._show_video(render_camera_frame(sample.frame, sample.box, sample.reading))
        self._emotion_label.configure(**_emotion_label_kwargs(sample.reading))

    def _show_video(self, image: Image.Image) -> None:
        """Wrap a rendered video frame as a `CTkImage` and display it."""
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(VIDEO_WIDTH_PX, VIDEO_HEIGHT_PX))
        self._video_label.configure(image=ctk_image)


def _emotion_label_kwargs(reading: tuple[Emotion, float] | None) -> dict[str, str]:
    """Build the emotion-word label's text and color for one reading."""
    if reading is None:
        return {"text": NO_FACE_TEXT.upper(), "text_color": theme.COLOR_TEXT_SECONDARY}
    emotion, _confidence = reading
    color = theme.EMOTION_LABEL_COLORS[emotion.value]
    return {"text": EMOTION_LABELS_ES[emotion].upper(), "text_color": color}
