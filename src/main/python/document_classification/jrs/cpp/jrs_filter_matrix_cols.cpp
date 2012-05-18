
#include "jrs_alglib_data.hpp"
#include <vector>
#include <set>

using namespace std;


int main(int argc, char* argv[]) {
	cout<<"The program detects and removes bad features from JRS-2012-Contest data..."<<endl;
    if (argc < 4) {
    	cout<<"Data file expected as a first parameter!"<<endl;
    	cout<<"Output data file expected as a next parameter!"<<endl;
     	cout<<"Output log file expected as a next parameter!"<<endl;
    	exit(-1);
    }

	char* fpath = argv[1];
	char* outpath = argv[2];
	char* outpath2 = argv[3];

	real_2d_array data;

	cout<<"Loading from "<<fpath<<" ..."<<endl;
	load_data(fpath, data);
    cout<<"\t"<<data.rows()<<" rows loaded...\n";
    cout<<"\t"<<data.cols()<<" cols loaded...\n";
    //cout<<"Data range = "<<datam.minval()<<" - "<<datam.maxval()<<"...\n";
    cout<<"Data preview:"<<endl;
    preview(data, 10, 10);

    ////////////////////////////////////////////////

    set<int> bad_cols;
    vector<float> col_sum;
    cout<<"Opening log file = "<<outpath2<<endl;
    FILE* flog = fopen(outpath2, "w");

    cout<<"Searching for empty (=0) features..."<<endl;
    fprintf(flog, "Empty columns:\n");
    //cout<<"Empty cols: ";
    for (int c=0; c<data.cols(); ++c) {
    	float sum = 0.0;
    	for (int r=0; r<data.rows(); ++r) {
    		sum += data[r][c];
    	}
    	if (sum == 0.0) {
    		//cout<<c<<"->"<<sum<<" ";
    		fprintf(flog,"%i ",c);
    		bad_cols.insert(c);
    	}
    	col_sum.push_back(sum);
    }
    fprintf(flog, "\n");
    //cout<<endl;
    cout<<"\t"<<bad_cols.size()<<" bad columns out of "<<data.cols()<<endl;

    cout<<"Searching for duplicated features..."<<endl;
    //cout<<"Duplicated cols: ";
    fprintf(flog, "Duplicated columns:\n");
    for (int c1=0; c1<data.cols(); ++c1) {
    	if (bad_cols.count(c1)>0) continue;
    	for (int c2=c1+1; c2<data.cols(); ++c2) {
    		if (bad_cols.count(c2)>0) continue;
    		if (col_sum[c1] != col_sum[c2]) continue;

    		bool cols_equal = true;
        	for (int r=0; r<data.rows() && cols_equal; ++r) {
        		cols_equal = data[r][c1]==data[r][c2];
        	}
        	if (cols_equal) {
        		//cout<<"("<<c1<<","<<c2<<") ";
        		fprintf(flog,"%i,%i ",c1,c2);
        		bad_cols.insert(c2);
        	}
    	}
    }
    fprintf(flog, "\n");
    //cout<<endl;
    cout<<"\t"<<bad_cols.size()<<" bad columns out of "<<data.cols()<<endl;

    cout<<"Building new filtered data..."<<endl;
	real_2d_array fdata;
	int numcols = data.cols() - bad_cols.size();
	cout<<"\t"<<numcols<<" will be left..."<<endl;
	fdata.setlength(data.rows(), numcols);
    for (int c=0, fc=0; c<data.cols(); ++c) {
    	if (bad_cols.count(c) > 0) continue;
    	//cout<<"Copying col="<<c<<" to fcol="<<fc<<endl;
    	for (int r=0; r<data.rows(); ++r) {
    		fdata[r][fc] = data[r][c];
    	}
    	//cout<<"Column copied..."<<endl;
    	fc++;
    }

    cout<<"Storing results into file = "<<outpath<<endl;
    store_idata(outpath, fdata);

    fclose(flog);
	cout<<"Done."<<endl;
	return 0;
}

