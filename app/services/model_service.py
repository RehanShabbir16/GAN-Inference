from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import logging
import time
import os
from concurrent.futures import ThreadPoolExecutor
from ..models.transformer import DataTransformer
from ..utils.drive_handler import DriveHandler
from ..config.config import Config

logger = logging.getLogger(__name__)


class ModelService:
    def __init__(self, config: Config):
        self.config = config
        self.drive_handler = DriveHandler(config)

    def _process_chunk(
        self, chunk: pd.DataFrame, transformer: DataTransformer
    ) -> np.ndarray:
        return transformer.transform(chunk.values)

    def process_data(self, drive_link: str) -> Dict[str, Any]:
        try:

            # Download file
            file_path = self.drive_handler.download_from_drive(drive_link)
            if not file_path:
                return {"status": "error", "message": "Failed to download file"}

            start_time = time.time()

            logger.info("Reading Data")

            # First read the entire data to fit the transformer
            train_data = pd.read_csv(file_path)[["Amount"]]

            logger.info("Dividing into chunks")

            # Initialize and fit transformer with all data
            transformer = DataTransformer(train_data=train_data)
            transformer.fit()

            # Now process in chunks
            chunks = []
            chunk_iterator = pd.read_csv(file_path, chunksize=self.config.CHUNK_SIZE)

            for chunk in chunk_iterator:
                # Select only the Amount column
                chunk = chunk[["Amount"]]
                chunks.append(chunk)

            logger.info(f"Total number of chunks: {len(chunks)}")

            logger.info("Transforming the chunks.")
            # Process chunks in parallel
            transformed_chunks = []
            with ThreadPoolExecutor(max_workers=self.config.MAX_WORKERS) as executor:
                futures = [
                    executor.submit(self._process_chunk, chunk, transformer)
                    for chunk in chunks
                ]
                transformed_chunks = [future.result() for future in futures]

            logger.info("Combining the results.")
            # Combine results
            transformed_data = np.concatenate(transformed_chunks, axis=0)

            # Save transformed data
            output_path = os.path.join(
                self.config.DOWNLOAD_DIR, f"transformed_{os.path.basename(file_path)}"
            )
            pd.DataFrame(transformed_data).to_csv(output_path, index=False)

            processing_time = time.time() - start_time

            return {
                "status": "success",
                "message": "Data transformed successfully",
                "transformed_file_path": output_path,
                "processing_time_seconds": processing_time,
                "input_rows": sum(len(chunk) for chunk in chunks),
                "output_columns": transformed_data.shape[1],
                "chunks_processed": len(chunks),
            }

        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            return {"status": "error", "message": str(e)}
