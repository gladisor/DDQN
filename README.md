# Reinforcement Learning Applied To Metamaterial Design

<p>Our aim in this research is to use reinforcement learning to design a broadband acoustic cloak through inverse design. For more information on the project you can view our presentations:</p>

* [MLSE 2020 Submission](https://www.mlse2020.com/posters/engineering-7)

* [Youtube video](https://www.youtube.com/watch?v=K_QukLcNlUM&feature=emb_logo)

## Demo

<p>These are examples of episodes of the trained DDPG (left) and DDQN (right) algorithms controling the positioning of 4 cylinder from a random configuration to one which produces low TSCS. Both algorithms were trained for 8000 episodes to minimize the root mean square (RMS) of TSCS across a range of wavenumbers from 0.45-0.35 ka.</p>
<p align="center">
	<img src="https://github.com/gladisor/TSCSProject/blob/master/images/ddpg4cyl0.45-0.35-8000decay.gif" width="300">
	<img src="https://github.com/gladisor/TSCSProject/blob/master/images/ddqn4cyl0.45-0.35-8000decay.gif" width="300">
</p>

## Example usage

```
from tscsRL.environments.TSCSEnv import ContinuousTSCSEnv
from tscsRL.agents import ddpg

env = ContinuousTSCSEnv(
	nCyl=2,
	kMax=0.45,
	kMin=0.35,
	nFreq=11,
	stepSize=0.5)

params = ddpg.default_params()
params['save_every'] = 100
params['decay_timesteps'] = 100
params['num_episodes'] = 120
params['noise_scale'] = 1.1
params['save_data'] = False
params['use_wandb'] = True

name = 'test_ddpg'

agent = ddpg.DDPGAgent(
	env.observation_space, 
	env.action_space, 
	params, 
	name)

agent.learn(env)	
```

## Diagrams of training loops

<h3>DDPG:</h3>
<p align="center">
	<img src="https://github.com/gladisor/TSCSProject/blob/master/images/DDPG.png">
</p>

<h3>DDQN:</h3>
<p align="center">
	<img src="https://github.com/gladisor/TSCSProject/blob/master/images/DDQN.png">
</p>

## Credits
Images:
[Linwei Zhou](https://github.com/DiuLaMaX)

Inspiration for structuring agents:
[Ray](https://github.com/ray-project/ray)
