


#ifndef SIM_AGGREGATION
#define SIM_AGGREGATION

#include <cmath>
#include "matrix_io.hpp"

inline bool custom_isnan(double var) {
    volatile double d = var;
    return d != d;
}

double sim_aggregation_avg_noweights(const Group& g1, const Group& g2, double** simmatrix) {
	double total_sim = 0.0;
	for (int i=0; i<g1.ixs.size(); ++i) {
		int ix1 = g1.ixs[i];
		for (int j=0; j<g2.ixs.size(); ++j) {
			int ix2 = g2.ixs[j];
			total_sim += simmatrix[ix1][ix2];
		}
	}
	return total_sim / g1.ixs.size() / g2.ixs.size();
}

double sim_aggregation_avg_link(const Group& g1, const Group& g2, double** simmatrix) {
	return sim_aggregation_avg_noweights(g1, g2, simmatrix);
}

double sim_aggregation_single_link(const Group& g1, const Group& g2, double** simmatrix) {
	double currentmax = 0.0;
	for (int i=0; i<g1.ixs.size(); ++i) {
		int ix1 = g1.ixs[i];
		for (int j=0; j<g2.ixs.size(); ++j) {
			int ix2 = g2.ixs[j];
			currentmax = max(simmatrix[ix1][ix2], currentmax);
		}
	}
	return currentmax;
}

double sim_aggregation_complete_link(const Group& g1, const Group& g2, double** simmatrix) {
	double currentmin = 0.0;
	for (int i=0; i<g1.ixs.size(); ++i) {
		int ix1 = g1.ixs[i];
		for (int j=0; j<g2.ixs.size(); ++j) {
			int ix2 = g2.ixs[j];
			currentmin = min(simmatrix[ix1][ix2], currentmin);
		}
	}
	return currentmin;
}




double sim_aggregation_avgw(const Group& g1, const Group& g2, double** simmatrix, double (*weight_calc)(double w1, double w2)) {
	double total_sim = 0.0;
	double total_weights = 0.0;

	for (int i=0; i<g1.ixs.size(); ++i) {
		int ix1 	= g1.ixs[i];
		double w1 	= g1.weights[i];
		for (int j=0; j<g2.ixs.size(); ++j) {
			int ix2 	= g2.ixs[j];
			double w2 	= g2.weights[j];

			float weight 	 = weight_calc(w1,w2);
			total_sim 		+= weight*simmatrix[ix1][ix2];
			total_weights 	+= weight;
		}
	}

	return total_sim / total_weights;
}

double avg_weight_calculator(double w1, double w2) {
	return (w1+w2)/2.0;
}

double sim_aggregation_avgw_avg(const Group& g1, const Group& g2, double** simmatrix) {
	return sim_aggregation_avgw(g1, g2, simmatrix, avg_weight_calculator);
}

double mul_weight_calculator(double w1, double w2) {
	return w1*w2;
}

double sim_aggregation_avgw_mul(const Group& g1, const Group& g2, double** simmatrix) {
	return sim_aggregation_avgw(g1, g2, simmatrix, mul_weight_calculator);
}


#endif
