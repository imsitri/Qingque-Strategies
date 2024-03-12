import numpy as np
import json
from multiprocessing import Process, Manager

suit = ['Wan', 'Tong', 'Tiao']

# check hand type (1/2/3/4 of a kind)
def hand_check(hand):
    unique, counts = np.unique(hand, return_counts= True)
    if (len(hand) == 0):
        return 0
    if len(hand) == 1:
        return 1
    if len(hand) == 2:
        return 3-len(unique)
    if len(hand) == 3:
        return 4-len(unique)
    if len(hand) == 4:
        if len(unique) == 1:
            return 4
        for count in counts:
            if count >= 3:
                return 3
        for count in counts:
            if count >= 2:
                return 2
        return 1

# i dont want to type count_zero
def count_tile(hand, tile):
    return np.count_nonzero(hand == tile)

# i dont want to write a loop every time
def remove(hand, tile):
    index = np.argwhere(hand == tile)
    hand = np.delete(hand, index[0])
    return hand
            

# i implement this according to Mihoyo's logic, dont @ me
def draw(hand):
    if len(hand) < 4:
        hand = np.append(hand, np.random.choice(suit,1))
        return hand
        
    if hand_check(hand) == 4:
        return hand
        
    hand = np.append(hand, np.random.choice(suit,1))
    # if Wan >= 2
    if count_tile(hand, 'Wan') >= 2 and len(hand) == 5:
        if count_tile(hand, 'Tong') == 0:
            if count_tile(hand, 'Wan') > count_tile(hand, 'Tiao'):
                hand = remove(hand, 'Tiao')
            else:
                hand = remove(hand, 'Wan')

        elif count_tile(hand, 'Tiao') == 0:
            if count_tile(hand, 'Wan') > count_tile(hand, 'Tong'):
                hand = remove(hand, 'Tong')
            else:
                hand = remove(hand, 'Wan')

        if count_tile(hand, 'Tong') >= 1 and count_tile(hand, 'Tiao') >= 1:
            if count_tile(hand, 'Tong') > count_tile(hand, 'Tiao'):
                hand =remove(hand, 'Tiao')
            elif count_tile(hand, 'Tiao') > count_tile(hand, 'Tong'):
                    hand =remove(hand, 'Tong')
            else:
                # 50/50 chance
                rand = np.random.choice([0,1])
                if (rand == 0):
                    hand = remove(hand, 'Tiao')
                else:
                    hand = remove(hand, 'Tong')

    # if Tong >=2
    if count_tile(hand, 'Tong') >= 2 and len(hand) == 5:
        if count_tile(hand, 'Wan') == 0:
            if count_tile(hand, 'Tong') > count_tile(hand, 'Tiao'):
                hand = remove(hand, 'Tiao')
            else:
                hand = remove(hand, 'Tong')

        elif count_tile(hand, 'Tiao') == 0:
            if count_tile(hand, 'Wan') > count_tile(hand, 'Tong'):
                hand = remove(hand, 'Tong')
            else:
                hand = remove(hand, 'Wan')

        if count_tile(hand, 'Wan') >= 1 and count_tile(hand, 'Tiao') >= 1:
            if count_tile(hand, 'Wan') > count_tile(hand, 'Tiao'):
                 hand = remove(hand, 'Tiao')
            elif count_tile(hand, 'Tiao') > count_tile(hand, 'Wan'):
                hand = remove(hand, 'Wan')
            else:
                # 50/50 chance
                rand = np.random.choice([0,1])
                if (rand == 0):
                    hand = remove(hand, 'Tiao')
                else:
                    hand = remove(hand, 'Wan')
            
    # if Tiao >=2
    if count_tile(hand, 'Tiao') >= 2 and len(hand) == 5:

        if count_tile(hand, 'Wan') == 0:
            if count_tile(hand, 'Tong') > count_tile(hand, 'Tiao'):
                hand = remove(hand, 'Tiao')
            else:
                hand = remove(hand, 'Tong')

        elif count_tile(hand, 'Tong') == 0:
            if count_tile(hand, 'Wan') > count_tile(hand, 'Tiao'):
                hand = remove(hand, 'Tiao')
            else:
               hand = remove(hand, 'Wan')

        if count_tile(hand, 'Wan') >= 1 and count_tile(hand, 'Tong') >= 1:
            if count_tile(hand, 'Wan') > count_tile(hand, 'Tong'):
                hand = remove(hand, 'Tong')
            elif count_tile(hand, 'Tong') > count_tile(hand, 'Wan'):
                hand = remove(hand, 'Wan')
            else:
                # 50/50 chance
                rand = np.random.choice([0,1])
                if (rand == 0):
                    hand = remove(hand, 'Tong')
                else:
                    hand = remove(hand, 'Wan')       
    return hand  
        

