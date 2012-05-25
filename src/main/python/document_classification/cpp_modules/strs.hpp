
#ifndef STRS_HPP
#define STRS_HPP

#include <iostream>
#include <ostream>
#include <sstream>
#include <vector>
#include <utility>
#include <string.h>
#include <stdio.h>
#include <cstdlib>
#include <math.h>

using namespace std;



vector<string> split(const string& strValue, char separator)
{
    vector<string> vecstrResult;
    int startpos=0;
    int endpos=0;

    endpos = strValue.find_first_of(separator, startpos);
    if (endpos == -1) {
    	vecstrResult.push_back(strValue);
    }
    while (endpos != -1)
    {
        vecstrResult.push_back(strValue.substr(startpos, endpos-startpos)); // add to vector
        startpos = endpos+1; //jump past sep
        endpos = strValue.find_first_of(separator, startpos); // find next
        if(endpos==-1)
        {
            //lastone, so no 2nd param required to go to end of string
            vecstrResult.push_back(strValue.substr(startpos));
        }
    }

    return vecstrResult;
}



string trim2(string& str)
{
  string::size_type pos = str.find_last_not_of(' ');
  if(pos != string::npos) {
    str.erase(pos + 1);
    pos = str.find_first_not_of(' ');
    if(pos != string::npos) str.erase(0, pos);
  }
  else str.erase(str.begin(), str.end());
  return str;
}

size_t findNotWs(const string& s, size_t p) {
	for (; p<s.length(); ++p) {
		if (s[p]!=' ' && s[p]!='\t') {
			return p;
		}
	}
	return string::npos;
}

int strToInt(const string& str) {
	int i;
	istringstream iss(str);
	iss >> i;
	return i;
}

string intToStr(int i) {
	  stringstream ss;//create a stringstream
	  ss << i;//add number to the stream
	  return ss.str();//return a string with the contents of the stream
}


double strToFloat(const string& str) {
	double value;
	std::istringstream sstr(str);
	sstr >> value;
	return value;
}

double strToDouble(const string& str) {
	return strToFloat(str);
}

void replaceStrLine(char* buf, char src, char dst) {
	for (char* p=buf; *p!=0 && *p!='\n'; ++p) {
		if (*p==src) {
			*p=dst;
		}
	}
}

#endif
