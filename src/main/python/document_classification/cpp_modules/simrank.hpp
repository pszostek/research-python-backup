
#ifndef SIMRANK_HPP
#define SIMRANK_HPP

#include "simrank_parallel_parts.hpp"

void simrank(const Graph* g, RFactory* rFactory, double C, int numIter) {
	cerr<<"[simrank] running sequenced version"<<endl;
	RNext* R0 = rFactory->getInitial(g);
	long starttime = time(0);
	initR0(g, R0);
	//rFactory->printData(cerr);

	for (int it=0; it<numIter; ++it) {
		cerr<<"[simrank]["<<(time(0)-starttime)<<"s] iteration no "<<it<<" started"<<endl;
		RNext* Rn = rFactory->getNext();
		RPrev* Rp = rFactory->getPrev();
		calcRnext(g, Rp, Rn, C);
		//rFactory->printData(cerr);
	}
};

void simrankParallel(const Graph* g, ParallelRFactory* rFactory, double C, int numIter, int numThreads=1) {
	if (numThreads == 1) {
		simrank(g, rFactory, C, numIter);
		return;
	}
	cerr<<"[simrank] running parallel version"<<endl;
	RNext* R0 = rFactory->getInitial(g, numThreads);
	long starttime = time(0);
	vector<ThreadArgs> targs = prepareThreadsArgs(numThreads, g, C);
	initR0Parallel(R0, targs);

	for (int it=0; it<numIter; ++it) {
		cerr<<"[simrank]["<<(time(0)-starttime)<<"s] iteration no "<<it<<" started"<<endl;
		RNext* Rn = rFactory->getNext();
		RPrev* Rp = rFactory->getPrev();
		calcRnextParallel(Rp, Rn, targs);
	}

	clearThreadArgs(targs);
};


#endif

