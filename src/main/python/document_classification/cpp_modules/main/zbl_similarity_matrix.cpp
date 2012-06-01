
#include <ctime>
#include <iostream>
#include <iomanip>
#include "../zbl_io.hpp"
#include "../sparse_vec_metrics.hpp"
#include "../strs.hpp"

using namespace std;

//////////////////////////////////////////////////////////////////////////////

string sparse_vector_field = "g2"; //can be set by parameter
int endIx = MAXINT; //only values with ix<endIx will be considered; can be set by parameter

//function used to calculate distance between two vectors
double (*metric_calc)(const IntDoubleListPairs&,const IntDoubleListPairs&, int endIx) = cosine;

const int DOUBLE_FILE_PRECISION = 20;

//////////////////////////////////////////////////////////////////////////////

vector< pair<ZblKey, IntDoubleListPairs> > zbl2vector;
int records_counter = 0;
int processed_counter = 0;

void zblRecordProcessor(const ZblRecord& record) {
	records_counter++;
	string id = record.find(ZBL_ID_FIELD)->second;
	ZblRecord::const_iterator f_it = record.find(sparse_vector_field);
	if (f_it == record.end()) return;
	string fieldValue = f_it->second;

	//cout<<"[zblRecordProcessor] -----"<<endl;
	zbl2vector.push_back( make_pair(id, IntDoubleListPairs()) );
	extractIntDoubleListPairs(fieldValue, zbl2vector.back().second);
	//cout<<"[zblRecordProcessor] id="<<id<<"->"<<zbl2vector.back().second.size()<<"elements"<<endl;
	processed_counter++;
}



int main(int argc, char *argv[]) {
	cerr<<"The program calculates distances between ZBL-records using sparse (sorted!) features vectors..."<<endl;
	cerr<<"Input records are read from stdin and output matrix is printed out to stdout."<<endl;
	cerr<<"First argument is optional = name of field [+ end index] (e.g. g2, g2-150) that contains sparse vector."<<endl;
	cerr<<"Sparse vector should be ','-separated-list [feature-index: value]. Only values with ix<end index will be considered."<<endl;
	cerr<<"Second argument is optional = distance metric (cos=cosine/tv=tversky/angular=pos-neg-angular)."<<endl;
	if (argc > 1) {
		if (contains(argv[1],'-')) {
			vector<string> parts = split(argv[1], '-');
			sparse_vector_field = parts[0];
			endIx = strToInt(parts[1]);
		} else {
			sparse_vector_field = argv[1];
		}
	}
	char* metric = (char*)"cos";
	if (argc > 2) {
		metric = argv[2];
	}
	cerr<<" sparse_vector_field(sorted by indexes!)="<<sparse_vector_field<<endl;
	cerr<<" end index="<<endIx<<endl;
	cerr<<" metric="<<metric<<endl;
	try {
		if (strcmp(metric,"cos") == 0) {
			cerr<<"Using cosine distance..."<<endl;
			metric_calc = cosine;
		} else
		if (strcmp(metric,"tv") == 0) {
			cerr<<"Using tversky metric..."<<endl;
			metric_calc = tversky;
		} else
		if (strcmp(metric,"angular") == 0){
			cerr<<"Using angular (positive and negative elements of vectors) metric..."<<endl;
			metric_calc = angular_posneg;
		} else {
			cerr<<"Unknown metric name (cos=cosine/tv=tversky/angular=pos-neg-angular  supported)!"<<endl;
			exit(-2);
		}

		cerr<<"loading input records..."<<endl;
		readZblStream(cin, zblRecordProcessor);
		cerr<<processed_counter<<" records extracted out of "<<records_counter<<" read"<<endl;


		cerr<<"printing rows' labels..."<<endl;
		for (int i=0; i<zbl2vector.size()-1; ++i) {
			cout<<zbl2vector[i].first<<"\t";
		}
		cout<<zbl2vector[zbl2vector.size()-1].first<<endl;

		cerr<<"printing cols' labels..."<<endl;
		for (int i=0; i<zbl2vector.size()-1; ++i) {
			cout<<zbl2vector[i].first<<"\t";
		}
		cout<<zbl2vector[zbl2vector.size()-1].first<<endl;

		cerr<<"calculating and printing data..."<<endl;
		cout<<setprecision(DOUBLE_FILE_PRECISION);
		cout.setf(ios::fixed, ios::floatfield);
		cout.setf(ios::showpoint);
		long starttime = time(0);
		for (int i=0; i<zbl2vector.size(); ++i) {
			if (i%1000==0) cerr<<"["<<(time(0)-starttime)<<"s] "<<i<<" rows processed..."<<endl;
			IntDoubleListPairs& v1 = zbl2vector[i].second;
			//printPairVector("v1=",v1);

			for (int j=0; j<zbl2vector.size()-1; ++j) {
				IntDoubleListPairs& v2 = zbl2vector[j].second;
				cout<<((i==j)?1.0:metric_calc(v1,v2,endIx))<<"\t";
			}
			IntDoubleListPairs& v2 = zbl2vector[zbl2vector.size()-1].second;
			cout<<metric_calc(v1,v2,endIx)<<endl;
		}
		cerr<<"["<<(time(0)-starttime)<<"s] "<<zbl2vector.size()<<" rows processed..."<<endl;

	} catch (const char *exception) {
		cerr<<"Error:"<<exception<<endl;
		return -1;
	}
	return 0;
}
