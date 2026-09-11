"""The webcam-emotion-to-avatar-reaction mirroring policy: which emotion the
avatar displays for a detected one, and which of those trigger its one-time
post-reply hop.

`map_emotion_to_avatar()` is the one function that may branch on emotion
strings for this mapping — nothing else special-cases it, per the design
spec's explicit instruction.
"""

from app.emotion.protocol import Emotion

# Whether angry/disgust ever reflect back at the user as themselves, or
# always mirror as neutral instead. Angry's own pose (steam puff, red
# cheeks, ...) still exists in `expressions.EXPRESSIONS` either way — this
# flag only controls what the avatar *displays* for a detected angry/disgust
# frame.
MIRROR_HOSTILE_EMOTIONS = True

_HOSTILE_TO_NEUTRAL = {
    Emotion.ANGRY: Emotion.NEUTRAL if MIRROR_HOSTILE_EMOTIONS else Emotion.ANGRY,
    Emotion.DISGUST: Emotion.NEUTRAL if MIRROR_HOSTILE_EMOTIONS else Emotion.DISGUST,
}

# Detected emotion -> what the avatar shows.
_AVATAR_EMOTION_FOR: dict[Emotion, Emotion] = {
    Emotion.HAPPY: Emotion.HAPPY,
    Emotion.SAD: Emotion.SAD,
    Emotion.SURPRISE: Emotion.SURPRISE,
    Emotion.FEAR: Emotion.SURPRISE,
    Emotion.NEUTRAL: Emotion.NEUTRAL,
    Emotion.ANGRY: _HOSTILE_TO_NEUTRAL[Emotion.ANGRY],
    Emotion.DISGUST: _HOSTILE_TO_NEUTRAL[Emotion.DISGUST],
}


def map_emotion_to_avatar(emotion: Emotion) -> Emotion:
    """Return the emotion the avatar should display for a detected `emotion`."""
    return _AVATAR_EMOTION_FOR[emotion]


# Emotions that trigger the avatar's one-time post-reply hop; a subset of
# the mirroring table above, not a policy of its own.
HOP_TRIGGER_EMOTIONS = frozenset({Emotion.HAPPY, Emotion.SURPRISE})
