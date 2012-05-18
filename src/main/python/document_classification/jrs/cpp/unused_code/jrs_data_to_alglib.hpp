#include <stdio.h>
#include <cstring>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <cmath>
#include "vector_metrics.hpp"
#include "jrs_data.hpp"
#include "alglib/alglib_headers.h"

template <typename T>
void move_to_alglib_matrix(DataMatrix<T>& datam, real_2d_array& dstm) {
	cout<<"Setting dimensions to:"<<datam.numrows<<"x"<<datam.numcols<<endl;
	dstm.setlength(datam.numrows,datam.numcols);
	cout<<"Moving..."<<endl;
	for (int r=0; r<datam.numrows; ++r) {
		if (r%100==0) {	cout<<(r*100/datam.numrows)<<"% moved..."<<endl; }
		for (int c=0; c<datam.numcols; ++c) {
			dstm[r][c] = datam.data[r][c];
		}
		delete[] datam.data[r]; //freeing src data!
	}
	delete[] datam.data; //freeing src data!
	cout<<"Done..."<<endl;
}

void print_alglib_matrix(const real_2d_array& dstm, int size) {
	for (int r=0; r<size; ++r) {
		for (int c=0; c<size; ++c) {
			cout<<dstm[r][c]<<"\t";
		}
		cout<<endl;
	}
}
