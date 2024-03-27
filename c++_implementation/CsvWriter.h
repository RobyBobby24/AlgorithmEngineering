

#ifndef PROJECT_CSVWRITER_H
#define PROJECT_CSVWRITER_H

#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <map>
#include <utility>

template<typename RowType>
using namespace std;

class CsvWriter {
    public:
        CsvWriter();
        virtual ~CsvWriter();
        void CsvWriter::write(vector<RowType> data, string filePath, string labels[],  map<string, string> (*itemToRowFunc)(RowType), bool overwrite=False);
        void CsvWriter::write(vector<RowType> data, string filePath, string labels[], bool overwrite=False);

};

#endif
