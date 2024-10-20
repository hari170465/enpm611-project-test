import sys
from typing import List

import pandas as pd
import matplotlib.pyplot as plt

import config
from data_loader import DataLoader
from model import Issue

class ReopenedIssueAnalysis:
    """
    Identifies which issue labels are associated with issues being reopened the most.
    """

    def __init__(self):
        self.LABEL: str = config.get_parameter('label')

    def run(self):
        issues: List[Issue] = DataLoader().get_issues()
        df = self.create_dataframe(issues)
        aggregated = self.aggregate(df)

        print('Labels associated with the most reopened issues:')
        print(aggregated)

        self.visualize_results(aggregated)

    def create_dataframe(self, issues) -> pd.DataFrame:
        data = []

        for issue in issues:
            # Filter by label if self.LABEL is provided
            if self.LABEL and self.LABEL not in issue.labels:
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

    def aggregate(self, df):
        aggregated = df.groupby('labels')['reopen_count'].sum().reset_index()
        return aggregated.sort_values(by='reopen_count', ascending=False)

    def visualize_results(self, aggregated):
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
