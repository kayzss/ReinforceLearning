#! python 
# @Time    : 17-12-19
# @Author  : kay
# @File    : run.py
# @E-mail  : 861186267@qq.com
# @Function:

from environment import MAZE
from SarsaAndQ_Learning import *


def update():
    for epoch in range(200):
        observation = env.reset()
        action = RL.choose_action(str(observation))

        while True:
            # refresh env
            env.render()

            # take action and get next observation and reward
            observation_, reward, done = env.step(action)

            action_ = RL.choose_action(str(observation_))
            RL.learn(str(observation), action, reward, str(observation_), action_)

            action = action_
            observation = observation_

            if done:
                break


if __name__ == '__main__':
    env = MAZE()
    RL = Sarsa(actions=list(range(env.n_actions)))
    env.after(100, update)
    env.mainloop()
