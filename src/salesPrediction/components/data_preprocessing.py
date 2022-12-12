import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from salesPrediction.logger import logger
from salesPrediction.entity import DataPreprocessingConfig
from salesPrediction.exception import SalesPredictionException
from salesPrediction.utils import read_yaml, store_numpy, save_bin


class DataPreprocessing:
    def __init__(self, config: DataPreprocessingConfig) -> None:
        self.config = config
        self._load_schema_file()

    def _load_schema_file(self):
        try:
            logger.info(f"Loading dataset from {self.config.raw_data_file}")
            self.df = pd.read_csv(self.config.raw_data_file)
            logger.info(f"Loading Schema from {self.config.schema_file}")
            self.schema = read_yaml(self.config.schema_file)
        except Exception as e:
            raise SalesPredictionException(e) from e

    def build_fit_preprocessing_pipeline(self):
        try:
            numerical_pipeline = Pipeline(
                steps=[("imputer", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())]
            )
            ordinal_pipeline = Pipeline(
                steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("ordinal", OrdinalEncoder())]
            )
            ohe_pipeline = Pipeline(
                steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(drop="first", sparse=False))]
            )
            self.transformer = ColumnTransformer(
                transformers=[
                    ("numerical", numerical_pipeline, self.schema["numerical_columns"]),
                    ("ordinal", ordinal_pipeline, self.schema["ordinal_columns"]),
                    ("ohe", ohe_pipeline, self.schema["ohe_columns"]),
                ],
                remainder="passthrough",
            )
            self.transformer.fit(self.df)
        except Exception as e:
            raise SalesPredictionException(e) from e

    def transform_save_data(self):
        try:
            transformed_data = self.transformer.transform(self.df)
            store_numpy(self.config.preprocessed_data_file, transformed_data)
        except Exception as e:
            raise SalesPredictionException(e) from e

    def save_preprocessing_obj(self):
        try:
            save_bin(self.config.preprocessing_obj,self.transformer)
        except Exception as e:
            raise SalesPredictionException(e) from e

    