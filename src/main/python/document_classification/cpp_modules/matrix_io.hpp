
#ifndef MATRIX_IO
#define MATRIX_IO

#include <stdlib.h>
#include <stdio.h>
#include "simrank_storage.hpp"

struct Matrix {
	vector<string> rows;
	vector<string> cols;
	double** data;
};

const int MAX_LINE_SIZE = 30*1024*1024;
static char buffer[MAX_LINE_SIZE];

void loadMatrix(FILE* f, Matrix& m) {
	char* line;
	cerr<<"[loadMatrix] loading headers..."<<endl;
	line = fgets(buffer, MAX_LINE_SIZE, f);
	m.rows = split(line, '\t');
	cerr<<"[loadMatrix]"<<m.rows.size()<<" rows to be loaded"<<endl;

	line = fgets(buffer, MAX_LINE_SIZE, f);
	m.cols = split(line, '\t');
	cerr<<"[loadMatrix]"<<m.cols.size()<<" cols to be loaded"<<endl;

	m.data = allocMatrix<double>(m.rows.size(), m.cols.size());
	for (int r=0; r<m.rows.size(); ++r) {
		for (int c=0; c<m.cols.size(); ++c) {
			fscanf(f, "%lf", &m.data[r][c]);
		}
		if (r%1000==0) cerr<<"[loadMatrix] row="<<r<<" out of="<<m.rows.size()<<endl;
	}

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
