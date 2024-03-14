//============================================================================
// Name        : standard_implementation.cpp
// Author      : Roberto Di Stefano
// Version     : 0.0
// Copyright   : Copyright © 2024 by Roberto Di Stefano
// Description :
//============================================================================
#include "Utility.h"

//using namespace NetworKit::CommunityDetectionAlgorithm;
//using namespace NetworKit::Centrality;
//using namespace NetworKit::SSSP;
using namespace NetworKit::GraphTools;
using namespace NetworKit;
using namespace std;

Utility::Utility(){}

Utility::~Utility(){}

pair<Partition,  map<int, Graph>> Utility::computeComunity(Graph* G){
    PLM* plmCommunityAlgo = new PLM(*G);
    plmCommunityAlgo->run();

    Partition* plmCommunity = new Partition();
    *plmCommunity = plmCommunityAlgo->getPartition();


    map<int, Graph> community_graphs;
    for(int i=0; i < plmCommunity->numberOfSubsets(); ++i){
        set<index> subset = plmCommunity->getMembers(i);
        unordered_set<index> subset_unordered  (subset.begin(), subset.end() );
        Graph community_graph = subgraphFromNodes(*G, subset_unordered);
        community_graphs[i] = community_graph;
    }

    pair<Partition,  map<int, Graph>> result (*plmCommunity, community_graphs );

    delete plmCommunityAlgo;
    delete plmCommunity;

    return result;
}

pair<node, double> Utility::btwMax(Graph* graph){
    Betweenness* LBC = new Betweenness( *graph);
    LBC->run();
    pair<node, double> result = LBC->ranking()[1];
    delete LBC;

    return result;
}

node Utility::computeCommunityGateway(Graph* graph,  Graph* communityGraph, set<index> communityNodes, pair<node, double> maxLBC_node ){
    int maxICL = 0;
    list<node> maxICL_node;
    node result;
    for(auto nodeFrom = communityNodes.begin(); nodeFrom != communityNodes.end(); nodeFrom ++ ) {
        int totalDegree = graph->degree(
                nodeFrom); // ToDo forse va messo il tipo count come anche nelle righe successive
        int innerDegree = communityGraph->degree(&nodeFrom);
        int outDegree = totalDegree - innerDegree;
        if (outDegree > maxICL) {
            maxICL_node = {&nodeFrom}
        } else if (outDegree == maxICL) {
            maxICL_node.push_back(&nodeFrom)
        }
    }
    if (maxICL_node.size() == 1){
        result = maxICL_node[0];
    }
    else {
        int minDistance = 0;
        int distance;
        node maxICL_node;
        for(auto nodeI = communityNodes.begin(); nodeI != communityNodes.end(); nodeI ++ ){
            BFS* bfs = new BFS( &communityGraph, &nodeI, false, false, maxLBC_node.first);
            bfs.run();
            distance = bfs.distance( maxLBC_node.first);
            if (minDistance == 0 || distance < minDistance){
                minDistance = distance;
                maxICL_node = maxLBC_node.first
            }
        }
        result = maxICL_node
    }
    return result
}

void Utility::stdImplementation(NetworKit::Graph* G){
    pair<Partition,  map<int, Graph>> plmCommunitiesAndGraphs = Utility::computeComunity(G);
    Partition* communitySets = &plmCommunitiesAndGraphs.first;
    map<int, Graph> communityGraphs = plmCommunitiesAndGraphs.second;

    map<int, int> maxLBC_community;
    map<int, int> gateways;

    for(auto i = communityGraphs.begin(); i != communityGraphs.end(); i ++ ){
        pair<node, double> maxLBC_node = Utility::btwMax(&i->second);
        maxLBC_community[i->first] = maxLBC_node;
        gateways[i] = computeCommunityGateway(G, communityGraphs[i], communitySets.getMembers(i), maxLBC_node);
    }
    // continua da riga 74


    cout << "end Algorithm\n";
}



