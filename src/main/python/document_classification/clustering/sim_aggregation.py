"""Functions that aggregates values from similarity matrix into single value."""


def matrix_fg(matrix, f, g):
    """For every row of squared matrix executes f(row) and then reduces using g."""
    return reduce(lambda x,y:g(x,y), (f(row) for row in matrix) )

def matrix_min(matrix):
    """Returns min value of squared matrix (given as a list of lists)."""    
    return matrix_fg(matrix, min, min)

def matrix_max(matrix):
    """Returns max value of squared matrix (given as a list of lists)."""    
    return matrix_fg(matrix, max, max)

def matrix_avg_U(matrix):
    """Returns avg value of upper triangle (above diagonal) of squared matrix (given as a list of lists)."""
    dim = len(matrix)    
    if dim == 1:
        return matrix[0][0]
    else:   
        return sum( sum(matrix[r][r+1:dim]) for r in xrange(dim) ) * 2.0 / (dim*dim-dim)
    