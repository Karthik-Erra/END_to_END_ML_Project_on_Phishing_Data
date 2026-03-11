import logging
import os
from datetime import datetime
import sys

log_file_name = f'{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.log'
log_directory_path = os.path.join(os.getcwd(),'logs')
os.makedirs(log_directory_path,exist_ok=True)

log_file_path = os.path.join(log_directory_path,log_file_name)

logging.basicConfig(
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

