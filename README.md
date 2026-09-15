# Health Insurance Premium Predictor

Flask application that predicts annual medical insurance premiums using a Random Forest regression model. It includes account registration and login, password hashing, salary-aware planning, policy recommendation, estimated benefit calculations, private prediction history, and a database configuration compatible with MySQL.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open `http://127.0.0.1:5000`.

Create an account on the first visit. Set a strong `SECRET_KEY` before deployment; the default development key is not suitable for production.

By default, predictions and history are stored in a local SQLite file. To use MySQL, create a database and set `DATABASE_URL` before launching:

`mysql+pymysql://USERNAME:PASSWORD@localhost/insurance_db`

## Dataset

Place the Medical Cost Personal Dataset at `data/insurance.csv`. It must contain: `age`, `sex`, `bmi`, `children`, `smoker`, `region`, and `charges`. The model automatically retrains when that file or the model source is newer than the saved model. If no dataset is provided, a synthetic demo dataset lets the app run, but should not be used for real pricing. The public dataset does not include salary, so the app derives a documented synthetic salary proxy for academic experimentation.

## Train and evaluate models

Run `python train.py` after adding the dataset. It compares Linear Regression, Random Forest, and XGBoost using an 80/20 train-test split and reports MAE, MSE, RMSE, and R². The best model is stored in `models/premium_model.joblib`. Results are saved to `models/evaluation_metrics.json` and the testing report is saved to `models/training_testing_report.md`.

## Project structure

- `app.py` — Flask routes, validation, and prediction storage
- `model.py` — data loading, model pipeline, and inference
- `train.py` — model comparison and evaluation
- `templates/` and `static/` — responsive frontend
- `database.sql` — optional MySQL initialization script

## Production notes

Set a strong `SECRET_KEY`, disable Flask debug mode, protect the history endpoint, and use representative, audited data before deployment.
