"""Per-model inference rules for Gemini's system instruction.

Each entry turns a common way of phrasing a value in Spanish into the exact
enum/unit the model's schema expects, so Gemini rarely has to ask for a
field a person would consider obvious from context.
"""

from app.intents.airline_codes import AIRPORT_CODES, CARRIER_CODES

_CODE_PAIR_TEMPLATE = "{name} -> {code}"
_CODE_LIST_SEPARATOR = ", "


def _render_code_table(table: dict[str, str]) -> str:
    """Render a name -> code table as one comma-separated list."""
    return _CODE_LIST_SEPARATOR.join(
        _CODE_PAIR_TEMPLATE.format(name=name, code=code) for name, code in table.items()
    )


MODEL_INFERENCE_RULES: dict[str, tuple[str, ...]] = {
    "car_price_regression": (
        "present_price está en lakhs de rupias; si el usuario da rupias, divide entre 100000; "
        "si da dólares u otra moneda, pide el valor en lakhs de rupias",
        "kms_driven es un número simple de kilómetros",
        "owner es 0 por defecto si dicen 'primer dueño', 'nuevo' o no lo mencionan",
        "year son 4 dígitos",
        "fuel_type es 'Diesel' para 'diesel'/'diésel', 'Petrol' para 'gasolina'/'petrol', 'CNG' "
        "para 'gas natural'",
        "seller_type es 'Dealer' para 'agencia'/'concesionario' y 'Individual' para 'particular'",
        "transmission es 'Manual' para 'manual' y 'Automatic' para 'automático'/'automatico'",
    ),
    "body_fat_regression": (
        "weight está en libras; si dan kilogramos, multiplica por 2.2046",
        "abdomen y wrist están en centímetros; si dan pulgadas, multiplica por 2.54",
    ),
    "stroke_classification": (
        "hypertension y heart_disease son true/false, de 'sí'/'no' o de si mencionan la condición",
        "ever_married es 'Yes' si dicen 'casado'/'casada', 'No' si dicen 'soltero'/'soltera'",
        "Residence_type es 'Urban' para 'ciudad' y 'Rural' para 'campo'/'rural'",
        "work_type es 'Govt_job' para 'gobierno', 'Private' para 'empresa privada'/'empleado', "
        "'Self-employed' para 'independiente'/'por cuenta propia', 'children' para 'niño'",
        "smoking_status es 'never smoked' para 'nunca fumó', 'formerly smoked' para 'dejó de "
        "fumar'/'ex fumador', 'smokes' para 'fuma', y 'Unknown' si no se sabe",
        "avg_glucose_level está en mg/dL",
        "bmi es opcional: nunca lo pidas si no se menciona",
    ),
    "hepatitis_type_classification": (
        "sex es 'm' para 'hombre'/'masculino' y 'f' para 'mujer'/'femenino'",
        "age está en años",
        "los diez valores del panel de sangre (ALB, ALP, ALT, AST, BIL, CHE, CHOL, CREA, GGT, "
        "PROT) son opcionales: nunca los pidas si no se mencionan",
    ),
    "cirrhosis_type_classification": (
        "sex es 'M' para 'hombre' y 'F' para 'mujer'",
        "edema es 'N' para 'no', 'S' para 'leve'/'tratado', 'Y' para 'sí'/presente",
        "ascites, hepatomegaly y spiders son 'Y'/'N' de 'sí'/'no'",
        "drug es 'D-penicillamine' para 'penicilamina' y 'Placebo' para 'placebo'",
        "age está en años; el resto de los valores de laboratorio son opcionales: nunca los "
        "pidas si no se mencionan",
    ),
    "wine_quality_classification": (
        "type es 'red' para 'tinto'/'rojo' y 'white' para 'blanco'",
        "toda medida de laboratorio no marcada como requerida en el schema es opcional: nunca "
        "la pidas si no se menciona",
    ),
    "avocado_price_regression": (
        "type es 'organic' para 'orgánico' y 'conventional' para 'convencional'",
        "region traduce el nombre de la ciudad o zona al valor del schema (p. ej. 'Los Ángeles' "
        "-> 'LosAngeles', 'todo Estados Unidos'/'nacional' -> 'TotalUS')",
        "date es una fecha ISO (AAAA-MM-DD); 'hoy' o 'esta semana' es la fecha actual",
        "los volúmenes y conteos de bolsas son opcionales solo si el schema los permite; si son "
        "requeridos y no se mencionan, pídelos una vez",
    ),
    "flight_delay_regression": (
        f"carrier traduce el nombre de la aerolínea a su código: {_render_code_table(CARRIER_CODES)}",
        f"origin y dest traducen la ciudad al código de aeropuerto: {_render_code_table(AIRPORT_CODES)}",
        "day_of_week es 1 para lunes ... 7 para domingo (p. ej. 'el viernes' -> 5)",
        "dep_hour es la hora de salida en 24 horas: 'en la mañana' -> 9, 'en la tarde' -> 15, "
        "'en la noche' -> 20",
        "distance está en millas; si dan kilómetros, divide entre 1.60934",
    ),
    "telecom_churn_classification": (
        "Contract es 'Month-to-month' para 'mes a mes', 'One year' o 'Two year' para contratos "
        "de uno o dos años",
        "InternetService es 'Fiber optic' para 'fibra', 'DSL' para 'dsl', 'No' para 'sin internet'",
        "PaymentMethod es 'Electronic check' para 'cheque electrónico', 'Mailed check' para "
        "'cheque por correo', 'Credit card (automatic)' para 'tarjeta', 'Bank transfer "
        "(automatic)' para 'transferencia'",
        "los campos de servicios adicionales (OnlineSecurity, OnlineBackup, DeviceProtection, "
        "TechSupport, StreamingTV, StreamingMovies, PaperlessBilling, Partner, Dependents, "
        "PhoneService, MultipleLines) son 'Yes'/'No' de 'tiene'/'no tiene'; pídelos si el "
        "usuario no los menciona, no asumas 'No' por defecto",
        "si el cliente no tiene internet (InternetService 'No'), entonces OnlineSecurity, "
        "OnlineBackup, DeviceProtection, TechSupport, StreamingTV y StreamingMovies son "
        "'No internet service' sin preguntar; si no tiene teléfono, MultipleLines es "
        "'No phone service'; 'una sola línea' es MultipleLines 'No' y 'varias líneas' es 'Yes'",
        "'sin pareja ni dependientes' es Partner 'No' y Dependents 'No'; 'con pareja y "
        "dependientes' es 'Yes' en ambos; 'sin streaming de tele ni películas' es 'No' en ambos",
        "tenure está en meses (p. ej. 'dos años' -> 24, 'lleva 3 meses' -> 3)",
        "MonthlyCharges y TotalCharges están en dólares; TotalCharges es opcional y, si falta, "
        "infiérelo como tenure * MonthlyCharges en vez de preguntarlo",
    ),
    "bitcoin_price_regression": (
        "days: 'mañana' -> 1, 'pasado mañana' -> 2, 'una semana' -> 7, 'quince días' -> 15, "
        "'un mes' -> 30; si piden 'el precio' sin plazo, usa 1",
    ),
}

_RULE_BULLET_TEMPLATE = "  * {rule}"
_LINE_SEPARATOR = "\n"


def build_model_rules_text(model_name: str) -> str:
    """Render one model's inference rules as indented bullet lines."""
    rules = MODEL_INFERENCE_RULES.get(model_name, ())
    return _LINE_SEPARATOR.join(_RULE_BULLET_TEMPLATE.format(rule=rule) for rule in rules)
