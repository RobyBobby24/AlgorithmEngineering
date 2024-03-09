from networkit import readGraph
from networkit import Format
from networkit import community as comity
from networkit import graphtools
from networkit import centrality
from networkit.graph import Graph
from networkit.distance import BFS


# plmCommunities = detectCommunities(G)
def compute_community(G):
    plm_communities = comity.detectCommunities(G, algo=comity.PLM(G, True))
    community_induced_graph = {}
    for i in range(plm_communities.numberOfSubsets()):
        subset = plm_communities.getMembers(i)
        community_induced_graph[i] = graphtools.subgraphFromNodes(G, subset)
    return plm_communities, community_induced_graph


def btw_max(graph):
    LBC = centrality.Betweenness(graph)
    LBC.run()
    return LBC.ranking()[1]


def compute_community_gateway(graph: Graph, community_graph: Graph, community_nodes, max_LBC_node):
    max_ICL = 0
    max_ICL_nodes = []
    for node_from in community_nodes:
        total_degree = graph.degree(node_from)
        inner_degree = community_graph.degree(node_from)
        out_degree = total_degree - inner_degree
        if out_degree > max_ICL:
            max_ICL_nodes = [node_from]
            max_ICL = out_degree
        elif out_degree == max_ICL:
            max_ICL_nodes.append(node_from)

    if len(max_ICL_nodes) == 1:
        return max_ICL_nodes[0]
    else:
        min_distance = 0
        max_ICL_node = -1
        for node in max_ICL_nodes:
            bfs = BFS(community_graph, node, False, False, max_LBC_node)
            bfs.run()
            distance = bfs.distance(max_LBC_node)
            if max_ICL_node == -1 or distance < min_distance:
                min_distance = distance
                max_ICL_node = node
        return max_ICL_node











def community_centrality_std(G):
    community_sets, community_graphs = compute_community(G)
    max_LBC_community = {}
    gateways = {}
    for i in community_graphs.keys():
        max_LBC_node = btw_max(community_graphs[i])[0]
        max_LBC_community[i] = max_LBC_node
        gateways[i] = compute_community_gateway(G, community_graphs[i], community_sets.getMembers(i), max_LBC_node)
    print(max_LBC_community)


if __name__ == "__main__":
    G = readGraph("../graphs/exemple_small.graph", Format.METIS)
    print(type(G))
    community_centrality_std(G)
