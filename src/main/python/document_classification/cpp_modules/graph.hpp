
#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <map>
#include <vector>
#include <iostream>
#include <fstream>
#include "strs.hpp"

using namespace std;

typedef string NodeId;
typedef int NodeIx;
typedef vector<NodeIx> IncomingNodes;
typedef vector<NodeIx> OutgoingNodes;

const int LINE_BUF_SIZE = 1024*1024;

struct Graph {
	map<NodeId, NodeIx> node2ix;
	vector<IncomingNodes> I;
	vector<OutgoingNodes> O;

	int getNumNodes() const {
		return node2ix.size();
	}

	vector<NodeId> getNodes() const {
		vector<NodeId> nodes;
		for(map<NodeId, NodeIx>::const_iterator n=node2ix.begin();
				n!=node2ix.end(); ++n) {
			nodes.push_back(n->first);
		}
		return nodes;
	}

	/* Reads graph from file where every line is in format:
	 * node-id:out-node1-id,out-node2-id,... */
	Graph(istream& in) {
		char buf[LINE_BUF_SIZE];
		while (!in.eof()) {
			in.getline(buf, LINE_BUF_SIZE);
			if (in.eof()) break;

			for (char* p=buf; p; ++p) //zastap ':' na ','
				if (*p==':') {
					*p=',';
					break;
				}
			vector<NodeId> nodes = split(buf, ',');
			//cerr<<"[Graph] next line:"<<buf<<" contains "<<nodes.size()<<endl;

			update_structures(nodes);
			NodeIx srcNodeIx = node2ix[ nodes[0] ];
			for (int i=1; i<nodes.size(); ++i) {
				NodeIx dstNodeIx = node2ix[ nodes[i] ];
				O[srcNodeIx].push_back(dstNodeIx);
				I[dstNodeIx].push_back(srcNodeIx);
			}
		}
	}

	void update_structures(const vector<NodeId>& nodes) {
		for (int i=0; i<nodes.size(); ++i) {
			if (node2ix.find(nodes[i]) == node2ix.end()) {
				node2ix.insert( make_pair<NodeId, NodeIx>(nodes[i], node2ix.size()) );
				I.push_back( IncomingNodes() );
				O.push_back( OutgoingNodes() );
			}
		}
	}

	void printLabels(ostream& o) {
		for (map<NodeId, NodeIx>::iterator it=node2ix.begin(); it!=node2ix.end(); ) {
			o<<it->first;
			++it;
			if (it==node2ix.end()) o<<endl; else o<<"\t";
		}
	}

	void print(ostream& o) {
		for (map<NodeId, NodeIx>::iterator it=node2ix.begin(); it!=node2ix.end(); ++it) {
			o<<it->first<<":="<<it->second<<endl;
		}
		for (int i=0; i<I.size(); ++i) {
			o<<i<<"<-\t";
			for (int j=0; j<I[i].size(); ++j) {
				o<<I[i][j]<<", ";
			}
			o<<endl;
		}

		for (int i=0; i<O.size(); ++i) {
			o<<i<<"->\t";
			for (int j=0; j<O[i].size(); ++j) {
				o<<O[i][j]<<", ";
			}
			o<<endl;
		}
	}

	void printCerr() {
		print(cerr);
	}
};


#endif
