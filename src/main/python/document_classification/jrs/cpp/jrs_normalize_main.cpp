#include <stdio.h>
#include <cstring>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <cmath>
#include "vector_metrics.hpp"
#include "jrs_data.hpp"


using namespace std;


int store_distm(const char* fpath, double** distm, int size) {
	return store_squared_rmatrix(fpath, distm, size);
}



int main(int argc, char *argv[]) {
	cout<<"The program normalizes features' matrix for JRS-2012-Contest data..."<<endl;
    if (argc < 3) {
    	cout<<"Data file expected as a first parameter!"<<endl;
    	cout<<"Output file expected as second parameter!"<<endl;
    	exit(-1);
    }

	char* fpath = argv[1];
	char* outpath = argv[2];

	cout<<"Loading from "<<fpath<<" ..."<<endl;
    DataMatrix<double> datam(fpath);
    cout<<datam.numrows<<" rows loaded...\n";
    cout<<datam.numcols<<" cols loaded...\n";
    cout<<"Data range = "<<datam.minval()<<" - "<<datam.maxval()<<"...\n";
    data_preview(datam);

    cout<<"Normalizing features' matrix..."<<endl;
    datam.normalize_data();

    cout<<"Storing to "<<outpath<<" ..."<<endl;
    if (store_rect_rmatrix(outpath, datam.data, datam.numrows, datam.numcols) != 0) {
    	 cerr<<"Failed to write "<<outpath<<" ..."<<endl;
    	 exit(-1);
    }

    cout<<"Done."<<endl;
    return 0;
}
