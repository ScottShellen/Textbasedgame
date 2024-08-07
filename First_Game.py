#Game
import time
import random
import sys

class Hero():
    def __init__(self, name, level=1, max_health= 100, health=100, strength=10, items = {'healing potion': 2}, money = 100):
        self.name = name 
        self.level = level
        self.max_health = max_health # max_health and health are needed in order to impose correct healing potion logic
        self.health = health # health as one variable can not contain two different values of a maximum and current placeholder
        self.strength = strength
        self.items = items
        self.money = money

    def __repr__(self):
       return "Your Hero's name is {}, you are level {}, you have {} health, and your attack strength is {}".format(self.name, self.level, self.health, self.strength)
    
    def attacks(self, enemy):
        attack = True
        attack_damage = self.strength * (1 - (random.randint(-1,1)/4))
        attack_accuracy = random.randint(1,10)
        if attack_accuracy % 4 == True:
            print("-----------------")
            print("{}'s attack missed".format(self.name))
            print("-----------------")
            attack = False
        else:
            print("-----------------")
            print("{}'s attack hit".format(self.name))
            print("-{} enemy damage".format(attack_damage))
            print("-----------------")
            attack = True
        if attack == True:
            enemy.health = enemy.health - attack_damage
        if enemy.health <= 0:
            attack = False

    def buy_item(self, npc):
        while True:
            print('----------------------------------')
            print(npc.items)
            print('----------------------------------')
            item_bought = input().strip().lower()
            if item_bought in npc.items:
                if self.money >= npc.items[item_bought]:
                    if item_bought in self.items:
                        self.items[item_bought] += 1     
                    else:
                        self.items.update({item_bought: 1})
                    
                    print("\nYou have bought a {}".format(item_bought))
                    self.money -= npc.items[item_bought]

                    cont_shop = input("Would you like to buy anything else: Y/N\n").strip().upper()

                    if cont_shop != 'Y':
                        break
                else:
                    print("\nYou don't have enough money to buy this item")
            else:
                print("\nThis item is not available")
            
# next time for items I would create a class on their own 
    def use_item(self):
        while True:
            print("----------------------------------")
            print("Choose one of your items {}".format(self.items))
            item_used = input().strip().lower()
            if item_used in self.items: # the multiple if statements allow for more readable code in this case 
                if self.items[item_used] > 0:
                    if item_used == 'healing potion':#chat gpt used to fix healing potion logic 
                        if self.health == self.max_health: # if hero health is at max the health potion does not increase the hero's health beyond max health it just returns it to the max_health
                            print("Your health is already at max health")
                        else:
                            healed_amount = min(20, self.max_health - self.health) # calculates heal amount
                            self.health += healed_amount                    
                            self.items['healing potion'] -= 1
                            print("+{} health\n Total Hero health: {}".format(healed_amount, self.health))
                        break                                       
                    # space to define more items may be useful to create a separate file for items if project get larger
                    elif item_used == 'strength potion':
                        print("Your strength surges within you")
                        self.strength += 5
                        self.items['strength potion'] -= 1
                        print("+{} strength\n Total Hero strength: {}".format(str(5), self.strength))#for this purpose I will leave strength larger after each use and not go down after battle
                        break
                    elif item_used == 'max health potion':
                        print("Your Life force surges")
                        self.max_health += 20
                        self.items['max health potion'] -= 1
                        print("+{} total health\n Total Max Hero Health: {}".format(str(20), self.max_health))
                        break
                else:
                    print("There are no more {}s".format(item_used)) 
                    print("------------------------------")
                    
            else:
                print("please type an item in your inventory")
                print("{}".format(self.items))
                print("---------------------------------------")

    def standby(self):
        print("Why are you just sitting there Hero")

    def dies(self):
        if self.health <= 0:
            print("DEAD")
            exit()
    

    

class Enemy(): #
    def __init__(self, name, level = 1, health = 50, strength = 20, items = None):
        self.name = name 
        self.level = level
        self.health = health
        self.strength = strength
        self.items = items

    def __repr__(self) -> str:
        return "enemy's health: {}".format(self.health)

    def attacks(self, hero): # enemy attack
        attack = True
        attack_damage = self.strength * (1 - (random.randint(-1,1)/4))
        attack_accuracy = random.randint(1,10)
        if attack_accuracy % 3 == True:
            print("-----------------")
            print("enemy's attack missed")
            print("-----------------")
            attack = False
        else:
            print("-----------------")
            print("{} attacks!".format(self.name))
            print("-{} hero health".format(int(attack_damage)))
            print("-----------------")
            attack = True
        if attack == True:
            hero.health = hero.health - int(attack_damage)
        return hero.health 
    
    def escapes(self): # enemy attempts an escape 
        chance_of_running = random.randint(1, 100)
        if chance_of_running % 5:
            print("{} has escaped".format(self.name))
        else:
            print("{} has failed to escape".format(self.name))

    def dies(self):
        if self.health <= 0:
            print("you got me...")
            
    # for the item dictionary of the npc the items are going to be associated with value not inevntory
