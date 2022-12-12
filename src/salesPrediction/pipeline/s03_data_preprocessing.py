from salesPrediction.components import DataPreprocessing
from salesPrediction.config import ConfigurationManager
from salesPrediction.logger import logger
from salesPrediction.exception import SalesPredictionException

STAGE_NAME = "Data Preprocessing Stage"


def main():
    config = ConfigurationManager()
    data_preprocessing_config = config.get_data_preprocessing_config()
    data_preprocessing = DataPreprocessing(data_preprocessing_config)
    data_preprocessing.build_fit_preprocessing_pipeline()
    data_preprocessing.transform_save_data()
    data_preprocessing.save_preprocessing_obj()


if __name__ == "__main__":
    try:
        logger.info(f"STAGE: {STAGE_NAME} STARTED".center(100, "="))
        main()
        logger.info(f"STAGE: {STAGE_NAME} COMPLETED".center(100, "="))
    except Exception as e:
        raise SalesPredictionException(e) from e
