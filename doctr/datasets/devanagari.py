# Copyright (C) 2021-2022, Mindee.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import json
import os
from pathlib import Path
from typing import Any, List, Tuple

from .datasets import AbstractDataset

__all__ = ["Devanagari"]


class Devanagari(AbstractDataset):
    """Dataset implementation for text recognition tasks

    >>> from doctr.datasets import RecognitionDataset
    >>> train_set = Devanagari(img_folder="/path/to/images",
    >>>                                labels_path="/path/to/labels.json")
    >>> img, target = train_set[0]

    Args:
        img_folder: path to the images folder
        labels_path: pathe to the json file containing all labels (character sequences)
        **kwargs: keyword arguments from `AbstractDataset`.
    """

    def __init__(
        self,
        img_folder: str = "../../../printed-dev-dataset/test/images",
        labels_path: str = "../../../printed-dev-dataset/test/labels.json",
        **kwargs: Any,
    ) -> None:
        super().__init__(img_folder, **kwargs)

        self.data: List[Tuple[str, str]] = []
        with open(labels_path) as f:
            labels = json.load(f)

        for img_name, label in labels.items():
            if not os.path.exists(os.path.join(img_folder, img_name)):
                raise FileNotFoundError(f"unable to locate {os.path.join(self.root, img_name)}")

            self.data.append((img_name, label))

    def merge_dataset(self, ds: AbstractDataset) -> None:
        # Update data with new root for self
        self.data = [(str(Path(self.root).joinpath(img_path)), label) for img_path, label in self.data]
        # Define new root
        self.root = Path("/")
        # Merge with ds data
        for img_path, label in ds.data:
            self.data.append((str(Path(ds.root).joinpath(img_path)), label))
