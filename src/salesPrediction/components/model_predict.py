import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from salesPrediction.entity import ModelPredictConfig
from salesPrediction.logger import logger
from salesPrediction.utils import load_bin, save_json
from salesPrediction.exception import SalesPredictionException


class ModelPredict:
    def __init__(self, config: ModelPredictConfig) -> None:
        self.config = config

    def _load_test_data(self):
        self.test_data = pd.read_csv(self.config.test_data_file)

    def _load_preprocessing_obj(self):
        self.preprocessing_obj = load_bin(self.config.preprocessing_obj)

    def _load_model(self):
        self.model = load_bin(self.config.model_file)

    def load_essentials(self):
        try:
            self._load_test_data()
            self._load_preprocessing_obj()
            self._load_model()
            logger.info(f"Test Data, Preprocessing Object and Model Loaded successfully")
        except Exception as e:
            raise SalesPredictionException(e) from e

    # def build_pipeline(self):
    #     self.pipeline = Pipeline(steps=[("preprocessing", self.preprocessing_obj), ("model", self.model)])
    #     logger.info(f"Pipeline initialized: {self.pipeline}")

    def run_pipeline(self):
        try:
            self.pipeline = Pipeline(steps=[("preprocessing", self.preprocessing_obj), ("model", self.model)])
            logger.info(f"Pipeline initialized: {self.pipeline}")
            logger.info("Starting Prediction...")
            # y_true=self.test_data.iloc[:,-1]
            y_pred = self.pipeline.predict(X=self.test_data.values)
            # r2=r2_score(y_true,y_pred)
            # mae=mean_absolute_error(y_true,y_pred)
            # rmse=mean_squared_error(y_true,y_pred,squared=False)
            # logger.info(f"r2: {r2}, mae: {mae}, rmse: {rmse}")
            np.savetxt(self.config.predict_file, y_pred)
            logger.info(f"Prediction stored at {self.config.predict_file}")
        except Exception as e:
            raise SalesPredictionException(e) from e
