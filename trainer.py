# -*- coding: utf-8 -*-
import time
from VectorSpaceGenerator import VectorSpaceMaker
from sklearn.feature_extraction.text import CountVectorizer
import numpy
import random
from sklearn.preprocessing import normalize
from tmodels.som import SOM
import sys
import pdb
#pdb.set_trace()
from tmodels.somC import SomC


class Trainer():
    def __init__(self):
        self.vsm = VectorSpaceMaker()
        self.tobetraineddata = self.vsm.getLinksandContents()
        # It is a dictionary with links and content
        self.trainingdata = self.tobetraineddata.values()
        self.trainingdatakeys = self.tobetraineddata.keys()

    '''Training Starts here '''

    def initialize(self):
        print("Starting intialization")
        self.vectorizer = CountVectorizer(min_df=3)
        self.X = self.vectorizer.fit_transform(self.trainingdata)
        self.n_number, self.n_dim = self.X.shape
        self.n_todim = 300
        print (len(self.vectorizer.vocabulary_))
        '''transformer = random_projection.GaussianRandomProjection()
        X_new = transformer.fit_transform(X)
        print X_new.shape'''
        ''' get new shape and array size here . 2/3 columns are zeros here.'''
        rand = numpy.empty([self.n_dim, self.n_todim])
        for i in range(0, self.n_number):
            for j in range(0, self.n_todim):
                a1 = random.random()
                if a1 < 2.0 / 3:
                    rand[i, j] = 0
                elif a1 < 5.0 / 6:
                    rand[i, j] = 1
                elif a1 < 1.0:
                    rand[i, j] = -1
        # apply random projection
        rand_normalized = normalize(rand, norm='l1', axis=0)
        #print rand_normalized

        # doing random projection here
        self.final_matrix = self.X.dot(rand_normalized)
        print("Initialization Done")
        #print final_matrix
        #print final_matrix.shape


    def startTraining(self):
        ''' Here we are passing SOM mesh, dimensions of each node, Mesh dimensions '''
        print("Starting Training")
        self.som = SomC(self.final_matrix, self.n_todim, (10, 10))
        for j in range(self.som.num_iterations):
            start = time.time()
            for i in range(self.n_number):
                self.som.train(self.final_matrix[i], j)
            print (" %d iteration on a %d-square grid took %f seconds" % (j, self.som.grid_size[0], time.time() - start))
            print(self.som.som_weights)

        print(self.som.som_weights)
        print("Training Done")

    def savetoFile(self):
        numpy.save("../savedata/narray", self.som.final_matrix)

'''for i in range(1,1300):
    if len(som.getSimilarArticles(final_matrix[i,:].tolist())) > 1:
        print "DFDF" '''

'''for i in range(20):
    for j in range(20):
        print (str(i) + " " + str(j))
        try:
            for k in som.nodes[i*10+j].content:
                sys.stdout.write(trainingdatakeys[k])
                sys.stdout.write(" ")
            print ("\n")
        except:
            pass'''
#print johnson_lindenstrauss_min_dim(n_samples=1330, eps=.5) #345

tr = Trainer()
tr.initialize()
tr.startTraining()
tr.savetoFile()

