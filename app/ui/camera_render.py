"""Pure: one webcam frame + detected face box -> a displayable `PIL.Image`,
per §8's camera card spec (center-cropped to 4:3, mirrored, cyan reticle).

No `customtkinter`/`tkinter` import — the emotion word shown under the video
is a separate `CTkLabel` the widget updates itself from the same `reading`.
"""

import cv2
import numpy as np
import numpy.typing as npt
from PIL import Image

from app.emotion.face_locator import BoundingBox
from app.emotion.protocol import Emotion

VIDEO_WIDTH_PX = 368
VIDEO_HEIGHT_PX = 276
# `#2DE2C9` in BGR order, since `cv2.rectangle` expects BGR (§8, §16).
FACE_BOX_COLOR_BGR = (201, 226, 45)
FACE_BOX_THICKNESS_PX = 3


def render_camera_frame(
    frame: npt.NDArray[np.uint8],
    box: BoundingBox | None,
    reading: tuple[Emotion, float] | None,
) -> Image.Image:
    """Center-crop to 4:3, mirror, draw the face box, and resize to the card."""
    del reading  # Formatted into the emotion-word label by the widget instead.
    cropped, crop_x = _center_crop_to_4_3(frame)
    mirrored = cv2.flip(cropped, 1)
    if box is not None:
        _draw_face_box(mirrored, _mirror_box(box, crop_x, cropped.shape[1]))
    resized = cv2.resize(mirrored, (VIDEO_WIDTH_PX, VIDEO_HEIGHT_PX), interpolation=cv2.INTER_AREA)
    return Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))


def _center_crop_to_4_3(frame: npt.NDArray[np.uint8]) -> tuple[npt.NDArray[np.uint8], int]:
    """Crop `frame` to a 4:3 aspect ratio, centered; return it with its x offset."""
    height, width = frame.shape[:2]
    target_width = round(height * VIDEO_WIDTH_PX / VIDEO_HEIGHT_PX)
    if target_width >= width:
        return frame, 0
    crop_x = (width - target_width) // 2
    return frame[:, crop_x : crop_x + target_width], crop_x


def _mirror_box(box: BoundingBox, crop_x: int, cropped_width: int) -> BoundingBox:
    """Shift `box` into crop-relative coordinates, then mirror it horizontally."""
    x = box.x - crop_x
    mirrored_x = cropped_width - x - box.width
    return BoundingBox(x=mirrored_x, y=box.y, width=box.width, height=box.height)


def _draw_face_box(frame: npt.NDArray[np.uint8], box: BoundingBox) -> None:
    """Draw the cyan HUD reticle around `box`, in place."""
    top_left = (box.x, box.y)
    bottom_right = (box.x + box.width, box.y + box.height)
    cv2.rectangle(frame, top_left, bottom_right, FACE_BOX_COLOR_BGR, FACE_BOX_THICKNESS_PX)
