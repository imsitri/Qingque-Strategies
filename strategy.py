from enum import Enum
import numpy as np
import qingque_probability as prob
import json as json

f = open('qingque_skill_probability.json', 'r')
data = json.loads(f.read())
f.close()

class Action(Enum):
    BASIC = 1
    SKILL = 2
    ULT = 3
    END = 4

def skill_spam_fold_at_5(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
        if len(action_dict[list(action_dict.keys())[-1]]) < 5 or action_dict[list(action_dict.keys())[-1]][-3:] != [Action.SKILL, Action.SKILL, Action.SKILL, Action.SKILL, Action.SKILL]:
            return Action.SKILL
    if qingque.energy >=140:
        return Action.ULT
    return Action.BASIC

def skill_spam_fold_at_4(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
        if len(action_dict[list(action_dict.keys())[-1]]) < 4 or action_dict[list(action_dict.keys())[-1]][-3:] != [Action.SKILL, Action.SKILL, Action.SKILL, Action.SKILL]:
            return Action.SKILL
    if qingque.energy >=140:
        return Action.ULT
    return Action.BASIC

def skill_spam_fold_at_3(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
        if len(action_dict[list(action_dict.keys())[-1]]) < 3 or action_dict[list(action_dict.keys())[-1]][-3:] != [Action.SKILL, Action.SKILL, Action.SKILL]:
            return Action.SKILL
    if qingque.energy >=140:
        return Action.ULT
    return Action.BASIC

'''
Early ult (after skill). Look for >50% chance of succeess with current SP
'''
def probability_50(current_SP, qingque, enemy_count = 1, action_dict = None):
    key = len(qingque.hand) * 1000 + prob.hand_check(qingque.hand)*100 + int(current_SP)*10
    if key < 1000:
        p = 0
    else:
        p = data[str(key)]
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if p >= 0.5:
        if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
            return Action.SKILL
    if qingque.energy >= 140:
        return Action.ULT
    return Action.BASIC

'''
Early ult (after skill). Look for >40% chance of succeess with current SP
'''
def probability_40(current_SP, qingque, enemy_count = 1, action_dict = None):
    key = len(qingque.hand) * 1000 + prob.hand_check(qingque.hand)*100 + int(current_SP)*10
    if key < 1000:
        p = 0
    else:
        p = data[str(key)]
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if p >= 0.4:
        if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
            return Action.SKILL
    if qingque.energy >= 140:
        return Action.ULT
    return Action.BASIC

'''
Late ult (after basic). Look for >40% chance of succeess with current SP
'''
def probability_40_late_ult(current_SP, qingque, enemy_count = 1, action_dict = None):
    key = len(qingque.hand) * 1000 + prob.hand_check(qingque.hand)*100 + int(current_SP)*10
    if key < 1000:
        p = 0
    else:
        p = data[str(key)]
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC and qingque.energy >=140:
        return Action.ULT
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.ULT:
        return Action.END
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if p >= 0.4:
        if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
            return Action.SKILL
    return Action.BASIC

'''
Early ult (after skill). Look for >30% chance of succeess with current SP
'''
def probability_30(current_SP, qingque, enemy_count = 1, action_dict = None):
    key = len(qingque.hand) * 1000 + prob.hand_check(qingque.hand)*100 + int(current_SP)*10
    if key < 1000:
        p = 0
    else:
        p = data[str(key)]
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if p >= 0.3:
        if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
            return Action.SKILL
    if qingque.energy >= 140:
        return Action.ULT
    return Action.BASIC

'''
Early ult (before skill), random skill/basic use. End after Basic
'''
def random(current_SP, qingque, enemy_count = 1, action_dict = None):
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
def skill_spam(current_SP, qingque, enemy_count = 1, action_dict = None):
    if len(action_dict[list(action_dict.keys())[-1]]) > 0 and action_dict[list(action_dict.keys())[-1]][-1] == Action.BASIC:
        return Action.END
    if current_SP >= 1 and prob.hand_check(qingque.hand) != 4:
        return Action.SKILL
    if qingque.energy >=140:
        return Action.ULT
    return Action.BASIC
        

def safe(current_SP, qingque, enemy_count=1, action_dict = None):
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



    