''' 
Random sampling hands with conditions (bounded random space)
Params: starting_hand_count is number of tiles hold, starting_same_suit is 1/2/3/4 of a kind
Some combinations are invalid, like 4:1 (can't have one a kind in a 4 tile hand)
'''
def hand_sampling(starting_hand_count, starting_same_suit):
    if (starting_hand_count == 4 and starting_same_suit == 1) or (starting_hand_count < starting_same_suit):
        return None
    hand = []
    while starting_same_suit != hand_check(hand):
        hand = np.random.choice(suit, starting_hand_count)
    return hand

def skill(hand):
    hand = draw(hand)
    hand = draw(hand)
    return hand


def cherryOnTop_sampling(tile_count, n_kind, skill_count, draw_count = 0, multiprocess_dict = None):
    count = 0
    sample_size = 100000
    for i in range(sample_size):
        hand = hand_sampling(tile_count, n_kind)
        for _ in range(draw_count):
            hand = draw(hand)
        for _ in range(skill_count):
            hand = skill(hand)
        if (hand_check(hand) == 4):
            count +=1
    prob = count/sample_size
    if multiprocess_dict != None:
        multiprocess_dict[tile_count*1000+n_kind*100+skill_count*10 + draw_count] = prob
    return prob


result_arr = {}

def multiprocess():
    with Manager() as manager:
        result_dict = manager.dict()
        jobs = []
        for tile_count in range(1,5):
            for n_kind in range(1,5):
                for skill_count in range(8):
                    if (tile_count == 4 and n_kind == 1) or tile_count < n_kind:
                        continue
                    else:
                        p = Process(target=cherryOnTop_sampling, args=(tile_count, n_kind, skill_count, 0, result_dict))
                        p.start()
                        jobs.append(p)
        for p in jobs:
            p.join()
        
        result_dict = dict(result_dict)
        json.dump(result_dict, open("qingque/qingque_skill_probability.json", "w"))
        print("Probability by key:")
        for tile_count in range(1,5):
            for n_kind in range(1,5):
                for skill_count in range(8):
                    if (tile_count == 4 and n_kind == 1) or tile_count < n_kind:
                        continue
                    else:
                        key = tile_count*1000+n_kind*100+skill_count*10
                        print(f"Tiles in hand: {tile_count}. {n_kind} of a kind. Use Skill {skill_count} times. Probability of getting Cherry On Top: {result_dict[key]*100:0.2f}%")
                        print("-----------------------------------------------------------------------------------------------------")         
        print("\n\n\n\n\nSorted Probability:")
        result_dict = dict(sorted(result_dict.items(),key=lambda item:item[1]))
        for item in result_dict.items():
            print(f"Tiles in hand: {int(item[0]/1000)}. {int(item[0]%1000/100)} of a kind. Use Skill {int(item[0]%100/10)} times. Probability of getting Cherry On Top: {item[1]*100:0.2f}%")
            print("-----------------------------------------------------------------------------------------------------")        
    

if __name__ == '__main__':
    multiprocess()
    
    


