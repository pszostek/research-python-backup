
#ifndef ZBL_IO_HPP
#define ZBL_IO_HPP

#include <iostream>
#include <map>
#include <utility>
#include <string.h>
#include <vector>
#include "strs.hpp"

using namespace std;

typedef string ZblKey;
typedef string ZblVal;
typedef map<ZblKey,ZblVal> ZblRecord;

const int LINE_BUF_SIZE = 1024*1024;
const char* ZBL_ID_FIELD = "an";
const char ZBL_DICT_FSEP = ',';
const char ZBL_DICT_VSEP = ':';

typedef vector< pair<int, double> > IntDoubleListPairs;

void extractIntDoubleListPairs(const string& fieldValue,
		IntDoubleListPairs& output,
		char dictSep = ZBL_DICT_FSEP,
		char dictPairSep = ZBL_DICT_VSEP) {
	//cerr<<"[extractIntFloatListPairs] src-string="<<fieldValue<<endl;
	vector<string> strpairs = split(fieldValue, dictSep);
	for (int i=0; i<strpairs.size(); ++i) {
		vector<string> pair = split(strpairs[i], dictPairSep);
		//cout<<"[extractIntFloatListPairs] next-extracted-pair="<<(pair[0])<<":"<<(pair[1])<<endl;
		int key = strToInt(pair[0]);
		double val = strToFloat(pair[1]);
		output.push_back( make_pair<int,double>(key, val) );
	}
}

pair<ZblKey, ZblVal> extractZblField(const char* buf) {
	string line = buf;
	size_t breakpoint = line.find(' ');
	if (breakpoint == string::npos) {
		throw "[extractZblField] Invalid line (no space breakpoint)!";
	}
	size_t startpoint = findNotWs(line, breakpoint);
	if (startpoint == string::npos) {
		throw "[extractZblField] Invalid line (no value startpoint)!";
	}
	return pair<ZblKey, ZblVal>(line.substr(0, breakpoint), line.substr(startpoint));
}

void zblRecordPrinter(const ZblRecord& record) {
	string an = record.find(ZBL_ID_FIELD)->second;
	cout<<ZBL_ID_FIELD<<"  "<<an<<endl;
	for (ZblRecord::const_iterator field=record.begin(); field!=record.end(); ++field) {
		if (field->first != ZBL_ID_FIELD) {
			cout<<field->first<<"  "<<field->second<<endl;
		}
	}
	cout<<endl;
}

void readZblStream(istream& in, void (*zblRecordProcessor)(const ZblRecord& zbl) = zblRecordPrinter ) {
	char buf[LINE_BUF_SIZE];
	ZblRecord zbl;
	while (!in.eof()) {
		in.getline(buf, LINE_BUF_SIZE);
		if (in.eof()) break;
		if (strlen(buf) <= 0) continue;
		pair<ZblKey, ZblVal> field = extractZblField(buf);
		//cout<<"key=<"<<field.first<<"> val=<"<<field.second<<">"<<endl;
		if (field.first == ZBL_ID_FIELD && zbl.size()>0) {
			//cout<<"Next record detected"<<endl;
			zblRecordProcessor(zbl);
			zbl.clear();
		}
		zbl.insert(field);
	}
	if (zbl.size()>0) {
		zblRecordProcessor(zbl);
	}
}


#endif
