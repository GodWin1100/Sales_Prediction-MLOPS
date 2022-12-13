from salesPrediction.logger import logger
from salesPrediction.components import ModelPredict
from salesPrediction.config import ConfigurationManager
from salesPrediction.exception import SalesPredictionException

STAGE_NAME = "Model Predict Stage"


def main():
    config = ConfigurationManager()
    model_predict_config = config.get_model_predict_config()
    model_predict = ModelPredict(model_predict_config)
    model_predict.load_essentials()
    model_predict.run_pipeline()


if __name__ == "__main__":
    try:
        logger.info(f"STAGE: {STAGE_NAME} STARTED".center(100, "="))
        main()
        logger.info(f"STAGE: {STAGE_NAME} COMPLETED".center(100, "="))
    except Exception as e:
        raise SalesPredictionException(e) from e
