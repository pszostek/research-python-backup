
#include "jrs_alglib_data.hpp"

using namespace std;


double** build_mahalonbis_distm(const real_2d_array& datam, const real_2d_array& icov) {
    int dim = datam.cols();
    int n = datam.rows();
    double r[dim],tmp[dim];

    double** distm = alloc_matrix_float(n);
    for (int i=0; i<n; ++i) {
        printf("calculating distance: row = %i\n", i);
        for (int j=i; j<n; ++j) {
        	//printf("calculating distance: col = %i\n", j);
        	for (int d=0; d<dim; ++d) {
        		r[d] = datam[i][d]-datam[j][d];
        		//printf("r[%i]=%f\n", d, r[d]);
        	}
        	for (int d2=0; d2<dim; ++d2) {
        		double sum = 0;
        		for (int d=0; d<dim; ++d) {
        			sum += icov[d][d2] * r[d];
        		}
        		tmp[d2] = sum;
        	}
        	double dist = 0;
        	for (int d=0; d<dim; ++d) {
        		dist += tmp[d]*r[d];
        	}

            distm[i][j] = dist;
            distm[j][i] = dist;
        }
    }

    return distm;
}

int store_distm(const char* fpath, double** distm, int size) {
	return store_squared_rmatrix(fpath, distm, size);
}

int main(int argc, char* argv[]) {
	cout<<"The program calculates distances between objects of JRS-2012-Contest data..."<<endl;
    if (argc < 4) {
    	cout<<"Data file expected as a first parameter!"<<endl;
     	cout<<"Inv-Cov-matrix input file expected as a next parameter!"<<endl;
     	cout<<"Output (distance matrix) file expected as a next parameter!"<<endl;
    	exit(-1);
    }

	char* fpath = argv[1];
	char* icovpath = argv[2];
	char* outpath = argv[3];

	real_2d_array data, icov;

	cout<<"Loading data from "<<fpath<<" ..."<<endl;
	load_data(fpath, data);
    cout<<data.rows()<<" rows loaded...\n";
    cout<<data.cols()<<" cols loaded...\n";
    //cout<<"Data range = "<<datam.minval()<<" - "<<datam.maxval()<<"...\n";
    cout<<"Data preview:"<<endl;
    preview(data, 10, 10);

	cout<<"Loading inv-covariance matrix out of "<<icovpath<<" ..."<<endl;
	load_data(icovpath, icov);
	cout<<icov.rows()<<" rows loaded...\n";
	cout<<icov.cols()<<" cols loaded...\n";
	cout<<"inv-Covariance matrix preview:"<<endl;
	preview(icov, 10, 10);

	if (data.cols() != icov.cols()) {
		cerr<<"Dimensions do not agree!"<<endl;
		exit(-1);
	}

	cout<<"Building distance matrix"<<endl;
	double** distm = build_mahalonbis_distm(data, icov);
	cout<<"Data preview:"<<endl;
	for (int r=0; r<min(10,data.rows()); ++r) {
		for (int c=0; c<min(10,data.rows()); ++c) {
			cout<<distm[r][c]<<"\t";
		}
		cout<<endl;
	}

	cout<<"Storing distance matrix to "<<outpath<<" ..."<<endl;
    if (store_distm(outpath, distm, data.rows()) != 0) {
    	 cerr<<"Failed to write "<<outpath<<" ..."<<endl;
    	 exit(-1);
    }

	cout<<"Done."<<endl;
	return 0;
}

