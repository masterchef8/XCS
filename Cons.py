class Cons:
    """ Specifies default XCS run constants. """
    def __init__(self):

        self.doGASubsumption = True
        self.doActionSetSubsumption = True
        self.alpha = 0.1   # The fall of rate in the fitness evaluation.
        self.beta = 0.1    # The learning rate for updating fitness, prediction, prediction error, and action set size estimate in XCS's classifiers.
        self.gamma = 0.95  # The discount rate in multi-step problems.
        self.delta = 0.1   # The fraction of the mean fitness of the population below which the fitness of a classifier may be considered in its vote for deletion.
        self.nu = 5       # Specifies the exponent in the power function for the fitness evaluation.
        self.theta_GA = 100  # The threshold for the GA application in an action set.
        self.theta_Select = 0.4   # Original Value as found in Butz 2002 Tournament Selection paper
        self.epsilon_0 = 20  # The error threshold under which the accuracy of a classifier is set to one.
        self.theta_del = 10  # Specified the threshold over which the fitness of a classifier may be considered in its deletion probability.
        self.pX = 0.8        # The probability of applying crossover in an offspring classifier.
        self.pM = 0.1       # The probability of mutating one allele and the action in an offspring classifier.
        self.P_dontcare = 0.3    # The probability of using a don't care symbol in an allele when covering.
        self.predictionErrorReduction = 0.25 # The reduction of the prediction error when generating an offspring classifier.
        self.fitnessReduction = 0.1  # The reduction of the fitness when generating an offspring classifier.
        self.theta_sub = 20  # The experience of a classifier required to be a subsumer.
        self.predictionIni = 10.0    # The initial prediction value when generating a new classifier (e.g in covering).
        self.predictionErrorIni = 0.0    # The initial prediction error value when generating a new classifier (e.g in covering).
        self.fitnessIni = 0.01   # The initial prediction value when generating a new classifier (e.g in covering).
        self.dontCare = '#'    # The don't care symbol (normally '#')
        self.nbAction = 4
        self.n = 1000
        self.pExplor = 0.9
