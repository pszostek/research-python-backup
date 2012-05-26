
#ifndef MATRIX_IO
#define MATRIX_IO

#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <map>
#include "strs.hpp"

using namespace std;

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

template <class T>
void printMatrix(T** simmatrix, ostream& o, int numrows, int numcols) {
	for (int r=0; r<numrows; ++r) {
		for (int c=0; c<numcols-1; ++c) {
			o<<simmatrix[r][c]<<"\t";
		}
		o<<simmatrix[r][numcols-1]<<endl;
	}
}


void printMatrix(double** simmatrix, FILE* f, int numrows, int numcols) {
	for (int r=0; r<numrows; ++r) {
		for (int c=0; c<numcols-1; ++c) {
			fprintf(f, "%.12f\t", simmatrix[r][c]);
		}
		fprintf(f, "%.12f\n", simmatrix[r][numcols-1]);
	}
}



struct Matrix {
	vector<string> rows;
	vector<string> cols;
	double** data;
};

const int MAX_LINE_SIZE = 30*1024*1024;
static char buffer[MAX_LINE_SIZE];

double** loadMatrixData(FILE* f, double** dst, int numrows, int numcols) {
	for (int r=0; r<numrows; ++r) {
		for (int c=0; c<numcols; ++c) {
			int numscanned = fscanf(f, "%lf", &dst[r][c]);
		}
		if (r%1000==0 && r>0) cerr<<"[loadMatrix] row="<<r<<" out of="<<numrows<<endl;
	}
	return dst;
}

char* readLine(FILE* f) {
	return fgets(buffer, MAX_LINE_SIZE, f);
}

vector<string> loadHeaderLine(FILE* f) {
	char* line;
	line = fgets(buffer, MAX_LINE_SIZE, f);
	return split(line, '\t');
}

void loadMatrix(FILE* f, Matrix& m) {
	cerr<<"[loadMatrix] loading headers..."<<endl;

	m.rows = loadHeaderLine(f);
	cerr<<"[loadMatrix]"<<m.rows.size()<<" rows to be loaded..."<<endl;
	m.cols = loadHeaderLine(f);
	cerr<<"[loadMatrix]"<<m.cols.size()<<" cols to be loaded..."<<endl;

	m.data = allocMatrix<double>(m.rows.size(), m.cols.size());
	loadMatrixData(f, m.data, m.rows.size(), m.cols.size());
}

struct Group {
	Group() {
	}
	Group(const string& n): name(n) {
	}
	string name;
	vector<int> ixs;
	vector<float> weights;
};

void loadGroups(FILE* f, map<string, int>& id2ix, vector<Group>& groups) {
	char* line;
	while (!feof(f)) {
		line = fgets(buffer, MAX_LINE_SIZE, f);
		if (line==NULL || strlen(line)<2) continue;
		for (char* p=line; p && *p!='\n'; ++p) if (*p==':' || *p==';' || *p=='-') *p=','; //ujednolicenie separatorow
		vector<string> parts = split(line, ',');
		groups.push_back(Group(parts[0]));
		Group& g = groups.back();
		for (int i=1; i<parts.size(); i+=2) {
			g.ixs.push_back( id2ix[ parts[i] ] );
			g.weights.push_back( atof(parts[i+1].c_str()) );
		}
		//cerr<<"[loadGroups] next group: name="<<g.name<<" num elems"<<g.weights.size()<<endl;
	}
}

#endif
