import argparse
import sys
from typing import List, Dict

import matplotlib.pyplot as plt
import pandas as pd

from analyses.base_analysis import BaseAnalysis
from data_loader import DataLoader
from models.Issue import Issue
from util.builders import ArgInfoBuilder


class ReopenedIssueAnalysis(BaseAnalysis):
    """
    Identifies which issue labels are associated with issues being reopened the most.
    """

    def __init__(self):
        self.labels_arg = (ArgInfoBuilder()
            .set_flags('--labels')
            .set_help('(Optional) The number of labels to show in the result')
            .build()
        )

    @property
    def feature_id(self) -> int:
        return 3

    def name(self) -> str:
        return 'ReopenedIssueAnalysis'

    def description(self) -> str:
        return 'Identifies which issue labels are associated with issues being reopened the most.'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            self.labels_arg.flags,
            type=int,
            default=10,
            required=False,
            help=self.labels_arg.help
        )

    def get_arguments_info(self) -> List[Dict[str, str]]:
        return [self.labels_arg]

    def run(self, args):
        issues: List[Issue] = DataLoader().get_issues()
        df = self.__create_dataframe(issues)
        aggregated = self.__aggregate(df, args.labels)

        print('Labels associated with the most reopened issues:')
        print(aggregated)

        self.__visualize_results(aggregated)

    def __create_dataframe(self, issues) -> pd.DataFrame:
        data = []

        for issue in issues:
            reopen_count = sum(1 for event in issue.events if event and event.event_type == 'reopened')
            if reopen_count > 0:
                data.append({
                    'labels': issue.labels,
                    'reopen_count': reopen_count
                })

        df = pd.DataFrame(data)
        if df.empty:
            print('No reopened issues found for the specified label.')
            sys.exit(1)

        return df.explode('labels')

    def __aggregate(self, df, number_of_labels: int):
        aggregated = df.groupby('labels')['reopen_count'].sum().reset_index()
        return aggregated.sort_values(by='reopen_count', ascending=False).head(number_of_labels)

    def __visualize_results(self, aggregated):
        plt.figure(figsize=(12, 6))
        plt.bar(aggregated['labels'], aggregated['reopen_count'])
        plt.xlabel('Label')
        plt.ylabel('Number of Reopens')
        plt.title('Issue Labels vs. Reopen Counts')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()