class NPC():
    def __init__(self, name, items = {'healing potion': 30, 'strength potion': 30, 'max health potion': 100}, money = 50):
        self.name = name
        self.items = items
        self.money = money


# Loop or series of statements in order to battle enemies 
def battle(hero, enemy): # function was fixed using chat gpt
    action_list = ['attack', 'use item', 'standby']
    slowprint("...BATTLE MODE...")
    while hero.health >= 0  or enemy.health >= 0: #battle will stop after one of the parties health is below or technically at 0
        print("Type an action you would like to take: attack, use item, standby")
        action = input().strip().lower()

        if action not in action_list:
            print("-------------------------------")
            print("please type an action listed")
            print("-------------------------------")
            continue

        if action == 'attack':     
            hero.attacks(enemy)
            if enemy.health <= 0:
                enemy.health = 0
                print(enemy)
                enemy.dies()        #enemy can only die on turn when hero is attacking anyways this keeps the code from running another turn and the enemy dying on that turn
                print ("Victory")
                return
            
            print(enemy)
            enemy.attacks(hero)
            if hero.health <= 0:
                hero.health = 0
                hero.dies()
                print("Defeat")
                return

        elif action == 'use item':
            if any(value > 0 for value in hero.items.values()): #if there is no items available breaks out of the loop
                hero.use_item()
                enemy.attacks(hero)
                if hero.health <= 0:
                    hero.health = 0
                    hero.dies()
                    print("Defeat")
                    return
            
                print("Health: {}".format(hero.health))
                print("-----------")  
            
            else:
                print("No items available to use")

        elif action == 'standby':
            hero.standby()
            enemy.attacks(hero)
            if hero.health <= 0:
                    hero.health = 0
                    hero.dies()
                    print("Defeat")
                    return
            print("Health: {}".format(hero.health))
            print("-----------")  


def slowprint(text):
    for word in text:
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(.05)
    print("\n")


# Chatgpt was mainly used to fix function of items in the system as they are now more robust and can handle edge cases better         

# without a doubt def need less slowprints it hampers the readability of the code 

# Beginning of the game
slowprint('*Your name*:')
name = input()
slowprint("\nAwaken "+ name +", there is no time left, they've come for us.")
slowprint('''They are burning the village to the ground\n
...\n
What?''')

hero = Hero(name,) #class instance of hero

soldier = Enemy('Soldier',) # class instance of enemy

sus_grandma = NPC('Sus Grandma') #class instance of npc
#these ccould be done withe super and sub classes  b ut just learned about those

slowprint('''Listen boy they are leaving nothing in their wake\n 
*Old man Gobert spits blood on your chest*''')

time.sleep(1)

slowprint('''THERE IS NO TIME FOR THIS YOU MUST RUN!!!\n
*Gobert collapses revealing an arrow lodged into his lung*\n
...''')

time.sleep(3)

slowprint("\n*Stay or Run*")

while True:
    choice1 = input().strip().lower()
    if choice1 == "run":
        slowprint("\n*You run away from the burning village*")
        break
    else:
        slowprint("You cannot stay here!")

slowprint("\n*You enter the forest there is a fork on the path: left or right")

while True:
    choice2 = input().strip().lower()
    if choice2 == 'left':
        slowprint("\nThere's another fork in the road, left seems to be bathed in darkness and right is illuminated by what looks like a campfire...")
        choice2_1 = input().strip().lower()
        if choice2_1 == 'left':
            slowprint("\nThere's nothing here, you head back to the first fork.")
        elif choice2_1 == 'right':
            slowprint('''\nAn old woman is sitting near a fire\n
*She looks at you*\n
It is dangerous here young one, would you like to purchase some wares before you head back''')
            
            hero.buy_item(sus_grandma)
            
            slowprint("You have nothing left to do here you turn back to the first fork in the road")
            
    if choice2 == 'right':
        slowprint('''\n*You walk along the path and hear someone*\n
*A soldier is sitting there, he looks like he has been separated from the main troop*\n
*He spots you from far away*\n
Who are you, what are you doing out here?\n
WHAT! A villager! Well, they said none left alive. Sorry, young one...''')

        battle(hero, soldier)

        slowprint('''I didn't think it would end like this... how pathetic...\nKnow this young one...\n
They will hunt you down to the...\n
*You look at the dead soldier, taking in the moment*''')
        
        time.sleep(2)

        slowprint('''*You run into the forest, deep, knowing whatever future lay ahead may be bleak...\n
                ...THE END...''')
        exit()
    else:
        slowprint("Please choose one of the directions")

#almost done finish the rest tomorrow