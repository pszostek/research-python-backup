#include <cmath>



template <typename T>
double euclid2_dist(const T* x, const T* y, int dim) {
    double dist = 0.0;
    for (int d=0; d<dim; ++d) {
        dist += (x[d]-y[d])*(x[d]-y[d]);
    }
    return dist;
}



template <typename T>
double vector_len(const T* x, int dim) {
    double len = 0.0;
    for (int d=0; d<dim; ++d) {
        len += x[d]*x[d];
    }
    return sqrt(len);//sqrt(len+1.0);
}

template <typename T>
double dot_product(const T* x, const T* y, int dim) {
    double v = 0.0;
    for (int d=0; d<dim; ++d) {
        v += x[d]*y[d];
    }
    return v; //v+1.0;
}

template <typename T>
double cosine_dist(const T* x, const T* y, int dim) {
    return 1.0 - dot_product(x,y,dim)/( vector_len(x,dim)*vector_len(y,dim) );
}
