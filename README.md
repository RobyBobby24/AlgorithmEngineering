# AlgorithmEngineering
The aim of this university project is analyze the algorithm exposed [here](https://www.sciencedirect.com/science/article/abs/pii/S092523121831275X?casa_token=uQSmx9U9HxgAAAAA:1JfbA2SrgGFICH43U-8lCMaTgXkPRmTgr_bgqvfY_3w0DfIskMExfGWyb5c8tCascCNf2Ujmkcw). 

for this purpose i proceeded following this steps: 
1) Verify the algorithm coplexity;
2) Test performances of the algorithm changing and optimize it.

before running the  python code make sure you have already done follow steps (assuming that you are using a Linux base environment): 
1) install python and pip (sudo apt install python3 python3-pip)
2) install necessary library (pip install -r requirements.txt)

before running the  C++ code make sure you have already done follow steps (assuming that you are using a Linux base environment): 
1) install g++ (sudo apt install g++ )
2) install cmake (sudo apt install cmake)
3) install gpp (sudo apt install gpp)
5) install libboost filesystem library (sudo apt install libboost-filesystem-dev)
6) install libboost serialization library (sudo apt install libboost-serialization-dev) 
7) install libboost_program_options library (sudo apt install libboost-program-options-dev)
8) install libboost_timer library (sudo apt install libboost-timer-dev)
9) install networkit ([istallation guide](https://github.com/networkit/networkit))
10) set LD_LIBRARY_PATH environment variable to networkit library location or move it to /usr/lib/ (write on ~/.bashrc export LD_LIBRARY_PATH=location/networkit/build/)

once the python initial setup is completed you can run python code just follow this steps:
1) navigate to the 'python_implementation' directory (cd python_implementation)
2) set appropriately the option and run code (python3 algorithms_implementation.py -g < graphPath > -f < executionFlag > -p < partitionPath > -u) (the only mandatory option is the graphPath)
3) input the path to the graph when prompted

once the C++ initial setup is completed you can run C++ code just follow this steps:
1) navigate to the 'c++_implementation' directory (cd c++_implementation)
2) compile code (make release)
3) set appropriately the option and run code (./main -g < graphPath > -f < executionFlag > -p < partitionPath > -u true) (the only mandatory option is the graphPath)

once both setup is completed you can exec doubling experiment just follow this steps:
1) navigate to the 'c++_implementation' directory (cd c++_implementation)
2) compile code (make release)
3) navigate to the 'double_experiment' directory (cd ../double_experiment)
4) setup experiment config (doubleexp_config.json)
5) run double_experiment file (python3 double_experiment.py)

once python setup is completed you can generate new graphs just follow this steps:
1) navigate to the 'graphs_generators' directory (cd utility/graphs_generators)
2) setup graphs generator config (genconfig.json)
3) generate graphs (python3 generate.py)

once python setup is completed you can generate new partition just follow this steps:
1) navigate to the 'partition_generators' directory (cd utility/partition_generators)
2) setup partitions generator config (partition_config.json)
3) generate graphs (python3 compute_partition.py)

- all results could be found in "results" folder
- the analysis of the results could be found in "analysis" folder
- all generated graphs could be found in "graphs" folder
- all generated partitions could be found in "partial_results/partitions" folder
