"""Per-emotion idle loop frame tables, one module per emotion (its own file
so each stays within the project's file-size limit and each emotion's data
table is easy to find). `idle_frames.py` concatenates all six into the flat
`IDLE_FRAMES` tuple and works out each one's start index there.
"""

from app.ui.avatar.loops.angry import ANGRY_FRAMES
from app.ui.avatar.loops.disgust import DISGUST_FRAMES
from app.ui.avatar.loops.fear import FEAR_FRAMES
from app.ui.avatar.loops.happy import HAPPY_FRAMES
from app.ui.avatar.loops.sad import SAD_FRAMES
from app.ui.avatar.loops.surprise import SURPRISE_FRAMES

__all__ = [
    "ANGRY_FRAMES",
    "DISGUST_FRAMES",
    "FEAR_FRAMES",
    "HAPPY_FRAMES",
    "SAD_FRAMES",
    "SURPRISE_FRAMES",
]
