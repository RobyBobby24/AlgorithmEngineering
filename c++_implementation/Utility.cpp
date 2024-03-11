//============================================================================
// Name        : standard_implementation.cpp
// Author      : Roberto Di Stefano
// Version     : 0.0
// Copyright   : Copyright © 2024 by Roberto Di Stefano
// Description :
//============================================================================
#include "Utility.h"

using namespace NetworKit::CommunityDetectionAlgorithm;
using namespace NetworKit::GraphTools;
using namespace NetworKit;
using namespace std;
using namespace Utility;

Utility(){}

~Utility(){}

pair<Partition*,  list<Graph*>> computeComunity(Graph& G){
    PLM* plmCommunityAlgo;
    pair<Partition*,  list<Graph*>>* result;
    Partition* plmCommunity;
    list<Graph*>* community_graphs;

    plmCommunityAlgo = new PLM(G);
    plmCommunityAlgo->run();
    plmCommunity = new Partition();
    *plmCommunity = plmCommunityAlgo->getPartition();

    community_graphs = new list<Graph*>;
    for(int i=0; i < plmCommunity->numberOfSubsets(); ++i){
        unordered_set<index>* subset (plmCommunity->getMembers(i));
        community_graphs->push_back(subgraphFromNodes(G, subset&));
    }

    result.first = plmCommunity;
    result.second = community_graphs;

    delete plmCommunityAlgo;
}

pair<Partition*,  list<Graph*>> computeComunity(Graph& G){
    PLM* plmCommunityAlgo;
    pair<Partition*,  list<Graph*>>* result;
    Partition* plmCommunity;
    list<Graph*>* community_graphs;

    plmCommunityAlgo = new PLM(G);
    plmCommunityAlgo->run();
    plmCommunity = new Partition();


    return result;
}

static void stdImplementation(Graph& G){
    pair<Partition*,  list<Graph*>>* plmCommunitiesAndGraphs = computeComunity(G);
    cout << "end Algorithm";
}



