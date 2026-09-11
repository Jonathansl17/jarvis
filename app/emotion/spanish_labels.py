"""Spanish-language display strings for the emotion vocabulary, shared by
every UI surface that shows a detected emotion to the user.
"""

from app.emotion.protocol import Emotion

EMOTION_LABELS_ES: dict[Emotion, str] = {
    Emotion.ANGRY: "enojado",
    Emotion.DISGUST: "disgusto",
    Emotion.FEAR: "miedo",
    Emotion.HAPPY: "feliz",
    Emotion.SAD: "triste",
    Emotion.SURPRISE: "sorpresa",
    Emotion.NEUTRAL: "neutral",
}

# Shown when the camera is on but no face is currently detected.
NO_FACE_TEXT = "sin rostro"
