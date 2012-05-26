
#ifndef SIMRANK_MEMDISK_STORAGE
#define SIMRANK_MEMDISK_STORAGE

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

struct MemDiskRPrev: public RPrev {
	double **storage;
	double get(int row, int col) const {
		return storage[row][col];
	}

	void load(const char* path) {
		cerr<<"[MemDiskRPrev::load] Loading previous matrix from file "<<path<<endl;
		FILE* fin = fopen(path, "r");
		vector<string> rows = loadHeaderLine(fin);
		readLine(fin); //skip cols header
		int size = rows.size();
		loadMatrixData(fin, storage, size, size);
		fclose(fin);
	}
};

struct MemDiskRNext: public RNext {
	const Graph* g;
	FILE* fout;
	int prevrow, prevcol, itercounter;

	MemDiskRNext() {
		itercounter = 0;
		fout = NULL;
		reset();
	}

	void reset() {
		prevrow = prevcol = 0;
	}

	void set(int row, int col, double val) {
		if (prevrow!=row) {
			fprintf(fout, "\n");
		}
		if (col!=0) {
			fprintf(fout, "\t");
		}
		fprintf(fout, "%.12f", val);
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
		return (string("DiskMemoryRFactory_")+char('a'+itercounter));
		//return string("/tmp/tmp.txt");
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
};

struct MemDiskRFactory: public RFactory {
	MemDiskRNext* rn;
	MemDiskRPrev* rp;
	int size;

	MemDiskRFactory() {
		rp = new MemDiskRPrev();
		rp->storage = NULL;
		rn = new MemDiskRNext();
		size = 0;
	}

	virtual ~MemDiskRFactory() {
		freeMemDisk();
		delete rp;
		delete rn;
	}

	void freeMemDisk() {
		if (rp->storage!=NULL) {
			freeMatrix(rp->storage, size);
			rp->storage = NULL;
		}
	}


	RNext* getInitial(const Graph* g, int numThreads) {
		freeMemDisk();
		size = g->getNumNodes();
		rp->storage = allocMatrix<double>(size);
		rn->g = g;
		rn->openNextTmpFile();
		rn->reset();
		return rn;
	}

	RNext* getNext() {
		rn->closeFile();
		rp->load(rn->getCurrentFileName().c_str());
		rn->openNextTmpFile();
		rn->reset();
		return rn;
	}

	RPrev* getPrev() {
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


#endif
