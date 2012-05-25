
#ifndef AUX_HPP
#define AUX_HPP

#include <iostream>
#include <map>
#include <vector>


using namespace std;

void siToisConvert(const map<string, int>& str2int, map<int, string>& int2str) {
	int2str.clear();
	for (map<string, int>::const_iterator it=str2int.begin(); it!=str2int.end(); ++it) {
		int2str.insert( make_pair<int, string>(it->second, it->first) );
	}
}

#endif

