
#ifndef SIMRANK_STORAGE
#define SIMRANK_STORAGE

#include "graph.hpp"
#include <iostream>
#include <ctime>

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

template <class T>
T **allocMatrix(int rows, int cols) {
	double** storage = new double*[rows];
	for (int i=0; i<rows; ++i) {
		storage[i] = new double[cols];
	}
	float totalmem = (rows/1024.0)*(cols/1024.0)*sizeof(double);
	cerr<<"[allocMatrix] rows="<<rows<<" cols="<<cols<<" ds="<<sizeof(double)<<" mem="<<round(totalmem)<<" MB"<<endl;
	return storage;
}

template <class T>
T **allocMatrix(int size) {
	return allocMatrix<T>(size, size);
}

template <class T>
void freeMatrix(T** matrix, int size) {
	if (matrix==NULL) return;
	for (int i=0; i<size; ++i) {
		delete[] matrix[i];
	}
	delete[] matrix;
}



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

	RNext* getInitial(const Graph* g)  {
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
