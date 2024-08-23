//============================================================================
// Name        : standard_implementation.cpp
// Author      : Roberto Di Stefano
// Version     : 0.0
// Copyright   : Copyright © 2024 by Roberto Di Stefano
// Description :
//============================================================================
#include "AlgorithmsImplementation.h"

//using namespace NetworKit::CommunityDetectionAlgorithm;
//using namespace NetworKit::Centrality;
using namespace NetworKit::GraphTools;
using namespace NetworKit;
using namespace std;

AlgorithmsImplementation::AlgorithmsImplementation(){}

AlgorithmsImplementation::~AlgorithmsImplementation(){}

pair<Partition*,  map<int, Graph*>> AlgorithmsImplementation::readCommunity(Graph* G, string filePath){
    BinaryPartitionReader* partitionReader = new BinaryPartitionReader();

    Partition* plmCommunity = new Partition();
    *plmCommunity = partitionReader->read(filePath);

    delete partitionReader;

    map<int, Graph*> community_graphs;
    for(int i= 0; i < plmCommunity->numberOfSubsets(); ++i){
        set<index> subset = plmCommunity->getMembers(i);
        unordered_set<index> subset_unordered  (subset.begin(), subset.end() );
        Graph* community_graph = new Graph( subgraphFromNodes(*G, subset_unordered));
        community_graphs[i] = community_graph;
    }

    pair<Partition*,  map<int, Graph*>> result (plmCommunity, community_graphs );

    return result;
}

pair<Partition*,  map<int, Graph*>> AlgorithmsImplementation::computeCommunity(Graph* G){
    PLM* plmCommunityAlgo = new PLM(*G, true);
    plmCommunityAlgo->run();

    Partition* plmCommunity = new Partition();
    *plmCommunity = plmCommunityAlgo->getPartition();


    map<int, Graph*> community_graphs;
    for(int i= 0; i < plmCommunity->numberOfSubsets(); ++i){
        set<index> subset = plmCommunity->getMembers(i);
        unordered_set<index> subset_unordered  (subset.begin(), subset.end() );
        Graph* community_graph = new Graph( subgraphFromNodes(*G, subset_unordered));
        community_graphs[i] = community_graph;
    }

    pair<Partition*,  map<int, Graph*>> result (plmCommunity, community_graphs );

    delete plmCommunityAlgo;

    return result;
}

pair<node, double> AlgorithmsImplementation::btwMax(Graph* graph){
    Betweenness* LBC = new Betweenness( *graph);
    LBC->run();
    pair<node, double> result = LBC->ranking()[0];
    delete LBC;

    return result;
}

node AlgorithmsImplementation::computeCommunityGateway(Graph* graph,  Graph* communityGraph, set<node> communityNodes, pair<node, double> maxLBC_node ){
    int maxICL = 0;
    list<node> maxICL_nodes;
    node result;
    for(auto nodeFrom = communityNodes.begin(); nodeFrom != communityNodes.end(); nodeFrom ++ ) {
        int totalDegree = graph->degree(*nodeFrom);
        int innerDegree = communityGraph->degree(*nodeFrom);
        int outDegree = totalDegree - innerDegree;
        if (outDegree > maxICL) {
            maxICL = outDegree;
            maxICL_nodes.clear();
            maxICL_nodes.push_back(*nodeFrom);
        }
        else if (outDegree == maxICL) {
            maxICL_nodes.push_back(*nodeFrom);
        }
    }
    if (maxICL_nodes.size() == 1){
        result = *maxICL_nodes.begin();
    }
    else {
        int minDistance = 0;
        int distance;
        node maxICL_node;
        for(auto nodeI = maxICL_nodes.begin(); nodeI != maxICL_nodes.end(); nodeI ++ ){
            BFS* bfs = new BFS( *communityGraph, *nodeI, false, false, maxLBC_node.first);
            bfs->run();
            distance = bfs->distance( maxLBC_node.first);
            if (minDistance == 0 || distance < minDistance){
                minDistance = distance;
                maxICL_node = *nodeI;
            }
        }
        result = maxICL_node;
    }
    return result;
}

