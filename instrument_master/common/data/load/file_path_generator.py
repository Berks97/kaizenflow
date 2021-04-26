"""
Import as:

import instrument_master.common.data.load.file_path_generator as vcdlfi
"""
import abc
from typing import Optional

import instrument_master.common.data.types as vcdtyp


class FilePathGenerator(abc.ABC):
    """
    Generate file path for specific security to store data on a file system
    (e.g., S3).
    """

    @abc.abstractmethod
    def generate_file_path(
        self,
        symbol: str,
        frequency: vcdtyp.Frequency,
        asset_class: vcdtyp.AssetClass,
        contract_type: Optional[vcdtyp.ContractType] = None,
        exchange: Optional[str] = None,
        currency: Optional[str] = None,
        unadjusted: Optional[bool] = None,
        # TODO(*): Is this needed?
        ext: vcdtyp.Extension = vcdtyp.Extension.Parquet,
    ) -> str:
        """
        Get the path to a specific symbol on s3.

        Parameters as in `read_data`.
        :return: path to the file
        """

    # TODO(gp): Do we really want to make it explicit?
    # No one is interested in this file except SymbolUniverse class.
    @staticmethod
    @abc.abstractmethod
    def get_latest_symbols_file() -> str:
        """
        Get the latest available file with symbols.
        """