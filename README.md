## About Project
This is my submission for ENPM611 project.

This code implements four different analyses to analyze GitHub issues from the `python-poetry/poetry` repository to generate insights into **issue activity**, **contributor engagement**, **issue reopening patterns**, and **contributor interactions**.

### Analysis 1: Most Active Issue Labels
Identifies the labels associated with the most active discussions by analyzing the number of comments on issues tagged with each label.

This helps to understand which types of issues generate the most engagement among contributors.

### Analysis 2: Contributor Activity Over Time
Analyzes contributor activity by examining the number of events (comments or issue closures) each contributor is involved in overtime.

This provides insights into the most active contributors and when they were so.
### Analysis 3: Counting Reopened Issues per Label
Counts the number of times issues are reopened per label.

This let us understand identify what kind of issues are usually the most problematic, require additional attention or indicate complex problem areas.

### (Bonus) Analysis 4: Network Analysis of Contributor Interactions
Constructs a network graph of contributors based on their interactions with issues.

Nodes represent contributors, and edges represent interactions between them.

This analysis shows collaboration patterns and key contributors. And still has space for improvements to build upon.

## How to Run the Program

### Prerequisites

- Python 3.x installed on your system.
- Required Python packages installed:
    - `pandas`
    - `matplotlib`
    - `networkx`
    - `python-dateutil`
    - `scipy`

Install the required packages using:
```bash  
pip install -r requirements.txt
```  

### Data File Configuration

Ensure that `poetry_issues.json` is available and that the `config.json` file is updated with the correct path to it,

### Running Analyses

The program is executed via the command line using `run.py`.   
Specify which analysis to run using the `--feature` flag followed by the feature number (1 to 4).   
Optional filters for user and label can be provided using the `--user` and `--label` flags.

```bash  
python run.py --feature <feature_number> [--user <username>] [--label <label_name>]
```  

#### Examples

1. **Run Analysis 1 (Most Active Issue Labels)**
```bash  
python run.py --feature 1 --label Bug
```  
1. **Run Analysis 2 (Contributor Activity Over Time)**

```bash  
python run.py --feature 2 --user rth
```  
1. **Run Analysis 3 (Counting Reopened Issues per Label)**
```bash  
python run.py --feature 3
```  
1. **Run Analysis 4 (Network Analysis of Contributor Interactions)**
```bash  
python run.py -f 4 --label Bug --user cmarmo  
```