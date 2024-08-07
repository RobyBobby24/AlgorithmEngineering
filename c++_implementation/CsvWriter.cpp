//============================================================================
// Name        : standard_implementation.cpp
// Author      : Roberto Di Stefano
// Version     : 0.0
// Copyright   : Copyright © 2024 by Roberto Di Stefano
// Description :
//============================================================================

#include "CsvWriter.h"

using namespace std;
using namespace std::filesystem;

CsvWriter::CsvWriter(){}

CsvWriter::~CsvWriter() {}

void CsvWriter::write(vector<map<string, string>> data, string filePath, string labels[], int labelsSize,std::ios_base::openmode mode, bool overwrite) {
    string fileName = filePath;
    if( !overwrite && mode != ios::app ){
        int resultId = 0;
        while(exists(fileName+".csv")){
            fileName = filePath + to_string(resultId);
            resultId += 1;
        }
    }


    fileName = fileName + ".csv";
    bool existFile = exists(fileName);
    ofstream csvFile (fileName, mode);
    if(!existFile || mode != ios::app){
        for (int i = 0; i < labelsSize-1; ++i) {
            csvFile << labels[i] << ";";
        }
        csvFile << labels[labelsSize-1] << "\n";
    }

    for (auto row = data.begin(); row != data.end(); ++row){
        for (int i = 0; i < labelsSize-1; ++i) {
            csvFile << row->at( labels[i] )<< ";";
        }
        csvFile << row->at( labels[labelsSize-1] ) << "\n";

    }

    csvFile.close();

}

