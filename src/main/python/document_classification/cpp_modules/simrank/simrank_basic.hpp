#ifndef SIMRANK_BASIC
#define SIMRANK_BASIC

#include "../graph.hpp"
#include "simrank_storage.hpp"
#include <ctime>
#include <cmath>
#include <stdlib.h>

//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////


void initR0(const Graph* g, RNext* R0,
			int start_a=0, int end_a=-1, int start_b=0, int end_b=-1) {
	//cerr<<"[simrank][initR0] initializing"<<endl;
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
	//int range_size = (end_a-start_a); //debug
	//int bigstep_size = range_size/20+1; //debug
	//cerr<<"[simrank] calcRnext start_a="<<start_a<<" end_a="<<end_a<<" start_b="<<start_b<<" end_b="<<end_b<<" Rprev="<<Rp<<" RNext="<<Rn<<endl;
	for (int a=start_a; a<end_a; ++a) {
		//if ( (a-start_a)%bigstep_size == 0) { //debug
		//	cerr<<"[calcRnext] progress:"<<((a-start_a)*100/range_size)<<"%"<<endl;
		//}
		for (int b=start_b; b<end_b; ++b) {
			//cerr<<"[calcRnext]"<<a<<"-"<<b<<"----------"<<endl;
			double val = (a==b)? 1.0: calcRab(g->I[a], g->I[b], Rp, C);
			Rn->set(a, b, val);
			//cerr<<"[calcRnext]"<<a<<"-"<<b<<"->"<<val<<endl;
		}
	}
}


//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////


void simrank(const Graph* g, RFactory* rFactory, double C, int numIter) {
	cerr<<"[simrank] running sequenced version"<<endl;
	RNext* R0 = rFactory->getInitial(g, 1);
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
}

#endif

