#ifndef AlgorithmsImplementation_H_
#define AlgorithmsImplementation_H_

#include <networkit/Globals.hpp>
#include <networkit/graph/Graph.hpp>
#include <networkit/community/PLM.hpp>
#include <networkit/structures/Partition.hpp>
#include <networkit/graph/GraphTools.hpp>
#include <networkit/distance/BFS.hpp>
#include <networkit/distance/SPSP.hpp>
#include <networkit/distance/MultiTargetBFS.hpp>
#include <networkit/centrality/Betweenness.hpp>
#include <networkit/io/BinaryPartitionReader.hpp>
#include <unordered_set>
#include <list>
#include <vector>
#include <map>
#include <iostream>
#include <utility>
#include "mytimer.h"

class AlgorithmsImplementation {
    public:
        AlgorithmsImplementation();
        virtual ~AlgorithmsImplementation();
        static std::vector<std::pair<NetworKit::node, double>> stdImplementation(NetworKit::Graph* G, mytimer* t_counter, std::map<std::string, std::string>* elapsedMap=NULL, std::string partitionPath="");
        static std::vector<std::pair<NetworKit::node, double>> undirectedImplementation(NetworKit::Graph* G, mytimer* t_counter, std::map<std::string, std::string>* elapsedMap=NULL, std::string partitionPath="");

    private:
        static std::pair<NetworKit::Partition*,  std::map<int, NetworKit::Graph*>> computeCommunity(NetworKit::Graph* G);
        static std::pair<NetworKit::Partition*,  std::map<int, NetworKit::Graph*>> readCommunity(NetworKit::Graph* G, std::string filePath);
        static std::pair<NetworKit::node, double> btwMax(NetworKit::Graph* graph);
        static NetworKit::node computeCommunityGateway(NetworKit::Graph* graph,  NetworKit::Graph* communityGraph, std::set<NetworKit::index> communityNodes, std::pair<NetworKit::node, double> maxLBC_node );
        static double computeGLR(NetworKit::node nodeI, NetworKit::Graph* graph,std::list<NetworKit::node> LBC_nodes, std::list<NetworKit::node> gateways, double alpha1=0.5, double alpha2=0.5);
        static bool compareCentralityNode(std::pair<NetworKit::node, double> node1, std::pair<NetworKit::node, double> node2);
        static std::vector<std::pair<NetworKit::node, double>> computeGlrUndirected(NetworKit::Graph* G, std::list<NetworKit::node> LBC_nodes, std::list<NetworKit::node> gateways, double alpha1=0.5, double alpha2=0.5);
        static NetworKit::node computeCommunityGatewayUndirected(NetworKit::Graph* graph,  NetworKit::Graph* communityGraph, std::set<NetworKit::index> communityNodes, std::pair<NetworKit::node, double> maxLBC_node );


};
#endif
