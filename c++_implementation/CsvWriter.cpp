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

void CsvWriter::write(vector<map<string, string>> data, string filePath, string labels[], bool overwrite=false) {

    if( !overwrite){
        int resultId = 0;
        string fileName = filePath;
        while(exists(fileName)){
            fileName = filePath + to_string(resultId)
        }
    }

    char delimiter = ";"

    ofstream csvFile (fileName);

    int size = sizeof(labels) / sizeof(labels[0]);

    for (int i = 0; i < size-1; ++i) {
        csvFile << array[i] << ";";
    }
    csvFile << array[size-1] << "\n";

    for (auto row = data.begin(); row != data.end(); ++row){
        for (int i = 0; i < size-1; ++i) {
            csvFile << *row[ array[i] ]<< ";";
        }
        csvFile << *row[ array[size-1] ] << "\n";

    }

    csvFile.close();

}

void CsvWriter::write(vector<RowType> data, string filePath, string labels[], map<string, string> (*itemToRowFunc)(RowType), bool overwrite=false) {
    if( !overwrite){
        int resultId = 0;
        string fileName = filePath;
        while(exists(fileName)){
            fileName = filePath + to_string(resultId)
        }
    }

    char delimiter = ";"

    ofstream csvFile (fileName);

    int size = sizeof(labels) / sizeof(labels[0]);

    for (int i = 0; i < size-1; ++i) {
        csvFile << array[i] << ";";
    }
    csvFile << array[size-1] << "\n";

    for (auto item = data.begin(); item != data.end(); ++item){
        map<string, string> row = itemToRowFunc(*item);
        for (int i = 0; i < size-1; ++i) {
            csvFile << row[ array[i] ]<< ";";
        }
        csvFile << row[ array[size-1] ] << "\n";

    }

    csvFile.close();

}

