from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class BossFight(Context, event.Event):
    def __init__(self, boss_name="Persephone", boss_health=100, player_health=100):
        super().__init__()
        self.name = "boss fight"
        self.boss_name = boss_name
        self.boss_health = boss_health
        self.player_health = player_health
        self.verbs = {
            'attack': self,
            'defend': self,
            'escape': self,
            'quit': self
        }
        self.result = {}
        self.go = True  

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "attack":
            damage_dealt = random.randint(5, 15)
            self.boss_health -= damage_dealt
            self.result["message"] = f"You attack the {self.boss_name} and deal {damage_dealt} damage."
            self.handle_boss_turn()
        elif verb == "defend":
            damage_taken = random.randint(15, 15)
            self.player_health -= damage_taken
            self.result["message"] = f"You defend against the {self.boss_name}'s attack but take {damage_taken} damage."
            self.handle_boss_turn()
        elif verb == "escape":
            if self.player_health > 0:  
                self.result["message"] = "You attempt to escape from the boss fight."
                self.go = False
        elif verb == "quit":
            self.result["message"] = "You decide to give up on the boss fight."
            self.go = False
        else:
            self.result["message"] = "Invalid command. You can 'attack', 'defend', 'escape', or 'quit'."

    def handle_boss_turn(self):
        if self.boss_health > 0 and self.player_health > 0:
            boss_attack = random.randint(5, 15)
            self.player_health -= boss_attack
            self.result["message"] += f"\nThe {self.boss_name} counterattacks and deals {boss_attack} damage."
            if self.player_health <= 0:
                self.result["message"] += f"\nOh no! You were defeated by the {self.boss_name}. Game Over."
                self.result["message"] += "\nPlease restart the island to fight the boss again. Better luck next time!"
                self.go = False
        elif self.boss_health <= 0:
            self.result["message"] += f"\nCongratulations! You defeated the {self.boss_name}!"
            self.result["message"] += "\nYou have saved this island!!!!"
            self.go = False
        elif self.player_health <= 0:
            self.result["message"] += f"\nOh no! You were defeated. Game Over."
            self.result["message"] += f"\nYou will need to restart the island. Better luck next time!"
            self.go = False


    def process(self, world):
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = f"You encounter the fearsome Persephone! Prepare for a battle!"

        while self.go:
            print(f"Player Health: {self.player_health} | {self.boss_name} Health: {self.boss_health}")
            print("What do you want to do?")
            Player.get_interaction([self])

        print(self.result["message"])
        return self.result