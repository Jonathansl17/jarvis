"""Data: how to rephrase a reply for each detected emotion."""

from dataclasses import dataclass

from app.emotion.protocol import Emotion


@dataclass(frozen=True)
class ToneRule:
    """Spanish phrasing pieces wrapped around a reply for one emotion.

    `terse` marks emotions where the reply should be kept to its first
    sentence instead of being wrapped in full, per the "calm and short"
    style requested for an already-angry user.
    """

    prefix: str
    suffix: str
    terse: bool = False


TONE_RULES: dict[Emotion, ToneRule] = {
    Emotion.ANGRY: ToneRule(prefix="Tranquilo, ", suffix="", terse=True),
    Emotion.DISGUST: ToneRule(prefix="¡Wákala! Esa cara lo dice todo. ", suffix=" Espero que esto no te dé más asco."),
    Emotion.FEAR: ToneRule(prefix="No te preocupes, ", suffix=" Estoy aquí para ayudarte."),
    Emotion.HAPPY: ToneRule(prefix="¡Genial! ", suffix=" Me alegra verte contento."),
    Emotion.SAD: ToneRule(prefix="", suffix=" Aquí estoy si necesitas algo más."),
    Emotion.SURPRISE: ToneRule(prefix="¡Vaya! ", suffix=""),
    Emotion.NEUTRAL: ToneRule(prefix="", suffix=""),
}
