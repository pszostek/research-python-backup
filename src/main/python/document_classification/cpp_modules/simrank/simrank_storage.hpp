
#ifndef SIMRANK_STORAGE
#define SIMRANK_STORAGE

#include "../graph.hpp"
#include "../matrix_io.hpp"
#include "../strs.hpp"
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
	int numcols;
	FILE* tmpFile;

	void set(int row, int col, double val) {
		//cerr<<"[LineMemoryRNext] row="<<row<<" col="<<col<<" numrows="<<numrows<<" startingrow="<<startingrow<<endl;
		storage[row-startingrow][col] = val;
	}

	void print(FILE* fout) {
		printMatrix(storage, fout, numrows, numcols);
	}

	void saveTmpResults() {
		print(tmpFile);
	}
};

struct LineMemoryRFactory {
	const Graph* g;
	int size;
	int itercounter;
	LineMemoryRNext* rn;
	LineMemoryRPrev* rp;
	FILE* fout;

	LineMemoryRFactory() {
		this->itercounter = 0;
		this->size = 0;

		rp = new LineMemoryRPrev();
		rp->storage = NULL;
		rn = new LineMemoryRNext();
		rn->storage = NULL;
		fout = NULL;
		g = NULL;
	}

	virtual ~LineMemoryRFactory() {
		freeMemory();
		if (fout) {
			fclose(fout);
		}
	}

	void freeMemory() {
		freeMatrix(rp->storage, size);
		freeMatrix(rn->storage, rn->numrows);
		rp->storage = NULL;
		rn->storage = NULL;
	}

	string getCurrentFileName() {
		return (string("LineMemoryRFactory_")+char('a'+itercounter));
		//return string("/tmp/tmp.txt");
	}

	FILE* moveToNextTmpFile() {
		if (fout != NULL) {
			cerr<<"[LineMemoryRFactory::moveToNextTmpFile] Closing previous file "<<fout<<endl;
			fclose(fout);
			fout = NULL;
		}
		++itercounter;
		string nextFileName = getCurrentFileName();
		cerr<<"[LineMemoryRFactory::moveToNextTmpFile] Opening "<<nextFileName<<" for writing"<<endl;
		fout = fopen(nextFileName.c_str(), "w");
		g->printLabels(fout); //print rows headers
		g->printLabels(fout); //print cols headers
		return fout;
	}

	LineMemoryRNext* getInitial(const Graph* g, int numThreads)  {
		freeMemory();

		itercounter = 0;
		this->g = g;
		this->size = g->getNumNodes();

		rp->storage 	= allocMatrix<double>(size);
		rn->storage 	= allocMatrix<double>(numThreads);
		rn->numrows 	= numThreads;
		rn->numcols 	= size;
		rn->startingrow	= 0;
		rn->tmpFile 	= moveToNextTmpFile();

		return rn;
	}

	LineMemoryRNext* getNext() {
		string prevFileName = getCurrentFileName();
		rn->tmpFile 	= moveToNextTmpFile();

		cerr<<"[LineMemoryRFactory::getNext] Loading previous (size="<<size<<") matrix from file "<<prevFileName.c_str()<<endl;
		FILE* fin = fopen(prevFileName.c_str(), "r");
		cerr<<readLine(fin); //skip rows header
		cerr<<readLine(fin); //skip cols header
		loadMatrixData(fin, rp->storage, size, size);
		fclose(fin);

		//for (int r=0; r<size; r++) {
		//	for (int c=0; c<size; ++c) {
		//		cerr<<rp->storage[r][c]<<"\t";
		//	}
		//	cerr<<endl;
		//}

		return rn;
	}

	LineMemoryRPrev* getPrev() {
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

struct DummyRFactory: public ParallelRFactory {
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
