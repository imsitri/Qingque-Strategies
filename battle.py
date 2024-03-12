import qingque_class as qq
import qingque_probability as prob
import strategy as strat

def battle_no_Sparkle(log_file ,rounds, strategy, sp_source = 2, init_hand = None, enemy_count = 1):
    # logging battle data
    # intialization
    hand = init_hand
    # if no preset add a random 1 tile hand
    if init_hand is None:
        hand = prob.hand_sampling(1,1)
    qingque = qq.Qingque(hand)
    log_file.write(f"Qingque's initial hand: {qingque.hand}\n")
    dmg_dict = {}
    action_dict = {}
    sp = 0
    for round in range(rounds):
        action_dict[round] = []
        log_file.write(f"Turn {round + 1}:\n")
        sp = min(5, sp+sp_source)
        dmg_dict[f"Turn {round + 1}"] = 0
        log_file.write(f"Other teammates supply {sp_source} SP. Current SP: {sp}\n")
        while True:
            decision = strategy(sp, qingque, enemy_count, action_dict)
            if decision != strat.Action.END:
                log_file.write(f"Current stats: {qingque.energy} Energy - {qingque.percent_ATK * 100} ATK% - {qingque.CR * 100} CR% - {qingque.CD* 100} CD% - {qingque.DMG * 100:0.2f} DMG%\n")
            else:
                log_file.write(f"Current stat before resolving turn: {qingque.energy} Energy - {qingque.percent_ATK * 100} ATK% - {qingque.CR * 100} CR% - {qingque.CD* 100} CD% - {qingque.DMG * 100:0.2f} DMG%\n")
            if decision == strat.Action.ULT:
                dmg = qingque.ult(enemy_count)
                log_file.write(f"Qingque uses Ult, does {dmg} DMG.\n")
                dmg_dict[f"Turn {round+1}"] += dmg
                action_dict[round].append(strat.Action.ULT)
            if decision == strat.Action.SKILL:
                sp -=1
                qingque.skill()
                if (qingque.autarky == 1):
                    log_file.write("Autarky procced!\n")
                log_file.write(f"Qingque uses Skill. Current SP: {sp}\n")
                log_file.write(f"Current hand after using Skill: {qingque.hand}\n")
                action_dict[round].append(strat.Action.SKILL)
            if decision == strat.Action.BASIC:
                if (prob.hand_check(qingque.hand) != 4):
                    sp = min(5, sp+1)
                    log_file.write(f"Qingque regain SP from non enhanced Basic. Current SP: {sp}\n")
                    dmg = qingque.attack(enemy_count)
                    log_file.write(f"Qingque uses non enhanced Basic, does {dmg} DMG.\n")
                else:
                    sp = min(5, sp+1)
                    log_file.write(f"Qingque regain SP from E6. Current SP: {sp}\n")
                    dmg = qingque.attack(enemy_count)
                    log_file.write(f"Qingque uses Cherry On Top, does {dmg} DMG.\n")
                dmg_dict[f"Turn {round+1}"] += dmg
                action_dict[round].append(strat.Action.BASIC)
            if decision == strat.Action.END:
                break
        log_file.write("\nEnding Qingque's turn, resolving buffs. Current buff stack to be resolved.\n")
        for effect in qingque.status_effect:
            log_file.write(f"Type: {effect.type} - Value: {effect.value} - Duration: {effect.duration}\n")
        log_file.write("\n")
        qingque.time_step()
        log_file.write("Draw tiles on teammates turns:\n")
        for _ in range(4):
            qingque.draw()
            log_file.write(f"Current hand after drawing: {qingque.hand}\n")
        log_file.write("\n")
    log_file.write("Combat report:\n")
    for key in dmg_dict.keys():
        log_file.write(f"{key} total damage: {dmg_dict[key]}\n")
    log_file.write(f"Total across {rounds} turns: {sum(dmg_dict.values()):0.2f}. Average: {sum(dmg_dict.values())/rounds :0.2f}\n\n")
    return dmg_dict

def run_all_strategies(rounds_per_iteration, iteration):
    for name, val in strat.__dict__.items():
        if callable(val) and name not in ["Enum", "Action"]:
            performance = {}
            log = open("log/"+val.__name__ + ".txt", "w")
            for i in range(iteration):
                log.write(f"Iteration {i}:")
                # technique
                init = prob.hand_sampling(1,1)
                init = prob.draw(init)
                performance[f"Iteration {i}"] = battle_no_Sparkle(log_file=log, rounds=rounds_per_iteration, 
                                                                      strategy=val, sp_source=2, init_hand= init)
            sum_helper = 0
            for key in performance.keys():
                sum_helper+= sum(performance[key].values())/rounds_per_iteration
            print(f"Damage/round of {name}: {sum_helper/iteration:0.2f}")
            log.close()


if __name__ == '__main__':
    run_all_strategies(rounds_per_iteration= 6, iteration= 1000)



        



