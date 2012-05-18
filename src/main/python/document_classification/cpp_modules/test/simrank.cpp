
#include "../graph.hpp"
#include "../simrank.hpp"
#include "../simrank_storage.hpp"

int main() {
	ifstream in("graph.txt");
	Graph g(in);
	g.printCerr();

	cerr.setf(ios::fixed, ios::floatfield);
	cerr.setf(ios::showpoint);

	MemoryRFactory rFactory;
	simrank(g, &rFactory, 0.8, 5);
	rFactory.printCerr();

	cerr<<"----------------"<<endl;
	simrank(g, &rFactory, 0.8, 10);
	rFactory.printCerr();

	cerr<<"----------------"<<endl;
	simrank(g, &rFactory, 0.8, 20);
	rFactory.printCerr();


	return 0;
}
