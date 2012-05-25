
#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <map>
#include <vector>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "strs.hpp"
#include "aux.hpp"

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

	/* Reads graph from file where every line is in format:
	 * node-id:out-node1-id,out-node2-id,... */
	Graph(istream& in);
	void update_node2ix(const vector<NodeId>& nodes);
	void printLabels(ostream& o)  const;
	void printLabels(FILE* f)  const;
	void print(ostream& o)  const;
	void printCerr()  const;

	int getNumNodes() const;
	vector<NodeId> getNodes() const;
};


Graph::Graph(istream& in) {
	char buf[LINE_BUF_SIZE];
	while (!in.eof()) {
		in.getline(buf, LINE_BUF_SIZE);
		if (in.eof()) break;
		replaceStrLine(buf, ':', ',');
		vector<NodeId> nodes = split(buf, ',');
		//cerr<<"[Graph] next line:"<<buf<<" contains "<<nodes.size()<<endl;

		update_node2ix(nodes);
		NodeIx srcNodeIx = node2ix[ nodes[0] ];
		for (int i=1; i<nodes.size(); ++i) {
			NodeIx dstNodeIx = node2ix[ nodes[i] ];
			O[srcNodeIx].push_back(dstNodeIx);
			I[dstNodeIx].push_back(srcNodeIx);
		}
	}
}

void Graph::update_node2ix(const vector<NodeId>& nodes) {
	for (int i=0; i<nodes.size(); ++i) {
		if (node2ix.find(nodes[i]) == node2ix.end()) {
			node2ix.insert( make_pair<NodeId, NodeIx>(nodes[i], node2ix.size()) );
			I.push_back( IncomingNodes() ); //expand Incoming Nodes' vector
			O.push_back( OutgoingNodes() ); //expand Outgoing Nodes' vector
		}
	}
}

void Graph::printLabels(ostream& o) const {
	map<NodeIx, NodeId> ix2node;
	siToisConvert(node2ix, ix2node);
	for (int ix=0; ix<ix2node.size()-1; ++ix) {
		o<<ix2node[ix]<<"\t";
	}
	o<<ix2node[ ix2node.size()-1 ]<<endl;
}

void Graph::printLabels(FILE* f) const {
	map<NodeIx, NodeId> ix2node;
	siToisConvert(node2ix, ix2node);
	for (int ix=0; ix<ix2node.size()-1; ++ix) {
		fprintf(f, "%s\t", ix2node[ix].c_str());
	}
	fprintf(f, "%s\n", ix2node[ix2node.size()-1].c_str());
}

void Graph::print(ostream& o)  const {
	for (map<NodeId, NodeIx>::const_iterator it=node2ix.begin(); it!=node2ix.end(); ++it) {
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

void Graph::printCerr()  const {
	print(cerr);
}

int Graph::getNumNodes() const {
	return node2ix.size();
}

vector<NodeId> Graph::getNodes() const {
	vector<NodeId> nodes;
	for(map<NodeId, NodeIx>::const_iterator n=node2ix.begin(); n!=node2ix.end(); ++n) {
		nodes.push_back(n->first);
	}
	return nodes;
}


#endif
