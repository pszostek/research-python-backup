#include <stdio.h>
#include <cstring>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <cmath>
#include <ctime>
#include "alglib/alglib_headers.h"
#include "jrs_data.hpp"

using namespace std;

void store_idata(const char* fpath, const real_2d_array& data) {
	FILE* f = fopen(fpath, "w");
	if (!f) throw "[store_data] Failed opening file!";
	for (int row=0; row<data.rows(); ++row) {
        for (int col=0; col<data.cols()-1; ++col) {
        	fprintf(f, "%i\t",(int)data[row][col]);
        }
        fprintf(f, "%i", (int)data[row][data.cols()-1]);
        //if (row != data.rows()-1)
		fprintf(f, "\n");
	}
	fclose(f);
}

void load_data(const char* fpath, real_2d_array& data, int readrows=-1) {
    int numrows = (readrows < 0)? get_file_numlines(fpath): readrows;
    int numcols = get_file_numcols(fpath);
    if (numrows <= 0 || numcols <= 0) {
    	throw "Failed to read data!";
    }
    data.setlength(numrows, numcols);

    char line[1000000];
    double rowvals[100000];
    FILE* f = fopen(fpath, "r");
    if (!f) throw "[load_data] Failed opening file!";
    for (int row=0; row<numrows; ++row) {
    	fgets (line, 1000000, f);

        int numvals = parse_row(line, rowvals);
        if (numcols != numvals) {
        	cerr<<"[load_data] numcols != numvals in row="<<row<<endl;
        	cerr<<"[load_data] numcols = "<<numcols<<endl;
        	cerr<<"[load_data] numvals = "<<numvals<<endl;
        	cerr<<"[load_data] line =["<<line<<"]"<<endl;
        	throw "Inconsistent data in input file!";
        }
        for (int col=0; col<numcols; ++col) {
        	data[row][col] = rowvals[col];
        }
    }
    fclose(f);
}

int min(int a, alglib::ae_int_t b) {
	return (a<b)? a: b;
}

void print_matrix(const real_2d_array& m, int row1, int row2, int col1, int col2) {
	row1 = min(row1, m.rows());
	row2 = min(row2, m.rows());
	col1 = min(col1, m.cols());
	col2 = min(col2, m.cols());
	for (int r=row1; r<row2; ++r) {
		for (int c=col1; c<col2; ++c) {
			cout<<m[r][c]<<"\t";
		}
		cout<<endl;
	}
}

void preview(const real_2d_array& data, int rows, int cols) {
	print_matrix(data, 0, rows, 0, cols);
}

void fill_matrix(real_2d_array& dstm, int size) {
	dstm.setlength(size,size);
	for (int i=0; i<size; ++i) {
		//cout<<"[fill_matrix] row = "<<i<<endl;
		for (int j=i; j<size; ++j) {
			//cout<<"[fill_matrix] col = "<<j<<endl;
			dstm[i][j] = i*j+j;
			dstm[j][i] = dstm[i][j];
		}
	}
}

void test_matrix_inv(int size) {
	real_2d_array dstm("[[3,1,4,5,6], [1,7,2,1,7], [4,2,5,3,9], [5,1,3,8,7], [6,7,9,7,1]]");
	//real_2d_array dstm("[[0,1,4,5,6], [1,0,2,1,7], [4,2,0,3,9], [5,1,3,0,7], [6,7,9,7,0]]");

	cout<<"Allocating memory:"<<size<<"x"<<size<<endl;
	cout<<"Filling-in matrix..."<<endl;
	fill_matrix(dstm, size);
	print_matrix(dstm, 0, 10, 0, 10);

	cout<<"Inverting matrix..."<<endl;
	time_t starttime = time(0);
	alglib::matinvreport  rep;
	alglib::ae_int_t      info;
	alglib::rmatrixinverse(dstm, info, rep);
	//alglib::spdmatrixinverse(dstm, info, rep); //macierze symetryczne z zerami na przekątnej
	cout<<"Inverted in "<<(time(0)-starttime)<<"s"<<endl;
	print_matrix(dstm, 0, 10, 0, 10);
	cout<<" Result code = "<<info<<endl;
}
