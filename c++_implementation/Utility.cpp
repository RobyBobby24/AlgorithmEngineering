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

node Utility::computeCommunityGateway(Graph* graph,  Graph* communityGraph, set<node> communityNodes, pair<node, double> maxLBC_node ){
    int maxICL = 0;
    list<node> maxICL_node;
    node result;
    for(auto nodeFrom = communityNodes.begin(); nodeFrom != communityNodes.end(); nodeFrom ++ ) {
        int totalDegree = graph->degree(*nodeFrom); // ToDo forse va messo il tipo count come anche nelle righe successive
        int innerDegree = communityGraph->degree(*nodeFrom);
        int outDegree = totalDegree - innerDegree;
        if (outDegree > maxICL) {
            maxICL_node = {*nodeFrom};
        }
        else if (outDegree == maxICL) {
            maxICL_node.push_back(*nodeFrom);
        }
    }
    if (maxICL_node.size() == 1){
        result = *maxICL_node.begin();
    }
    else {
        int minDistance = 0;
        int distance;
        node maxICL_node;
        for(auto nodeI = communityNodes.begin(); nodeI != communityNodes.end(); nodeI ++ ){
            BFS* bfs = new BFS( *communityGraph, *nodeI, false, false, maxLBC_node.first);
            bfs->run();
            distance = bfs->distance( maxLBC_node.first);
            if (minDistance == 0 || distance < minDistance){
                minDistance = distance;
                maxICL_node = maxLBC_node.first;
            }
        }
        result = maxICL_node;
    }
    return result;
}

double Utility::computeGLR(node nodeI, Graph* graph,list<node> LBC_nodes, list<node> gateways, double alpha1, double alpha2){
    MultiTargetBFS* bfs = new MultiTargetBFS(*graph, nodeI, LBC_nodes.begin(), LBC_nodes.end());
    bfs->run();
    vector<double> distances = bfs->getDistances();
    double summationLBC_distances = accumulate(distances.begin(), distances.end(), 0);

    bfs = new MultiTargetBFS(*graph, nodeI, gateways.begin(), gateways.end());
    bfs->run();
    distances = bfs->getDistances();
    double summationGatewaysDistances = accumulate(distances.begin(), distances.end(), 0);

    return 1.0/(alpha1*summationLBC_distances + alpha2*summationGatewaysDistances);
}

bool Utility::compareCentralityNode(pair<node, double> node1, pair<node, double> node2){
    return node1.second < node2.second ;
}

vector<pair<node, double>> Utility::stdImplementation(NetworKit::Graph* G){
    pair<Partition,  map<int, Graph>> plmCommunitiesAndGraphs = Utility::computeComunity(G);
    Partition* communitySets = &plmCommunitiesAndGraphs.first;
    map<int, Graph> communityGraphs = plmCommunitiesAndGraphs.second;

    map<int, pair<node, double>> maxLBC_community;
    list<node> maxLBC_communityList;
    map<int, int> gateways;
    list<node> gatewaysList;

    for(auto i = communityGraphs.begin(); i != communityGraphs.end(); i ++ ){
        pair<node, double> maxLBC_node = Utility::btwMax(&i->second);
        maxLBC_community[i->first] = maxLBC_node;
        maxLBC_communityList.push_back(maxLBC_node.first);
        node communityGateway = computeCommunityGateway(G, &communityGraphs[i->first], communitySets->getMembers(i->first), maxLBC_node);
        gatewaysList.push_back(communityGateway);
    }

    vector<pair<node, double>> rankingNodes;
    for( auto nodeI : G->nodeRange() ){
        double glrI = computeGLR(nodeI, G, maxLBC_communityList, gatewaysList);
        pair<node, double> nodeAndGLR = make_pair(nodeI, glrI);
        rankingNodes.push_back(nodeAndGLR);
    }
    sort(rankingNodes.begin(), rankingNodes.end(), Utility::compareCentralityNode);
    return rankingNodes;
}



