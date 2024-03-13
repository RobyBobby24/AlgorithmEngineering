#ifndef UTILITY_H_
#define UTILITY_H_

#include <networkit/Globals.hpp>
#include <networkit/graph/Graph.hpp>
#include <networkit/community/PLM.hpp>
#include <networkit/structures/Partition.hpp>
#include <networkit/graph/GraphTools.hpp>
#include <networkit/centrality/Betweenness.hpp>
#include <unordered_set>
#include <list>
#include <vector>
#include <map>
#include <iostream>
#include <utility>

class Utility {
    public:
        Utility();
        virtual ~Utility();
        static void stdImplementation(NetworKit::Graph* G);

    private:
        static std::pair<NetworKit::Partition,  std::map<int, NetworKit::Graph>> computeComunity(NetworKit::Graph* G);
        static std::pair<NetworKit::node, double> btwMax(NetworKit::Graph* graph);
        static NetworKit::node Utility::computeCommunityGateway(NetworKit::Graph* graph,  NetworKit::Graph* communityGraph, std::set<NetworKit::index> communityNodes, std::pair<NetworKit::node, double> maxLBC_node );


};
#endif
