from DuelingNetwork.model import Net
import numpy as np
import matplotlib.pyplot as plt
import gym
import random
import torch
from torch import nn
from torch import optim

from frameSave import save_frames_as_gif
from collections import namedtuple
import warnings
import time
import torch.nn.functional as F
model = torch.load("pth/cartpole.pth")
model.eval()
ENV = 'CartPole-v0'
env=gym.make(ENV)
observation = env.reset()
state=observation
state=torch.from_numpy(state).type(torch.FloatTensor)
state=torch.unsqueeze(state,0)
frames = []

for i in range(200):
    with torch.no_grad():
        model.eval()
        action=model(state).max(1)[1].view(1,1)
        observation_next, _, done, _ = env.step(
                    action.item())
        if done:
            break
        else:
            state_next = observation_next  # 관측 결과를 그대로 상태로 사용
            state_next = torch.from_numpy(state_next).type(
                        torch.FloatTensor)  # numpy 변수를 파이토치 텐서로 변환
            state_next = torch.unsqueeze(state_next, 0)
        state = state_next
    # env.render()
    frames.append(env.render(mode="rgb_array"))
    time.sleep(0.01)
    # print(i)
env.close()
save_frames_as_gif(frames,filename='CartPole.gif')
