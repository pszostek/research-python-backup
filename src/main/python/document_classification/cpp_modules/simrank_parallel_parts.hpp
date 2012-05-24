#ifndef SIMRANK_PARALLEL_PARTS
#define SIMRANK_PARALLEL_PARTS

#include "simrank_basic.hpp"


//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////

struct ThreadArgs {
	ThreadArgs(const Graph* graph): g(graph) {
		start_b = end_b = start_a = end_a = 0;
		Rn = NULL;
		Rp = NULL;
		C = 0.0;
	}
	int start_a, end_a, start_b, end_b;
	pthread_t tid;
	RNext* Rn;
	RPrev* Rp;
	double C;
	const Graph* g;
};

vector<ThreadArgs> prepareThreadsArgs(int numThreads, const Graph* graph, double C) {
	vector<ThreadArgs> targs;
	int numNodes = graph->getNumNodes();
	int nodesPerThread = numNodes/numThreads + 1;
	cerr<<"[prepareThreadsArgs] nodesPerThread="<<nodesPerThread<<endl;
	for (int t=0; t<numThreads; ++t) {
		ThreadArgs args(graph);
		args.start_a	= min(t*nodesPerThread, numNodes-1);
		args.end_a		= min((t+1)*nodesPerThread, numNodes);
		args.start_b 	= 0;
		args.end_b 		= numNodes;
		args.C 			= C;
		//args.storage = allocMatrix<double>(args.end_a-args.start_a, numNodes);
		targs.push_back(args);
	}
	return targs;
}

void setThreadArgsR(vector<ThreadArgs>& targs, RNext* rnext, RPrev* rprev) {
	for (int i=0; i<targs.size(); ++i) {
		targs[i].Rn = rnext;
		targs[i].Rp = rprev;
	}
}

void clearThreadArgs(vector<ThreadArgs>& targs) {
	for (int i=0; i<targs.size(); ++i) {
		//freeMatrix(targs[i].storage, targs[i].end_a-targs[i].start_a);
		//targs[i].storage = NULL;
		targs[i].end_b=targs[i].start_b=targs[i].end_a=targs[i].start_a=0;
		targs[i].C = 0.0;
		targs[i].Rn = NULL;
		targs[i].Rp = NULL;
	}
}

void waitThreads(vector<ThreadArgs>& targs) {
	for (int t=0; t<targs.size(); ++t) {
		pthread_join(targs[t].tid, (void **)NULL);
	}
}

///////////////////////////////////////////////////////////////

void* rnextSingleThread(void* arg) {
	ThreadArgs* targs = (ThreadArgs*)arg;
	//cerr<<"[rnextSingleThread] Thread="<<targs->tid<<" range="<<targs->start_a<<"-"<<targs->end_a<<endl;
	calcRnext(	targs->g, targs->Rp, targs->Rn,
				targs->C,
				targs->start_a, targs->end_a,
				targs->start_b, targs->end_b);
}

void* initR0SingleThread(void* arg) {
	ThreadArgs* targs = (ThreadArgs*)arg;
	initR0(	targs->g, targs->Rn,
			targs->start_a, targs->end_a,
			targs->start_b, targs->end_b);
}


void calcRnextParallel(RPrev* Rp, RNext* Rn, vector<ThreadArgs>& targs) {
	setThreadArgsR(targs, Rn, Rp);
	for (int t=0; t<targs.size(); ++t) {
		pthread_create(&(targs[t].tid), NULL, &rnextSingleThread, &targs[t]);
	}
	waitThreads(targs);
}


void initR0Parallel(RNext* R0, vector<ThreadArgs>& targs) {
	setThreadArgsR(targs, R0, NULL);
	for (int t=0; t<targs.size(); ++t) {
		pthread_create(&(targs[t].tid), NULL, &initR0SingleThread, &targs[t]);
	}
	waitThreads(targs);
}

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////


#endif
