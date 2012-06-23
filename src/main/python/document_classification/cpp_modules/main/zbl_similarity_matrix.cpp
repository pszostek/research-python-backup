
#include <ctime>
#include <iostream>
#include <fstream>
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

	//(*fout)<<"[zblRecordProcessor] -----"<<endl;
	zbl2vector.push_back( make_pair(id, IntDoubleListPairs()) );
	extractIntDoubleListPairs(fieldValue, zbl2vector.back().second);
	//(*fout)<<"[zblRecordProcessor] id="<<id<<"->"<<zbl2vector.back().second.size()<<"elements"<<endl;
	processed_counter++;
}



int main(int argc, char *argv[]) {
	cerr<<"[zbl_similarity_matrix] #########################################"<<endl;
	cerr<<"[zbl_similarity_matrix] The program calculates distances between ZBL-records using sparse (sorted!) features vectors..."<<endl;
	cerr<<"[zbl_similarity_matrix] Input records are read from stdin and output matrix is printed out to stdout."<<endl;
	cerr<<"[zbl_similarity_matrix] First argument is optional = name of field [+ end index] (e.g. g2, g2-150) that contains sparse vector."<<endl;
	cerr<<"[zbl_similarity_matrix] Sparse vector should be ','-separated-list [feature-index: value]. Only values with ix<end index will be considered."<<endl;
	cerr<<"[zbl_similarity_matrix] Second argument is optional = distance metric (cos=cosine/tv=tversky/angular=pos-neg-angular)."<<endl;

	istream* fin = &cin;
	ostream* fout = &cout;
	ifstream fileInput;
	ofstream fileOutput;
	if (argc > 4) {
		cerr<<"[zbl_similarity_matrix] Opening for reading:"<<argv[3]<<endl;
		fileInput.open(argv[3]);
		fin = &fileInput;
		cerr<<"[zbl_similarity_matrix] Opening for writing:"<<argv[4]<<endl;
		fileOutput.open(argv[4]);
		fout = &fileOutput;
	}

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
	cerr<<"[zbl_similarity_matrix]  sparse_vector_field(sorted by indexes!)="<<sparse_vector_field<<endl;
	cerr<<"[zbl_similarity_matrix]  end index="<<endIx<<endl;
	cerr<<"[zbl_similarity_matrix]  metric="<<metric<<endl;
	try {
		if (strcmp(metric,"cos") == 0) {
			cerr<<"[zbl_similarity_matrix] Using cosine distance..."<<endl;
			metric_calc = cosine;
		} else
		if (strcmp(metric,"tv") == 0 || strcmp(metric,"tversky") == 0) {
			cerr<<"[zbl_similarity_matrix] Using tversky metric..."<<endl;
			metric_calc = tversky;
		} else
		if (strcmp(metric,"angular") == 0){
			cerr<<"[zbl_similarity_matrix] Using angular (positive and negative elements of vectors) metric..."<<endl;
			metric_calc = angular_posneg;
		} else {
			cerr<<"[zbl_similarity_matrix] Unknown metric name (cos=cosine/tv=tversky/angular=pos-neg-angular  supported)!"<<endl;
			exit(-2);
		}

		cerr<<"[zbl_similarity_matrix] loading input records..."<<endl;
		readZblStream(*fin, zblRecordProcessor);
		cerr<<"[zbl_similarity_matrix] "<<processed_counter<<" records extracted out of "<<records_counter<<" read"<<endl;


		cerr<<"[zbl_similarity_matrix] printing rows' labels..."<<endl;
		for (int i=0; i<zbl2vector.size()-1; ++i) {
			(*fout)<<zbl2vector[i].first<<"\t";
		}
		(*fout)<<zbl2vector[zbl2vector.size()-1].first<<endl;

		cerr<<"[zbl_similarity_matrix] printing cols' labels..."<<endl;
		for (int i=0; i<zbl2vector.size()-1; ++i) {
			(*fout)<<zbl2vector[i].first<<"\t";
		}
		(*fout)<<zbl2vector[zbl2vector.size()-1].first<<endl;

		cerr<<"[zbl_similarity_matrix] calculating and printing data..."<<endl;
		(*fout)<<setprecision(DOUBLE_FILE_PRECISION);
		(*fout).setf(ios::fixed, ios::floatfield);
		(*fout).setf(ios::showpoint);
		long starttime = time(0);
		for (int i=0; i<zbl2vector.size(); ++i) {
			if (i%1000==0) cerr<<"[zbl_similarity_matrix] ["<<(time(0)-starttime)<<"s] "<<i<<" rows processed..."<<endl;
			IntDoubleListPairs& v1 = zbl2vector[i].second;
			//printPairVector("v1=",v1);

			for (int j=0; j<zbl2vector.size()-1; ++j) {
				IntDoubleListPairs& v2 = zbl2vector[j].second;
				(*fout)<<((i==j)?1.0:metric_calc(v1,v2,endIx))<<"\t";
			}
			IntDoubleListPairs& v2 = zbl2vector[zbl2vector.size()-1].second;
			(*fout)<<metric_calc(v1,v2,endIx)<<endl;
		}
		cerr<<"[zbl_similarity_matrix] ["<<(time(0)-starttime)<<"s] "<<zbl2vector.size()<<" rows processed..."<<endl;

	} catch (const char *exception) {
		cerr<<"[zbl_similarity_matrix] Error:"<<exception<<endl;
		return -1;
	}
	return 0;
}
