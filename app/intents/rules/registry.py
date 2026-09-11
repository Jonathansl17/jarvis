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
    "car_price_regression": (
        "carro", "auto", "automovil", "automóvil", "vehiculo", "vehículo", "coche", "camioneta",
        "pickup", "pick up", "suv", "sedan", "sedán", "moto", "motocicleta", "usado", "segunda mano",
        "precio del carro", "cuanto vale", "cuánto vale", "valor de venta", "revender",
    ),
    "body_fat_regression": (
        "grasa corporal", "porcentaje de grasa", "grasa", "body fat", "masa corporal", "masa grasa",
        "cuanta grasa", "cuánta grasa", "medidas corporales", "composicion corporal", "composición corporal",
    ),
    "stroke_classification": (
        "derrame", "derrame cerebral", "acv", "accidente cerebrovascular", "accidente cerebro vascular",
        "stroke", "infarto cerebral", "embolia", "ictus", "apoplejia", "apoplejía", "riesgo cerebral",
    ),
    "hepatitis_type_classification": (
        "hepatitis", "hepatitis c", "panel hepatico", "panel hepático", "donante de sangre", "fibrosis",
        "enzimas hepaticas", "enzimas hepáticas", "examen de higado", "examen de hígado",
    ),
    "cirrhosis_type_classification": (
        "cirrosis", "cirrosis hepatica", "cirrosis hepática", "etapa de cirrosis", "estadio de cirrosis",
        "higado", "hígado", "biliar", "colangitis", "bilirrubina", "albumina", "albúmina",
    ),
    "wine_quality_classification": (
        "vino", "vinos", "calidad del vino", "vino tinto", "vino blanco", "cata", "bodega", "uva",
        "cosecha", "vinedo", "viñedo", "wine",
    ),
    "avocado_price_regression": (
        "aguacate", "aguacates", "palta", "paltas", "avocado", "hass", "guacamole",
        "precio del aguacate", "precio de la palta",
    ),
    "flight_delay_regression": (
        "vuelo", "vuelos", "retraso de vuelo", "retraso del vuelo", "delay", "avion", "avión",
        "aerolinea", "aerolínea", "aeropuerto", "llegada del vuelo", "atraso del vuelo", "demora del vuelo",
        "viaje en avion", "viaje en avión", "se atrasa el vuelo", "se retrasa el vuelo",
    ),
    "telecom_churn_classification": (
        "churn", "abandono de clientes", "cliente se vaya", "cliente se va", "se cambie de compania",
        "se cambie de compañia", "se cambie de compañía", "cancelar el servicio", "dar de baja", "darse de baja",
        "telefonia", "telefonía", "telecomunicaciones", "operador", "operadora", "plan de celular",
        "plan de internet", "fuga de clientes", "perder el cliente", "cliente de telecom",
    ),
    "bitcoin_price_regression": (
        "bitcoin", "btc", "cripto", "criptomoneda", "criptomonedas", "crypto", "precio del bitcoin",
        "tipo de cambio", "cotizacion", "cotización", "moneda digital",
    ),
}
