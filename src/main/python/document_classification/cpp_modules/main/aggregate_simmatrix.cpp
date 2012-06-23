

#include <ctime>
#include <iostream>
#include <iomanip>
#include <stdio.h>
#include "../matrix_io.hpp"
#include "../sim_aggregation.hpp"
#include <ctime>
#include <map>
#include <fstream>

using namespace std;

const int DOUBLE_FILE_PRECISION = 20;
double (*sim_aggregation_func)(const Group& g1, const Group& g2, double** simmatrix) = sim_aggregation_avg_noweights;


int main(int argc, char *argv[]) {
	cerr<<"[aggregate_simmatrix] ##############################################################"<<endl;
	cerr<<"[aggregate_simmatrix] The program aggregates similarity matrix."<<endl;

	FILE* fin = stdin;
	ostream* fout = &cout;
	ofstream fileOutput;
	if (argc > 4) {
		cerr<<"[aggregate_simmatrix] Opening for reading:"<<argv[3]<<endl;
		fin = fopen(argv[3], "r");
		cerr<<"[aggregate_simmatrix] Opening for writing:"<<argv[4]<<endl;
		fileOutput.open(argv[4]);
		fout = &fileOutput;
	}


	const char* groups_path;
	if (argc>1) {
		groups_path = argv[1];
	} else {
		cerr<<"[aggregate_simmatrix] Argument expected: groups-path"<<endl;
		cerr<<"[aggregate_simmatrix] Argument1: groups-path"<<endl;
		cerr<<"[aggregate_simmatrix] Argument2: aggregation method (a=average/s=single link (maximum)/m=complete link (minimum)/avgw=weighted average)"<<endl;
		exit(-1);
	}

	char* agrfunc = "a";
	if (argc>2) {
		agrfunc = argv[2];
	}

	cerr<<"[aggregate_simmatrix] Aggregation function name="<<agrfunc<<endl;
	if (strlen(agrfunc)>4) {
		agrfunc[4] = '\0';
	}
	if (strcmp(agrfunc, "a")==0) {
		cerr<<"[aggregate_simmatrix] Aggregation function=sim_aggregation_avg"<<endl;
		sim_aggregation_func = sim_aggregation_avg_link;
	} else
	if (strcmp(agrfunc, "avgw")==0) {
		cerr<<"[aggregate_simmatrix] Aggregation function=sim_aggregation_avgw_avg"<<endl;
		sim_aggregation_func = sim_aggregation_avgw_avg;
	} else
	if (strcmp(agrfunc, "s")==0) {
		cerr<<"[aggregate_simmatrix] Aggregation function=sim_aggregation_single_link"<<endl;
		sim_aggregation_func = sim_aggregation_single_link;
	} else
	if (strcmp(agrfunc, "m")==0) {
		cerr<<"[aggregate_simmatrix] Aggregation function=sim_aggregation_complete_link"<<endl;
		sim_aggregation_func = sim_aggregation_complete_link;
	} else {
		cerr<<"[aggregate_simmatrix] Unknown aggregation function!."<<endl;
		exit(-2);
	}

	//cerr<<setprecision(DOUBLE_FILE_PRECISION);
	//cerr.setf(ios::fixed, ios::floatfield);
	//cerr.setf(ios::showpoint);
	(*fout)<<setprecision(DOUBLE_FILE_PRECISION);
	(*fout).setf(ios::fixed, ios::floatfield);
	(*fout).setf(ios::showpoint);

	cerr<<"[aggregate_simmatrix] Loading similarity matrix from stdin..."<<endl;
	long starttime = time(0);
	Matrix m;
	loadMatrix(fin, m);
	cerr<<"[aggregate_simmatrix]  matrix loaded in "<<(time(0)-starttime)<<"s"<<endl;

	cerr<<"[aggregate_simmatrix] Converting matrix ids to ixs..."<<endl;
	map<string, int> id2ix;
	for (int ix=0; ix<m.rows.size(); ++ix) {
		id2ix[m.rows[ix]] = ix;
	}

	cerr<<"[aggregate_simmatrix] Loading groups from file "<<groups_path<<endl;
	FILE* groups_file = fopen(groups_path, "r");
	vector<Group> groups;
	loadGroups(groups_file, id2ix, groups);
	fclose(groups_file);
	cerr<<"[aggregate_simmatrix] "<<groups.size()<<" groups loaded."<<endl;

	long num_pairs = 0;
	for (int i=0; i<groups.size(); ++i) {
		for (int j=0; j<groups.size(); ++j) {
			num_pairs += groups[i].ixs.size() * groups[j].ixs.size();
		}
	}
	cerr<<"[aggregate_simmatrix] "<<num_pairs<<" pairs of elements need to be considered."<<endl;

	cerr<<"[aggregate_simmatrix] Calculating matrix..."<<endl;
	double** simmatrix = allocMatrix<double>( groups.size() );
	for (int i=0; i<groups.size(); ++i) {
		if (i%100==0) cerr<<"[aggregate_simmatrix]  group no="<<i<<" out of "<<groups.size()<<endl;
		for (int j=i; j<groups.size(); ++j) {
			double sim = sim_aggregation_func(groups[i], groups[j], m.data);
			if (custom_isnan(sim)) {
				cerr<<"[aggregate_simmatrix] [Error] NaN value in row="<<groups[i].name<<" col="<<groups[j].name<<endl;
			}
			simmatrix[i][j] = sim;
			simmatrix[j][i] = sim;
		}
	}
	cerr<<"[aggregate_simmatrix]  group no="<<groups.size()-1<<" out of "<<groups.size()<<endl;


	cerr<<"[aggregate_simmatrix] Printing matrix to (*fout)..."<<endl;
	for (int g=0; g<groups.size()-1; ++g) {
		(*fout)<<groups[g].name<<"\t";
	}
	(*fout)<<groups.back().name<<endl;
	for (int g=0; g<groups.size()-1; ++g) {
		(*fout)<<groups[g].name<<"\t";
	}
	(*fout)<<groups.back().name<<endl;
	printMatrix(simmatrix, (*fout), groups.size(), groups.size());

	cerr<<"[aggregate_simmatrix] ##############################################################"<<endl;
}
