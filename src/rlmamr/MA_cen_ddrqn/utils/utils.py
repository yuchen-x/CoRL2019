import torch
import os
import numpy as np
import random

class Linear_Decay(object):

    def __init__ (self, 
                  total_steps, 
                  init_value, 
                  end_value):
        """
        Parameters
        ----------
        total_steps : int
            Total decay steps.
        init_value : float
            Initial value.
        end_value : float
            Ending value
        """

        self.total_steps = total_steps
        self.init_value = init_value
        self.end_value = end_value

    def _get_value(self, step):
        frac = min(float(step) / self.total_steps, 1.0)
        return self.init_value + frac * (self.end_value-self.init_value)

def inv_joint_a(joint_a, n_actions):
    assert joint_a < np.prod(n_actions), "Out of joint_action space"
    return [joint_a % n_actions[i] if i == 0 else joint_a // np.prod(n_actions[:i]) % n_actions[i] for i in range(len(n_actions))]

def get_joint_a(a_idxes, n_actions):
    assert all(a_idx < n_actions[i] for i, a_idx in enumerate(a_idxes)), "Out of certain action space"
    return np.sum([a_idx if i == 0 else a_idx * np.prod(n_actions[:i]) for i, a_idx in enumerate(a_idxes)])

def _prune_o(obs, id_valid):

    """Given an joint experience (o,a,o',r), the element in o of Q(o,a) which is learnt 
    should be zero if the previous action is not done yet."""

    assert type(obs) is list, "Obs is not a list"
    n_agent = id_valid[0].shape[-1]
    for i in range(len(obs)):
        id_v = torch.ones_like(id_valid[i])
        id_v[1:] = id_valid[i][0:-1]
        obs[i] = id_v.view(obs[i].shape[0], n_agent, -1).float() * obs[i].view(obs[i].shape[0], n_agent, -1)
        obs[i] = obs[i].reshape(obs[i].shape[0], -1)
    return tuple(obs)

def _prune_o_n(obs, id_valid):

    """Given an experience (o,a,o',r), the element in o' of argmax_a' Q(o',a') 
    should be zero if the current action a is not done yet."""

    assert type(obs) is list, "Obs is not a list"
    n_agent = id_valid[0].shape[-1]
    for i in range(len(obs)):
        obs[i] = id_valid[i].view(obs[i].shape[0], n_agent, -1).float() * obs[i].view(obs[i].shape[0], n_agent, -1)
        obs[i] = obs[i].reshape(obs[i].shape[0], -1)
    return tuple(obs)

def _prune_filtered_o(obs, id_valid):

    """Given an joint experience (o,a,o',r), the element in o of Q(o,a) which is learnt 
    should be zero if the previous action is not done yet."""

    assert type(obs) is list, "Obs is not a list"
    n_agent = id_valid[0].shape[-1]
    for i in range(len(obs)):
        obs[i] = id_valid[i][:-1].view(obs[i].shape[0], n_agent, -1).float() * obs[i].view(obs[i].shape[0], n_agent, -1)
        obs[i] = obs[i].reshape(obs[i].shape[0], -1)
    return tuple(obs)
 
def _prune_filtered_o_n(obs, id_valid):

    """Given an experience (o,a,o',r), the element in o' of argmax_a' Q(o',a') 
    should be zero if the current action a is not done yet."""

    assert type(obs) is list, "Obs is not a list"
    n_agent = id_valid[0].shape[-1]
    for i in range(len(obs)):
        obs[i] = id_valid[i][1:].view(obs[i].shape[0], n_agent, -1).float() * obs[i].view(obs[i].shape[0], n_agent, -1)
        obs[i] = obs[i].reshape(obs[i].shape[0], -1)
    return tuple(obs)

def save_check_point(cen_controller, cur_step, n_epi, cur_hysteretic, cur_eps, save_dir, mem, run_id, test_perform, max_save=3):

    #PATH = "./performance/" + save_dir + "/check_point/" + str(run_id) + "_agent_" + str(agent.idx) + ".{}tar"
    PATH = "./performance/" + save_dir + "/check_point/" + str(run_id) + "_cen_controller_" + "{}.tar"

    for n in list(range(max_save-1, 0, -1)):
        os.system('cp -rf ' + PATH.format(n) + ' ' + PATH.format(n+1) )
    PATH = PATH.format(1)

    torch.save({
                'cur_step': cur_step,
                'n_epi': n_epi,
                'policy_net_state_dict':cen_controller.policy_net.state_dict(),
                'target_net_state_dict':cen_controller.target_net.state_dict(),
                'optimizer_state_dict':cen_controller.optimizer.state_dict(),
                'cur_hysteretic':cur_hysteretic,
                'cur_eps':cur_eps,
                'TEST_PERFORM': test_perform,
                'mem_buf':mem.buf,
                'random_state':random.getstate(),
                'np_random_state': np.random.get_state(),
                'torch_random_state': torch.random.get_rng_state()
                }, PATH)
