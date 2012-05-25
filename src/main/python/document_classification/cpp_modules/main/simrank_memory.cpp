#include <iostream>
#include <iomanip>
#include "../graph.hpp"
#include "../simrank/simrank.hpp"

const int DOUBLE_FILE_PRECISION = 10;

int main(int argc, char *argv[]) {
	cerr<<"The program calculates simrank for given graph (result stored in memory)..."<<endl;
	cerr<<"Input records are read from stdin and output matrix is printed out to stdout."<<endl;
	cerr<<"Optional args: C,numIter,numThreads."<<endl;
	double C = 0.6;
	int numIter = 10;
	int numThreads = 1;
	if (argc > 1) {
		C = atof(argv[1]);
	}
	if (argc > 2) {
		numIter = atoi(argv[2]);
	}
	if (argc > 3) {
		numThreads = atof(argv[3]);
	}
	cerr<<setprecision(DOUBLE_FILE_PRECISION);
	cerr.setf(ios::fixed, ios::floatfield);
	cerr.setf(ios::showpoint);

	cerr<<"Loading graph..."<<endl;
	Graph g(cin);
	cerr<<g.node2ix.size()<<" nodes loaded"<<endl;
	//g.print(cerr);
	//vector<NodeId> nodes = g.getNodes();
	//ofstream nodes_file("/tmp/loaded_nodes.txt");
	//for (int i=0; i <nodes.size(); ++i) nodes_file<<nodes[i]<<endl;

	cerr<<"Calculating simrank..."<<endl;
	cerr<<"\tC="<<C<<"\tnumIter="<<numIter<<"\tnumThreads="<<numThreads<<endl;
	//DummyRFactory rFactory;
	MemoryRFactory rFactory;
	simrankParallel(&g, &rFactory, C, numIter, numThreads);
	//LineMemoryRFactory rFactory;
	//simrankSingleLineParallel(&g, &rFactory, C, numIter, numThreads);

	cerr<<"Printing out results..."<<endl;
	g.printLabels(cout);
	g.printLabels(cout);
	cout<<setprecision(DOUBLE_FILE_PRECISION);
	cout.setf(ios::fixed, ios::floatfield);
	cout.setf(ios::showpoint);
	rFactory.printData(cout);

	return 0;

}
