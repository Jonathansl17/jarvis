"""Extracts cirrhosis_type_classification fields from Spanish free text."""

from typing import Any, ClassVar

from app.intents.rules.base import find_literal, find_number_near

_AGE_KEYWORDS = ("años", "anos", "edad")
_SEX_ALIASES = {"M": ("hombre", "masculino", "varon", "varón"), "F": ("mujer", "femenino")}
_EDEMA_ALIASES = {
    "Y": ("edema presente", "con edema", "edema: si"),
    "S": ("edema leve", "edema moderado"),
    "N": ("sin edema", "no edema"),
}

_ASCITES_ALIASES = {"Y": ("con ascitis",), "N": ("sin ascitis",)}
_HEPATOMEGALY_ALIASES = {"Y": ("con hepatomegalia",), "N": ("sin hepatomegalia",)}
_SPIDERS_ALIASES = {"Y": ("con arañas vasculares", "con aranas vasculares"), "N": ("sin arañas vasculares",)}
_DRUG_ALIASES = {"D-penicillamine": ("penicilamina",), "Placebo": ("placebo",)}
_OPTIONAL_NUMBER_KEYWORDS: dict[str, tuple[str, ...]] = {
    "bilirubin": ("bilirrubina",),
    "cholesterol": ("colesterol",),
    "albumin": ("albumina", "albúmina"),
    "copper": ("cobre",),
    "alk_phos": ("fosfatasa alcalina",),
    "sgot": ("sgot",),
    "tryglicerides": ("trigliceridos", "triglicéridos"),
    "platelets": ("plaquetas",),
    "prothrombin": ("protrombina",),
}


class CirrhosisTypeClassificationExtractor:
    """Extracts a patient's demographics, signs, treatment arm, and labs."""

    required_fields: ClassVar[list[str]] = ["age", "sex", "edema"]

    def extract(self, text: str) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        self._add_required(text, fields)
        self._add_optional(text, fields)
        return fields

    @staticmethod
    def _add_required(text: str, fields: dict[str, Any]) -> None:
        age = find_number_near(text, _AGE_KEYWORDS)
        if age is not None:
            fields["age"] = age
        sex = find_literal(text, _SEX_ALIASES)
        if sex is not None:
            fields["sex"] = sex
        edema = find_literal(text, _EDEMA_ALIASES)
        if edema is not None:
            fields["edema"] = edema

    @staticmethod
    def _add_optional(text: str, fields: dict[str, Any]) -> None:
        for field, aliases in (
            ("ascites", _ASCITES_ALIASES),
            ("hepatomegaly", _HEPATOMEGALY_ALIASES),
            ("spiders", _SPIDERS_ALIASES),
            ("drug", _DRUG_ALIASES),
        ):
            value = find_literal(text, aliases)
            if value is not None:
                fields[field] = value
        for field, keywords in _OPTIONAL_NUMBER_KEYWORDS.items():
            value = find_number_near(text, keywords)
            if value is not None:
                fields[field] = value
