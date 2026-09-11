import pandas as pd # reading all required header files
import numpy as np
import random
import operator
import math
import matplotlib.pyplot as plt

def FuzzyMeansAlgorithm(matrix, k, d, m, MAX_ITERS):
  weight_arr = initializeMembershipWeights()
  #plt.figure(figsize=(50,50))
  for z in range(MAX_ITERS):
    C = computeCentroids(weight_arr)
    updateWeights(weight_arr,C)
    #plotData(z,C)
  #plt.show()
  return (weight_arr,C)


def initializeMembershipWeights(k, n):
  weight = np.random.dirichlet(np.ones(k),n)
  weight_arr = np.array(weight)
  return weight_arr


def computeCentroids(weight_arr, k, m, d, matrix):
  C = []
  for i in range(k):
    weight_sum = np.power(weight_arr[:,i],m).sum()
    Cj = []
    for x in range(d):
      numerator = ( df.iloc[:,x].values * np.power(weight_arr[:,i],m)).sum()
      c_val = numerator/weight_sum;
      Cj.append(c_val)
    C.append(Cj)
  return C




def updateWeights(weight_arr,C):
  denom = np.zeros(n)
  for i in range(k):
    dist = (df.iloc[:,:].values - C[i])**2
    dist = np.sum(dist, axis=1)
    dist = np.sqrt(dist)
    denom  = denom + np.power(1/dist,1/(m-1))

  for i in range(k):
    dist = (df.iloc[:,:].values - C[i])**2
    dist = np.sum(dist, axis=1)
    dist = np.sqrt(dist)
    weight_arr[:,i] = np.divide(np.power(1/dist,1/(m-1)),denom)
  return weight_arr
