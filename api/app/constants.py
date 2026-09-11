"""Named values used by the API that are not carried inside a model bundle.

Every value a model needs to run (features, fill values, thresholds,
encodings, classes, training ranges) is read from its `.joblib` bundle at
request time. The constants below are route/wire-level or domain encodings
that were never persisted in any bundle and therefore have nowhere else to
live.
"""

MODELS_DIR_ENV_VAR = "MODELS_DIR"
BUNDLE_FILE_SUFFIX = ".joblib"

PREDICT_ROUTE_PREFIX = "/predict"
MODELS_ROUTE = "/models"
MODEL_SCHEMA_ROUTE = MODELS_ROUTE + "/{model_name}/schema"
HEALTH_ROUTE = "/health"

# stroke_classification: booleans encoded 1/0 by the training notebook,
# not stored in the bundle (only the one-hot reference categories are).
STROKE_GENDER_POSITIVE = "Male"
STROKE_MARRIED_POSITIVE = "Yes"
STROKE_RESIDENCE_POSITIVE = "Urban"

# hepatitis_type_classification: 'm' maps to 1, 'f' to 0.
HEPATITIS_SEX_POSITIVE = "m"

# cirrhosis_type_classification: 'M' maps to 1, 'F' to 0 (see bundle
# `encoding['Sex']`, which documents but does not machine-encode the rule).
CIRRHOSIS_SEX_POSITIVE = "M"
CIRRHOSIS_SIGN_POSITIVE = "Y"

# wine_quality_classification: red maps to 0, white to 1, per the training
# notebook; the bundle does not carry a `type_encoding` for this model.
WINE_TYPE_ENCODING = {"red": 0, "white": 1}

# avocado_price_regression: the region one-hot columns in the bundle carry
# this prefix ahead of the human-facing region name.
AVOCADO_REGION_COLUMN_PREFIX = "region_"
