import copy
import random as rd
from Classifier import Classifier
import Interface
import Cons
import matplotlib.pyplot as plt



def run_exp(pop):
    """

    :param pop:
    :return:
    """


def does_match(cl, perception):
    for i in range(len(cl.condition)):
        if cl.condition[i] != cons.dontCare and cl.condition[i] != perception[i]:
            return False
    return True


def generate_covering_classifier(env, action):
    newcl = Classifier()
    newcl.condition = ['0'] * len(env)

    for i in range(len(env)):
        if rd.random() < cons.P_dontcare:
            newcl.condition[i] = cons.dontCare
        else:
            newcl.condition[i] = env[i]
    for i in range(len(action)):
        if action[i] is False:
            newcl.action = i
    newcl.prediction = cons.predictionIni
    newcl.predictionError = cons.predictionErrorIni
    newcl.fitness = cons.fitnessIni
    newcl.experience = 0
    newcl.timeStamp = time
    newcl.actionSetSize = 1
    newcl.numerosity = 1
    return newcl


def delete_from_population(Pop):
    sum = 0
    sum1 = 0
    for c in Pop:
        sum += c.numerosity
        sum1 += c.fitness

    if sum <= cons.n:
        return None
    avFitnessInPopulation = sum / sum1
    voteSum = 0

    for c in Pop:
        voteSum = voteSum + c.getDelProp(avFitnessInPopulation)

    choicePoint = rd.random() * voteSum
    voteSum = 0
    for c in Pop:
        voteSum = voteSum + c.getDelProp(avFitnessInPopulation)
        if voteSum > choicePoint:
            if c.numerosity > 1:
                c.numerosity -= 1
            else:
                Pop.remove(c)
            return None


def gen_match_set(Pop: list, perception: list):
    """
    :param Pop:
    :param perception:
    :return: list
    """
    m = []

    action = [False]*4
    while True:
        m = []
        for cl in Pop:
            if does_match(cl, perception):
                m.append(cl)
                action[cl.action] = True
        for i in range(cons.nbAction):
            pass
        if action != [True] * cons.nbAction:
            newCL = generate_covering_classifier(perception, action)
            Pop.append(newCL)
            delete_from_population(Pop)
            m = None
        if m is not None:
            break
    return m


def gen_prediction_array(M):
    """

    :type M: List
    """
    pa = [0.0] * cons.nbAction
    fitSum = [0.0] * cons.nbAction

    for cl in M:
        if pa[cl.action] is None:
            pa[cl.action] = cl.prediction * cl.fitness
        else:
            pa[cl.action] = pa[cl.action] + cl.prediction * cl.fitness
        fitSum[cl.action] = fitSum[cl.action] + cl.fitness
    for i in range(cons.nbAction):
        if fitSum[i] != 0.0:
            pa[i] /= fitSum[i]
    return pa


def select_action(pa):
    best_action = 0.0
    if rd.random() < cons.pExplor:
        best_action = rd.choice(pa)

    else:
        for i in range(len(pa)):
            if best_action < pa[i]:
                best_action = pa[i]

    for i in range(len(pa)):
        if best_action == pa[i]:
            best_action = i
    return best_action


def gen_action_set(M, act):
    action_set = []
    for cl in M:
        if cl.action == act:
            action_set.append(cl)
    return action_set


def select_offspring(A):
    """

    :param A:
    :return:
    """
    fitnessSum = 0
    for cl in A:
        fitnessSum += cl.fitness
    choicePoint = rd.random() * fitnessSum
    fitnessSum = 0
    for cl in A:
        fitnessSum = fitnessSum + cl.fitness
        if fitnessSum > choicePoint:
            return cl


def apply_crossover(cl1, cl2):
    #assert (cl1 is type(Classifier)), "Wrong argument for apply_crossover"
    #assert (cl2 is type(Classifier)), "Wrong argument for apply_crossover"
    """
    :type cl1: Classifier
    :param cl1:
    :param cl2:
    :return:
    """
    # noinspection PyTypeChecker
    x = rd.random() * len(cl1.condition) + 1
    # noinspection PyTypeChecker
    y = rd.random() * len(cl1.condition) + 1

    if x > y:
        tmp = x
        x = y
        y = x
    i = 0
    while True:
        if x <= i < y:
            tp = cl1.condition[i]
            cl1.condition[i] = cl2.condition[i]
            cl2.condition[i] = tp
        i += 1
        if i < y:
            break

def apply_mutation(cl, perception):
    """
    :type cl: Classifier
    :param cl:
    :type perception: list
    :param perception:
    :return:
    """
    for i in range(len(cl.condition)):
        if rd.random() < cons.nu:
            if cl.condition[i] == cons.dontCare:
                cl.condition[i] = perception[i]
            else:
                cl.condition[i] = cons.dontCare
    if rd.random() < cons.nu:
        c = rd.choice([i for i in range(0,(cons.nbAction-1))])
        cl.action = c

def insert_in_population(cl, Pop):
    for c in Pop:
        if c.equals(c):
            c.numerosity += 1
            return
    P.append(cl)

