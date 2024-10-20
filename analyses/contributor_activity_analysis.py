from typing import List

import matplotlib.pyplot as plt
import pandas as pd

import config
from data_loader import DataLoader
from models.Issue import Issue


class ContributorActivityAnalysis:
    """
     Analyzes contributor activity (comments, events) over time.
    """

    def __init__(self):
        self.USER: str = config.get_parameter('user')

    def run(self):
        issues: List[Issue] = DataLoader().get_issues()
        df = self.__create_dataframe(issues)
        aggregated = self.__aggregate(df)
        self.__visualize_results(df, aggregated)

    def __create_dataframe(self, issues) -> pd.DataFrame:
        data = []
        for issue in issues:
            for event in issue.events:
                data.append({'author': event.author, 'event_date': event.event_date})
        df = pd.DataFrame(data)
        df['event_date'] = pd.to_datetime(df['event_date'])
        if self.USER:
            df = df[df['author'] == self.USER]
        return df

    def __aggregate(self, df):
        df.set_index('event_date', inplace=True)
        return df.groupby(['author', pd.Grouper(freq='M')]).size().reset_index(name='event_count')


    def __visualize_results(self, df, aggregated):
        top_authors = df['author'].value_counts().head(5).index
        for author in top_authors:
            author_data = aggregated[aggregated['author'] == author]
            plt.plot(author_data['event_date'], author_data['event_count'], label=author)
        plt.xlabel('Date')
        plt.ylabel('Number of Events')
        plt.title('Contributor Activity Over Time')
        plt.legend()
        plt.show()



if __name__ == '__main__':
    ContributorActivityAnalysis().run()
