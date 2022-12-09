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
