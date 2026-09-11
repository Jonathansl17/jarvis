"""Single Open/Closed registration point mapping model name to adapter class."""

from app.adapters.avocado_price_regression import AvocadoPriceRegressionAdapter
from app.adapters.base import ModelAdapter
from app.adapters.bitcoin_price_regression import BitcoinPriceRegressionAdapter
from app.adapters.body_fat_regression import BodyFatRegressionAdapter
from app.adapters.car_price_regression import CarPriceRegressionAdapter
from app.adapters.cirrhosis_type_classification import (
    CirrhosisTypeClassificationAdapter,
)
from app.adapters.flight_delay_regression import FlightDelayRegressionAdapter
from app.adapters.hepatitis_type_classification import (
    HepatitisTypeClassificationAdapter,
)
from app.adapters.stroke_classification import StrokeClassificationAdapter
from app.adapters.telecom_churn_classification import (
    TelecomChurnClassificationAdapter,
)
from app.adapters.wine_quality_classification import WineQualityClassificationAdapter

ADAPTERS: dict[str, type[ModelAdapter]] = {
    CarPriceRegressionAdapter.name: CarPriceRegressionAdapter,
    BodyFatRegressionAdapter.name: BodyFatRegressionAdapter,
    StrokeClassificationAdapter.name: StrokeClassificationAdapter,
    HepatitisTypeClassificationAdapter.name: HepatitisTypeClassificationAdapter,
    CirrhosisTypeClassificationAdapter.name: CirrhosisTypeClassificationAdapter,
    WineQualityClassificationAdapter.name: WineQualityClassificationAdapter,
    AvocadoPriceRegressionAdapter.name: AvocadoPriceRegressionAdapter,
    FlightDelayRegressionAdapter.name: FlightDelayRegressionAdapter,
    TelecomChurnClassificationAdapter.name: TelecomChurnClassificationAdapter,
    BitcoinPriceRegressionAdapter.name: BitcoinPriceRegressionAdapter,
}