def run_ga(A, Pop, env):
    sumNum = 0
    sumTSN = 0
    for cl in A:
        sumTSN += cl.timeStamp * cl.numerosity
        sumNum += cl.numerosity
    if (time - sumTSN) / sumNum > cons.theta_GA:
        for cl in A:
            cl.timeStamp = time
        parent1 = select_offspring(A)
        parent2 = select_offspring(A)

        child1 = copy.copy(parent1)
        child2 = copy.copy(parent2)

        child1.numerosity += 1
        child2.numerosity += 1

        child1.experience += 0
        child2.experience += 0

        if rd.random() < cons.pX:
            apply_crossover(child1,child2)
            child1.prediction = (parent1.prediction + parent2.prediction) / 2
            child1.predictionError = (parent1.predictionError + parent2.predictionError) / 2

            child1.fitness = (parent1.fitness + parent2.fitness) / 2

            child2.prediction = child1.prediction
            child2.predictionError = child1.predictionError
            child2.fitness = child1.fitness

            child1.fitness *= 0.1
            child2.fitness *= 0.1

            apply_mutation(child1, env)
            apply_mutation(child2, env)
            if cons.doGASubsumption:
                if child1.subsumes(parent1):
                    parent1.numerosity += 1
                elif child1.subsumes(parent2):
                    parent2.numerosity += 1
                else:
                    insert_in_population(child1, Pop)
            else:
                insert_in_population(child1, Pop)
            if cons.doGASubsumption:
                if child2.subsumes(parent1):
                    parent1.numerosity += 1
                elif child2.subsumes(parent2):
                    parent2.numerosity += 1
                else:
                    insert_in_population(child2, Pop)
            else:
                insert_in_population(child2, Pop)
            delete_from_population(Pop)


def update_fitness(A):
    assert (type(A) == list), 'expected List got'
    accurancySum = 0
    k = [0] * len(A)
    for i in range(len(A)):
        if A[i].predictionError < cons.epsilon_0:
            k[i] = 1
        else:
            k[i] = cons.alpha * ((A[i].predictionError / cons.epsilon_0) ** (-cons.nu))
        accurancySum = accurancySum + k[i] * A[i].numerosity
    for i in range(len(A)):
        A[i].fitness = A[i].fitness + cons.beta * (k[i] * A[i].numerosity / accurancySum - A[i].fitness)


def do_action_set_subsumption(A, Pop):
    subsumer = None
    for cl in A:
        if cl.isSubsumer():
            if subsumer is None or cl.isMoreGeneral(subsumer):
                subsumer = cl
    # If a subsumer was found, subsume all more specific classifiers in the action set
    if subsumer != None:
        for cl in A:
            if subsumer.isMoreGeneral(cl):
                subsumer.numerosity += cl.numerosity
                A.remove(cl)
                Pop.remove(cl)


def update_set(A, p, Pop):
    sumNum = 0
    for cl in A:
        sumNum += cl.numerosity
    for cl in A:
        cl.experience += 1
        # Update prediction cl.prediction
        if cl.experience < 1 / cons.beta:
            cl.prediction = cl.prediction + (p - cl.prediction) / cl.experience
        else:
            cl.prediction = cl.prediction + cons.beta * (p - cl.prediction)

        # update prediction error cl.experience
        if cl.experience < 1 / cons.beta:
            cl.predictionError += (abs(p - cl.prediction) - cl.predictionError) / cl.experience
        else:
            cl.predictionError += cons.beta * (abs(p - cl.prediction) - cl.predictionError)

        # update action set size estimate

        if cl.experience < 1 / cons.beta:
            cl.actionSetSize = cl.actionSetSize * (sumNum - cl.actionSetSize) / cl.experience
        else:
            cl.actionSetSize += cons.beta * (sumNum - cl.actionSetSize)

    update_fitness(A)
    if cons.doActionSetSubsumption:
        do_action_set_subsumption(A, Pop)


if __name__ == '__main__':
    print("Hello")
    perf = []
    perfFitness = []
    perfClasseur = []
    rwd = 0
    M = []
    Pop = []
    PA = []
    act = None
    env = Interface.Maze()
    perception_ = None
    A_ = None
    p = None
    p_ = None
    cons = Cons.Cons()
    time = 0
    bool = True
    while bool:
        perception = env.perception
        M = gen_match_set(Pop, perception)
        PA = gen_prediction_array(M)
        act = select_action(PA)
        A = gen_action_set(M, act)
        p = env.execute_action(act)

        if A_ is not None:
            # noinspection PyUnresolvedReferences
            P = p_ + cons.gamma * max(PA)
            update_set(A_, P, Pop)
            run_ga(A_, Pop, perception_)

        if env.eop():
            P = p
            update_set(A, P, Pop)
            run_ga(A, Pop, perception)
            A_ = None
            env.stop()
        else:
            A_ = A
            p_ = p
            perception_ = perception

        time += 1
        print(time)
        if time == 10000:
            bool = False

        if time % 1 == 0:
            perfClasseur.append(len(Pop))
            m = 0
            for cl in Pop:
                m += cl.getAccuracy()
            m /= len(Pop)
            perfFitness.append(m)

        if bool is False:
            break

    for cl in Pop:
        print(cl.condition, '', cl.action, '', cl.prediction, ',', cl.predictionError, cl.fitness)
    print(len(perf))
    print(len(Pop))
    print(perfClasseur)
    print(perfFitness)

    plt.plot(perfClasseur)
    plt.ylabel('Numbers of Classifier')
    plt.xlabel('Time')
    plt.show()

    plt.plot(perfFitness)
    plt.ylabel('Quality q')
    plt.xlabel('Time')
    plt.show()
