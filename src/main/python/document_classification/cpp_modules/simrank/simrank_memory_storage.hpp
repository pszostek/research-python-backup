
#ifndef SIMRANK_MEMORY_STORAGE
#define SIMRANK_MEMORY_STORAGE

#include "simrank_storage.hpp"
#include "../graph.hpp"
#include "../matrix_io.hpp"
#include "../strs.hpp"
#include <iostream>
#include <ctime>
#include <stdio.h>

using namespace std;

//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////

struct MemoryRPrev: public RPrev {
	double **storage;
	double get(int row, int col) const {
		return storage[row][col];
	}
};

struct MemoryRNext: public RNext {
	double **storage;
	void set(int row, int col, double val) {
		storage[row][col] = val;
	}
};

struct MemoryRFactory: public RFactory {
	MemoryRNext* rn;
	MemoryRPrev* rp;
	int size;

	MemoryRFactory() {
		rp = new MemoryRPrev();
		rp->storage = NULL;
		rn = new MemoryRNext();
		rn->storage = NULL;
		size = 0;
	}

	virtual ~MemoryRFactory() {
		freeMemory();
	}

	void freeMemory() {
		freeMatrix(rp->storage, size);
		freeMatrix(rn->storage, size);
		rp->storage = NULL;
		rn->storage = NULL;
	}

	RNext* getInitial(const Graph* g, int numThreads) {
		freeMemory();
		size = g->getNumNodes();
		rp->storage = allocMatrix<double>(size);
		rn->storage = allocMatrix<double>(size);
		return rn;
	}

	RNext* getNext() {
		double** tmp_storage = rn->storage;
		rn->storage = rp->storage;
		rp->storage = tmp_storage;
		return rn;
	}

	RPrev* getPrev() {
		return rp;
	}

	void printCerr() {
		printData(cerr);
	}

	void printData(ostream& o) {
		double** s = rn->storage;
		for (int i=0; i<size; ++i) {
			for (int j=0; j<size; ++j) {
				o<<s[i][j]<<"\t";
			}
			o<<endl;
		}
	}
};

#endif
