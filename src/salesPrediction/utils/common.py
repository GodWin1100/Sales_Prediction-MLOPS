import os
import yaml
import json
import numpy as np
import pickle
from pathlib import Path
from salesPrediction.logger import logger
from salesPrediction.exception import SalesPredictionException


def read_yaml(yaml_path: Path) -> dict:
    """Read yaml file and return it's content as python object `dict`

    Args:
        yaml_path (Path): path to yaml file

    Raises:
        SalesPredictionException: If file is empty or internal error

    Returns:
        dict: content of yaml file
    """
    try:
        with open(yaml_path) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {yaml_path} loaded successfully")
            if not content:
                raise Exception("YAML file is empty")
            return content
    except Exception as e:
        raise SalesPredictionException(e) from e


def create_directories(dir_paths: list, verbose=True):
    for path in dir_paths:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created Directory: {path}")


def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


def store_numpy(file_path: Path, np_obj: np.ndarray) -> None:
    try:
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, np_obj)
        logger.info(f"Saved numpy array at {file_path}")
    except Exception as e:
        raise SalesPredictionException(e) from e


def save_bin(file_path: Path, obj) -> None:
    try:
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)
        logger.info(f"Saved binary object at {file_path}")
    except Exception as e:
        raise SalesPredictionException(e) from e