double AlgorithmsImplementation::computeGLR(node nodeI, Graph* graph,list<node> LBC_nodes, list<node> gateways, double alpha1, double alpha2){
    MultiTargetBFS* bfs = new MultiTargetBFS(*graph, nodeI, LBC_nodes.begin(), LBC_nodes.end());
    bfs->run();
    vector<double> distances = bfs->getDistances();
    double summationLBC_distances = accumulate(distances.begin(), distances.end(), 0);

    bfs = new MultiTargetBFS(*graph, nodeI, gateways.begin(), gateways.end());
    bfs->run();
    distances = bfs->getDistances();
    double summationGatewaysDistances = accumulate(distances.begin(), distances.end(), 0);

    delete bfs;
    return 1.0/(alpha1*summationLBC_distances + alpha2*summationGatewaysDistances);
}

bool AlgorithmsImplementation::compareCentralityNode(pair<node, double> node1, pair<node, double> node2){
    return node1.second < node2.second ;
}

//undirected
vector<pair<node, double>> AlgorithmsImplementation::computeGlrUndirected(Graph* G, list<node> LBC_nodes, list<node> gateways, double alpha1, double alpha2){
    vector<pair<node, double>> result;
    list<node> sources = LBC_nodes;
    sources.insert(sources.end(), gateways.begin(), gateways.end());
    SPSP* distancesComputer = new SPSP(*G, sources.begin(), sources.end());
    distancesComputer->run();
    for( auto nodeI : G->nodeRange() ){
        double summationLBC_distances = 0.0;
        for(auto uI = LBC_nodes.begin(); uI != LBC_nodes.end(); uI ++ ){
            summationLBC_distances += distancesComputer->getDistance(*uI, nodeI);
        }
        double summationGatewaysDistances = 0.0;
        for(auto uI = gateways.begin(); uI != gateways.end(); uI ++ ){
            summationGatewaysDistances += distancesComputer->getDistance(*uI, nodeI);
        }
        double glrI = 1.0/(alpha1*summationLBC_distances + alpha2*summationGatewaysDistances);
        pair<node, double> nodeAndGLR = make_pair(nodeI, glrI);
        result.push_back(nodeAndGLR);
    }
    return result;
}


node AlgorithmsImplementation::computeCommunityGatewayUndirected(Graph* graph,  Graph* communityGraph, set<node> communityNodes, pair<node, double> maxLBC_node ){
    int maxICL = 0;
    list<node> maxICL_nodes;
    node result;
    for(auto nodeFrom = communityNodes.begin(); nodeFrom != communityNodes.end(); nodeFrom ++ ) {
        int totalDegree = graph->degree(*nodeFrom);
        int innerDegree = communityGraph->degree(*nodeFrom);
        int outDegree = totalDegree - innerDegree;
        if (outDegree > maxICL) {
            maxICL = outDegree;
            maxICL_nodes.clear();
            maxICL_nodes.push_back(*nodeFrom);
        }
        else if (outDegree == maxICL) {
            maxICL_nodes.push_back(*nodeFrom);
        }
    }
    if (maxICL_nodes.size() == 1){
        result = *maxICL_nodes.begin();
    }
    else {
        MultiTargetBFS* bfs = new MultiTargetBFS(*communityGraph, maxLBC_node.first, maxICL_nodes.begin(), maxICL_nodes.end());
        bfs->run();
        vector<double> distances = bfs->getDistances();
        int minDistance = 0;
        node maxICL_node;
        int i = 0;
        for(auto nodeI = maxICL_nodes.begin(); nodeI != maxICL_nodes.end(); nodeI ++ ){
            if (minDistance == 0 || distances[i] < minDistance){
                minDistance = distances[i];
                maxICL_node = *nodeI;
            }
            i += 1;
        }
        result = maxICL_node;
    }
    return result;
}

