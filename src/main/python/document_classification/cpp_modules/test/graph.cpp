
#include "../graph.hpp"


int main() {
	cout<<"Opening"<<endl;
	ifstream in("graph.txt");
	cout<<"Loading"<<endl;
	Graph g(in);
	cout<<"Printing"<<endl;
	g.printLabels(cout);
	g.print(cout);
	return 0;
}
