from networkit import readGraph
from networkit import Format
from networkit import community as comity
from networkit import graphtools
from networkit import centrality


#plmCommunities = detectCommunities(G)
def compute_community(G):
    plm_communities = comity.detectCommunities(G, algo=comity.PLM(G, True))
    community_induced_graph = {}
    for i in range(plm_communities.numberOfSubsets()):
        graphtools.subgraphAndNeighborsFromNodes(G, plm_communities)
    return plm_communities, community_induced_graph,

def community_centrality_std(G):
    community_sets, community_graphs = compute_community(G)
    max_LBC_community = {}
    for i in community_graphs.keys():
        LBC = centrality.Betweenness(community_graphs[i])
        LBC.run()
        max_LBC_community[i] = LBC.ranking()[1]



if __name__ == "__main__":
    G = readGraph("../graphs/exemple_small.graph", Format.METIS)
    community_centrality_std(G)