//algorithms
vector<pair<node, double>> AlgorithmsImplementation::stdImplementation(NetworKit::Graph* G, mytimer* t_counter, map<string, string>* elapsedMap, string partitionPath){
    pair<Partition*,  map<int, Graph*>> plmCommunitiesAndGraphs;
    if( partitionPath == "" ){
        plmCommunitiesAndGraphs = AlgorithmsImplementation::computeCommunity(G);
    }
    else{
        plmCommunitiesAndGraphs = AlgorithmsImplementation::readCommunity(G, partitionPath);
    }

    //pair<Partition*,  map<int, Graph*>>
    Partition* communitySets = plmCommunitiesAndGraphs.first;
    map<int, Graph*> communityGraphs = plmCommunitiesAndGraphs.second;

    double elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "community computation "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"Community computation", to_string(elapsed)});
    }
    t_counter->resume();

    //map<int, pair<node, double>> maxLBC_community;
    list<node> maxLBC_communityList;
    //map<int, int> gateways;
    list<node> gatewaysList;

    for(auto i = communityGraphs.begin(); i != communityGraphs.end(); i ++ ){
        if( communitySets->getMembers(i->first).size() != 0){
            pair<node, double> maxLBC_node = AlgorithmsImplementation::btwMax(i->second);
            //maxLBC_community[i->first] = maxLBC_node;
            maxLBC_communityList.push_back(maxLBC_node.first);
            node communityGateway = computeCommunityGateway(G, communityGraphs[i->first], communitySets->getMembers(i->first), maxLBC_node);
            gatewaysList.push_back(communityGateway);
        }
    }

    elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "nodes computation "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"Nodes computation", to_string(elapsed)});
    }
    t_counter->resume();

    vector<pair<node, double>> rankingNodes;
    for( auto nodeI : G->nodeRange() ){
        double glrI = computeGLR(nodeI, G, maxLBC_communityList, gatewaysList);
        pair<node, double> nodeAndGLR = make_pair(nodeI, glrI);
        rankingNodes.push_back(nodeAndGLR);
    }

    elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "GLR computation "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"GLR computation", to_string(elapsed)});
    }
    t_counter->resume();

    sort(rankingNodes.begin(), rankingNodes.end(), AlgorithmsImplementation::compareCentralityNode);
    elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "Total "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"Total", to_string(elapsed)});
    }
    t_counter->resume();


    return rankingNodes;
}



vector<pair<node, double>> AlgorithmsImplementation::undirectedImplementation(NetworKit::Graph* G, mytimer* t_counter, map<string, string>* elapsedMap, string partitionPath){
    pair<Partition*,  map<int, Graph*>> plmCommunitiesAndGraphs;
    if( partitionPath == "" ){
        plmCommunitiesAndGraphs = AlgorithmsImplementation::computeCommunity(G);
    }
    else{
        plmCommunitiesAndGraphs = AlgorithmsImplementation::readCommunity(G, partitionPath);
    }

    //pair<Partition*,  map<int, Graph*>>
    Partition* communitySets = plmCommunitiesAndGraphs.first;
    map<int, Graph*> communityGraphs = plmCommunitiesAndGraphs.second;

    double elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "community computation "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"Community computation", to_string(elapsed)});
    }
    t_counter->resume();

    //map<int, pair<node, double>> maxLBC_community;
    list<node> maxLBC_communityList;
    //map<int, int> gateways;
    list<node> gatewaysList;

    for(auto i = communityGraphs.begin(); i != communityGraphs.end(); i ++ ){
        if( communitySets->getMembers(i->first).size() != 0){
            pair<node, double> maxLBC_node = AlgorithmsImplementation::btwMax(i->second);
            //maxLBC_community[i->first] = maxLBC_node;
            maxLBC_communityList.push_back(maxLBC_node.first);
            node communityGateway = computeCommunityGatewayUndirected(G, communityGraphs[i->first], communitySets->getMembers(i->first), maxLBC_node);
            gatewaysList.push_back(communityGateway);
        }
    }

    elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "nodes computation "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"Nodes computation", to_string(elapsed)});
    }
    t_counter->resume();

    vector<pair<node, double>> rankingNodes = computeGlrUndirected(G, maxLBC_communityList, gatewaysList);

    elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "GLR computation "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"GLR computation", to_string(elapsed)});
    }
    t_counter->resume();

    sort(rankingNodes.begin(), rankingNodes.end(), AlgorithmsImplementation::compareCentralityNode);
    elapsed = t_counter->elapsed();
    t_counter->pause();
    cout << "Total "<<"elapsed time: "<< elapsed << "\n";
    if(elapsedMap != NULL){
        elapsedMap->insert({"Total", to_string(elapsed)});
    }
    t_counter->resume();


    return rankingNodes;
}



