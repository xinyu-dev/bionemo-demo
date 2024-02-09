from bionemo.data.preprocess import ResourcePreprocessor
from bionemo.utils.remote import RemoteResource
from nemo.utils import logging
from dataclasses import dataclass
from typing import List
import re
import os
import gzip
import shutil
import random
import pandas as pd

__all__ = ['OASPairedPreprocess']

# BIONEMO_HOME = os.getenv('BIONEMO_HOME', '/workspace/bionemo')
BIONEMO_HOME = '/workspace/bionemo'
OAS_DOWNLOAD_LINKS_PATH = f'{BIONEMO_HOME}/bionemo/data/preprocess/protein/oas_paired_subset_download.sh' # this is teh .sh file you downloaded from OAS


@dataclass
class OASPairedPreprocess(ResourcePreprocessor):
    """OASPairedPreprocess to download and preprocess OAS paired antibody data for heavy chains."""
    random_seed: int = 0
    root_directory: str = '/workspace/bionemo/data' #root direcotry
    dest_directory: str = 'OASpaired/raw' # output folder of OAS
    processed_directory: str = 'OASpaired/processed/heavy'  # for LC, use OASpaired/processed/light
    columns_to_keep = ['sequence_id_heavy','sequence_alignment_aa_heavy']  # for LC, use sequence_id_light, sequence_alignment_aa_light
    num_val_files = 2
    num_test_files = 2

    def get_remote_resources(self, download_script_path: str = OAS_DOWNLOAD_LINKS_PATH) -> List[RemoteResource]:
        """Download and verify each file from the download script path."""

        with open(download_script_path, 'r') as fh:
            url_list = [re.split('\s+', x.strip())[1] for x in fh.readlines()]

        # Add calculated checksums
        #         checksums = {"SRR11528761_paired.csv.gz": "3b671ee3d376445fdafd89932cb4687e",
        #                      "SRR11528762_paired.csv.gz": "69988520b12162b1f0613a55236d13a7",
        #                      "SRR10358523_paired.csv.gz": "fb5f7242f1f2b555c0bb798da449454e",
        #                      "SRR10358524_paired.csv.gz": "5db80ccbf8f47c855daa0d4d13d13d59",
        #                      "SRR10358525_paired.csv.gz": "d9df83c314bc426bb7ad00a3375a5994",
        #                      "SRR9179273_paired.csv.gz": "8e91cb8b719c4a2d30b2467cc5f6f080",
        #                      "SRR9179274_paired.csv.gz": "cc7b54cf168a86012773073bc6016cd2",
        #                      "SRR9179275_paired.csv.gz": "1660af663e0bdcf9e4a2dc0d8f79bfae",
        #                      "SRR9179276_paired.csv.gz": "56336af0a20afde929c263e628be6828",
        #                      "SRR9179277_paired.csv.gz": "48ac0e0f4ded0df1e345c7fbbb161601"}

        resources = list()
        for url in url_list:
            filename = os.path.basename(url)
            resource = RemoteResource(
                dest_directory=self.dest_directory,
                dest_filename=filename,
                root_directory=self.root_directory,
                checksum=None,  # disable checksum for convenience
                url=url
            )
            resources.append(resource)

        return resources

    def prepare_resource(self,
                         resource: RemoteResource,
                         delete_gzipped: bool = False) -> str:
        """Logs and downloads the passed resource. Extracts the gzipped file

        resource: RemoteResource - Resource to be prepared.
        delete_gzipped: boolean, default: True - Delete gzipped file once extracted.

        Returns - the absolute destination path for the downloaded resource
        """
        logging.info(f"Downloading {resource.url}")
        fully_qualified_gz_filename = resource.download_resource(overwrite=False)

        logging.info(f"Extracting the gzipped file")
        fully_qualified_dest_filename = os.path.splitext(fully_qualified_gz_filename)[0]
        with gzip.open(fully_qualified_gz_filename, 'rb') as f_gz:
            with open(fully_qualified_dest_filename, 'wb') as f_ext:
                shutil.copyfileobj(f_gz, f_ext)

        if delete_gzipped:
            shutil.rmtree(fully_qualified_gz_filename)

        return fully_qualified_dest_filename

    def process_files(self, filepaths: List[str], ):
        """
        Do train, test val split
        :param filepaths: File paths to split. Train, test val will be split based on filepaths
        :return: None
        """
        file_fill_size = 3  # pad file name with zeros. E.g. x001.csv, x002.csv, etc. 3 is the total number of digits
        full_processed_path = os.path.join(self.root_directory, self.processed_directory)
        os.makedirs(full_processed_path, exist_ok=True)

        # Assign two files to validation, two to test, and the rest to train
        shuffled_paths = filepaths.copy()
        random.seed = self.random_seed
        random.shuffle(shuffled_paths)

        # Split the files according to shuffled file path
        val_paths = shuffled_paths[:self.num_val_files]
        test_paths = shuffled_paths[self.num_val_files:self.num_val_files + self.num_test_files]
        train_paths = shuffled_paths[self.num_val_files + self.num_test_files:]

        # Split the data and clean up extra information
        for split, filenames in zip(['train', 'val', 'test'], [train_paths, val_paths, test_paths]):
            split_path = os.path.join(full_processed_path, split)
            os.makedirs(split_path, exist_ok=True)

            for num, filename in enumerate(filenames):
                output_name = os.path.join(split_path, f'x{str(num).zfill(file_fill_size)}.csv')
                logging.info(f"Converting {filename} to {output_name}")
                data = pd.read_csv(filename, skiprows=[0], usecols=self.columns_to_keep)
                data.to_csv(output_name, index=False)

    def prepare(self):
        filepaths = [self.prepare_resource(resource)
                     for resource in self.get_remote_resources()]

        self.process_files(filepaths)

