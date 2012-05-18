
#include "../graph.hpp"


int main() {
	ifstream in("graph.txt");
	Graph g(in);
	g.printCerr();
	return 0;
}
