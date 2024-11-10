import sys
from typing import List, Dict

import matplotlib.pyplot as plt
import networkx as nx

import config
from data_loader import DataLoader
from models.Issue import Issue
from analyses.base_feature import BaseFeature
import argparse


class ContributorsInteractionsAnalysis(BaseFeature):
    """
    1. Analyzes and visualizes the interaction network between contributors based on issue comments and events.
    2. Identifies key contributors, collaboration patterns, and community structure within the project.
    """

    @property
    def feature_id(self) -> int:
        return 4

    def name(self) -> str:
        return 'ContributorsInteractionsAnalysis'

    def description(self) -> str:
        return (
            'Visualizes the interaction network between contributors based on issue comments and events'
        )

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--label',
            type=str,
            required=False,
            help='Optional parameter for analyses focusing on a specific label'
        )
        parser.add_argument(
            '--user',
            type=str,
            required=False,
            help='Optional parameter to focus on a specific user'
        )

    def get_arguments_info(self) -> List[Dict[str, str]]:
        return [
            {
                'flags': '--label',
                'help': 'Optional parameter for analyses focusing on a specific label'
            },
            {
                'flags': '--user',
                'help': 'Optional parameter to focus on a specific user'
            }
        ]

    def run(self, args):
        issues: List[Issue] = DataLoader().get_issues()
        graph = self.__create_graph(issues, args.label, args.user)
        degree_centrality, top_contributors = self.__analyze_network(graph)
        self.__visualize_results(graph, degree_centrality, top_contributors)

    def __analyze_network(self, graph):
        degree_centrality = nx.degree_centrality(graph)
        top_contributors = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:30]

        print("Top Contributors by Degree Centrality:")
        for contributor, centrality_score in top_contributors:
            print(f"{contributor}: {centrality_score:.4f}")

        return degree_centrality, top_contributors

    def __create_graph(self, issues, label_filter, user_filter):
        interactions = []
        for issue in issues:
            if label_filter and label_filter not in issue.labels:
                continue

            participants = self.__get_participants(issue)
            if user_filter:
                if user_filter not in participants:
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

    def __get_participants(self, issue):
        participants = set()
        if issue.creator:
            participants.add(issue.creator)
        for event in issue.events:
            if event.author:
                participants.add(event.author)
        return participants

    def __visualize_results(self, graph, degree_centrality, top_contributors):
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