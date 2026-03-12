import os
from network_security.logging.logger import logging

class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        logging.info('Entered the sync_folder_to_s3 function')
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        logging.info('Entered the sync_folder_from_s3 function')
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        os.system(command)