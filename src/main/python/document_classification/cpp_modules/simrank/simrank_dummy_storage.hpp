
#ifndef SIMRANK_DUMMY_STORAGE
#define SIMRANK_DUMMY_STORAGE

#include "simrank_storage.hpp"

struct DummyRPrev: public RPrev {
	double get(int row, int col) const {
		return row==col;
	}
};

struct DummyRNext: public RNext {
	long starttime;

	void set(int row, int col, double val) {
		if (row%1==0 && col==0) {
			if (row==0) starttime = time(0);
			cerr<<"[DummyRNext]["<<(time(0)-starttime)<<"s]"<<row<<" rows processed"<<endl;
		}
	}
};

struct DummyRFactory: public RFactory {
	DummyRNext rn;
	DummyRPrev rp;
	int size;

	DummyRFactory() {
		size = 0;
	}

	virtual ~DummyRFactory() {
	}

	RNext* getInitial(const Graph* g, int numThreads)  {
		return &rn;
	}


	RNext* getNext() {
		return &rn;
	}

	RPrev* getPrev() {
		return &rp;
	}

	void printCerr() {
		printData(cerr);
	}

	void printData(ostream& o) {
		o<<"[DummyRStorage] There is no real data in dummy storage"<<endl;
	}
};


#endif

