
#ifndef SIM_AGGREGATION
#define SIM_AGGREGATION

#include <cmath>

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


double sim_aggregation_avg_mul(const Group& g1, const Group& g2, double** simmatrix) {

	double total_sim = 0.0;
	double total_weights = 0.0;

	for (int i=0; i<g1.ixs.size(); ++i) {
		int ix1 = g1.ixs[i];
		for (int j=0; j<g2.ixs.size(); ++j) {
			int ix2 = g2.ixs[j];

			float weight = g1.weights[i]*g2.weights[i];
			total_sim += weight*simmatrix[ix1][ix2];
			total_weights += weight;
		}
	}

	return total_sim / total_weights;
}


#endif
