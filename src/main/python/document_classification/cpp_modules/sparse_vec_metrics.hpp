
#ifndef SPARSE_VEC_METRICS_HPP
#define SPARSE_VEC_METRICS_HPP

#include "zbl_io.hpp"
#include <iostream>
#include <cmath>
#include <set>

using namespace std;

inline
void printPairVector(const char* label, const IntDoubleListPairs& v) {
	cerr<<label;
	for(int i=0;i<v.size();++i) {
		cerr<<v[i].first<<":"<<v[i].second<<",\t";
	}
	cerr<<endl;
}

double mul(const IntDoubleListPairs& v1, const IntDoubleListPairs& v2) {
	//printPairVector("v1=", v1);
	//printPairVector("v2=", v2);
	double sum = 0.0;
	for (int i=0,j=0; i<v1.size(); ++i) {
		while (j<v2.size() && v2[j].first<v1[i].first) ++j;
		if (j>=v2.size()) break;
		if (v2[j].first==v1[i].first) sum += (v2[j].second*v1[i].second);
	}
	//cerr<<"-------------->"<<sum<<endl;
	return sum;
}


double len(const IntDoubleListPairs& v) {
	double sum = 0.0;
	for (int i=0; i<v.size(); ++i) {
		sum += (v[i].second*v[i].second);
	}
	return sqrt(sum);
}

void normalize(const IntDoubleListPairs& v, IntDoubleListPairs& v2) {
	double l = len(v);
	for (int i=0; i<v.size(); ++i) {
		v2.push_back( make_pair<int,double>(v[i].first, v[i].second/l) );
	}
}

/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////

double cosine(const IntDoubleListPairs& v1, const IntDoubleListPairs& v2) {
	return mul(v1,v2) / (len(v1)*len(v2));
	//IntDoubleListPairs nv1,nv2; normalize(v1, nv1); normalize(v2, nv2);
	//return mul(nv1,nv2);
}

double angular_posneg(const IntDoubleListPairs& v1, const IntDoubleListPairs& v2) {
	double c = cosine(v1,v2);
	return 1.0 - ( acos(c) / M_PI );
}

double tversky(const IntDoubleListPairs& vv1, const IntDoubleListPairs& vv2) {
	const IntDoubleListPairs& v1 = (vv1.size()<vv2.size())? vv1: vv2;
	const IntDoubleListPairs& v2 = (vv1.size()>=vv2.size())? vv1: vv2;
	set<int> words1;
	for (int i=0; i<v1.size(); ++i) {
		words1.insert(v1[i].first);
	}

	int a=0, b=0;
	for (int j=0; j<v2.size(); ++j) {
		set<int>::iterator wit = words1.find(v2[j].first);
		if (wit==words1.end()) {
			++b; //tylko w v2
		} else {
			++a; //w obu
		}
	}
	int c=words1.size()-a; //tylko w v1

	return double(a) / (a+b+c);
}

#endif

