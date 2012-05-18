
#ifndef SIMRANK_HPP
#define SIMRANK_HPP

#include "graph.hpp"
#include "simrank_storage.hpp"
#include <ctime>
#include <cmath>
#include <stdlib.h>

//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////


void initR0(const Graph* g, RNext* R0,
			int start_a=0, int end_a=-1, int start_b=0, int end_b=-1) {
	cerr<<"[simrank][initR0] initializing"<<endl;
	if (end_a < 0) end_a = g->getNumNodes();
	if (end_b < 0) end_b = g->getNumNodes();
	for (int a=start_a; a<end_a; ++a) {
		for (int b=start_b; b<end_b; ++b) {
			R0->set(a, b, double(a==b));
		}
	}
}

double calcRab(const IncomingNodes& Ia, const IncomingNodes& Ib,
			   RPrev* Rp, double C) {
	if (Ia.size()==0 || Ib.size()==0) return 0.0;
	double sum = 0.0;
	for (int i=0; i<Ia.size(); ++i) {
		for (int j=0; j<Ib.size(); ++j) {
			//cerr<<"[calcRab]"<<Ia[i]<<"-"<<Ib[j]<<"->"<<Rp->get(Ia[i], Ib[j])<<endl;
			sum += Rp->get(Ia[i], Ib[j]);
		}
	}
	return C*sum / (Ia.size() * Ib.size());
}

void calcRnext(const Graph* g, RPrev* Rp, RNext* Rn, double C,
		int start_a=0, int end_a=-1, int start_b=0, int end_b=-1) {
	if (end_a < 0) end_a = g->getNumNodes();
	if (end_b < 0) end_b = g->getNumNodes();
	for (int a=start_a; a<end_a; ++a) {
		for (int b=start_b; b<end_b; ++b) {
			//cerr<<"[calcRnext]"<<a<<"-"<<b<<"----------"<<endl;
			double val = (a==b)? 1.0: calcRab(g->I[a], g->I[b], Rp, C);
			Rn->set(a, b, val);
			//cerr<<"[calcRnext]"<<a<<"-"<<b<<"->"<<val<<endl;
		}
	}
}

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

void simrankParallel(const Graph* g, RFactory* rFactory, double C, int numIter, int numThreads=1) {
	if (numThreads == 1) {
		simrank(g, rFactory, C, numIter);
		return;
	}
	cerr<<"[simrank] running parallel version"<<endl;
	RNext* R0 = rFactory->getInitial(g);
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

