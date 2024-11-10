from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd

import config
from data_loader import DataLoader
from models.Issue import Issue
from analyses.base_feature import BaseFeature
import argparse


class ContributorActivityAnalysis(BaseFeature):
    """
    Analyzes contributor activity (comments, events) over time.
    """

    @property
    def feature_id(self) -> int:
        return 2

    def name(self) -> str:
        return 'ContributorActivityAnalysis'

    def description(self) -> str:
        return 'Analyzes contributor activity (comments, events) over time.'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--user',
            type=str,
            required=False,
            help='Optional parameter to focus on a specific user'
        )

    def get_arguments_info(self) -> List[Dict[str, str]]:
        return [
            {
                'flags': '--user',
                'help': 'Optional parameter to focus on a specific user'
            }
        ]

    def run(self, args):
        issues: List[Issue] = DataLoader().get_issues()
        df = self.__create_dataframe(issues, args.user)
        aggregated = self.__aggregate(df)
        self.__visualize_results(df, aggregated)

    def __create_dataframe(self, issues, user_filter) -> pd.DataFrame:
        data = []
        for issue in issues:
            for event in issue.events:
                data.append({'author': event.author, 'event_date': event.event_date})
        df = pd.DataFrame(data)
        df['event_date'] = pd.to_datetime(df['event_date'])
        if user_filter:
            df = df[df['author'] == user_filter]
        return df

    def __aggregate(self, df):
        df.set_index('event_date', inplace=True)
        return df.groupby(['author', pd.Grouper(freq='M')]).size().reset_index(name='event_count')

    def __visualize_results(self, df, aggregated):
        top_authors = df['author'].value_counts().head(5).index
        for author in top_authors:
            author_data = aggregated[aggregated['author'] == author].sort_values('event_date')
            # Apply smoothing using a rolling average with a window of 3 months
            author_data['smoothed_event_count'] = author_data['event_count'].rolling(window=3, min_periods=1).mean()
            plt.plot(author_data['event_date'], author_data['smoothed_event_count'], label=author)
        plt.xlabel('Date')
        plt.ylabel('Number of Events (Smoothed)')
        plt.title('Contributor Activity Over Time (Smoothed)')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    ContributorActivityAnalysis().run()