
#include "../matrix_io.hpp"

int main(int argc, char* argv[]) {
	char *matrix1_path, *matrix2_path;
	if (argc>2) {
		matrix1_path = argv[1];
		matrix2_path = argv[2];
	} else {
		cerr<<"Two paths expected: pattern-similarity-matrix to-be-compared-similarity-matrix"<<endl;
		exit(-1);
	}

	cout<<"Loading first matrix from "<<matrix1_path<<endl;
	Matrix m1;
	FILE* f1 = fopen(matrix1_path, "r");
	loadMatrix(f1, m1);
	fclose(f1);

	cout<<"Loading first matrix from "<<matrix2_path<<endl;
	Matrix m2;
	FILE* f2 = fopen(matrix2_path, "r");
	loadMatrix(f2, m2);
	fclose(f2);

	if (m1.rows.size()!=m1.cols.size() ||
		m1.rows.size()!=m2.rows.size() ||
		m1.cols.size()!=m2.cols.size()) {
		cerr<<"Matrices' dimensions must agree!"<<endl;
		exit(-2);
	}
	int N = m1.rows.size();
	for (int i=0; i<N; ++i) {
		if (m1.rows[i] != m1.cols[i] ||
		    m2.rows[i] != m2.cols[i] ||
		    m1.rows[i] != m2.rows[i] ) {
			cerr<<"Matrices' labels must agree!"<<endl;
			exit(-3);
		}
	}


	cout<<"Comparing matrices..."<<endl;
	double** d1 = m1.data;
	double** d2 = m2.data;
	int skipped=0, compared=0, correct=0;
	for (int i=0; i<N; ++i) {
		for (int j=i+1; j<N; ++j) {
			for (int k=j+1; k<N; ++k) {
				//cerr<<" i="<<i<<" j="<<j<<" k="<<k;
				//cerr<<" d1ij="<<d1[i][j]<<" d1ik="<<d1[i][k]<<" d2ij="<<d2[i][j]<<" d2ik="<<d2[i][k]<<endl;
				if (d1[i][j] == d1[i][k]) {
					++skipped;
					continue;
				}
				correct += (d1[i][j] > d1[i][k])? (d2[i][j] > d2[i][k]): (d2[i][j] < d2[i][k]);
				++compared;
			}
		}
	}

	cout<<"skipped="<<skipped<<endl;
	cout<<"compared="<<compared<<endl;
	cout<<"correct="<<correct<<endl;
	cout<<"correct/compared="<<(correct*100.0)/compared<<"%"<<endl;
}
