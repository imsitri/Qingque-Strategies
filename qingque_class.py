import qingque_probability as prob
import numpy as np

class Qingque:
    def __init__(self, initial_hand, base_atk = 1129, flat_atk = 352, percent_atk = 0.712, cr = 0.6, cd = 1.2, dmg = 0.532):
        self.Base_ATK = base_atk
        self.Flat_ATK = flat_atk
        self.percent_ATK = percent_atk
        self.CR = cr
        self.CD = cd
        self.DMG = dmg
        self.status_effect = []
        self.basic = 1.1
        self.enhanced_target = 2.64
        self.enhanced_blast = 1.1
        self.hand = initial_hand
        self.autarky = 0
        self.energy = 70
        self.hidden_hand = False
    
    def add_status_effect(self, effect):
        self.status_effect.append(effect)
        match effect.type:
            case "ATK%":
                self.percent_ATK += effect.value
            case "Flat_ATK":
                self.Flat_ATK += effect.value
            case "CR":
                self.CR += effect.value
            case "CD":
                self.CD += effect.value
            case "DMG%":
                self.DMG += effect.value
            case _:
                pass

    def time_step(self):
        for effect in list(self.status_effect):
            effect.duration -=1
            if effect.duration <= 0:
                match effect.type:
                    case "ATK%":
                        self.percent_ATK -= effect.value
                    case "Flat_ATK":
                        self.Flat_ATK -= effect.value
                    case "CR":
                        self.CR -= effect.value
                    case "CD":
                        self.CD -= effect.value
                    case "DMG%":
                        self.DMG -= effect.value
                    case _:
                        pass
                self.status_effect.remove(effect)

    def attack(self, enemy_count = 1):
        Atk = self.Base_ATK*(1+self.percent_ATK) + self.Flat_ATK
        Crit = 1 + self.CR * self.CD
        self.energy +=20
        if prob.hand_check(self.hand) == 4:
            dmg =  (self.enhanced_target + self.enhanced_blast * (enemy_count - 1)) * Atk * Crit * (1 + self.DMG)
            if self.hidden_hand:
                self.hidden_hand = False
                for effect in list(self.status_effect):
                    if effect.type == "ATK%" and effect.value == 0.792:
                        self.status_effect.remove(effect)
                        self.percent_ATK -= 0.792
            Atk = self.Base_ATK*(1+self.percent_ATK) + self.Flat_ATK
            dmg += self.enhanced_target * self.autarky * Atk * Crit * (1 + self.DMG)
            self.hand = prob.hand_sampling(0,0)
        else:
            dmg = self.basic * (self.autarky + 1) * Atk * Crit * (1+self.DMG)
        self.autarky = 0
        return dmg
    
    def ult(self, enemy_count = 1):
        Atk = self.Base_ATK*(1+self.percent_ATK) + self.Flat_ATK
        Crit = 1 + self.CR * self.CD
        if (self.energy < 140):
            return
        else:
            self.hand = prob.hand_sampling(4,4)
            self.energy = 5
            dmg =  2.16 * enemy_count * Atk * Crit * (1+self.DMG+0.1)
            if not self.hidden_hand:
                self.hidden_hand = True
                self.add_status_effect(Buff("ATK%", 0.792, 100000000))
            return dmg
    
    def skill(self):
        if prob.hand_check(self.hand) == 4:
            return
        skill_counter = 0
        for effect in self.status_effect:
            if effect.type == "DMG%" and effect.value == 0.308:
                skill_counter +=1
        if skill_counter < 4:
            self.add_status_effect(Buff("DMG%", 0.308, 1))
        self.energy+= 2
        self.hand = prob.skill(self.hand)
        autarky = np.random.choice([1,2,3,4], 1)
        if autarky == 1 and self.autarky != 1:
            self.autarky = 1
        if prob.hand_check(self.hand) == 4 and not self.hidden_hand:
            self.hidden_hand = True
            self.add_status_effect(Buff("ATK%", 0.792, 1000000000))
        return 0
        
    def draw(self):
        if prob.hand_check(self.hand) == 4:
            return
        self.hand = prob.draw(self.hand)
        self.energy+= 1
        if prob.hand_check(self.hand) == 4 and not self.hidden_hand:
            self.hidden_hand = True
            self.add_status_effect(Buff("ATK%", 0.792, 1000000000))
        
        
class Buff:
    def __init__(self, type, value, duration):
        self.type = type
        self.value = value
        self.duration = duration


