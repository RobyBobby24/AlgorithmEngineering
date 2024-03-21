# AlgorithmEngineering
The aim of this university project is analyze the algorithm exposed [here](https://www.sciencedirect.com/science/article/abs/pii/S092523121831275X?casa_token=uQSmx9U9HxgAAAAA:1JfbA2SrgGFICH43U-8lCMaTgXkPRmTgr_bgqvfY_3w0DfIskMExfGWyb5c8tCascCNf2Ujmkcw). 

for this purpose i proceeded following this steps: 
1) Verify the algorithm coplexity;
2) Test performances of the algorithm changing the centrality measure intra community.

before running the  python code make sure you have already done follow steps: 
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