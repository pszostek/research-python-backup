#include <stdio.h>
#include <cstring>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <fstream>
#include <cmath>
#include <string.h>

using namespace std;

template <typename M>
int store_squared_rmatrix(const char* fpath, M distm, int size) {
	FILE* f = fopen(fpath, "w");
	if (f == NULL) {
		return -1;
	}
	for (int r=0; r<size; ++r) {
		//cout<<"Writing row ="<<r<<endl;
		for (int c=0; c<size-1; ++c) {
			fprintf(f, "%f\t", distm[r][c]);
		}
		fprintf(f, "%f\n", distm[r][size-1]);
	}
	fclose(f);
	return 0;
}

template <typename M>
int store_rect_rmatrix(const char* fpath, M distm, int rows, int cols) {
	FILE* f = fopen(fpath, "w");
	if (f == NULL) {
		return -1;
	}
	for (int r=0; r<rows; ++r) {

		//cout<<"Writing row ="<<r<<endl;
		for (int c=0; c<cols-1; ++c) {
			fprintf(f, "%f\t", distm[r][c]);
		}
		fprintf(f, "%f\n", distm[r][cols-1]);

	}
	fclose(f);
	return 0;
}

/*
int get_file_numlines(const char *filename) {
    FILE *f;
    char line[1000000];
    int lines = 0;

    f = fopen(filename, "r");
    if(f == NULL)
        return 0;
    while(!feof(f)) {
    	fgets (line, 1000000, f);
        if(!feof(f) && strlen(line) > 2) {
            lines++;
        }
    }
    fclose(f);
    return lines;
}*/

int get_file_numlines(const char *filename) {
	ifstream in(filename);
	std::string tmpstr;
	int numLines = 0;
	while ( std::getline(in, tmpstr) ) {
		if (tmpstr.length() > 2)
			++numLines;
	}
	return numLines;
}

template <typename T>
int parse_row(const char* line, T* row) {
	stringstream s(line);
    int i;
    for(i = 0; !s.eof() ;++i) {
        s>>row[i];
    }
    return i-1;
}


int get_file_numcols(const char *filename) {
    char line[1000000];
    float rowvals[100000];

    FILE *f = fopen(filename, "r");
    if(f == NULL || feof(f))
        return 0;

    fgets (line, 1000000, f);
    int numvals = parse_row(line, rowvals);

    fclose(f);
    return numvals;
}

template <typename T>
inline bool is_nan(T value)
{
	return value != value;
}


double** alloc_matrix_float(int n) {
    double** distm = new double*[n];
    for (int i=0; i<n; ++i) {
        distm[i] = new double[n];
    }
    return distm;
}

template <typename T>
struct DataMatrix {    
    T** data;
    int numrows;
    int numcols;

    DataMatrix() {
    	numrows = 0;
    	numcols = 0;
    	data = NULL;
    }

    DataMatrix(const char* fpath) {
        load_data(fpath);
    }
    
    ~DataMatrix() {
    	if (data != NULL) {
    		free_memory();
    	}
    }


    void load_data(const char* fpath, int readrows=-1) {
        numrows = (readrows < 0)? get_file_numlines(fpath): readrows;
        if (numrows <= 0) {
        	throw "Failed to read data!";
        }

        data = new T*[numrows];
        FILE* f = fopen(fpath, "r");
        char line[1000000];
        T rowvals[100000];
        numcols = -1;
        for (int row=0; row<numrows; ++row) {
        	fgets (line, 1000000, f);

            int numvals = parse_row(line, rowvals);
            if (numcols < 0) {
            	numcols = numvals;
            } else if (numcols != numvals) {
            	cerr<<"[DataMatrix::load_data] numcols != numvals in row="<<row<<endl;
            	cerr<<"[DataMatrix::load_data] numcols = "<<numcols<<endl;
            	cerr<<"[DataMatrix::load_data] numvals = "<<numvals<<endl;
            	cerr<<"[DataMatrix::load_data] line =["<<line<<"]"<<endl;
            	throw "Inconsistent data in input file!";
            }
            data[row] = new T[numcols];
            memcpy(data[row], rowvals, numcols*sizeof(T));
        }
        fclose(f);           
    }

    T maxval() {
        T v = data[0][0];
        for (int r=0; r<numrows; ++r) {
            for (int c=0; c<numcols; ++c) {
                v = max(data[r][c], v);
            }
        }
        return v;
    }

    T minval() {
    	T v = data[0][0];
        for (int r=0; r<numrows; ++r) {
            for (int c=0; c<numcols; ++c) {
                v = min(data[r][c], v);
            }
        }
        return v;
    }

    void print_rect(int size) {
        for (int r=0; r<min(size, numrows); ++r) {
            for (int c=0; c<min(size, numcols); ++c) {
            	cout<<data[r][c]<<" ";
            }
            cout<<endl;
        }
    }

    void free_memory() {
    	for (int r=0; r<numrows; ++r) {
    		delete[] data[r];
    	}
    	delete[] data;
    	data = NULL;
    	numrows = 0;
    	numcols = 0;
    }

    double* get_avg() {
    	double* avg = new double[numcols];
    	memset(avg, 0, sizeof(double)*numcols);

    	for (int r=0; r<numrows; ++r) {
    		for (int c=0; c<numcols; ++c) {
    			avg[c] = avg[c] + data[r][c];
    		}
    	}

    	for (int c=0; c<numcols; ++c) {
    		avg[c] = avg[c]/numrows;
    	}

    	return avg;
    }

    double* get_std(const double* avg) {
    	double* std = new double[numcols];
    	memset(std, 0, sizeof(double)*numcols);

    	for (int r=0; r<numrows; ++r) {
    		for (int c=0; c<numcols; ++c) {
    			double dist = data[r][c]-avg[c];
    			std[c] += dist*dist;
    	    }
    	}

    	for (int c=0; c<numcols; ++c) {
    		std[c] = sqrt(std[c]/numrows);
    		//if (is_nan(std[c])) printf("[get_std] NaN detected!\n");
    	}

    	return std;
    }

    void normalize_data() {
    	double* avg = get_avg();
    	double* std = get_std(avg);

    	for (int r=0; r<numrows; r++) {
    		for (int c=0; c<numcols; c++) {
    			double denominator = (std[c]==0.0)? 1.0: std[c]; //WARN!
    			//if (is_nan(data[r][c])) printf("[normalize_data] Before normalization: NaN detected!");
    			data[r][c] = (data[r][c] - avg[c]) / denominator;
    			if (is_nan(data[r][c])) fprintf(stderr,"[normalize_data] NaN detected (std[c]=%f)!\n",std[c]);
    		}
    	}

    	delete[] std;
    	delete[] avg;
    }

};


template <typename T>
void data_preview(DataMatrix<T>& datam) {
    cout<<"Sample data (1-25 x 1-25):"<<endl;
    datam.print_rect(25);
    cout<<"Data avg:"<<endl;
    double* avg = datam.get_avg();
    for (int c=0; c<datam.numcols; ++c) {
    	cout<<avg[c]<<" ";
    }
    cout<<endl;
    cout<<"Data std:"<<endl;
    double* std = datam.get_std(avg);
    for (int c=0; c<datam.numcols; ++c) {
    	cout<<std[c]<<" ";
    }
    cout<<endl;
    delete[] std;
    delete[] avg;
}
