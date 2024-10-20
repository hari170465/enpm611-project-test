import sys
from typing import List

import matplotlib.pyplot as plt
import networkx as nx

import config
from data_loader import DataLoader
from model import Issue
from itertools import permutations


class ContributorsInteractionsAnalysis:
    """
    1. Analyzes and visualizes the interaction network between contributors based on issue comments and events.
    2. Identifies key contributors, collaboration patterns, and community structure within the project.
    """

    def __init__(self):
        self.LABEL: str = config.get_parameter('label')
        self.USER: str = config.get_parameter('user')

    def run(self):
        issues: List[Issue] = DataLoader().get_issues()
        graph = self.create_graph(issues)
        degree_centrality, top_contributors = self.analyze_network(graph)
        self.visualize_results(graph, degree_centrality, top_contributors)

    def analyze_network(self, graph):
        degree_centrality = nx.degree_centrality(graph)
        top_contributors = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:30]

        print("Top Contributors by Degree Centrality:")
        for contributor, centrality_score in top_contributors:
            print(f"{contributor}: {centrality_score:.4f}")

        return degree_centrality, top_contributors

    def create_graph(self, issues):
        interactions = []
        for issue in issues:
            if self.LABEL and self.LABEL not in issue.labels:
                continue

            participants = self.get_participants(issue)
            if self.USER:
                if self.USER not in participants:
                    continue

            # Create pairs of participants
            for p1 in participants:
                for p2 in participants:
                    if p1 != p2:
                        interactions.append((p1, p2))

        graph = nx.Graph()
        for c1, c2 in interactions:
            if graph.has_edge(c1, c2):
                graph[c1][c2]['weight'] += 1
            else:
                graph.add_edge(c1, c2, weight=1)

        if graph.number_of_nodes() == 0:
            print("No interactions found for the specified filters.")
            sys.exit(1)
        return graph

    def get_participants(self, issue):
        participants = set()
        if issue.creator:
            participants.add(issue.creator)
        for event in issue.events:
            if event.author:
                participants.add(event.author)
        return participants

    def visualize_results(self, graph, degree_centrality, top_contributors):
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(graph, k=0.15, iterations=20)

        node_sizes = [5000 * degree_centrality[node] for node in graph.nodes()]
        nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)

        edge_widths = [graph[u][v]['weight'] * 0.1 for u, v in graph.edges()]
        nx.draw_networkx_edges(graph, pos, width=edge_widths, alpha=0.5)

        labels = {node: node for node, _ in top_contributors}
        nx.draw_networkx_labels(graph, pos, labels, font_size=12)

        plt.title("Contributor Interaction Network")
        plt.axis('off')
        plt.tight_layout()
        plt.show()



if __name__ == '__main__':
    ContributorsInteractionsAnalysis().run()
