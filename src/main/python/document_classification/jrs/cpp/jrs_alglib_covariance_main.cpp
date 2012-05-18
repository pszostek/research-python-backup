
#include "jrs_alglib_data.hpp"

using namespace std;


int main(int argc, char* argv[]) {
	cout<<"The program builds covariance and inverted-covariance matrix for JRS-2012-Contest data..."<<endl;
    if (argc < 4) {
    	cout<<"Data file expected as a first parameter!"<<endl;
    	cout<<"Cov-matrix output file expected as a next parameter!"<<endl;
     	cout<<"Inv-Cov-matrix output file expected as a next parameter!"<<endl;
    	exit(-1);
    }

	char* fpath = argv[1];
	char* outpath = argv[2];
	char* outpath2 = argv[3];

	real_2d_array data, cov;

	cout<<"Loading from "<<fpath<<" ..."<<endl;
	load_data(fpath, data);
    cout<<data.rows()<<" rows loaded...\n";
    cout<<data.cols()<<" cols loaded...\n";
    //cout<<"Data range = "<<datam.minval()<<" - "<<datam.maxval()<<"...\n";
    cout<<"Data preview:"<<endl;
    preview(data, 10, 10);

	cout<<"Building covariance matrix out of "<<fpath<<" ..."<<endl;
	covm(data, cov);
	cout<<"Covariance matrix preview:"<<endl;
	preview(cov, 10, 10);
	cout<<"Writing covariance matrix to "<<outpath<<endl;
	store_squared_rmatrix(outpath, cov, cov.rows());

	cout<<"Inverting matrix..."<<endl;
	time_t starttime = time(0);
	alglib::matinvreport  rep;
	alglib::ae_int_t      info;
	alglib::rmatrixinverse(cov, info, rep);
	cout<<"Inverted in "<<(time(0)-starttime)<<"s"<<". result code = "<<info<<endl;
	cout<<"Inverted matrix preview:"<<endl;
	preview(cov, 10, 10);
	cout<<"Writing inverted covariance matrix to "<<outpath2<<endl;
	store_squared_rmatrix(outpath2, cov, cov.rows());

	cout<<"Done."<<endl;
	return 0;
}

