#include <stdio.h>
#include <cstring>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <cmath>
#include "vector_metrics.hpp"
#include "jrs_data.hpp"


using namespace std;

template <typename T>
double** build_distm(const DataMatrix<T>& datam, double (*distance_calculator)(const T*,const T*,int)) {
    int dim = datam.numcols;
    int n = datam.numrows;

    double** distm = alloc_matrix_float(n);
    for (int i=0; i<n; ++i) {
        //printf("calculating distance: row = %i\n", i);
        for (int j=i; j<n; ++j) {
            double dist = distance_calculator(datam.data[i], datam.data[j], dim);
            distm[i][j] = dist;
            distm[j][i] = dist;
        }
    }

    return distm;
}

int store_distm(const char* fpath, double** distm, int size) {
	return store_squared_rmatrix(fpath, distm, size);
}



int main(int argc, char *argv[]) {
	cout<<"The program calculates distances between objects of JRS-2012-Contest data..."<<endl;
    if (argc < 4) {
    	cout<<"Data file expected as a first parameter!"<<endl;
    	cout<<"Distance method (1/2/3/4) expected as a second parameter!"<<endl;
    	cout<<"Output file expected as third parameter!"<<endl;
    	exit(-1);
    }

	char* fpath = argv[1];
	int method = atoi(argv[2]);
	char* outpath = argv[3];

	cout<<"Loading from "<<fpath<<" ..."<<endl;
    DataMatrix<double> datam(fpath);
    cout<<datam.numrows<<" rows loaded...\n";
    cout<<datam.numcols<<" cols loaded...\n";
    cout<<"Data range = "<<datam.minval()<<" - "<<datam.maxval()<<"...\n";
    if (argc>4) data_preview(datam);

    double** distm = NULL;
    switch (method) {
    	case 1:
    		printf("Calculating cosine distance matrix...\n");
    		distm = build_distm(datam, cosine_dist);
    		break;
    	case 2:
    		printf("Calculating cosine distance matrix for normalized data...\n");
    		datam.normalize_data();
    		if (argc>4) data_preview(datam);
    	    distm = build_distm(datam, cosine_dist);
    	    break;
    	case 3:
    		printf("Calculating euclid^2 distance matrix for normalized data...\n");
    		datam.normalize_data();
    		if (argc>4) data_preview(datam);
    		distm = build_distm(datam, euclid2_dist);
    		break;
    	default:
    		printf("Calculating euclid^2 distance matrix ...\n");
    	    distm = build_distm(datam, euclid2_dist);
    }

    cout<<"Storing to "<<outpath<<" ..."<<endl;
    if (store_distm(outpath, distm, datam.numrows) != 0) {
    	 cerr<<"Failed to write "<<outpath<<" ..."<<endl;
    	 exit(-1);
    }

    cout<<"Done."<<endl;
    return 0;
}
