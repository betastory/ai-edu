import numpy as np
import copy

# 式 (9.6.1) 计算 q，假设已知 v*(s')
def q_star(p_s_r, gamma, V):
    q = 0
    # 遍历每个转移概率,以计算 q
    for p, s_next, r in p_s_r:
        # math: \sum_{s'} p_{ss'}^a [ r_{ss'}^a + \gamma *  v_{\pi}(s')]
        q += p * (r + gamma * V[s_next])
    return q

# 式 (9.6.3) 计算 v*
def v_star(s, actions, gamma, V, Q):
    list_q = []                     # 准备列表记录所有下游的 q*
    for a, p_s_r in actions:        # 遍历每个动作以计算q值，进而计算v值
        q = q_star(p_s_r, gamma, V) # 计算 q*
        list_q.append(q)            # 加入列表
        Q[s,a] = q                  # 记录下所有的q(s,a)值,不需要再单独计算一次
    return max(list_q)              # 返回几个q*中的最大值,即 v=max(q)

def calculate_VQ_star(env, gamma, max_iteration):
    V = np.zeros(env.nS)
    Q = np.zeros((env.nS, env.nA))
    count = 0
    # 迭代
    while (count < max_iteration):
        V_old = V.copy()
        # 遍历所有状态 s
        for s in range(env.nS):
            if env.is_end(s):   # 终止状态v=0
                continue            
            # 获得 状态->动作 策略概率
            actions = env.get_actions(s)
            V[s] = v_star(s, actions, gamma, V, Q)
        # 检查收敛性
        if abs(V-V_old).max() < 1e-4:
            break
        count += 1
    # end while
    print("迭代次数 = ",count)
    return V, Q

def get_policy(env, V, gamma):
    policy = np.zeros((env.nS, env.nA))    
    for s in range(env.nS):
        actions = env.get_actions(s)
        list_q = []
        if actions is None:
            continue
        # 遍历每个策略概率
        for action, next_p_s_r in actions:
            q_star = 0
            for p, s_next, r in next_p_s_r:
                q_star += p * (r + gamma * V[s_next])
            list_q.append(q_star)
        policy[s, np.argmax(list_q)] = 1
    return policy

