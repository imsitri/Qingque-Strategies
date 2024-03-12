from enum import Enum
import numpy as np
import qingque_probability as prob

class Action(Enum):
    BASIC = 1
    SKILL = 2
    ULT = 3
    END = 4
'''
Early ult (before skill), random skill/basic use. End after Basic
'''
def random_strategy(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if qingque.energy >= 140:
        return Action.ULT
    else:
        if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
            return np.random.choice([Action.BASIC, Action.SKILL], 1)
        else:
            return Action.BASIC
    
'''
Early ult (after skill), Spam Skill. End after Basic
'''        
def skill_spam_strategy(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
        return Action.SKILL
    if qingque.energy >=140:
        return Action.ULT
    return Action.BASIC
        

def safe_strategy(current_SP, qingque, enemy_count=1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if qingque.energy >= 140:
        if current_SP >=1 :
            return Action.SKILL
        else:
            return Action.ULT
    else:
        return Action.BASIC

'''
Early ult (after skill), Spam Skill if there is 2 of a kind or more. End after Basic
'''   
def one_of_a_kind_averse(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if prob.hand_check(qingque.hand) > 1:
        if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
            return Action.SKILL
        if qingque.energy >= 140:
            return Action.ULT
    return Action.BASIC


'''
Early ult (after skill), Spam Skill if there is 3 of a kind or more. End after Basic
'''   
def two_of_a_kind_averse(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if prob.hand_check(qingque.hand) > 2:
        if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
            return Action.SKILL
        if qingque.energy >= 140:
            return Action.ULT
    return Action.BASIC

'''
Late ult (after basic), Spam Skill. End after Ult
'''     
def skill_spam_ult_late(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC and qingque.energy >=140:
        return Action.ULT
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.ULT:
        return Action.END
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
        return Action.SKILL
    else:
        return Action.BASIC