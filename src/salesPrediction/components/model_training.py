from os import getenv
from urllib.parse import urlparse

import mlflow
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

from salesPrediction.entity import ModelTrainingConfig
from salesPrediction.exception import SalesPredictionException
from salesPrediction.logger import logger
from salesPrediction.utils import load_numpy, read_yaml, save_bin, save_json


class ModelTraining:
    def __init__(self, config: ModelTrainingConfig) -> None:
        self.config = config
        self._load_param_data_file()

    def _load_param_data_file(self):
        try:
            logger.info(f"Loading params from {self.config.param_file}")
            self.params = read_yaml(self.config.param_file)
            logger.info(f"Loading data from {self.config.preprocessed_data_file}")
            self.data = load_numpy(self.config.preprocessed_data_file)
        except Exception as e:
            raise SalesPredictionException(e) from e

    def build_train_model(self):
        try:
            logger.info(f"Training Model\nParams: {self.params}")
            self.model = XGBRegressor(**self.params)
            self.model.fit(X=self.data[:, :-1], y=self.data[:, -1])
            save_bin(self.config.model_file, self.model)
        except Exception as e:
            raise SalesPredictionException(e) from e

    @staticmethod
    def _eval_metrics(y_true, y_pred):
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return {"rmse": rmse, "mae": mae, "r2": r2}

    def log_model(self, remote: bool = False):
        try:
            logger.info("MlFlow tracking started")
            with mlflow.start_run():
                if remote:
                    mlflow.set_tracking_uri(getenv("MLFLOW_URI"))
                y_pred = self.model.predict(self.data[:, :-1])
                y_true = self.data[:, -1]
                metrics = self._eval_metrics(y_true, y_pred)
                save_json(self.config.score_file,metrics)
                tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
                mlflow.log_params(self.params)
                mlflow.log_metrics(metrics)
                signature = mlflow.models.infer_signature(self.data[:, :-1], y_pred)
                if tracking_url_type_store != "file":
                    print(tracking_url_type_store)
                    mlflow.sklearn.log_model(
                        self.model, "model", registered_model_name="XGBRegressor", signature=signature
                    )
                else:
                    mlflow.sklearn.log_model(self.model, "model", signature=signature)
            logger.info(f"Model tracked with MLFLOW at {mlflow.get_tracking_uri()}")
        except Exception as e:
            raise SalesPredictionException(e) from e
