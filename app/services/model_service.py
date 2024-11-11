from typing import Dict, Any
import pandas as pd
import numpy as np
import logging
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..models.transformer import DataTransformer
from ..utils.drive_handler import DriveHandler
from ..config.config import Config

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self, config: Config):
        self.config = config
        self.drive_handler = DriveHandler(config)
        self.transformer = None  # Initialized with `process_data`

    def _process_and_save_chunk(self, chunk: pd.DataFrame, output_path: str):
        """Transforms a chunk and appends the result to the output CSV file."""
        transformed_chunk = self.transformer.transform(chunk.values)
        # Save each chunk of transformed data as rows
        pd.DataFrame(transformed_chunk).to_csv(output_path, mode='a', header=False, index=False)
        logger.info("Processed and saved chunk.")

    def _inverse_and_save_chunk(self, chunk: pd.DataFrame, output_path: str):
        """Inverse transforms a chunk, reshapes it if necessary, and appends the result to the output CSV file."""
        values = chunk.values
        reshaped_chunk = values.reshape(values.shape[0], -1)
        
        inverse_transformed_chunk = self.transformer.inverse_transform(reshaped_chunk)
        
        pd.DataFrame(inverse_transformed_chunk, columns=["Amount"]).to_csv(output_path, mode='a', header=False, index=False)
        logger.info("Inverse transformed and saved chunk.")

    def _initialize_transformer(self, train_data: pd.DataFrame):
        """Initializes the DataTransformer with training data."""
        self.transformer = DataTransformer(train_data=train_data)
        self.transformer.fit()
        logger.info("Transformer initialized and fitted.")

    def process_data(self, drive_link: str) -> Dict[str, Any]:
        try:
            file_path = self.drive_handler.download_from_drive(drive_link)
            if not file_path:
                return {"status": "error", "message": "Failed to download file"}

            start_time = time.time()
            logger.info("Initializing transformer with a sample of the data")

            sample_data = pd.read_csv(file_path, usecols=["Amount"], nrows=10000)
            self._initialize_transformer(sample_data)

            output_path = os.path.join(
                self.config.DOWNLOAD_DIR, f"transformed_{os.path.basename(file_path)}"
            )

            # Create the output CSV with header for transformed data
            pd.DataFrame(columns=["TransformedData"]).to_csv(output_path, index=False)

            logger.info("Processing data in chunks with parallel processing.")

            chunk_iterator = pd.read_csv(file_path, chunksize=self.config.CHUNK_SIZE, usecols=["Amount"])
            futures = []

            with ThreadPoolExecutor(max_workers=4) as executor:
                for chunk in chunk_iterator:
                    futures.append(executor.submit(self._process_and_save_chunk, chunk, output_path))

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"Error processing chunk: {str(e)}")

            processing_time = time.time() - start_time

            return {
                "status": "success",
                "message": "Data transformed and saved successfully",
                "transformed_file_path": output_path,
                "processing_time_seconds": processing_time,
            }

        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            return {"status": "error", "message": str(e)}

    
    def inverse_data(self, transformed_file_path: str) -> dict:
        try:
            # Check if transformer is initialized before performing inverse transform
            if self.transformer is None:
                raise ValueError("Transformer has not been initialized. Please transform the data first.")
            
            output_inverse_path = os.path.join(self.config.DOWNLOAD_DIR, f"inverse_{os.path.basename(transformed_file_path)}")
            
            df = pd.read_csv(transformed_file_path, skiprows=1, header=None)

            values = df.values
            reshaped_values = values.reshape(values.shape[0], -1)

            data = self.transformer.inverse_transform(reshaped_values)

            result_df = pd.DataFrame(data, columns=["Amount"])
            result_df.to_csv(output_inverse_path, index=False)

            return {
                "status": "success",
                "message": "Inverse transformation completed successfully",
                "inverse_file_path": output_inverse_path,
            }
        except Exception as e:
            print(f"Error during inverse transformation: {str(e)}")
            return {"status": "error", "message": str(e)}