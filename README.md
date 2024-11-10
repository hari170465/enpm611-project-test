## About Project
This is Team 12's submission for the ENPM611 project.

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

## Software Engineering Techniques

To enhance the modularity, maintainability, and scalability of the codebase, several software engineering techniques were employed.

#### Base Class and Automatic Feature Discovery

- **Base Class (`BaseAnalysis`)**
    - An abstract base class was created to define a common interface for all analysis features.
    - This ensures consistency across different analyses and enforces the implementation of essential methods such as `run`, `add_arguments`, and `get_arguments_info`.

- **Automatic Feature Discovery:**
    - The application dynamically discovers and registers all available features by scanning the `analyses` package.
    - This eliminates the need to manually register each new feature.
    - This follows the Open-Closed Principle.
        - New features can be added without modifying the core application logic.
        - Centralizes feature management

    - **How It Works:**
        - Upon initialization, the application imports all modules within the `analyses` directory.
        - It identifies classes that inherit from `BaseAnalysis` and registers them based on their unique `feature_id`.

#### Command-Line Interface Enhancements

- **Subparsers for Feature-Specific Arguments**
    - Each feature can define its own set of arguments.
    - Users can easily understand which arguments are applicable to each feature.
    - Supports complex argument structures without cluttering the global namespace.

    - **Example Output:**
        ```
        Available Features:
            1: ActiveLabelsAnalysis: Identifies labels associated with the most active discussions.
                --active-labels           Number of top active labels to analyze (default: 10)
                --label                   Optional parameter for analyses focusing on a specific label

            2: ContributorActivityAnalysis: Analyzes contributor activity (comments, events) over time.
                --user                    Optional parameter to focus on a specific user
        ```

#### **Modular Code Structure**
I re-organized the project into distinct modules and packages, separating concerns and facilitating easier navigation and maintenance.

### Builder Design Pattern
Using the builder pattern to create the arginfo object enhances code readability and maintainability.
It provides a clear approach to construct the object.
It ensures all required properties are initialized by the user.
It reduces the risk of inconsistent states.
It allows easy modifications or extensions without altering the core logic.
It abstracts the construction details, leading to cleaner and more organized code.
It simplifies testing and debugging, as each step of the object creation is isolated and manageable.

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
2. **Run Analysis 2 (Contributor Activity Over Time)**
```bash  
python run.py --feature 2 --user rth
```  
3. **Run Analysis 3 (Counting Reopened Issues per Label)**
```bash  
python run.py --feature 3
```  
4. **Run Analysis 4 (Network Analysis of Contributor Interactions)**
```bash  
python run.py -f 4 --label Bug --user cmarmo 
```