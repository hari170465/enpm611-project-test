import abc
import argparse
from typing import List

from util.builders import ArgInfo


class BaseAnalysis(abc.ABC):
    """
    Abstract base class for all analysis features.
    """

    @property
    @abc.abstractmethod
    def feature_id(self) -> int:
        """
        Returns the unique integer ID of the feature.
        """
        pass

    @abc.abstractmethod
    def name(self) -> str:
        """
        Returns the name of the feature. This will be used as the subcommand name.
        """
        pass

    @abc.abstractmethod
    def description(self) -> str:
        """
        Returns a brief description of the feature.
        """
        pass

    @abc.abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        """
        Adds feature-specific arguments to the parser.
        """
        pass

    @abc.abstractmethod
    def get_arguments_info(self) -> List[ArgInfo]:
        """
        Returns a list of ArgInfo objects containing information about each argument.
        Each ArgInfo should define the 'flags' and 'help' keys.
        """
        pass

    @abc.abstractmethod
    def run(self, args):
        """
        Executes the feature using the parsed arguments.
        """
        pass
