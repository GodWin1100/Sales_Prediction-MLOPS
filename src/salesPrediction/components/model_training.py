from xgboost import XGBRegressor
from salesPrediction.entity import ModelTrainingConfig
from salesPrediction.logger import logger
from salesPrediction.utils import read_yaml, save_bin, load_numpy
from salesPrediction.exception import SalesPredictionException


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
