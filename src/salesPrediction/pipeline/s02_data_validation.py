from salesPrediction.components import DataValidation
from salesPrediction.config import ConfigurationManager
from salesPrediction.logger import logger
from salesPrediction.exception import SalesPredictionException

STAGE_NAME = "Data Validation Stage"


def main():
    config = ConfigurationManager()
    data_validation_config = config.get_data_validation_config()
    data_validation = DataValidation(data_validation_config)
    data_validation.validate_data_schema()
    data_validation.generate_data_drift_report()
    data_validation.generate_data_drift_page()


if __name__ == "__main__":
    try:
        logger.info(f"STAGE: {STAGE_NAME} STARTED".center(100, "="))
        main()
        logger.info(f"STAGE: {STAGE_NAME} COMPLETED".center(100, "="))
    except Exception as e:
        raise SalesPredictionException(e) from e
