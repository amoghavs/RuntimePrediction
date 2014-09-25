
Contents of repo:

File							Role
RuntimeBenchmarksGeneration.py			Generates the source file but does not have MPI constructs.
MPIRuntimeBenchmarksGeneration.py		Generates the source file also has MPI constructs.
ConfigGeneratorCompile.py			Generates permutation of all the parameters, generate the source file for specific configuration and compile it.
CommandLineConfigGeneratorCompile.py		Has command line options for few of parameters used in ConfigGen...
RandomConfigGeneratorCompile.py			Same as ConfigGen.. but is tailored to generate tests for random access. CAUTION: Do not use Min/Max stride to be anything other than 1.
BenchmarksResultLogging.py			Gets a list of source files' name, run them, detects basic blocks of the function and then simulate it. Different Spatial Windows can be used. 
SourceFiles.log					Sample list of source files. 
config.txt					Sample config file for RuntimeBenchmarksGen.. 
 
