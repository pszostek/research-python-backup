import random

def add_random_column(input_stream):
	"""Adds random float from <-1, 1> as a feature column to the input csv"""
	for l in input_stream:
		vec = [i for i in l.split(';')]	
		#print vec
		vec = vec[0:len(vec)-1]+[str(2*(0.5-random.random()))]+[vec[len(vec)-1].replace("\n", "")]
		print ";".join(vec)

def randomize_columns(input_stream, a):
	"""Adds random float from <-a, a> to all feature columns to the input csv"""
	for l in input_stream:
		vec = [i for i in l.split(';')]	
		#print vec
		vec = [vec[0]]+[str(float(x)+2*a*(0.5-random.random())) for x in vec[1:len(vec)-1]]+[vec[len(vec)-1].replace("\n", "")]
		print ";".join(vec)

def double_column(input_stream, num):
	"""Doubles one of the columns in the inpyt csv"""
	for l in input_stream:
		vec = [i for i in l.split(';')]	
		#print vec
		vec = vec[0:num+1]+vec[num:len(vec)-2]+[vec[len(vec)-1].replace("\n", "")]
		print ";".join(vec)

if __name__ == "__main__":
	import sys
	with open(sys.argv[1]) as f:
		double_column(f, int(sys.argv[2]))
