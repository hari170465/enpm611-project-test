"""Starting point of the application."""

import argparse

import config
from active_labels_analysis import ActiveLabelsAnalysis
from example_analysis import ExampleAnalysis


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


if __name__ == "__main__":
    args = parse_args()
    config.overwrite_from_args(args)    # Other parts access args through `config`

    if args.feature == 0:
        ExampleAnalysis().run()
    elif args.feature == 1:
        ActiveLabelsAnalysis().run()
    elif args.feature == 2:
        raise RuntimeError("Feature not implemented yet")
    elif args.feature == 3:
        raise RuntimeError("Feature not implemented yet")
    else:
        print('Need to specify which feature to run with --feature flag.')
