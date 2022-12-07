from salesPrediction.components import DataIngestion
from salesPrediction.config import ConfigurationManager
from salesPrediction.logger import logger
from salesPrediction.exception import SalesPredictionException

STAGE_NAME = "Data Ingestion Stage"


def main():
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.unzip_file()


if __name__ == "__main__":
    try:
        logger.info(f"STAGE: {STAGE_NAME} STARTED".center(100, "="))
        main()
        logger.info(f"STAGE: {STAGE_NAME} COMPLETED".center(100, "="))
    except Exception as e:
        raise SalesPredictionException(e) from e
