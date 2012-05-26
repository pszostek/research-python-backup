#include <iostream>
#include <iomanip>
#include "../graph.hpp"
#include "../simrank/simrank_parallel.hpp"
#include "../simrank/simrank_dummy_storage.hpp"
#include "../simrank/simrank_memory_storage.hpp"
#include "../simrank/simrank_memdisk_storage.hpp"
#include "../simrank/simrank_line_parallel.hpp"

const int DOUBLE_FILE_PRECISION = 10;

int main(int argc, char *argv[]) {
	cerr<<"The program calculates simrank for given graph (result stored in memory)..."<<endl;
	cerr<<"Input records are read from stdin and output matrix is printed out to stdout."<<endl;
	cerr<<"Optional args: C,numIter,numThreads,mode."<<endl;
	double C = 0.6;
	int numIter = 10;
	int numThreads = 1;
	int mode = 0;
	if (argc > 1) {
		C = atof(argv[1]);
	}
	if (argc > 2) {
		numIter = atoi(argv[2]);
	}
	if (argc > 3) {
		numThreads = atof(argv[3]);
	}
	if (argc > 4) {
		mode = atoi(argv[4]);
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

	cerr<<"Printing out labels..."<<endl;
	g.printLabels(cout);
	g.printLabels(cout);
	cout<<setprecision(DOUBLE_FILE_PRECISION);
	cout.setf(ios::fixed, ios::floatfield);
	cout.setf(ios::showpoint);

	cerr<<"Calculating simrank..."<<endl;
	cerr<<"\tC="<<C<<"\tnumIter="<<numIter<<"\tnumThreads="<<numThreads<<endl;
	RFactory* output;
	if (mode==1) {
		cerr<<" Using MemoryRFactory..."<<endl;
		MemoryRFactory rFactory;
		simrankParallel(&g, &rFactory, C, numIter, numThreads);
		cerr<<"Printing out data..."<<endl;
		rFactory.printData(cout);
	} else if (mode==2) {
		cerr<<" Using MemDiskRFactory..."<<endl;
		MemDiskRFactory rFactory;
		simrankParallel(&g, &rFactory, C, numIter, numThreads);
		cerr<<"Printing out data..."<<endl;
		rFactory.printData(cout);
	} else if (mode==3) {
		cerr<<" Using DummyRFactory..."<<endl;
		DummyRFactory rFactory;
		simrankParallel(&g, &rFactory, C, numIter, numThreads);
		cerr<<"Printing out data..."<<endl;
		rFactory.printData(cout);
	} else {
		cerr<<" Using LineMemoryRFactory..."<<endl;
		LineMemoryRFactory rFactory;
		simrankSingleLineParallel(&g, &rFactory, C, numIter, numThreads);
		cerr<<"Printing out data..."<<endl;
		rFactory.printData(cout);
	}


	return 0;

}
