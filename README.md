# AI project: machine learning assistant

Group project for the Artificial Intelligence course (ITCR, San Carlos).
Ten machine learning models built with CRISP-DM, a REST API that serves
them, and a user-facing app (in progress).

## Repository layout

```
notebooks/   one folder per model, each with its executed CRISP-DM notebook
models/      one .joblib bundle per model, written by the notebooks, read by the API
api/         FastAPI service, one endpoint per model
app/         user-facing application (placeholder)
```

| # | Notebook | Technique | Target |
|---|----------|-----------|--------|
| 1 | `bitcoin_price_regression` | ARIMA | daily closing price |
| 2 | `car_price_regression` | multiple linear regression | used car price |
| 3 | `telecom_churn_classification` | neural network (MLP) | churn yes/no |
| 4 | `wine_quality_classification` | k nearest neighbours | low / medium / high |
| 5 | `flight_delay_regression` | decision tree | arrival delay (minutes) |
| 6 | `stroke_classification` | logistic regression | stroke yes/no |
| 7 | `cirrhosis_type_classification` | support vector machine | cirrhosis stage |
| 8 | `avocado_price_regression` | random forest | average price |
| 9 | `hepatitis_type_classification` | gaussian naive bayes | donor / hepatitis / fibrosis / cirrhosis |
| 10 | `body_fat_regression` | multiple linear regression | body fat percentage |

## Notebooks

Every notebook downloads its own dataset with `kagglehub` (or from a public
URL), so it runs unchanged in Google Colab and locally. Open the `.ipynb` in
Colab and run all cells. The last cells save the trained model to
`models/<name>.joblib`, two levels above the notebook.

Local run:

```bash
python3 -m venv env
./env/bin/pip install -r notebooks/requirements.txt
./env/bin/jupyter notebook notebooks/
```

## API

```bash
./env/bin/pip install -r api/requirements.txt
cd api
../env/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Interactive docs at `http://localhost:8000/docs`. Endpoints:

| Method | Path | What it does |
|--------|------|--------------|
| GET | `/health` | liveness |
| GET | `/models` | names of the loaded models |
| POST | `/predict/{model_name}` | runs one model on a JSON body |

The models are loaded once at startup from `models/`. Nothing is trained on
request. Configuration through environment variables `MODELS_DIR`, `HOST`,
`PORT` (see `api/README.md`).

### Request bodies

Optional fields (`null` or omitted) are filled with the value the notebook
used for missing data. Regressions return `meta.warnings` when an input falls
outside the range the model was trained on.

```bash
curl -X POST localhost:8000/predict/car_price_regression -H 'content-type: application/json' -d '{
  "present_price": 10, "year": 2015, "kms_driven": 40000, "owner": 0,
  "fuel_type": "Diesel", "seller_type": "Dealer", "transmission": "Manual"}'

curl -X POST localhost:8000/predict/body_fat_regression -H 'content-type: application/json' -d '{
  "abdomen": 90, "weight": 175, "wrist": 18}'

curl -X POST localhost:8000/predict/stroke_classification -H 'content-type: application/json' -d '{
  "gender": "Male", "age": 68, "hypertension": true, "heart_disease": false,
  "ever_married": "Yes", "work_type": "Private", "Residence_type": "Urban",
  "avg_glucose_level": 140, "bmi": 31, "smoking_status": "formerly smoked"}'

curl -X POST localhost:8000/predict/hepatitis_type_classification -H 'content-type: application/json' -d '{
  "age": 45, "sex": "m", "ALB": 38, "ALP": 60, "ALT": 30, "AST": 90, "BIL": 30,
  "CHE": 5, "CHOL": 4, "CREA": 80, "GGT": 120, "PROT": 70}'

curl -X POST localhost:8000/predict/cirrhosis_type_classification -H 'content-type: application/json' -d '{
  "age": 55, "sex": "F", "edema": "N", "ascites": "N", "hepatomegaly": "Y",
  "spiders": "N", "drug": "Placebo", "bilirubin": 2.5, "albumin": 3.2,
  "copper": 100, "alk_phos": 1500, "sgot": 120, "platelets": 200, "prothrombin": 11}'

curl -X POST localhost:8000/predict/wine_quality_classification -H 'content-type: application/json' -d '{
  "type": "white", "alcohol": 13.5, "density": 0.99, "free_sulfur_dioxide": 30,
  "total_sulfur_dioxide": 120, "volatile_acidity": 0.25, "residual_sugar": 2}'

curl -X POST localhost:8000/predict/avocado_price_regression -H 'content-type: application/json' -d '{
  "type": "organic", "region": "SanFrancisco", "date": "2017-09-10",
  "total_volume": 20000, "plu_4046": 5000, "plu_4225": 6000, "plu_4770": 1000,
  "total_bags": 8000, "small_bags": 7000, "large_bags": 1000, "xlarge_bags": 0}'

curl -X POST localhost:8000/predict/flight_delay_regression -H 'content-type: application/json' -d '{
  "month": 12, "day_of_month": 19, "day_of_week": 5, "dep_hour": 18,
  "carrier": "AA", "origin": "ORD", "dest": "LAX", "distance": 1745}'

curl -X POST localhost:8000/predict/telecom_churn_classification -H 'content-type: application/json' -d '{
  "gender": "Female", "SeniorCitizen": false, "Partner": "No", "Dependents": "No",
  "PhoneService": "Yes", "MultipleLines": "No", "InternetService": "Fiber optic",
  "OnlineSecurity": "No", "OnlineBackup": "No", "DeviceProtection": "No",
  "TechSupport": "No", "StreamingTV": "Yes", "StreamingMovies": "Yes",
  "Contract": "Month-to-month", "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check", "tenure": 3, "MonthlyCharges": 95}'

curl -X POST localhost:8000/predict/bitcoin_price_regression -H 'content-type: application/json' -d '{"days": 7}'
```

Classifiers answer with `label`, `probability` and the `threshold` applied.
Regressions answer with the predicted value in the units of the notebook
(lakhs of rupees, percent of body fat, dollars, minutes). Bitcoin answers with
a list of `{date, price, lower, upper}`.

## Authors

Jonathan Sancho Loaiza, Jennifer Lopez Miranda, Magdaleno Gomez Diaz.
