import gdown
import os
from typing import Optional
import logging
from ..config.config import Config

logger = logging.getLogger(__name__)


class DriveHandler:
    def __init__(self, config: Config):
        self.config = config
        os.makedirs(self.config.DOWNLOAD_DIR, exist_ok=True)

    def download_from_drive(self, link: str) -> Optional[str]:
        try:
            file_id = link.split("/d/")[1].split("/")[0]
            download_url = f"https://drive.google.com/uc?id={file_id}"
            output_path = os.path.join(self.config.DOWNLOAD_DIR, f"data_{file_id}.csv")

            for attempt in range(self.config.MAX_RETRIES):
                try:
                    gdown.download(
                        download_url,
                        output_path,
                        quiet=False,
                    )
                    logger.info(f"File downloaded successfully to {output_path}")
                    return output_path
                except Exception as e:
                    if attempt == self.config.MAX_RETRIES - 1:
                        raise e
                    logger.warning(
                        f"Download attempt {attempt + 1} failed, retrying..."
                    )

        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return None
