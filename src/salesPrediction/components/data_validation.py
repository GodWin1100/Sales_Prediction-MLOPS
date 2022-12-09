import json
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
from salesPrediction.logger import logger
from salesPrediction.entity import DataValidationConfig
from salesPrediction.exception import SalesPredictionException
from salesPrediction.utils import read_yaml


class DataValidation:
    def __init__(self, config: DataValidationConfig) -> None:
        self.config = config
        self._load_data_schema()

    def _load_data_schema(self):
        try:
            logger.info(f"Loading DataFrame from {self.config.data_file}")
            self.df = pd.read_csv(self.config.data_file)
            logger.info(f"Loading Schema from {self.config.schema_file}")
            self.schema = read_yaml(self.config.schema_file)
        except Exception as e:
            raise SalesPredictionException(e) from e

    def validate_data_schema(self):
        try:
            error = []
            logger.info("Validating Dataset with Schema")
            logger.info("Validating No. of columns")
            for col in self.df.columns:
                if col not in self.schema["columns"]:
                    logger.warn(f"[ {col} ] is extra column present in dataset")
            for col in self.schema["columns"]:
                if col not in self.df.columns:
                    logger.warn(f"[ {col} ] column is not present in dataset")
            if len(self.df.columns) != len(self.schema["columns"]):
                error.append("No. of columns does not match with schema")
            logger.info("Validating datatype of columns")
            col_error = False
            for col in self.df.columns:
                if self.df[col].dtype != self.schema["columns_datatype"][col]:
                    logger.warn(
                        f"{col} is of type [ {self.df[col].dtype} ], required type [ {self.schema['columns'][col]} ]"
                    )
                    col_error = True
            if col_error:
                error.append("Column datatype mismatched")
            logger.info("Validation of Dataset completed")
            if error:
                raise Exception("\n".join(error))
            logger.info("Validation is successful")
        except Exception as e:
            raise SalesPredictionException(e) from e

    def generate_data_drift_report(self):
        try:
            logger.info("Creating Data Drift Report")
            profile = Profile(sections=[DataDriftProfileSection()])
            profile.calculate(self.df.sample(frac=0.7, random_state=64), self.df.sample(frac=0.3, random_state=8))
            profile_json = json.loads(profile.json())
            with open(self.config.report_file, "w") as f:
                json.dump(profile_json, f, indent=4)
            drift_found = profile_json["data_drift"]["data"]["metrics"]["dataset_drift"]
            logger.warn("Drift found in dataset") if drift_found else logger.info("Dataset is not drifted")
            logger.info(f"Successfully created Data Drift Report at {self.config.report_file}")
        except Exception as e:
            raise SalesPredictionException(e) from e

    def generate_data_drift_page(self):
        try:
            logger.info("Creating Data Drift page")
            dashboard = Dashboard(tabs=[DataDriftTab()])
            dashboard.calculate(self.df.sample(frac=0.7, random_state=64), self.df.sample(frac=0.3, random_state=8))
            dashboard.save(self.config.report_page)
            logger.info(f"Successfully created Data Drift page at {self.config.report_page}")
        except Exception as e:
            raise SalesPredictionException(e) from e
