CXX = g++ -std=c++17
DBG = -g
OPT = -Ofast -DNDEBUG -march=native
VALGRIND = -g -DNDEBUG
UTILITY = Utility


OPTIONS = -lboost_serialization -lboost_program_options -lboost_system -lboost_filesystem -fopenmp -lnetworkit -lboost_timer

INCLUDEPATH = $(HOME)/networkit/include/ -I/usr/include/valgrind  -I$(HOME)/networkit/extlibs/tlx/ -I$(HOME)/networkit/extlibs/ttmath/
PATHLIB = $(HOME)/networkit/build/

TARGETS = standard_implementation

debug:
	$(foreach var,$(TARGETS),$(CXX) $(var).cpp $(UTILITY).cpp $(DBG) -o $(var) -I$(INCLUDEPATH) -L$(PATHLIB) $(OPTIONS);)

release:
	$(foreach var,$(TARGETS),$(CXX) $(var).cpp $(UTILITY).cpp $(OPT) -o $(var) -I$(INCLUDEPATH) -L$(PATHLIB) $(OPTIONS);)

valgrind:
	$(foreach var,$(TARGETS),$(CXX) $(var).cpp $(UTILITY).cpp $(VALGRIND) -o $(var) -I$(INCLUDEPATH) -L$(PATHLIB) $(OPTIONS);)


clean:
	$(foreach var,$(TARGETS),rm -rf $(var);)
