from game import location
import game.config as config
from game.display import announce
from game.events import *
import random 
from game.items import *
from game.events.fish import FishingGame  
from game import location
import game.config as config 
from game.events.boss_fight import BossFight

class Island(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'Y'
        self.visitable = True
        self.starting_location = CrashSite(self)
        self.locations = {
            "CrashSite": self.starting_location,
            "MysticalForest": MysticalForest(self),
            "AncientRuins": AncientRuins(self), 
            "Shoreline": Shoreline(self), "Unknown": Unknown(self)
        }

    def enter(self, ship):
        print("Arrived at an island. There's a crash site and a couple of other locations")
        

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


# Items
class AncientRelic(Item):
    relics = 0
    def __init__(self):
        super().__init__("ancient relic", 100)  
        self.damage = (20, 80)  
        self.skill = "mystic_power"  
        self.verb = "invoke"  
        self.verb2 = "invokes"  

# Locations
class Unknown(location.SubLocation):
    def __init__(self, m): 
        super().__init__(m)
        self.name = "Unknown"
        self.boss_fight = BossFight()
        self.verbs['fight'] = self

    
    def enter(self):
        announce("You have entered a random spot.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["MysticalForest"]
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["CrashSite"]
        elif verb == "fight":
            self.boss_fight.process({})

class CrashSite(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Crash Site"
        self.verbs['west'] = self
        self.verbs['east'] = self
        self.verbs['north'] = self
        self.verbs['inspect'] = self
        self.ancient_relic = AncientRelic()

    def enter(self):
        announce("You have entered the Crash Site.")
        announce("North of the crash site is our ship. South, West, and East are other unknown locations")
        announce("Explore at your own risk\n")
        announce("You notice something shiny in the crash site, do you want to 'inspect' it?")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["Unknown"]
        elif verb == "east":
            config.the_player.next_loc = self.main_location.locations["Shoreline"]
            announce("You have entered shoreline")
            announce("To the south of shoreline it looks like there are some ancient artifacts....")
            announce("To the north of shoreline it looks like a random spot.....")
            announce("To the west of shoreline is the crashsite.....\n")
        elif verb == "inspect":
            if random.random() < 0.2:
                config.the_player.add_to_inventory([self.ancient_relic])
                announce("You catch ancient relic")
                AncientRelic.relics += 1
            else: 
                announce("Nothing here")
        elif verb == "north":
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False


class MysticalForest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Mystical Forest"
        self.verbs['fish'] = self
        self.ancient_relic = AncientRelic()

    def enter(self):
        announce("You have entered the Mystical Forest.")
        announce("You notice a peaceful river. What would you like to do?")
        announce("Type 'fish' to start fishing.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["Unknown"]
        elif verb == "fish":
            announce("In the water, you notice something shiny that looks like an ancient relic")
            self.events.append(FishingGame())
            fishing_game = next((event for event in self.events if isinstance(event, FishingGame)), None)
            if fishing_game:
                announce("You decide to try fishing...")
                announce("You can 'catch', 'release', or 'quit'.")
                result = fishing_game.process({}) 
                announce(result["message"])

                if fishing_game.ancient_relic >= 1:
                    config.the_player.add_to_inventory([self.ancient_relic])
                    announce("You catch ancient relic")
                    AncientRelic.relics += 1
                    print(AncientRelic.relics)

                if fishing_game.go:
                    announce("You finish fishing and return to the Mystical Forest.")
                self.events.remove(fishing_game)
                del fishing_game
                announce("1 Ancient Relic added to your inventory")

class AncientRuins(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Ancient Ruins"
        self.verbs['open'] = self
        self.verbs['inspect'] = self
        self.ancient_relic = AncientRelic()

    def enter(self):
        announce("You have entered the Ancient Ruins.")
        announce("You notice something shiny on the ground that you can 'inspect' it....\n")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["Shoreline"]
        if verb == "inspect":
            if self.ancient_relic is not None:
                announce("You take the ancient relic from the ruins.")
                config.the_player.add_to_inventory([self.ancient_relic])
                AncientRelic.relics += 1
                announce("OH NO!! Suddenly the ground started shaking!...")
                announce("OH WOW!! your crew starts to panick and before they try to run off...")
                announce("...")
                announce("...")
                announce("...")
                announce("you see a large stone pedestal...")
                announce("it looks like its a chamber with a large stone pedestal at its center. Surrounding the pedestal are several engraved symbols on the walls...")
                announce("Your crew mates tell you to 'open' it...")
            else:
                announce("There is no ancient relic here.")
        if verb == "open":
            print(self.ancient_relic.relics)
            if self.ancient_relic.relics >= 4:
                announce("You place all your relics and get teleported to unkown location...")
                announce("Get ready for boss fight...")
                announce("Type 'fight' to start the boss battle...")
                announce("Your commands are 'attack' and 'defend'")
                announce("If you lose... you cannot fight boss again!")
                config.the_player.location = self.main_location.locations["Unknown"]
            else:
                announce("Come back when you have enough Ancient Relics")


class Shoreline(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Shoreline"
        self.verbs['ignore'] = self
        self.verbs['fish'] = self
        self.ancient_relic = AncientRelic()

    def enter(self):
        announce("You have reached the Shoreline.")
        announce("You notice a peaceful river. What would you like to do?")
        announce("Type 'fish' to start fishing")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["CrashSite"]
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["AncientRuins"]
        elif verb == "fish":
            announce("In the water, you notice something shiny that looks like an ancient relic")
            self.events.append(FishingGame())
            fishing_game = next((event for event in self.events if isinstance(event, FishingGame)), None)
            if fishing_game:
                announce("You decide to try fishing...")
                announce("You can 'catch', 'release', or 'quit'.")
                result = fishing_game.process({}) 
                announce(result["message"])
                if fishing_game.ancient_relic >= 1:
                    config.the_player.add_to_inventory([self.ancient_relic])
                    announce("You catch ancient relic")
                    AncientRelic.relics += 1
                if fishing_game.go:
                    announce("You finish fishing and return to the Shoreline.")

                self.events.remove(fishing_game)
                del fishing_game
                announce("1 Ancient Relic added to your inventory")
    


