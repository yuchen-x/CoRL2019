# Macro-Action-Based Deep Multi-Agent Reinforcement Learning

This is the code for implementing the macro-action-based decentralized learning and centralized learning frameworks presented in the paper [Macro-Action-Based Deep Multi-Agent Reinforcement Learning](https://drive.google.com/file/d/1R5bh7Hqs_Dhzz7FMmPP8TmMmk_IppcWL/view).

## Installation

- To install the anaconda virtual env with all the dependencies:
  ```
  cd Anaconda_Env/
  conda env create -f 367_corl2019_env.yml
  conda activate corl2019
  ```
- To install the python module:
  ```
  cd MacDeepMARL/
  pip install -e .
  ```
## Decentralized Learning for Decentralized Execution

The first framework presented in this paper extends [Dec-HDRQN](https://arxiv.org/pdf/1703.06182.pdf) with Double Q-learning to learn the decentralized macro-action-value function for each agent by proposing a **Macro-Action Concurrent Experience Replay Trajectories (Mac-CERTs)** to maintain macro-action-observation transitions for training.

Visualization of Mac-CERTs:

![](https://github.com/yuchen-x/CoRL2019/blob/master/images/dec_buffer.png)

A mini-batch of squeezed experience is then used for optimizing each agent's decentralized macro-action Q-net.

Training in three domains (single run):
- Capture Target
  ```
  ma_hddrqn.py --grid_dim 10 10 --env_name=CT_MA_v1 --env_terminate_step=60 --batch_size=32 --trace_len=4 --rnn_h_size=64 --train_freq=5 --total_epi=20000 --seed=0 --run_id=0 --eps_l_d --dynamic_h --rnn --save_dir=ctma_10_10 --replay_buffer_size=50000 --h_stable_at=4000 --eps_l_d_steps=4000 --l_rate=0.001 --discount=0.95 --start_train=2
  ```
- Box Pushing
  ```
  ma_hddrqn.py --grid_dim 10 10 --env_name=BP_MA --env_terminate_step=100 --batch_size=128 --rnn_h_size=32 --train_freq=14 --total_epi=15000 --seed=0 --run_id=0 --eps_l_d --dynamic_h --rnn --save_dir=bpma_10_10 --replay_buffer_size=50000 --h_stable_at=4000 --eps_l_d_steps=4000 --l_rate=0.001 --discount=0.98 --start_train=2 --trace_len=14
  ```
- Warehouse Tool Delivery
  ```
  ma_hddrqn.py --env_name=OSD_S_4 --env_terminate_step=150 --batch_size=16 --rnn_h_size=64 --train_freq=30 --total_epi=40000 --seed=0 --run_id=0 --eps_l_d --dynamic_h --rnn --save_dir=osd_single_v4_dec --replay_buffer_size=1000 --h_stable_at=6000 --eps_l_d_steps=6000 --l_rate=0.0006 --discount=1.0 --start_train=2 --sample_epi --h_explore
  ```
  
The results presented in our paper are the averaged performance over 40 runs using seeds 0-39. By specifing `--save_dir`, `--seed` and `--run_id` for each training, the correpsonding results and policies are separately saved under `/performance` and `/policy_nns` directories.

## Centralized Learning for Centralized Execution

The second framework presented in this paper extends Double-DRQN method to learn a centralized macro-action-value function by proposing a **Macro-Action Joint Experience Replay Trajectories (Mac-JERTs)** to maintain joint macro-action-observation transitions for training.

Visualization of Mac-JERTs:
<p align="center">
  <img src="https://github.com/yuchen-x/MacDeepMARL/blob/master/images/cen_buffer.png" width="70%">
</p>

A mini-batch of squeezed experience is then used for optimizing the centralized macro-action Q-net. Note that, we propose a **conditional target valaue prediction** taking into account the asynchronous macro-action executions over agents for obtaining more accurate value estimation.

Training in two domains via *conditional target prediction* (single run):

- Box Pushing
  ```
  ma_cen_condi_ddrqn.py --grid_dim 10 10 --env_name=BP_MA --env_terminate_step=100 --batch_size=128 --rnn_h_size=64 --train_freq=15 --total_epi=15000 --seed=0 --run_id=0 --eps_l_d --dynamic_h --rnn --save_dir=cen_condi_bpma_10_10 --replay_buffer_size=100000 --h_stable_at=4000 --eps_l_d_steps=4000 --l_rate=0.001 --discount=0.98 --start_train=2 --trace_len=15
  ```
- Warehouse Tool Delivery
  ```
  ma_cen_condi_ddrqn.py --env_name=OSD_S_4 --env_terminate_step=150 --batch_size=16 --rnn_h_size=128 --train_freq=30 --total_epi=40000 --seed=0 --run_id=0 --eps_l_d --dynamic_h --rnn --save_dir=osd_single_v4 --replay_buffer_size=1000 --h_stable_at=6000 --eps_l_d_steps=6000 --l_rate=0.0006 --discount=1.0 --start_train=2 --sample_epi --h_explore
  ```
Training in Box Pushing domain via *unconditional target prediction* (single run):

- Box Pushing
  ```
  ma_cen_ddrqn.py --grid_dim 10 10 --env_name=BP_MA --env_terminate_step=100 --batch_size=128 --rnn_h_size=64 --train_freq=15 --total_epi=15000 --seed=0 --run_id=0 --eps_l_d --dynamic_h --rnn --save_dir=cen_condi_bpma_10_10 --replay_buffer_size=100000 --h_stable_at=4000 --eps_l_d_steps=4000 --l_rate=0.001 --discount=0.98 --start_train=2 --trace_len=15
  ```

## How to Run the Algorithms on a New Macro-Action/Primitive-Action Based Domain

- Encode the new macro/primitve-action domain as a gym env;
- Add "obs_size", "n_action" and "action_spaces" as properties into the env class;
- Let the step function return <a, o', r, t, v> instead of <o', r, t>, where
  - a is the current macro/primitve actions indice of agents, **List[int]**; 
  - o' is the new macro/premitive observations, **List[ndarry]**; 
  - r is the reward, **float**; 
  - t is whether terminates or not, **bool**;
  - v is a binary value indicate whether each agent's macro/primitive action terminates or not, **List[int]**. In primitive-action version, v should be always 1.

## Visualization of a Trained Centralized Policy in the Warehouse Domain

Under the default Turtlebot's moving speed (v=0.6):
  ```
  cd ./test/
  python test_osd_s_policy.py
  ```
Press `c` to run a learnt centralized policy.

Run the same policy but under a higher Turtlebot's moving speed (v=0.8):
  ```
  cd ./test/
  python test_osd_s_policy.py --tbot_speed=0.8
  ```

## Code Structure
- `./scripts/ma_hddrqn.py` the main training loop for the decentralized learning method
- `./scripts/ma_cen_ddrqn.py` the main training loop for the unconditional centralized learning method 
- `./scripts/ma_cen_condi_ddrqn.py`the main training loop for the conditional centralized learning method
- `./src/rlmamr/method_name` the source code for each corresponding method
- `./src/rlmamr/method_name/team.py` the class for a team of agents with useful functions for learning
- `./src/rlmamr/method_name/learning_methods.py` core code for the algorithm
- `./src/rlmamr/method_name/env_runner.py` multi-processing for parallel envs
- `./src/rlmamr/method_name/model.py` the neural network module
- `./src/rlmamr/method_name/utils/` other useful functions
- `./src/rlmamr/my_env` code for each domain problem

## Paper Citation
If you used this code for your reasearch or found it helpful, please consider citing the following paper:
```
@InProceedings{xiao_corl_2019,
    author = "Xiao, Yuchen and Hoffman, Joshua and Amato, Christopher",
    title = "Macro-Action-Based Deep Multi-Agent Reinforcement Learning",
    booktitle = "3rd Annual Conference on Robot Learning",
    year = "2019"
}
```
