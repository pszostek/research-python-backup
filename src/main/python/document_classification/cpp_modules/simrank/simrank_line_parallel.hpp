
#ifndef SIMRANK_LINE_PARALLEL
#define SIMRANK_LINE_PARALLEL

#include "../simrank/simrank_line_storage.hpp"

void setSingleLineThreadArgsR(vector<ThreadArgs>& targs, RNext* rnext, RPrev* rprev, int firstRow) {
	int numNodes = targs[0].g->getNumNodes();

	for (int i=0; i<targs.size(); ++i) {
		targs[i].Rn = rnext;
		targs[i].Rp = rprev;

		targs[i].start_a 	= min(firstRow+i, numNodes-1);
		targs[i].end_a		= min(firstRow+(i+1), numNodes);
	}
}

void calcRnextSingeLineParallel(LineMemoryRPrev* Rp, LineMemoryRNext* Rn, vector<ThreadArgs>& targs) {
	int numRows = targs[0].g->getNumNodes();

	for (int firstRow=0; firstRow<numRows; firstRow+=targs.size()) {
		if (firstRow%(3*targs.size())==0) cerr<<"[calcRnextSingeLineParallel] row="<<firstRow<<" out of "<<numRows<<endl;
		Rn->startingRow = firstRow;
		//cerr<<"[calcRnextSingeLineParallel] running next "<<targs.size()<<" threads starting from line "<<firstRow<<endl;
		setSingleLineThreadArgsR(targs, Rn, Rp, firstRow);
		for (int t=0; t<targs.size(); ++t) {
			//cerr<<"[calcRnextSingeLineParallel] Running Thread t="<<t<<endl;
			pthread_create(&(targs[t].tid), NULL, &rnextSingleThread, &targs[t]);
		}
		//cerr<<"[calcRnextSingeLineParallel] waiting for threads"<<endl;
		waitThreads(targs);
		//cerr<<"[calcRnextSingeLineParallel] saving temporary results starting from line "<<firstRow<<endl;
		Rn->saveTmpResults();
	}
}


void initR0SingeLineParallel(LineMemoryRNext* R0, vector<ThreadArgs>& targs) {
	int numRows = targs[0].g->getNumNodes();

	for (int firstRow=0; firstRow<numRows; firstRow+=targs.size()) {
		R0->startingRow = firstRow;
		//cerr<<"[initR0SingeLineParallel] running next "<<targs.size()<<" threads starting from line "<<firstRow<<endl;
		setSingleLineThreadArgsR(targs, R0, NULL, firstRow);
		for (int t=0; t<targs.size(); ++t) {
			//cerr<<"[initR0SingeLineParallel] Running Thread t="<<t<<endl;
			pthread_create(&(targs[t].tid), NULL, &initR0SingleThread, &targs[t]);
		}
		//cerr<<"[initR0SingeLineParallel] waiting for threads"<<endl;
		waitThreads(targs);
		//cerr<<"[initR0SingeLineParallel] saving temporary results starting from line "<<firstRow<<endl;
		R0->saveTmpResults();
	}

}


void simrankSingleLineParallel(const Graph* g, LineMemoryRFactory* rFactory, double C, int numIter, int numThreads=1) {
	cerr<<"[simrankLineStorage] running parallel version"<<endl;
	LineMemoryRNext* R0 = rFactory->getInitial(g, numThreads);
	long starttime = time(0);
	vector<ThreadArgs> targs = prepareThreadsArgs(numThreads, g, C);
	initR0SingeLineParallel(R0, targs);

	for (int it=0; it<numIter; ++it) {
		cerr<<"[simrankLineStorage]["<<(time(0)-starttime)<<"s] iteration no "<<it<<" started"<<endl;
		LineMemoryRNext* Rn = rFactory->getNext();
		LineMemoryRPrev* Rp = rFactory->getPrev();
		calcRnextSingeLineParallel(Rp, Rn, targs);
	}

	clearThreadArgs(targs);
}


#endif
