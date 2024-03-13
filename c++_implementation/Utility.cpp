//============================================================================
// Name        : standard_implementation.cpp
// Author      : Roberto Di Stefano
// Version     : 0.0
// Copyright   : Copyright © 2024 by Roberto Di Stefano
// Description :
//============================================================================
#include "Utility.h"

//using namespace NetworKit::CommunityDetectionAlgorithm;
using namespace NetworKit::GraphTools;
using namespace NetworKit;
using namespace std;

Utility::Utility(){}

Utility::~Utility(){}

pair<Partition*,  list<Graph*>> Utility::computeComunity(Graph* G){
    PLM* plmCommunityAlgo = new PLM(*G);
    plmCommunityAlgo->run();

    Partition* plmCommunity = new Partition();
    *plmCommunity = plmCommunityAlgo->getPartition();

    list<Graph*> community_graphs;
    for(int i=0; i < plmCommunity->numberOfSubsets(); ++i){
        set<index> subset = plmCommunity->getMembers(i);
        unordered_set<index> subset_unordered  (subset.begin(), subset.end() );
        Graph community_graph = subgraphFromNodes(*G, subset_unordered);
        community_graphs.push_back(&community_graph);
    }

    pair<Partition*,  list<Graph*>> result (plmCommunity, community_graphs );

    delete plmCommunityAlgo;

    return result;
}

void Utility::stdImplementation(NetworKit::Graph* G){
    pair<Partition*,  list<Graph*>> plmCommunitiesAndGraphs = Utility::computeComunity(G);
    cout << plmCommunitiesAndGraphs.first << "end Algorithm\n";
}



