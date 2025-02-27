from pathlib import Path

CONFIG_FILE_PATH = Path("./configs/config.yaml")


# config.yaml Keys
ARTIFACTS_ROOT_KEY = "artifacts_root"

# Data Ingestion config key
DATA_INGESTION_KEY = "data_ingestion"
DATA_INGESTION_ROOT_DIR_KEY = "root_dir"
DATA_INGESTION_SOURCE_URL_KEY = "source_url"
DATA_INGESTION_LOCAL_DATA_FILE_KEY = "local_data_file"
DATA_INGESTION_UNZIP_DIR_KEY = "unzip_dir"

# Data Validation config key
DATA_VALIDATION_KEY = "data_validation"
DATA_VALIDATION_ROOT_DIR = "root_dir"
DATA_VALIDATION_DATA_FILE = "data_file"
DATA_VALIDATION_SCHEMA_FILE = "schema_file"
DATA_VALIDATION_REPORT_FILE = "report_file"
DATA_VALIDATION_REPORT_PAGE = "report_page"

# Data Preprocessing config key
DATA_PREPROCESSING_KEY = "data_preprocessing"
DATA_PREPROCESSING_ROOT_DIR = "root_dir"
DATA_PREPROCESSING_RAW_DATA_FILE = "raw_data_file"
DATA_PREPROCESSING_SCHEMA_FILE = "schema_file"
DATA_PREPROCESSING_PREPROCESSED_DATA_FILE = "preprocessed_data_file"
DATA_PREPROCESSING_PREPROCESSING_OBJ = "preprocessing_obj"

# Model Training config key
MODEL_TRAINING_KEY = "model_training"
MODEL_TRAINING_ROOT_DIR = "root_dir"
MODEL_TRAINING_MODEL_FILE = "model_file"
MODEL_TRAINING_PREPROCESSED_DATA_FILE = "preprocessed_data_file"
MODEL_TRAINING_PARAM_FILE = "param_file"
MODEL_TRAINING_SCORE_FILE = "score_file"

# Model Evaluation config key
MODEL_PREDICT_KEY = "model_predict"
MODEL_PREDICT_ROOT_DIR = "root_dir"
MODEL_PREDICT_MODEL_FILE = "model_file"
MODEL_PREDICT_TEST_DATA_FILE = "test_data_file"
MODEL_PREDICT_PREDICT_FILE = "predict_file"
MODEL_PREDICT_PREPROCESSING_OBJ = "preprocessing_obj"
