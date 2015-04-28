from scipy.io import wavfile
import numpy as np
import os
from os import path

STEPS = 4000
FACTOR = 1.2

class TwoWordRecognizer:

    def scaler(self,arr):
        return arr/np.max(np.abs(arr))*100

    def get_startingpoint(self,arr):
        arr = np.abs(arr)
        st_i = 0
        e_i = STEPS
        old_value = np.sum(arr[st_i:e_i,0])
        counter = 0
        while e_i < arr.shape[0]:
            arr_sum = np.sum(arr[st_i:e_i,0])
            if(arr_sum>old_value*FACTOR):
                return st_i
            else:
                if(old_value<arr_sum):
                    old_value = arr_sum
                st_i+=STEPS
                e_i+=STEPS
        return 10000

    def get_endingpoint(self,arr):
        arr = np.abs(arr)
        e_i = arr.shape[0]-1
        st_i = e_i - STEPS
        old_value = np.sum(arr[st_i:e_i,0])
        while st_i > 0:
            arr_sum = np.sum(arr[st_i:e_i,0])
            if(arr_sum>old_value*FACTOR):
                return e_i
            else:
                if(old_value<arr_sum):
                        old_value = arr_sum
                st_i -= STEPS
                e_i -= STEPS
        return 10000

    def euclidean_distance(self,arr1,arr2):
        a1 = arr1.copy()
        a2 = arr2.copy()
        if(a1.shape[0]<a2.shape[0]):
            zero_rows = a2[a1.shape[0]:a2.shape[0],[0,1]].copy()
            zero_rows[:,:] = 0
            a1 = np.concatenate((a1,zero_rows))
        elif(a1.shape[0]>a2.shape[0]):
            zero_rows = a1[a2.shape[0]:a1.shape[0],[0,1]].copy()
            zero_rows[:,:] = 0
            a2 = np.concatenate((a2,zero_rows))
        dist = np.sqrt((a2[:,0]-a1[:,0])**2)
        return np.sum(dist)

    def loadReferenceWords(self, word1_path, word2_path):
        fs, self.word1 = wavfile.read(word1_path)
        fs, self.word2 = wavfile.read(word2_path)
        self.word1 =  self.scaler(self.word1)
        self.word2 = self.scaler(self.word2)
        self.word1 = self.word1[self.get_startingpoint(self.word1):self.get_endingpoint(self.word1),:]
        self.word2 = self.word2[self.get_startingpoint(self.word2):self.get_endingpoint(self.word2),:]

    def loadData(self, ressourcepath1, ressourcepath2):
        print(ressourcepath1)
        dirList = os.listdir(ressourcepath1)
        fullpath1 = []
        for fname in dirList:
            fullpath1.append(ressourcepath1+""+fname)

        dirList = os.listdir(ressourcepath2)
        fullpath2 = []
        for fname in dirList:
            fullpath2.append(ressourcepath2+""+fname)
        counter = 0
        for path in fullpath1:
            if counter == 0:
                fs, w1 = wavfile.read(path)
                w1 = self.scaler(w1)
                w1 = w1[self.get_startingpoint(w1):self.get_endingpoint(w1),:]
                X = np.array([self.euclidean_distance(self.word1,w1),self.euclidean_distance(self.word2,w1)])
                y = np.array([1])
                counter = 1
            else:
                fs, w1 = wavfile.read(path)
                w1 = self.scaler(w1)
                w1 = w1[self.get_startingpoint(w1):self.get_endingpoint(w1),:]
                X = np.vstack((X,np.array([self.euclidean_distance(self.word1,w1),self.euclidean_distance(self.word2,w1)])))
                y = np.hstack((y,np.array([1])))

        for path in fullpath2:
                fs, w2 = wavfile.read(path)
                w2 = self.scaler(w2)
                w2 = w2[self.get_startingpoint(w2):self.get_endingpoint(w2),:]
                X = np.vstack((X,np.array([self.euclidean_distance(self.word1,w2),self.euclidean_distance(self.word2,w2)])))
                y = np.hstack((y,np.array([2])))
        from sklearn.neighbors.nearest_centroid import NearestCentroid
        self.clf = NearestCentroid()
        self.clf.fit(X,y)
        #import matplotlib.pyplot as plt
        #plt.scatter(X[:,0],X[:,1])
        #plt.show()

    def predict(self,input_path):
        fs, raw_arr = wavfile.read(input_path)
        raw_arr = self.scaler(raw_arr)
        word= raw_arr[self.get_startingpoint(raw_arr):self.get_endingpoint(raw_arr),:]
        x0 = np.array([self.euclidean_distance(self.word1,word),self.euclidean_distance(self.word2,word)])
        return self.clf.predict(x0)
