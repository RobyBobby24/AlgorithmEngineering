//============================================================================
// Name        : standard_implementation.cpp
// Author      : Roberto Di Stefano
// Version     : 0.0
// Copyright   : Copyright © 2024 by Roberto Di Stefano
// Description :
//============================================================================
#include <iostream>
#include <boost/program_options.hpp>
#include "AlgorithmsImplementation.h"
#include "CsvWriter.h"
#include <networkit/io/METISGraphReader.hpp>
#include "mytimer.h"

using namespace std;
using namespace NetworKit;

vector<map<string, string>> ToCsvFormat(vector<pair<node, double>> rankingNodes, string labels[2]){
    vector<map<string, string>> data;
    for( auto dataRow = rankingNodes.begin(); dataRow != rankingNodes.end(); ++dataRow){
        map<string, string> row;
        row[ labels[0]] = to_string(dataRow -> first);
        row[ labels[1]] = to_string(dataRow -> second);
        data.push_back(row);
    }
    return data;
}

string getFileName(string filePath) {
    // Find position of the last '/'
    size_t lastSlashPos = filePath.find_last_of('/');
    string fileName = filePath;
    // Check if is valid position
    if (lastSlashPos != std::string::npos) {
        // Get Substring '/'
        fileName = filePath.substr(lastSlashPos + 1);
    }

    return fileName;
}

int main(int argc, char** argv) {
	// number of string writed from user
	// argv array of string writed (program_name, 1°param, ...)
	cout << "Start Algorithm\n";


	namespace po = boost::program_options; // define po namespace
	po::options_description desc("Allowed options");

	desc.add_options()
	("graph_location,g", po::value<std::string>(), "Input Graph File Location")
	("flag,f", po::value<std::string>(), "Input Flag String")
	("partitionPath,p", po::value<std::string>(), "Input Partition File Location");


	po::variables_map vm;
	po::store(po::parse_command_line(argc, argv, desc), vm);
	po::notify( vm);

	int source = -1;
	string graph_location;
	string flag;
	string partitionPath = "";

	if (vm.empty()){
			cout << desc << "\n";
			throw runtime_error("Empty options");
	}

	if (vm.count("graph_location"))
			graph_location = vm["graph_location"].as<string>();

    if (vm.count("flag")) {
            flag = vm["flag"].as<std::string>();
    }
    if (vm.count("partitionPath")) {
            partitionPath = vm["partitionPath"].as<std::string>();
    }

	if(graph_location == ""){
		cout << desc << "\n";
		throw std::runtime_error("wrong graph_location");
	}


    // read graph
	METISGraphReader* graphReader = new METISGraphReader();
	Graph* graph = new Graph();

	*graph = graphReader->read(graph_location);
	std::cout << "number of nodes: " << graph->numberOfNodes()<< "\n";

	// get graph file name
	string fileName = getFileName(graph_location);

    // setup time
    mytimer* t_counter = new mytimer();
    map<string, string>* elapsedMap = new map<string, string>();
    elapsedMap->insert({"Code", "C++"});
    elapsedMap->insert({"Graph", fileName});
    elapsedMap->insert({"Flag", flag});
    // algorithm execution
    vector<pair<node, double>> rankingNodes = AlgorithmsImplementation::stdImplementation(graph, t_counter, elapsedMap, partitionPath);

    // save results
    string labels[2] = {"Node", "Centrality Degree"};
    CsvWriter* csvWriter = new CsvWriter();
    vector<map<string, string>> rankingNodesCsv = ToCsvFormat(rankingNodes, labels);
    string pathFile = "../results/C++Std";
    pathFile = pathFile + "(" + fileName + ")";
    csvWriter->write(
            rankingNodesCsv,
            pathFile,
            labels,
            2);


// save times
    string labelsTime[7] = {"Code", "Graph", "Flag", "Community computation","Nodes computation", "GLR computation", "Total"};
    vector<map<string, string>> elapsedMapCsv;
    elapsedMapCsv.push_back(*elapsedMap);
    csvWriter->write(
            elapsedMapCsv,
            "../results/time",
            labelsTime,
            7,
            ios::app);



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
	delete t_counter;
    delete csvWriter;


	return 0;
}






