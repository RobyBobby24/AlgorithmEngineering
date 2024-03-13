#ifndef UTILITY_H_
#define UTILITY_H_

#include <networkit/graph/Graph.hpp>
#include <networkit/community/PLM.hpp>
#include <networkit/structures/Partition.hpp>
#include <networkit/graph/GraphTools.hpp>
#include <unordered_set>
#include <list>
#include <iostream>
#include <utility>

class Utility {
    public:
        Utility();

        static void stdImplementation(NetworKit::Graph* G);

        static std::pair<NetworKit::Partition*,  std::list<NetworKit::Graph*>> computeComunity(NetworKit::Graph* G);

        virtual ~Utility();

};
#endif
