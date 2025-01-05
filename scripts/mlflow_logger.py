import mlflow

def log_model_details(model_params: dict, metrics: dict, model_name: str, dataset_path: str):
    mlflow.set_tracking_uri("http://172.18.0.4:5000")
    mlflow.set_experiment("BIST_MLOps_Experiment")

    with mlflow.start_run():
        # Model ismi ve veri seti bilgilerini logla
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("dataset", dataset_path)

        # Model parametrelerini logla
        for param, value in model_params.items():
            mlflow.log_param(param, value)

        # Performans metriklerini logla
        for metric, value in metrics.items():
            mlflow.log_metric(metric, value)

        print("Model bilgileri ve metrikler MLflow'a loglandi.")
