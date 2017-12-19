#! python 
# @Time    : 17-12-19
# @Author  : kay
# @File    : SarsaAndQ_Learning.py
# @E-mail  : 861186267@qq.com
# @Function:

import pandas as pd
import numpy as np


class ReinforceLearning(object):
    def __init__(self, actions, lr, gamma, epsilon):
        '''
        :param action: the action
        :param lr: learning rate
        :param gamma: the rewarding decay
        :param epilon: the e-greedy
        '''
        self.actions = actions
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon

        self.table = pd.DataFrame(columns=self.actions)

    def check_state_exits(self, state):
        if state not in self.table.index:
            self.table = self.table.append(pd.Series([0] * len(self.actions), index=self.table.columns, name=state))

    def choose_action(self, observation):
        self.check_state_exits(observation)

        if np.random.rand() < self.epsilon:
            state_actions = self.table.ix[observation, :]
            state_actions = state_actions.reindex(np.random.permutation(state_actions.index))
            action = state_actions.argmax()
        else:
            action = np.random.choice(self.actions)

        return action

    def learn(self, *args):
        pass


# on-policy, a greedy policy
class Sarsa(ReinforceLearning):
    '''
    The basic class is ReinforceLearning
    '''

    def __init__(self, actions, lr=0.1, gamma=0.9, epsilon=0.9):
        super(Sarsa, self).__init__(actions=actions, lr=lr, gamma=gamma, epsilon=epsilon)

    def learn(self, s, a, r, s_, a_):
        '''
        :param s: current state
        :param a: current action
        :param r: rewarding
        :param s_: next state
        :param a_: next action
        :return: 
        '''
        self.check_state_exits(s_)
        self.prediction = self.table.ix[s, a]
        if s_ != 'terminal':
            target = r + self.gamma * self.table.ix[s_, a_]  # next state is not terminal
        else:
            target = r  # next state is terminal

        self.table.ix[s, a] += self.lr * (target - self.prediction)


# off-policy
class Q_Learning(ReinforceLearning):
    '''
    The basic class is ReinforceLearning
    '''

    def __init__(self, actions, lr=0.1, gamma=0.9, epsilon=0.9):
        super(Q_Learning, self).__init__(actions=actions, lr=lr, gamma=gamma, epsilon=epsilon)

    def learn(self, s, a, r, s_):
        self.check_state_exits(s_)
        self.prediction = self.table.ix[s, a]

        if s_ != 'terminal':
            # get the maximum at s_ no matter which action it's
            target = r + self.gamma * self.table.ix[s_, :].max()
        else:
            target = r
        self.table.ix[s, a] += self.lr * (target - self.prediction)
