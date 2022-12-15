from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_file: Path
    schema_file: Path
    report_file: Path
    report_page: Path


@dataclass(frozen=True)
class DataPreprocessingConfig:
    root_dir: Path
    raw_data_file: Path
    schema_file: Path
    preprocessed_data_file: Path
    preprocessing_obj: Path


@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir: Path
    model_file: Path
    preprocessed_data_file: Path
    param_file: Path
    score_file: Path


@dataclass(frozen=True)
class ModelPredictConfig:
    root_dir: Path
    model_file: Path
    test_data_file: Path
    predict_file: Path
    preprocessing_obj: Path
