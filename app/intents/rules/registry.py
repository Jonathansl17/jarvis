"""Single Open/Closed registration point mapping model name to field
extractor and to the Spanish keywords that identify it, mirroring
`api/app/adapters/__init__.py`'s `ADAPTERS` dict.
"""

from app.intents.rules.base import FieldExtractor
from app.intents.rules.extractors.avocado_price_regression import AvocadoPriceRegressionExtractor
from app.intents.rules.extractors.bitcoin_price_regression import BitcoinPriceRegressionExtractor
from app.intents.rules.extractors.body_fat_regression import BodyFatRegressionExtractor
from app.intents.rules.extractors.car_price_regression import CarPriceRegressionExtractor
from app.intents.rules.extractors.cirrhosis_type_classification import (
    CirrhosisTypeClassificationExtractor,
)
from app.intents.rules.extractors.flight_delay_regression import FlightDelayRegressionExtractor
from app.intents.rules.extractors.hepatitis_type_classification import (
    HepatitisTypeClassificationExtractor,
)
from app.intents.rules.extractors.stroke_classification import StrokeClassificationExtractor
from app.intents.rules.extractors.telecom_churn_classification import (
    TelecomChurnClassificationExtractor,
)
from app.intents.rules.extractors.wine_quality_classification import WineQualityClassificationExtractor

FIELD_EXTRACTORS: dict[str, FieldExtractor] = {
    "car_price_regression": CarPriceRegressionExtractor(),
    "body_fat_regression": BodyFatRegressionExtractor(),
    "stroke_classification": StrokeClassificationExtractor(),
    "hepatitis_type_classification": HepatitisTypeClassificationExtractor(),
    "cirrhosis_type_classification": CirrhosisTypeClassificationExtractor(),
    "wine_quality_classification": WineQualityClassificationExtractor(),
    "avocado_price_regression": AvocadoPriceRegressionExtractor(),
    "flight_delay_regression": FlightDelayRegressionExtractor(),
    "telecom_churn_classification": TelecomChurnClassificationExtractor(),
    "bitcoin_price_regression": BitcoinPriceRegressionExtractor(),
}

MODEL_KEYWORDS: dict[str, tuple[str, ...]] = {
    "car_price_regression": ("carro", "auto", "vehiculo", "vehículo", "coche"),
    "body_fat_regression": ("grasa corporal", "porcentaje de grasa"),
    "stroke_classification": ("derrame", "acv", "accidente cerebrovascular"),
    "hepatitis_type_classification": ("hepatitis",),
    "cirrhosis_type_classification": ("cirrosis",),
    "wine_quality_classification": ("vino",),
    "avocado_price_regression": ("aguacate", "palta"),
    "flight_delay_regression": ("vuelo", "retraso de vuelo"),
    "telecom_churn_classification": ("churn", "abandono de clientes", "cliente se vaya"),
    "bitcoin_price_regression": ("bitcoin", "btc"),
}
