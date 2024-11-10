# run.py
"""Starting point of the application."""

import argparse
import sys
import analyses
import config

def __parse_args():
    """
    Parses the command line arguments using subparsers for each feature.
    """
    
    # Create the main parser with help enabled
    parser = argparse.ArgumentParser(
        description="Run different analysis features."
    )
    
    # Create a mutually exclusive group: either --feature or --list-features
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--feature', '-f',
        type=int,
        help='Which feature to run (integer ID)'
    )
    group.add_argument(
        '--list-features', '-l',
        action='store_true',
        help='List all available features with their IDs and arguments'
    )
    
    # Parse known arguments first
    args, remaining_argv = parser.parse_known_args()
    
    if args.list_features:
        # List all available features and their arguments
        print("Available Features:")
        for fid, feature in sorted(analyses.FEATURES.items()):
            print(f"  {fid}: {feature.name()}: {feature.description()}")
            arguments_info = feature.get_arguments_info()
            for arg in arguments_info:
                print(f"\t{arg['flags']:<25} {arg['help']}")
            print()
        sys.exit(0)
    
    if not args.feature:
        print("Error: --feature is required unless --list-features is specified.")
        parser.print_help()
        sys.exit(1)
    
    feature_id = args.feature
    feature = analyses.FEATURES.get(feature_id)
    
    if not feature:
        print(f"Error: Feature with ID {feature_id} is not recognized.")
        available_ids = ', '.join(str(fid) for fid in analyses.FEATURES.keys())
        print(f"Available feature IDs: {available_ids}")
        sys.exit(1)
    
    # Create a new parser for feature-specific arguments
    feature_parser = argparse.ArgumentParser(
        description=f"Run the '{feature.name()}' feature."
    )
    # Re-add the --feature argument to ensure it's recognized
    feature_parser.add_argument(
        '--feature', '-f',
        type=int,
        required=True,
        help='Which feature to run (integer ID)'
    )
    # Let the feature add its own arguments
    feature.add_arguments(feature_parser)
    
    # Parse all arguments including feature-specific ones
    feature_args = feature_parser.parse_args()
    
    return feature_args

def main():
    args = __parse_args()
    config.overwrite_from_args(args)

    feature = analyses.FEATURES.get(args.feature)
    if feature:
        feature.run(args)
    else:
        # A redundant safety checkk. Redundant becvause we checked in __parse_args
        print(f"Error: Feature '{args.feature}' not recognized!")
        print(f"Need to pick a feature between 1 and {len(analyses.FEATURES)}")
        sys.exit(1)

if __name__ == "__main__":
    main()