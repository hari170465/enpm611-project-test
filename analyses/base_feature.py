import abc
import argparse
from typing import List, Dict

class BaseFeature(abc.ABC):
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
    def get_arguments_info(self) -> List[Dict[str, str]]:
        """
        Returns a list of dictionaries containing information about each argument.
        Each dictionary should have 'flags' and 'help' keys.
        Example:
            [
                {
                    'flags': '--active-labels, -a',
                    'help': 'Number of top active labels to analyze (default: 10)'
                },
                ...
            ]
        """
        pass

    @abc.abstractmethod
    def run(self, args):
        """
        Executes the feature using the parsed arguments.
        """
        pass
