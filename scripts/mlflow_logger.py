import mlflow

def log_to_mlflow(stock_name: str, prediction: float):
    # MLflow baglanti bilgileri
    mlflow.set_tracking_uri("http://172.18.0.4:5000")
    mlflow.set_experiment("BIST_MLOps_Experiment")

    with mlflow.start_run():
        mlflow.log_param("stock_name", stock_name)
        mlflow.log_metric("prediction", prediction)
        print(f"Tahmin MLflow'a loglandi: {stock_name}, {prediction:.2f}%")
