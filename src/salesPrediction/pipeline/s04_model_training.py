from dotenv import load_dotenv

from salesPrediction.components import ModelTraining
from salesPrediction.config import ConfigurationManager
from salesPrediction.exception import SalesPredictionException
from salesPrediction.logger import logger

STAGE_NAME = "Model Training Stage"
load_dotenv()


def main():
    config = ConfigurationManager()
    model_training_config = config.get_model_training_config()
    model_training = ModelTraining(model_training_config)
    model_training.build_train_model()
    model_training.log_model(remote=False)


if __name__ == "__main__":
    try:
        logger.info(f"STAGE: {STAGE_NAME} STARTED".center(100, "="))
        main()
        logger.info(f"STAGE: {STAGE_NAME} COMPLETED".center(100, "="))
    except Exception as e:
        raise SalesPredictionException(e) from e
