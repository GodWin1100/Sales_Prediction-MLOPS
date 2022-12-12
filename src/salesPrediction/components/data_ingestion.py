import os
import requests
from zipfile import ZipFile
from tqdm import tqdm
from salesPrediction.logger import logger
from salesPrediction.entity import DataIngestionConfig
from salesPrediction.exception import SalesPredictionException
from salesPrediction.utils import get_size


class DataIngestion:
    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config

    def download_file(self):
        try:
            logger.info("Trying to download file...")
            if not os.path.exists(self.config.local_data_file):
                logger.info("Download started...")
                req = requests.get(self.config.source_url)
                with open(self.config.local_data_file, "wb") as f:
                    f.write(req.content)
                logger.info(f"{self.config.local_data_file} Downloaded.\n{req.headers}")
            else:
                size = get_size(self.config.local_data_file)
                logger.info(f"File already exists of size: {size}")
        except Exception as e:
            raise SalesPredictionException(e) from e

    def _preprocess(self, zf: ZipFile, f: str, working_dir: str):
        target_filepath = os.path.join(working_dir, f)
        if not os.path.exists(target_filepath):
            zf.extract(f, working_dir)
        if os.path.getsize(target_filepath) == 0:
            os.remove(target_filepath)
            logger.info(f"File Remove: {target_filepath}")

    def unzip_file(self):
        logger.info(f"Unzipping the file: {self.config.local_data_file}")
        with ZipFile(file=self.config.local_data_file, mode="r") as zf:
            list_of_files = zf.namelist()
            for f in tqdm(list_of_files):
                self._preprocess(zf, f, self.config.unzip_dir)
        logger.info("Unzipping Done")
