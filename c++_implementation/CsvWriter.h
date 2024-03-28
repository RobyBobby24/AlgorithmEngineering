

#ifndef PROJECT_CSVWRITER_H
#define PROJECT_CSVWRITER_H

#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <map>
#include <utility>

class CsvWriter {
    public:
        CsvWriter();
        virtual ~CsvWriter();
        void write(std::vector<std::map<std::string, std::string>> data, std::string filePath, std::string labels[],int labelsSize, bool overwrite=false);

};

#endif
