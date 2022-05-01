import os
import sys
import pathlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import copy

from pymdp.agent import Agent
from pymdp import utils
from pymdp.envs import TMazeEnv


def plot_beliefs(belief_dist, title=""):
    plt.grid(zorder=0)
    plt.bar(range(belief_dist.shape[0]), belief_dist, color='r', zorder=3)
    plt.xticks(range(belief_dist.shape[0]))
    plt.title(title)
    plt.show()


def plot_likelihood(A, title=""):
    ax = sns.heatmap(A, cmap="OrRd", linewidth=2.5)
    plt.xticks(range(A.shape[1]))
    plt.yticks(range(A.shape[0]))
    plt.title(title)
    plt.show()




