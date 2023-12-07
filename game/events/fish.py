from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class FishingGame(Context, event.Event):
    def __init__(self):
        super().__init__()
        self.name = "fishing spot"
        self.fish_count = 5
        self.ancient_relic = 0
        self.verbs = {
            'catch': self,
            'release': self,
            'quit': self
        }
        self.result = {}
        self.go = True  

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "catch":
            self.catch_fish()
        elif verb == "release":
            self.release_fish()
        elif verb == "quit":
            self.quit_fishing()
        else:
            self.handle_invalid_command()

    def catch_fish(self):
        if self.fish_count > 0:
            caught_fish = random.choice(["Ancient Relic", "Bass", "Salmon"])
            print(f"You caught a {caught_fish}!")
            self.fish_count -= 1
            if caught_fish == "Ancient Relic":
                print(f"You caught an ancient relic")
                self.ancient_relic += 1
        else:
            self.result["message"] = "There are no more fish in the fishing spot."

    def release_fish(self):
        self.fish_count += 1
        self.result["message"] = "You released a fish back into the water."

    def quit_fishing(self):
        self.result["message"] = "You decide to stop fishing."
        self.go = False

    def handle_invalid_command(self):
        self.result["message"] = "Invalid command. You can 'catch', 'release', or 'quit'."
        print("Invalid command. You can 'catch', 'release', or 'quit'.")

    def process(self, world):
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = "Welcome to the fishing spot. What do you want to do?"
        print(self.result["message"])

        while self.go:
            print(f"{self.fish_count} fish in the water. What do you want to do?")
            Player.get_interaction([self])

        return self.result