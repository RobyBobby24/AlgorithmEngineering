from networkit import community as comity
from networkit import readGraph
from networkit import Format
from networkit.graphio import BinaryPartitionWriter
from csv_writer import CsvWriter
import os

def save_community(G):
    plm_community_algo = comity.PLM(G, True)
    plm_community_algo.run()
    plm_communities = plm_community_algo.getPartition()
    partition_writer = BinaryPartitionWriter()
    partition_writer.write(plm_communities, "../partial_results/community")



    """
    for i in range(plm_communities.numberOfSubsets()):
        subset = plm_communities.getMembers(i)
        for member in subset:
            communities.append({"Node": member, "Community": i})
    
    CsvWriter().write(
        communities,
        "../partial_results/community",
        ["Node", "Community"]
    )
    """



if __name__ == '__main__':
    for i, gp in enumerate(os.listdir("../graphs/")):
        print(f"{i+1}) ../graphs/{gp}")
    graph_path = input("Enter the graph path (above you can find some suggestions):")
    G = readGraph(graph_path, Format.METIS)
    save_community(G)