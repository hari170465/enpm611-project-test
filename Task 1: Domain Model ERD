# Task Definition
Task 1: Domain model
The application domain is a fundamental building block of the requirements engineering and application design process. 
It describes the types of elements that need to be tracked, their attributes, and relationship with each other. 
In this task, you will create an Entity Relationship Diagram (ERD) that describes the domain of your application. 
In this project, the application domain consists of elements revolving around GitHub issue tracking, such as issues, users, comments, etc. 
You will create an ERD that describes that domain in the Crow’s Foot notation used in class. 
You will use the mermaid.js service to create that diagram: https://www.mermaidchart.com/play#pako

The diagram should capture the information represented in the data file that was provided to you in JSON format. 
Study the elements in the JSON data file and create elements, attributes, and relationships (with cardinalities) that describe the data.

# Tentative Solution
[Link](https://mermaid.live/edit#pako:eNqtU01rxCAQ_SviefcP5NpeSnsoLb0tLBOdTQQ_Fh0pIcl_r4npbtNYyKEeFN88Zp5vnJ4LJ5FXHP2jgsaDOVmW1lMIEdkwHI-uZw_OGLTEKnbiLYQTL3BeoEY9MwiaBiX7VNRumcPAPgL6mSg8AiVm3RUzviEIUs6Wy_b5Mq1AXtmGKclenzcoKdK4QWsnuzsokwxSBtmi6AxUCMar_DsotAu_YkupQIlzR200dXp_PjI85iPvszsF37O0mwk_aSujQMo1aa9R2jXKbu3rrlhQ-a1sb_L_8HslIH-3veUtmO0fkBiEV9fJuU1MOO1K3blZvbeycJaSUTvePvIDN-gNKJnGcc6fZqnFpJxPjZV4gahp6u1EhUjuvbOCV-QjHrh3sWl5dQEd0i17t0x0poxfEQcz_w)

### Entities:
- Issue: The central entity representing GitHub issues
- User: Represents GitHub users who interact with issues
- Comment: Represents comments on issues
- Label: Represents labels that can be applied to issues
- Reaction: Represents emoji reactions to issues or comments

### Relationships:
- An Issue is created by one User (1:1)
- An Issue can have many Comments (1:many)
- An Issue can have many Labels (1:many)
- An Issue can have many Reactions (1:many)
- A User can create many Comments (1:many)
- A User can add many Reactions (1:many)

### Attributes:
- Issue: id, title, body, created_at, updated_at, closed_at, state, number
- User: id, login, type
- Comment: id, body, created_at, updated_at
- Label: id, name, description, color
- Reaction: id, content, created_at
