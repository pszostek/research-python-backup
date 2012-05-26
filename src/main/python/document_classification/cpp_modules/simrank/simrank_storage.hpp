
#ifndef SIMRANK_STORAGE
#define SIMRANK_STORAGE


struct RPrev {
	virtual double get(int row, int col) const = 0;
};

struct RNext {
	virtual void set(int row, int col, double val) = 0;
};

struct RFactory {
	RFactory(){}

	virtual RNext* getInitial(const Graph* g, int numThreads) = 0;
	virtual RNext* getNext() = 0;
	virtual RPrev* getPrev() = 0;
	virtual void printData(ostream& o) = 0;
	virtual ~RFactory() {};
};




#endif
