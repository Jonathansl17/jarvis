"""Resolves the emotion the avatar actually displays for a detected one —
a tiny wrapper around `mirroring.map_emotion_to_avatar` that also handles
"no emotion detected" (`None`), used by both the animator's idle-loop
selection and its reaction-transition trigger.
"""

from app.emotion.protocol import Emotion
from app.ui.avatar.mirroring import map_emotion_to_avatar


def displayed_emotion(emotion: Emotion | None) -> Emotion | None:
    """The emotion the avatar shows for `emotion` (mirroring policy
    applied), or `None` if `emotion` is `None`."""
    return map_emotion_to_avatar(emotion) if emotion is not None else None
