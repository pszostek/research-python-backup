
#ifndef SIMRANK_LINE_STORAGE
#define SIMRANK_LINE_STORAGE


//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////

#include "simrank_storage.hpp"
#include "../graph.hpp"
#include "../matrix_io.hpp"
#include "../strs.hpp"
#include <iostream>
#include <ctime>
#include <stdio.h>

using namespace std;

struct LineMemoryRPrev: public RPrev {
	double **storage;
	double get(int row, int col) const {
		return storage[row][col];
	}

	void load(const char* path) {
		cerr<<"[LineMemoryRPrev::load] Loading previous matrix from file "<<path<<endl;
		FILE* fin = fopen(path, "r");
		vector<string> rows = loadHeaderLine(fin);
		readLine(fin); //skip cols header
		int size = rows.size();
		loadMatrixData(fin, storage, size, size);
		fclose(fin);
	}
};

struct LineMemoryRNext: public RNext {
	const Graph* g;
	FILE* fout;
	int prevrow, prevcol, itercounter;
	int startingRow, numRows;
	double** storage;

	LineMemoryRNext() {
		itercounter = 0;
		fout = NULL;
		reset();
	}

	void reset() {
		prevrow = prevcol = 0;
	}

	void set(int row, int col, double val) {
		storage[row-startingRow][col] = val;
		prevrow = row;
		prevcol = col;
	}

	void closeFile() {
		if (fout != NULL) {
			cerr<<"[closePrevFile] Closing previous file "<<fout<<endl;
			fclose(fout);
			fout = NULL;
		}
	}

	string getCurrentFileName() {
		return (string("LineMemoryRFactory_")+char('a'+itercounter));
	}

	void openNextTmpFile() {
		closeFile();
		++itercounter;
		string nextFileName = getCurrentFileName();
		cerr<<"[moveToNextTmpFile] Opening "<<nextFileName<<" for writing"<<endl;
		fout = fopen(nextFileName.c_str(), "w");
		g->printLabels(fout); //print rows headers
		g->printLabels(fout); //print cols headers
	}

	void saveTmpResults() {
		int size = g->getNumNodes();
		int rows = min(numRows,size-startingRow);
		printMatrix(storage, fout, rows, size);
	}
};

struct LineMemoryRFactory: public RFactory {
	LineMemoryRNext* rn;
	LineMemoryRPrev* rp;
	int size;

	LineMemoryRFactory() {
		rp = new LineMemoryRPrev();
		rp->storage = NULL;
		rn = new LineMemoryRNext();
		rn->storage = NULL;
		size = 0;
	}

	virtual ~LineMemoryRFactory() {
	}

	LineMemoryRNext* getInitial(const Graph* g, int numThreads)  {
		size = g->getNumNodes();
		rp->storage = allocMatrix<double>(size);
		rn->storage = allocMatrix<double>(numThreads, size);
		rn->g = g;
		rn->openNextTmpFile();
		rn->reset();
		rn->numRows = numThreads;
		return rn;
	}

	LineMemoryRNext* getNext() {
		rn->closeFile();
		rp->load(rn->getCurrentFileName().c_str());
		rn->openNextTmpFile();
		rn->reset();
		return rn;
	}

	LineMemoryRPrev* getPrev() {
		return rp;
	}

	void printCerr() {
		printData(cerr);
	}

	void printData(ostream& o) {
		rn->closeFile();
		rp->load(rn->getCurrentFileName().c_str());

		double** s = rp->storage;
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




#endif
