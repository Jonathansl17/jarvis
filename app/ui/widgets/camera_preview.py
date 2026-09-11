"""Renders the latest webcam frame as a full-frame half-block mirror image,
plus a status row naming the detected emotion in Spanish."""

import cv2
import numpy as np
import numpy.typing as npt
from rich.style import Style
from rich.text import Text
from textual.widgets import Static

from app.emotion.face_locator import BoundingBox
from app.emotion.spanish_labels import EMOTION_LABELS_ES, NO_FACE_TEXT
from app.workers.emotion_sampling import EmotionReading, EmotionSample

_GRID_COLUMNS = 38
_GRID_ROWS = 16
# Each character cell shows two vertically stacked pixels via a half-block
# glyph: its foreground colors the top pixel, its background the bottom one.
_PIXEL_ROWS = _GRID_ROWS * 2
_HALF_BLOCK = "▀"
_DISABLED_LABEL = "cámara apagada"
_FACE_BOX_COLOR = "#59F2C4"
_STATUS_LINE_TEMPLATE = "{label} {confidence:.0f} %"
_CONFIDENCE_PERCENT_SCALE = 100


class CameraPreview(Static):
    """Shows a downscaled, mirrored webcam preview, or a disabled label."""

    def on_mount(self) -> None:
        self.show_disabled()

    def show_disabled(self) -> None:
        """Show the centered placeholder for when the camera is off."""
        self.update(_DISABLED_LABEL)

    def update_sample(self, sample: EmotionSample | None) -> None:
        """Render the sampled frame, its detected face box, and its reading."""
        if sample is None:
            return
        self.update(_render_frame(sample.frame, sample.box, sample.reading))


def _render_frame(
    frame: npt.NDArray[np.uint8], box: BoundingBox | None, reading: EmotionReading
) -> Text:
    """Build the mirrored half-block preview, its face box, and status line."""
    pixels = _downscale_and_mirror(frame)
    grid_box = _scale_box(box, frame.shape[1], frame.shape[0]) if box is not None else None
    text = _build_half_block_text(pixels, grid_box)
    text.append(_status_line(reading).center(_GRID_COLUMNS))
    return text


def _status_line(reading: EmotionReading) -> str:
    """Build the emotion status text shown under the preview grid."""
    if reading is None:
        return NO_FACE_TEXT
    emotion, confidence = reading
    percent = confidence * _CONFIDENCE_PERCENT_SCALE
    return _STATUS_LINE_TEMPLATE.format(label=EMOTION_LABELS_ES[emotion], confidence=percent)


def _downscale_and_mirror(frame: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    """Resize to the preview's pixel grid and mirror it like a mirror."""
    resized = cv2.resize(
        frame, (_GRID_COLUMNS, _PIXEL_ROWS), interpolation=cv2.INTER_AREA
    )
    mirrored = cv2.flip(resized, 1)
    return cv2.cvtColor(mirrored, cv2.COLOR_BGR2RGB)


def _scale_box(box: BoundingBox, frame_width: int, frame_height: int) -> BoundingBox:
    """Scale a face box from frame pixels to the preview's character grid."""
    scale_x = _GRID_COLUMNS / frame_width
    scale_y = _GRID_ROWS / frame_height
    width = max(1, round(box.width * scale_x))
    height = max(1, round(box.height * scale_y))
    x = round(box.x * scale_x)
    mirrored_x = max(0, min(_GRID_COLUMNS - width, _GRID_COLUMNS - x - width))
    y = max(0, min(_GRID_ROWS - height, round(box.y * scale_y)))
    return BoundingBox(x=mirrored_x, y=y, width=width, height=height)


def _build_half_block_text(pixels: npt.NDArray[np.uint8], box: BoundingBox | None) -> Text:
    """Pair each two pixel rows into one styled half-block character row."""
    text = Text()
    for row in range(_GRID_ROWS):
        top, bottom = pixels[row * 2], pixels[row * 2 + 1]
        for col in range(_GRID_COLUMNS):
            style = _cell_style((top[col], bottom[col]), (row, col), box)
            text.append(_HALF_BLOCK, style=style)
        text.append("\n")
    return text


def _cell_style(
    pixel_pair: tuple[npt.NDArray[np.uint8], npt.NDArray[np.uint8]],
    position: tuple[int, int],
    box: BoundingBox | None,
) -> Style:
    """Tint a cell in the face-box accent color if it sits on its border."""
    if box is not None and _on_box_border(position, box):
        return Style(color=_FACE_BOX_COLOR, bgcolor=_FACE_BOX_COLOR)
    top_pixel, bottom_pixel = pixel_pair
    return Style(color=_rgb(top_pixel), bgcolor=_rgb(bottom_pixel))


def _on_box_border(position: tuple[int, int], box: BoundingBox) -> bool:
    """Return whether grid cell `position` (row, col) sits on `box`'s perimeter."""
    row, col = position
    left, top = box.x, box.y
    right, bottom = box.x + box.width - 1, box.y + box.height - 1
    within_rows, within_cols = top <= row <= bottom, left <= col <= right
    return (within_rows and col in (left, right)) or (within_cols and row in (top, bottom))


def _rgb(pixel: npt.NDArray[np.uint8]) -> str:
    """Format an RGB pixel as a Rich `rgb(r,g,b)` color string."""
    return f"rgb({pixel[0]},{pixel[1]},{pixel[2]})"
