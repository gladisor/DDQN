from tscsRL.environments.TSCSEnv import ContinuousTSCSEnv, DiscreteTSCSEnv
from tscsRL.environments.GradientTSCSEnv import ContinuousGradientTSCSEnv, DiscreteGradientTSCSEnv
from tscsRL.environments.RadiiTSCSEnv import ContinuousRadiiTSCSEnv, DiscreteRadiiTSCSEnv
from tscsRL.agents import ddpg, ddqn
from tscsRL import utils
import imageio
import torch

## Name of the run we want to evaluate
name = 'ddqnRigidRadii_19cyl'

path = 'results/' + name
env_params = utils.jsonToDict(path + '/env_params.json')
agent_params = utils.jsonToDict(path + '/agent_params.json')

## Change this environment to whatever one you need
# env = DiscreteGradientTSCSEnv(
# 	nCyl=env_params['nCyl'],
# 	kMax=env_params['kMax'],
# 	kMin=env_params['kMin'],
# 	nFreq=env_params['nFreq'],
# 	stepSize=env_params['stepSize'])

env = DiscreteRadiiTSCSEnv(
	kMax=env_params['kMax'],
	kMin=env_params['kMin'],
	nFreq=env_params['nFreq'])

## Make sure these parameters are set from the env_params
env.ep_len = env_params['ep_len']
env.grid_size = env_params['grid_size']
# env.grid_size = 7

## Change this to the correct agent you want to evaluate
agent = ddqn.DDQNAgent(
	env.observation_space,
	env.action_space,
	agent_params,
	name)

## Set exploration rate to low amount
agent.epsilon = 0.05
# agent.noise_scale = 0.02

## Load weights, specify checkpoint number
agent.load_checkpoint(path + '/checkpoints/', 2400)

## For creating a video of the episode
writer = imageio.get_writer(name + '.mp4', format='mp4', mode='I', fps=15)

## THIS WHOLE BLOCK IS THE INTERACTION LOOP

## Starting from a random config
state = env.reset()
## End starting from random config

## Starting from a predefined config
# env.config = torch.tensor([[-4.9074,  3.9546,  2.6997,  0.7667,  0.6999,  4.5946,  4.9415, -0.2377]])
# env.counter = torch.tensor([[0.0]])
# env.setMetric(env.config)

# env.info['initial'] = env.RMS.item()
# env.info['lowest'] = env.info['initial']
# env.info['final'] = None
# env.info['score'] = 0
# state = env.getState()
## End starting from random config

done = False

results = {
		'radii': [],
		'rms': [],
		'tscs': []}

while not done:
	results['radii'].append(env.radii)
	results['rms'].append(env.RMS)
	results['tscs'].append(env.TSCS)

	img = env.getIMG(env.radii)
	writer.append_data(img.view(env.img_dim).numpy())

	action = agent.select_action(state)
	nextState, reward, done, info = env.step(action)

	print(env.RMS.item(), done)
	state = nextState

## Initial stuff
initialConfig = results['radii'][0]
initialRMS = results['rms'][0]
initialTSCS = results['tscs'][0]

## Optimal stuff
minIdx = results['rms'].index(min(results['rms']))
optimalConfig = results['radii'][minIdx]
optimalRMS = results['rms'][minIdx]
optimalTSCS = results['tscs'][minIdx]

print('RESULTS:')
print(f'Initial radii: {initialConfig}')
print(f'Initial RMS: {initialRMS}')
print(f'Initial TSCS: {initialTSCS}')
print()
print(f'Min radii: {optimalConfig}')
print(f'Min rms: {optimalRMS}')
print(f'Min tscs: {optimalTSCS}')

writer.close()
