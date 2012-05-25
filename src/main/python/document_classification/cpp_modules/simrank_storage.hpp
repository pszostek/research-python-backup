
#ifndef SIMRANK_STORAGE
#define SIMRANK_STORAGE

#include "graph.hpp"
#include "matrix_io.hpp"
#include "strs.hpp"
#include <iostream>
#include <ctime>
#include <stdio.h>

using namespace std;

struct RPrev {
	virtual double get(int row, int col) const = 0;
};

struct RNext {
	virtual void set(int row, int col, double val) = 0;
};

struct RFactory {
	RFactory(){}

	virtual RNext* getInitial(const Graph* g) = 0;
	virtual RNext* getNext() = 0;
	virtual RPrev* getPrev() = 0;
	virtual void printData(ostream& o) = 0;
	virtual ~RFactory() {};
	virtual void saveTmpResults() {};
};

struct ParallelRFactory: public RFactory {
	virtual RNext* getInitial(const Graph* g, int numThreads) = 0;
};

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

struct MemoryRFactory: public ParallelRFactory {
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

	RNext* getInitial(const Graph* g)  {
		freeMemory();
		size = g->getNumNodes();
		rp->storage = allocMatrix<double>(size);
		rn->storage = allocMatrix<double>(size);
		return rn;
	}

	RNext* getInitial(const Graph* g, int numThreads) {
		return getInitial(g);
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

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////

struct LineMemoryRPrev: public RPrev {
	double **storage;
	double get(int row, int col) const {
		return storage[row][col];
	}
};

struct LineMemoryRNext: public RNext {
	double **storage;
	int startingrow;
	int numrows;
	void set(int row, int col, double val) {
		storage[row][col] = val;
	}
};

struct LineMemoryRFactory: public ParallelRFactory {
	MemoryRNext* rn;
	MemoryRPrev* rp;
	int size;
	int numlines;
	int itercounter;
	FILE* fout;

	LineMemoryRFactory() {
		this->itercounter = 0;
		this->size = 0;
		this->numlines = 0;

		rp = new MemoryRPrev();
		rp->storage = NULL;
		rn = new MemoryRNext();
		rn->storage = NULL;
		fout = NULL;
	}

	virtual ~LineMemoryRFactory() {
		freeMemory();
	}

	void freeMemory() {
		freeMatrix(rp->storage, size);
		freeMatrix(rn->storage, size);
		rp->storage = NULL;
		rn->storage = NULL;
	}

	void reloadOutputFile() {
		if (fout != NULL) {
			fclose(f);
		}
		fout = fopen((string("LineMemoryRFactory_")+intToStr(itercounter)).c_str(), "w");
	}


	RNext* getInitial(const Graph* g, int numThreads)  {
		freeMemory();
		numlines = numThreads;
		itercounter = 0;
		size = g->getNumNodes();
		rp->storage = allocMatrix<double>(size);
		rn->storage = allocMatrix<double>(this->numlines);
		return rn;
	}

	RNext* getNext() {
		//rn->storage = rp->storage;
		//rp->storage = tmp_storage;
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

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////



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

	RNext* getInitial(const Graph* g)  {
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
