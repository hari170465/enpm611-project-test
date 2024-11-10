from typing import List, Dict

import matplotlib.pyplot as plt
import pandas as pd
import argparse

import config
from analyses.base_feature import BaseFeature
from data_loader import DataLoader
from models.Issue import Issue



class ActiveLabelsAnalysis(BaseFeature):
    """
     Identifies labels associated with the most active discussions.
    """

    @property
    def feature_id(self) -> int:
        return 1

    def name(self) -> str:
        return 'ActiveLabelsAnalysis'

    def description(self) -> str:
        return 'Identifies labels associated with the most active discussions.'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--active-labels', '-a',
            type=int,
            default=10,
            help='Number of top active labels to analyze (default: 10)'
        )
        parser.add_argument(
            '--label',
            type=str,
            help='Optional parameter for analyses focusing on a specific label'
        )

    def get_arguments_info(self) -> List[Dict[str, str]]:
        return [
            {
                'flags': '--active-labels',
                'help': 'Number of top active labels to analyze (default: 10)'
            },
            {
                'flags': '--label',
                'help': 'Optional parameter for analyses focusing on a specific label'
            }
        ]

    def run(self, args):
        issues: List[Issue] = DataLoader().get_issues()
        label_filter = args.label

        if label_filter:
            self.__print_occurrences(issues, label_filter)

        df = self.__create_dataframe(issues, label_filter)
        aggregated = self.__aggregate(df)
        self.__visualize_results(aggregated, args.active_labels, label_filter)

    def __print_occurrences(self, issues, label):
        total = sum(issue.labels.count(label) for issue in issues if issue.labels)
        output = f"The label '{label}' occurred {total} times across {len(issues)} issues."
        print(f'\n\n{output}\n')

    def __create_dataframe(self, issues, label_filter) -> pd.DataFrame:
        data = []
        for issue in issues:
            num_comments = sum(1 for event in issue.events if event and event.event_type == 'commented')
            for label in issue.labels:
                if label_filter and label != label_filter:
                    continue
                data.append({'label': label, 'num_comments': num_comments})
        df = pd.DataFrame(data)
        return df

    def __aggregate(self, df):
        return df.groupby('label')['num_comments'].sum().sort_values(ascending=False)

    def __visualize_results(self, label_activity, top_n, label_filter):
        label_activity.head(top_n).plot(kind='bar')
        plt.xlabel('Label')
        plt.ylabel('Number of Comments')
        if label_filter:
            plt.title(f"Activity on the '{label_filter}' label")
        else:
            plt.title(f'Top {top_n} Most Active Labels')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    ActiveLabelsAnalysis().run()
