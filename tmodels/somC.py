__author__ = 'tintin'

import numpy as np
import numba
import time
import math
from numba.decorators import jit as jit
import pdb
#pdb.set_trace()
np.random.seed(1)
nd0 = numba.double
nd1 = numba.double[:]
nd2 = numba.double[:, :]

class SomC:

    # http://stackoverflow.com/questions/6768245/difference-between-frompyfunc-and-vectorize-in-numpy
    #filler = np.frompyfunc(lambda x: list(), 1, 1)
    #a = np.empty((3, 4), dtype=np.object)
    #filler(a, a)
    # Set parameters, shared between objects
    num_iterations = 10
    learning_rate_initial = 0.5
    learning_rate_final = 0.1
    learning_spread_final = 1.0
    # index to SOM and its dimensions
    # we convert grid_indices to hold the list of urls
    #grid_indices = np.zeros((num_nodes, len(grid_size)), dtype='d')
    fillerfn = np.frompyfunc(lambda x: list(), 1, 1)
    # we fill in the indices
    #grid_indices[:, 0] = raw_grid[0].ravel()
    #grid_indices[:, 1] = raw_grid[1].ravel()

    @jit(argtypes=[nd0, nd0, nd0])
    def scale(self, start, end, position):
        return np.double(start + (end - start)*position)

    def __init__(self, matrix, n_dims, grid_size):
        self.num_nodes = grid_size[0]*grid_size[1]
        self.n_dims = n_dims
        self.grid_size = grid_size
        self.learning_spread_initial = np.max(grid_size) / 5.0
        t_grid_links = np.empty((self.num_nodes, 1), dtype=np.object)
        self.grid_links = self.fillerfn(t_grid_links, t_grid_links)
        self.abs_distances = np.zeros((self.num_nodes, ), dtype='d')

        #Full SOM Grid
        self.som_weights = matrix
        #self.the_som = np.reshape(self.som_weights, (self.grid_size[0], self.grid_size[1], self.n_dims))

    # update weights in the SOM, arguments are the sample, SOM mesh, winner Node index, index of SOM, learning
    # rate, learning spread
    @jit(argtypes = [nd1, nd2, nd0, nd2, nd0, nd0])
    def update_weights(self, this_sample, som_weights, winner_idx, grid_indices, learning_rate, learning_spread):
        #winner_x = som_weights[winner_idx, 0]
        #winner_y = som_weights[winner_idx, 1]

        # Here we the geometric distance b/w them and update the som weight to match same color
        num_nodes, num_dims = som_weights.shape
        for i in range(num_nodes):
            # compute euclidean distance b/w som node and winner node
            #grid_distance = np.subtract(som_weights[i], som_weights[winner_idx])
            #grid_distance = np.dot(grid_distance, grid_distance)
            #grid_distance = np.sqrt(grid_distance)
            grid_distance = np.linalg.norm(som_weights[i]-som_weights[winner_idx])
            #grid_distance = ((winner_x - som_weights[i,0]) ** 2.0) + ((winner_y - som_weights[i,1])**2.0)
            dampening = math.e ** (-1.0 * grid_distance / ( 2.0 * learning_spread**2.0))
            dampening *= learning_rate

            for j in range(num_dims):
                som_weights[i,j] += dampening * (this_sample[j] - som_weights[i,j])

    #find winner passes the SOM grid, sample to be checked, outputs abs_distances between nodes
    @jit(argtypes = [nd2, nd1, nd1])
    def find_winner(self, som_weights, this_sample, abs_distances):
        num_nodes, num_dims = som_weights.shape

        for i in range(num_nodes):
            abs_distances[i] = 0.0
            for j in range(num_dims):
                abs_distances[i] += (((this_sample[j] - som_weights[i, j]) **2 ) ** .5)

    # train your SOM
    @jit(argtypes = [nd1])
    def train(self, this_sample, i):
        ''' # Pre-calculate the number of iterations (which will never be so impossibly large as to not store the indices)
        idx = np.random.randint(0, self.n_samples, (self.num_iterations,))
        # Pick a random vector
        this_sample = self.X[idx[i],:] '''

        winner_idx = 0
        winner_distance = 1.0e100
        # Figure out who's the closest weight vector (and calculate distances between weights and the sample)
        self.find_winner(self.som_weights, this_sample, self.abs_distances)
        winner_idx = np.argmin(self.abs_distances)
        # here we need to add our sample to the winner_idx in grid_links
        # Calculate the new learning rate and new learning spread
        normalized_progress = float(i) / float(self.num_iterations)
        learning_rate = self.scale(self.learning_rate_initial, self.learning_rate_final, normalized_progress)
        learning_spread = self.scale(self.learning_spread_initial, self.learning_spread_final, normalized_progress)

        # Update those weights
        self.update_weights(this_sample, self.som_weights, winner_idx, self.som_weights, learning_rate, learning_spread)

'''a = SomC()
for j in range(a.num_iterations):
    start = time.time()
    for i in range(a.n_samples):
        a.train(a.X[i], j)
    print (" 1 iteration on a %d-square grid took %f seconds" % (a.grid_size[0], time.time() - start))'''