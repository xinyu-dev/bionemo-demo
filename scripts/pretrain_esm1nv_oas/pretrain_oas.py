# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nemo.core.config import hydra_runner
from nemo.utils import logging
from omegaconf.omegaconf import OmegaConf

from bionemo.data import FLIPPreprocess, UniRef50Preprocess
from bionemo.model.protein.esm1nv import ESM1nvModel
from bionemo.model.utils import setup_trainer
from bionemo.callbacks.utils import setup_dwnstr_task_validation_callbacks
from bionemo.data.preprocess.protein.oas_preprocess import OASPairedPreprocess ### Import OAS preprocessor
import os, hashlib



@hydra_runner(config_path="../../../examples/protein/esm1nv/conf", config_name="pretrain_oas")
def main(cfg) -> None:
    logging.info("\n\n************** Experiment configuration ***********")
    logging.info(f'\n{OmegaConf.to_yaml(cfg)}')

    callbacks = setup_dwnstr_task_validation_callbacks(cfg)

    trainer = setup_trainer(cfg, callbacks=callbacks)

    if cfg.do_training:
        logging.info("************** Starting Training ***********")
        if cfg.restore_from_path:
            logging.info("\nRestoring model from .nemo file " + cfg.restore_from_path)
            model = ESM1nvModel.restore_from(
                cfg.restore_from_path, cfg.model, trainer=trainer, save_restore_connector=BioNeMoSaveRestoreConnector()
            )
        else:
            model = ESM1nvModel(cfg.model, trainer)
        trainer.fit(model)
        logging.info("************** Finished Training ***********")
    else:
        logging.info("************** Starting Preprocessing ***********")
        # use the custom OAS preprocessor
        preprocessor = OASPairedPreprocess() ### Create instance of preprocess class
        preprocessor.prepare() ### Prepare data

if __name__ == '__main__':
    main()
