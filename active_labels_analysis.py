from typing import List

import matplotlib.pyplot as plt
import pandas as pd

import config
from data_loader import DataLoader
from model import Issue


class ActiveLabelsAnalysis:
    """
     Identify labels associated with the most active discussions.
    """

    def __init__(self):
        self.LABEL: str = config.get_parameter('label')

    def run(self):
        issues: List[Issue] = DataLoader().get_issues()
        if self.LABEL:
            self.print_occurrences(issues)

        df = self.create_dataframe(issues)
        if self.LABEL:
            # filter by label if label arg got passed
            df = df[df['label'] == self.LABEL]

        label_activity = self.get_label_activity(df)
        self.visualize_results(label_activity)

    def print_occurrences(self, issues):
        # How many self.LABEL instances exist
        total = sum(issue.labels.count(self.LABEL) for issue in issues if issue.labels)

        output: str = f"The label '{total}' occurred across {len(issues)} issues"
        print(f'\n\n{output}\n')

    def create_dataframe(self, issues) -> pd.DataFrame:
        data = []
        for issue in issues:
            num_comments = sum(1 for event in issue.events if event.event_type == 'commented')
            for label in issue.labels:
                data.append({'label': label, 'num_comments': num_comments})
        return pd.DataFrame(data)

    def get_label_activity(self, df):
        return df.groupby('label')['num_comments'].sum().sort_values(ascending=False)

    def visualize_results(self, label_activity):
        label_activity.head(10).plot(kind='bar')
        plt.xlabel('Label')
        plt.ylabel('Number of Comments')
        if self.LABEL:
            plt.title(f"Activity on the '{self.LABEL}' label")
        else:
            plt.title('Top 10 Most Active Labels')
        plt.show()


if __name__ == '__main__':
    ActiveLabelsAnalysis().run()
