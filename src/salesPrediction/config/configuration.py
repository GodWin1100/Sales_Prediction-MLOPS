from pathlib import Path
from salesPrediction.constants import *
from salesPrediction.entity import *
from salesPrediction.logger import logger
from salesPrediction.exception import SalesPredictionException
from salesPrediction.utils import read_yaml, create_directories


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH) -> None:
        self.config = read_yaml(config_filepath)
        create_directories([self.config[ARTIFACTS_ROOT_KEY]])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            config = self.config[DATA_INGESTION_KEY]
            create_directories([config[DATA_INGESTION_ROOT_DIR_KEY]])
            data_ingestion_config = DataIngestionConfig(
                root_dir=Path(config[DATA_INGESTION_ROOT_DIR_KEY]),
                source_url=config[DATA_INGESTION_SOURCE_URL_KEY],
                local_data_file=Path(config[DATA_INGESTION_LOCAL_DATA_FILE_KEY]),
                unzip_dir=Path(config[DATA_INGESTION_UNZIP_DIR_KEY]),
            )
            logger.info(f"Data Ingestion Config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise SalesPredictionException(e) from e

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            config = self.config[DATA_VALIDATION_KEY]
            create_directories([config[DATA_VALIDATION_ROOT_DIR]])
            data_validation_config = DataValidationConfig(
                root_dir=Path(config[DATA_VALIDATION_ROOT_DIR]),
                data_file=Path(config[DATA_VALIDATION_DATA_FILE]),
                schema_file=Path(config[DATA_VALIDATION_SCHEMA_FILE]),
                report_file=Path(config[DATA_VALIDATION_REPORT_FILE]),
                report_page=Path(config[DATA_VALIDATION_REPORT_PAGE]),
            )
            logger.info(f"Data Validation Config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            raise SalesPredictionException(e) from e

    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        try:
            config = self.config[DATA_PREPROCESSING_KEY]
            create_directories([config[DATA_PREPROCESSING_ROOT_DIR]])
            data_preprocessing_config = DataPreprocessingConfig(
                root_dir=Path(config[DATA_PREPROCESSING_ROOT_DIR]),
                raw_data_file=Path(config[DATA_PREPROCESSING_RAW_DATA_FILE]),
                schema_file=Path(config[DATA_PREPROCESSING_SCHEMA_FILE]),
                preprocessed_data_file=Path(config[DATA_PREPROCESSING_PREPROCESSED_DATA_FILE]),
                preprocessing_obj=Path(config[DATA_PREPROCESSING_PREPROCESSING_OBJ]),
            )
            logger.info(f"Data Preprocessing Config: {data_preprocessing_config}")
            return data_preprocessing_config
        except Exception as e:
            raise SalesPredictionException(e) from e

    def get_model_training_config(self) -> ModelTrainingConfig:
        try:
            config = self.config[MODEL_TRAINING_KEY]
            create_directories([config[MODEL_TRAINING_ROOT_DIR]])
            model_training_config = ModelTrainingConfig(
                root_dir=Path(config[MODEL_TRAINING_ROOT_DIR]),
                model_file=Path(config[MODEL_TRAINING_MODEL_FILE]),
                preprocessed_data_file=Path(config[MODEL_TRAINING_PREPROCESSED_DATA_FILE]),
                param_file=Path(config[MODEL_TRAINING_PARAM_FILE]),
            )
            logger.info(f"Model Training Config: {model_training_config}")
            return model_training_config
        except Exception as e:
            raise SalesPredictionException(e) from e

    def get_model_predict_config(self) -> ModelPredictConfig:
        try:
            config = self.config[MODEL_PREDICT_KEY]
            create_directories([config[MODEL_PREDICT_ROOT_DIR]])
            model_predict_config = ModelPredictConfig(
                root_dir=Path(config[MODEL_PREDICT_ROOT_DIR]),
                model_file=Path(config[MODEL_PREDICT_MODEL_FILE]),
                test_data_file=Path(config[MODEL_PREDICT_TEST_DATA_FILE]),
                predict_file=config[MODEL_PREDICT_PREDICT_FILE],
                preprocessing_obj=config[MODEL_PREDICT_PREPROCESSING_OBJ],
            )
            logger.info(f"Model Predict Config: {model_predict_config}")
            return model_predict_config
        except Exception as e:
            raise SalesPredictionException(e) from e
