

#include <ctime>
#include <iostream>
#include <iomanip>
#include <stdio.h>
#include "../matrix_io.hpp"
#include "../sim_aggregation.hpp"
#include <ctime>
#include <map>

using namespace std;

const int DOUBLE_FILE_PRECISION = 20;
double (*sim_aggregation_func)(const Group& g1, const Group& g2, double** simmatrix) = sim_aggregation_avg_noweights;


int main(int argc, char *argv[]) {
	cerr<<"[aggregate_simmatrix] ##############################################################"<<endl;
	cerr<<"[aggregate_simmatrix] The program aggregates similarity matrix."<<endl;

	const char* groups_path;
	if (argc>1) {
		groups_path = argv[1];
	} else {
		cerr<<"[aggregate_simmatrix] Argument expected: groups-path"<<endl;
		cerr<<"[aggregate_simmatrix] Argument1: groups-path"<<endl;
		cerr<<"[aggregate_simmatrix] Argument2: aggregation method (a=average/s=single link (maximum)/m=complete link (minimum)/avgw=weighted average)"<<endl;
		exit(-1);
	}

	const char* agrfunc = "a";
	if (argc>2) {
		agrfunc = argv[2];
	}

	if (strcmp(agrfunc, "a")==0) {
		cerr<<"[aggregate_simmatrix] Aggregation function=sim_aggregation_avg"<<endl;
		sim_aggregation_func = sim_aggregation_avg_link;
	} else
	if (strcmp(agrfunc, "avgw")==0) {
		cerr<<"[aggregate_simmatrix] Aggregation function=sim_aggregation_avg_mul"<<endl;
		sim_aggregation_func = sim_aggregation_avg_mul;
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
	cout<<setprecision(DOUBLE_FILE_PRECISION);
	cout.setf(ios::fixed, ios::floatfield);
	cout.setf(ios::showpoint);

	cerr<<"[aggregate_simmatrix] Loading similarity matrix from stdin..."<<endl;
	long starttime = time(0);
	Matrix m;
	loadMatrix(stdin, m);
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


	cerr<<"[aggregate_simmatrix] Printing matrix to cout..."<<endl;
	for (int g=0; g<groups.size()-1; ++g) {
		cout<<groups[g].name<<"\t";
	}
	cout<<groups.back().name<<endl;
	for (int g=0; g<groups.size()-1; ++g) {
		cout<<groups[g].name<<"\t";
	}
	cout<<groups.back().name<<endl;
	printMatrix(simmatrix, cout, groups.size(), groups.size());

	cerr<<"[aggregate_simmatrix] ##############################################################"<<endl;
}
