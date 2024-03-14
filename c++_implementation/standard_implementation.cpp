//============================================================================
// Name        : standard_implementation.cpp
// Author      : Roberto Di Stefano
// Version     : 0.0
// Copyright   : Copyright © 2024 by Roberto Di Stefano
// Description :
//============================================================================
#include <iostream>
#include <boost/program_options.hpp>
#include "Utility.h"
#include <networkit/io/METISGraphReader.hpp>
#include "mytimer.h"

using namespace std;
using namespace NetworKit;

int main(int argc, char** argv) {
	// number of string writed from user
	// argv array of string writed (program_name, 1°param, ...)
	cout << "Start Algorithm\n";


	namespace po = boost::program_options; // define po namespace
	po::options_description desc("Allowed options");

	desc.add_options()
	("graph_location,g", po::value<std::string>(), "Input Graph File Location");


	po::variables_map vm;
	po::store(po::parse_command_line(argc, argv, desc), vm);
	po::notify( vm);

	int source = -1;
	string graph_location;

	if (vm.empty()){
			cout << desc << "\n";
			throw runtime_error("Empty options");
	}

	if (vm.count("graph_location"))
			graph_location = vm["graph_location"].as<string>();


	if(graph_location == ""){
		cout << desc << "\n";
		throw std::runtime_error("wrong graph_location");
	}

	METISGraphReader* graphReader = new METISGraphReader();
	Graph* graph = new Graph();

	*graph = graphReader->read(graph_location);
	std::cout << "number of nodes: " << graph->numberOfNodes()<< "\n";

    mytimer* t_counter = new mytimer();
    vector<pair<node, double>> rankingNodes = Utility::stdImplementation(graph);
    double elapsed = t_counter->elapsed();
    cout << "end Algorithm "<<"elapsed time: "<< elapsed << "\n";
    /*
    t_counter->restart();
    while(t_counter->elapsed() < 1){
        cout << "...";
    }

    cout << "\n Node \t|\t Centrality Degree \n";
    cout << "___________________________________\n";
    for(auto i = rankingNodes.begin(); i != rankingNodes.end(); i ++ ){
        cout << i->first << "\t|\t" << i->second << "\n";
        cout << "___________________________________\n";
    }
     */


	delete graphReader;
	delete graph;


	return 0;
}
