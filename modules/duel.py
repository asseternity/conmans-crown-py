import random
from modules.combatant import Combatant

class Duel:
    def __init__ (self, id, win_story, lose_story, enemy: Combatant):
        self.id = id
        self.win_story = win_story
        self.lose_story = lose_story
        self.enemy = enemy      

    def tactic_hint(self, combatant: Combatant):
        if combatant.power > combatant.max_power * 0.7:
            return f"{combatant.name}'s posture shifts — shoulders tense, eyes fierce. A mighty blow seems imminent!"
        elif combatant.power < combatant.max_power * 0.3:
            return f"{combatant.name} appears winded, steps lighter and blade hesitant. A defensive move or feeble jab is likely."
        else:
            return f"{combatant.name}'s stance wavers between caution and ambition — a measured strike may be coming."
        
    def choose_enemy_action(self):
        enemy_action = 0
        if (self.enemy.power > self.enemy.max_power * 0.7):
            random_number = random.randint(0, 100)
            if random_number < 50:
                enemy_action = self.enemy.power
            else:
                enemy_action = min(self.enemy.power, random.randint(1, 3))
        elif (self.enemy.power < self.enemy.max_power * 0.3):
            random_number = random.randint(0, 100)
            if random_number < 70:
                enemy_action = 0
            else:
                if self.enemy.power > 0:
                    enemy_action = min(self.enemy.power, random.randint(1, self.enemy.power))
                else:
                    enemy_action = 0            
        elif (self.enemy.health == 1):
            enemy_action = self.enemy.power
        else:
            random_number = random.randint(0, 100)
            if random_number < 50:
                enemy_action = 0
            elif random_number < 85:
                enemy_action = min(self.enemy.power, random.randint(1, 3))
            else:
                enemy_action = self.enemy.power
        return enemy_action
        
    def damage_phase(self, player, player_spent, enemy_spent):
        p_spent = player.spend_power(player_spent)
        e_spent = self.enemy.spend_power(enemy_spent)

        if p_spent == 0 and e_spent == 0:
            # Both defend, no damage
            return "Both warriors circle one another cautiously, eyes locked — but neither dares strike. The tension grows; no blood is spilled this turn."
        elif p_spent == 0:
            # Player defends, takes 1 damage
            player.take_damage(1)
            return f"{player.name} braces for the blow, steel raised in defense — yet {self.enemy.name}'s strike slips through, leaving a shallow wound!"
        elif e_spent == 0:
            # Enemy defends, takes 1 damage
            self.enemy.take_damage(1)
            return f"{self.enemy.name} retreats behind a guarded stance, but {player.name}'s cunning feint lands true — a minor cut, but a message sent."
        else:
            # Both attack
            if p_spent > e_spent:
                damage = self.calculate_damage(e_spent)
                self.enemy.take_damage(damage)
                return f"{player.name} unleashes a furious assault, overpowering {self.enemy.name}'s efforts. The blow lands hard — {damage} damage dealt!"
            elif e_spent > p_spent:
                damage = self.calculate_damage(p_spent)
                player.take_damage(damage)
                return f"{self.enemy.name} finds an opening and strikes like lightning! {player.name} reels back, taking {damage} damage."
            else:
                # Equal spent power, both take 1 damage
                player.take_damage(1)
                self.enemy.take_damage(1)
                return "Steel clashes against steel in perfect synchronicity — both combatants land glancing hits. Blood is drawn on both sides."

    def calculate_damage(self, loser_spent):
        if loser_spent == 0:
            return 1
        elif loser_spent <= 5:
            return 2
        else:
            return 4     
    
    def restore_after(self, player, player_action, enemy_action):
        if player_action < 3:
            amount = max(1, 4 - player_action)
            missing_power = player.max_power - player.power
            if missing_power > 0:
                player.restore_power(random.randint(1, min(amount, missing_power)))
        if enemy_action < 3:
            amount = max(1, 4 - enemy_action)
            missing_power = self.enemy.max_power - self.enemy.power
            if missing_power > 0:
                self.enemy.restore_power(random.randint(1, min(amount, missing_power)))