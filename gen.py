#!/usr/bin/python

import numpy
import shutil
import os
import sys

TESTS_DIR = "tests"
MIN_MATRIX_SIZE = 100
MAX_MATRIX_SIZE = 1000
MATRIX_INT_MIN = -10000
MATRIX_INT_MAX = 10000

print "Test matrix generator script for AESC Summer School Contest"

def random_size():
	return numpy.random.randint(MIN_MATRIX_SIZE, MAX_MATRIX_SIZE + 1)

def gen_random(N):
	matrix = numpy.random.random_integers(MATRIX_INT_MIN, MATRIX_INT_MAX, size = (N, N))
	return matrix

def gen_diagonal(N):
	diagonal = numpy.random.random_integers(MATRIX_INT_MIN, MATRIX_INT_MAX, size = (N))
	return numpy.diag(diagonal)

def gen_triangular(N):
	matrix = gen_random(N)
	if numpy.random.choice([True, False]):
		return numpy.triu(matrix)
	else:
		return numpy.tril(matrix)

def gen_symmetric(N):
	matrix = numpy.random.random_integers(MATRIX_INT_MIN, MATRIX_INT_MAX, size = (N, N))
	matrix = (matrix + matrix.T)/2
	return matrix

def gen_skew_symmetric(N):
	matrix = numpy.random.random_integers(MATRIX_INT_MIN, MATRIX_INT_MAX, size = (N, N))
	matrix = numpy.triu(matrix)
	matrix = matrix - matrix.T
	return matrix

def gen_sparse(N):
	matrix = numpy.zeros(shape = (N, N))
	for index in numpy.ndenumerate(matrix):
		if numpy.random.choice([True, False], p = [0.1, 0.9]):
			matrix[index[0]] = numpy.random.randint(MATRIX_INT_MIN, MATRIX_INT_MAX + 1)
	return matrix

def gen_toeplitz(N):
	c = numpy.random.random_integers(MATRIX_INT_MIN, MATRIX_INT_MAX, size = (N))
	r = numpy.random.random_integers(MATRIX_INT_MIN, MATRIX_INT_MAX, size = (N))
	# from scipy.linalg.toeplitz
	c = numpy.asarray(c).ravel()
	if r is None:
		r = c.conjugate()
	else:
		r = numpy.asarray(r).ravel()
	# Form a 1D array of values to be used in the matrix, containing a reversed
	# copy of r[1:], followed by c.
	vals = numpy.concatenate((r[-1:0:-1], c))
	a, b = numpy.ogrid[0:len(c), len(r) - 1:-1:-1]
	indx = a + b
	# `indx` is a 2D array of indices into the 1D array `vals`, arranged so
	# that `vals[indx]` is the Toeplitz matrix.
	return vals[indx]

def save_matrix(matrix, filename):
	file = open(os.path.join(TESTS_DIR, filename), 'w')
	print >> file, matrix.shape[0]
	for row in matrix:
		for cell in row:
			print >> file, cell,
		else:
			print >> file
	file.close()

shutil.rmtree(TESTS_DIR, ignore_errors = True)
os.mkdir(TESTS_DIR)

if len(sys.argv) < 2:
    sys.exit('Usage: %s n\nn - number of matrices of each type to be generated' % sys.argv[0])
N = int(sys.argv[1])

for i in range(N):
	size = random_size()
	matrix = gen_random(size)
	save_matrix(matrix, "random_" + str(i) + ".txt")
print "random generated"
for i in range(N):
	size = random_size()
	matrix = gen_diagonal(size)
	save_matrix(matrix, "diagonal_" + str(i) + ".txt")
print "diagonal generated"
for i in range(N):
	size = random_size()
	matrix = gen_triangular(size)
	save_matrix(matrix, "triangular_" + str(i) + ".txt")
print "triangular generated"
for i in range(N):
	size = random_size()
	matrix = gen_symmetric(size)
	save_matrix(matrix, "symmetric_" + str(i) + ".txt")
print "symmetric generated"
for i in range(N):
	size = random_size()
	matrix = gen_skew_symmetric(size)
	save_matrix(matrix, "skew_symmetric_" + str(i) + ".txt")
print "skew symmetric generated"
for i in range(N):
	size = random_size()
	matrix = gen_sparse(size)
	save_matrix(matrix, "sparse_" + str(i) + ".txt")
print "sparse generated"
for i in range(N):
	size = random_size()
	matrix = gen_toeplitz(size)
	save_matrix(matrix, "toeplitz_" + str(i) + ".txt")
print "toeplitz generated"
