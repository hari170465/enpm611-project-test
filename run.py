"""Starting point of the application."""

import argparse
import sys

import config
from analyses.active_labels_analysis import ActiveLabelsAnalysis
from analyses.contributor_activity_analysis import ContributorActivityAnalysis
from analyses.contributors_interactions_analysis import ContributorsInteractionsAnalysis
from analyses.reopened_issue_analysis import ReopenedIssueAnalysis


def parse_args():
    """
    Parses the command line arguments that were provided along
    with the python command.
    """
    ap = argparse.ArgumentParser("run.py")
    
    ap.add_argument('--feature', '-f', type=int, required=True,
                    help='Which of the three features to run')
    
    ap.add_argument('--user', '-u', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific user')

    ap.add_argument('--label', '-l', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific label')
    
    return ap.parse_args()

def unrecognized_feature():
    print(f'Error: Need to pick a feature between 1 and {len(FEATURES)}')
    sys.exit(1)


FEATURES = {
    0: lambda: print("This code doesn't implement the Example Analysis"),
    1: lambda: ActiveLabelsAnalysis().run(),
    2: lambda: ContributorActivityAnalysis().run(),
    3: lambda: ReopenedIssueAnalysis().run(),
    4: lambda: ContributorsInteractionsAnalysis().run(),
}


if __name__ == "__main__":
    args = parse_args()
    config.overwrite_from_args(args)
    FEATURES.get(args.feature, unrecognized_feature)()
