"""`EmotionDetector` implementation backed by a local ONNX classifier."""

from pathlib import Path

import cv2
import numpy as np
import numpy.typing as npt
import onnxruntime as ort

from app.constants import ONNX_INTRA_OP_THREADS, EMOTION_INPUT_SIZE_PX
from app.emotion.face_locator import BoundingBox, FaceLocator
from app.emotion.protocol import Detection, Emotion
from app.errors import EmotionDetectionError

_PIXEL_FULL_SCALE = 255.0


class OnnxEmotionDetector:
    """Classifies the emotion of the largest face found in a frame."""

    def __init__(self, model_path: Path, face_locator: FaceLocator) -> None:
        self._face_locator = face_locator
        try:
            options = ort.SessionOptions()
            options.intra_op_num_threads = ONNX_INTRA_OP_THREADS
            self._session = ort.InferenceSession(
                str(model_path), sess_options=options, providers=["CPUExecutionProvider"]
            )
        except Exception as exc:  # onnxruntime raises its own Fail/RuntimeException types
            raise EmotionDetectionError(f"Failed to load emotion model at '{model_path}'") from exc

        self._input_name = self._session.get_inputs()[0].name

    def detect(self, frame: npt.NDArray[np.uint8]) -> Detection | None:
        """Return the dominant emotion in `frame` with its location, or `None`."""
        box = self._face_locator.locate(frame)
        if box is None:
            return None

        face_input = self._preprocess(frame, box)
        try:
            scores = self._session.run(None, {self._input_name: face_input})[0][0]
        except Exception as exc:  # onnxruntime raises its own Fail/RuntimeException types
            raise EmotionDetectionError("Failed to classify face crop") from exc

        probabilities = _softmax(scores)
        index = int(np.argmax(probabilities))
        emotion = list(Emotion)[index]
        return Detection(box=box, emotion=emotion, confidence=float(probabilities[index]))

    def _preprocess(
        self, frame: npt.NDArray[np.uint8], box: BoundingBox
    ) -> npt.NDArray[np.float32]:
        """Crop, resize, and normalize a detected face for the model's input."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        crop = gray[box.y : box.y + box.height, box.x : box.x + box.width]
        resized = cv2.resize(crop, (EMOTION_INPUT_SIZE_PX, EMOTION_INPUT_SIZE_PX))
        normalized = resized.astype(np.float32) / _PIXEL_FULL_SCALE
        return normalized.reshape(1, EMOTION_INPUT_SIZE_PX, EMOTION_INPUT_SIZE_PX, 1)


def _softmax(scores: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    """Return `scores` normalized into a probability distribution."""
    shifted = scores - np.max(scores)
    exponentials = np.exp(shifted)
    return exponentials / np.sum(exponentials)
