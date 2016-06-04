# coding=utf-8
"""
@author : somebody
@date : 03/06/16

@project : XCS
@file : Classifier

@Class description :
"""

import Cons
from random import random
cons = Cons.Cons()

class Classifier():
    def __init__(self):
        self.condition = []
        self.action = 0
        self.prediction = 0.0
        self.predictionError = 0.0
        self.fitness = 0.0
        self.numerosity = 1.0
        self.experience = 0.0
        self.actionSetSize = 1.0
        self.timeStamp = 0.0


    def __str__(self):
        """ the string represetation of the classifier
        used for printin purposed (usefull for debugin) """
        return str(self.condition) + "\t" + str(self.action) + "\t" + str(self.prediction) + "\t" + str(
            self.predictionError) + "\t" + str(self.fitness) + "\t" + str(self.numerosity) + "\t" + str(
            self.experience) + "\t" + str(self.actionSetSize) + "\t" + str(self.timeStamp)

    def createRandomAction(self, numberOfActions):
        """ Creates a random action.
        @param numberOfActions The number of actions to chose from.
        NOT USED IN CURRENT IMPLEMENTAION """
        action = int(random() * numberOfActions)

    def classifierSetVariables(self, setSize, time):
        """ Sets the initial variables of a new classifier.
        @param setSize The size of the set the classifier is created in.
        @param time The actual number of instances the XCS learned from so far. """

        self.prediction = cons.predictionIni
        self.predictionError = cons.predictionErrorIni
        self.fitness = cons.fitnessIni

        self.numerosity = 1
        self.experience = 0
        self.actionSetSize = setSize
        self.timeStamp = time

    def equals(self, cl):
        """ Returns if the two classifiers are identical in condition and action.
        @param cl The classifier to be compared. """

        if cl.condition == self.condition:
            if cl.action == self.action:
                return True
        return False

    def isMoreGeneral(self, cl):
        """ Returns if the classifier is more general than cl. It is made sure that the classifier is indeed more general and
        not equally general as well as that the more specific classifier is completely included in the more general one (do not specify overlapping regions)
        :param cl: The classifier that is tested to be more specific. """

        ret = False
        length = len(self.condition)
        for i in range(length):
            if self.condition[i] != cons.dontCare and self.condition[i] != cl.condition[i]:
                return False
            elif self.condition[i] != cl.condition[i]:
                ret = True
        return ret

    def getDelProp(self, meanFitness):
        vote = self.actionSetSize * self.numerosity

        if self.experience > cons.theta_del and self.fitness / self.numerosity < cons.delta * meanFitness:
            vote = vote * meanFitness / (self.fitness / self.numerosity)
        return vote

    def subsumes(self, cl):
        """ Returns if the classifier subsumes cl.
        :param cl : The new classifier that possibly is subsumed. """

        if cl.action == self.action:
            if self.isSubsumer() and self.isMoreGeneral(cl):
                return True
        return False

    def isSubsumer(self):
        """ Returns if the classifier is a possible subsumer. It is affirmed if the classifier
        has a sufficient experience and if its reward prediction error is sufficiently low.  """

        if self.experience > cons.theta_sub and self.predictionError < cons.epsilon_0:
            return True
        return False

    def getAccuracy(self):
        """ Returns the accuracy of the classifier.
        The accuracy is determined from the prediction error of the classifier using Wilson's
        power function as published in 'Get Real! XCS with continuous-valued inputs' (1999) """

        if self.predictionError <= cons.epsilon_0:
            accuracy = 1.0
        else:
            accuracy = cons.alpha * ((self.predictionError / cons.epsilon_0) ** (-cons.nu))

        return accuracy