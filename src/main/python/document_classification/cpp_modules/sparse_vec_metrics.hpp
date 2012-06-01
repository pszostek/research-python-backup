
#ifndef SPARSE_VEC_METRICS_HPP
#define SPARSE_VEC_METRICS_HPP

#include "zbl_io.hpp"
#include <iostream>
#include <cmath>
#include <set>
#include <limits>

using namespace std;
#define MAXINT std::numeric_limits<int>::max()

inline
void printPairVector(const char* label, const IntDoubleListPairs& v, int endIx=MAXINT) {
	cerr<<label;
	for(int i=0;i<v.size();++i) {
		if (v[i].first>=endIx) break;
		cerr<<v[i].first<<":"<<v[i].second<<",\t";
	}
	cerr<<endl;
}

double mul(const IntDoubleListPairs& v1, const IntDoubleListPairs& v2, int endIx=MAXINT) {
	//printPairVector("v1=", v1);
	//printPairVector("v2=", v2);
	double sum = 0.0;
	for (int i=0,j=0; i<v1.size(); ++i) {
		while (j<v2.size() && v2[j].first<v1[i].first) ++j;
		if (j>=v2.size()) break;
		if (v2[j].first>=endIx || v1[i].first>=endIx) break;
		if (v2[j].first==v1[i].first) sum += (v2[j].second*v1[i].second);
	}
	//cerr<<"-------------->"<<sum<<endl;
	return sum;
}


double len(const IntDoubleListPairs& v, int endIx=MAXINT) {
	double sum = 0.0;
	for (int i=0; i<v.size(); ++i) {
		if (v[i].first>=endIx) break;
		sum += (v[i].second*v[i].second);
	}
	return sqrt(sum);
}

void normalize(const IntDoubleListPairs& v, IntDoubleListPairs& v2, int endIx=MAXINT) {
	double l = len(v, endIx);
	for (int i=0; i<v.size(); ++i) {
		if (v[i].first>=endIx) break;
		v2.push_back( make_pair<int,double>(v[i].first, v[i].second/l) );
	}
}

/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////

double cosine(const IntDoubleListPairs& v1, const IntDoubleListPairs& v2, int endIx=MAXINT) {
	return mul(v1,v2,endIx) / (len(v1,endIx)*len(v2,endIx));
	//IntDoubleListPairs nv1,nv2; normalize(v1, nv1); normalize(v2, nv2);
	//return mul(nv1,nv2);
}

double angular_posneg(const IntDoubleListPairs& v1, const IntDoubleListPairs& v2, int endIx=MAXINT) {
	double c = cosine(v1,v2,endIx);
	return 1.0 - ( acos(c) / M_PI );
}

double tversky(const IntDoubleListPairs& vv1, const IntDoubleListPairs& vv2, int endIx=MAXINT) {
	//TODO: replace with linear-time-complexity implementation
	const IntDoubleListPairs& v1 = (vv1.size()<vv2.size())? vv1: vv2;
	const IntDoubleListPairs& v2 = (vv1.size()>=vv2.size())? vv1: vv2;
	set<int> words1;
	for (int i=0; i<v1.size(); ++i) {
		if (v1[i].first>=endIx) break;
		words1.insert(v1[i].first);
	}

	int a=0, b=0;
	for (int j=0; j<v2.size(); ++j) {
		if (v2[j].first>=endIx) break;

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

