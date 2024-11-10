import sys
from typing import List, Dict

import matplotlib.pyplot as plt
import pandas as pd

import config
from data_loader import DataLoader
from models.Issue import Issue
from analyses.base_feature import BaseFeature
import argparse


class ReopenedIssueAnalysis(BaseFeature):
    """
    Identifies which issue labels are associated with issues being reopened the most.
    """

    @property
    def feature_id(self) -> int:
        return 3

    def name(self) -> str:
        return 'ReopenedIssueAnalysis'

    def description(self) -> str:
        return 'Identifies which issue labels are associated with issues being reopened the most.'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--label',
            type=str,
            required=False,
            help='Optional parameter for analyses focusing on a specific label'
        )

    def get_arguments_info(self) -> List[Dict[str, str]]:
        return [
            {
                'flags': '--label',
                'help': 'Optional parameter for analyses focusing on a specific label'
            }
        ]

    def run(self, args):
        issues: List[Issue] = DataLoader().get_issues()
        df = self.__create_dataframe(issues, args.label)
        aggregated = self.__aggregate(df)

        print('Labels associated with the most reopened issues:')
        print(aggregated)

        self.__visualize_results(aggregated)

    def __create_dataframe(self, issues, label_filter) -> pd.DataFrame:
        data = []

        for issue in issues:
            # Filter by label if label_filter is provided
            if label_filter and label_filter not in issue.labels:
                continue

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

    def __aggregate(self, df):
        aggregated = df.groupby('labels')['reopen_count'].sum().reset_index()
        return aggregated.sort_values(by='reopen_count', ascending=False)

    def __visualize_results(self, aggregated):
        plt.figure(figsize=(12, 6))
        plt.bar(aggregated['labels'], aggregated['reopen_count'])
        plt.xlabel('Label')
        plt.ylabel('Number of Reopens')
        plt.title('Issue Labels vs. Reopen Counts')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    ReopenedIssueAnalysis().run()