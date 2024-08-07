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

        # goal of the function below is to use a healing potion, if there are no more healing potions then it will return to battle action
        #if the input is wrong it will ask again until valid input is used
    def buy_item(self, npc):
        while True:
            print('----------------------------------')
            item_bought = input().strip().lower()
            if item_bought in npc.items:
                if self.money >= item_bought.value():
                    if item_bought in self.items:
                        self.items[item_bought] += 1
                        print("You have bought ")
                    else:
                        self.items.update({item_bought: 1})
                    break
                elif npc.items.value() <= self.money:
                    print("You don't have enough money to buy this item")
            

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
                            print("+{} health, Total Hero health: {}".format(healed_amount, self.health))
                        break                                       
                    # space to define more items may be useful to create a separate file for items if project get larger

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
            print("you got me you son of a bitch")
            
        
class NPC():
    def __init__(self, name, dialogue, items = {}, money = 50):
        self.name = name
        self.dialogue = dialogue
        self.items = items
        self.money = money

    def sell_items(self):
        print("Here are my wares: "+{}.format(self.items))
        


    

# Loop or series of statements in order to battle enemies 
def battle(hero, enemy): # function was fixed using chat gpt
    action_list = ['attack', 'use item', 'standby']
    while hero.health >= 0  or enemy.health >= 0: #battle will stop after one of the parties health is below or technically at 0
        print("Type an action you would like to take: attack, use item, standby")
        action = input().strip().lower(),

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
#       
# Beginning of the game
slowprint('*Your name*:')
name = input()
slowprint("Awaken"+ name +", there is no time left, they've come for us.")
slowprint("They are burning the village to the ground")
slowprint("...")
slowprint("What?")

slowprint("Listen boy they are leaving nothing in their wake")
slowprint("*Old man Gobert spits blood on your chest*")
time.sleep(1)
slowprint("THERE IS NO TIME FOR THIS YOU MUST RUN!!!")
slowprint("*Gobert collapses revealing an arrow lodged into his lung*")
slowprint("...")
time.sleep(3)

slowprint("*Stay or Run*")


while True:
    choice1 = input().strip().lower()
    if choice1 == "run":
        slowprint("*You run away from the burning village*")
        break
    else:
        slowprint("You cannot stay here!")

slowprint("*You enter the forest there is a fork on the path: left or right")
while True:
    choice2 = input().strip().lower()
    if choice2 == 'left':
        slowprint("There's another fork in the road, left seems to be bathed in darkness and right is illuminated by what looks like a campfire...")
        choice2_1 = input().strip().lower()
        if choice2_1 == 'left':
            slowprint("There's nothing here, turn back around.")
        elif choice2_1 == 'right':
            slowprint("An old woman is sitting near a fire")
            slowprint("*She looks at you*")
            slowprint("It is dangerous here young one, would you like to purchase some wares before you head back")
        else:
            slowprint("Please choose one of the directions")
            
    if choice2 == 'right':
        slowprint("You head through and come to another fork in the road")
    else:
        slowprint("Please choose one of the directions")

hero1 = Hero(name,)
print(hero1)
narrator = Enemy('narrator',)



#slowprint(name + ", huh, well that's a dumb name")
#time.sleep(1)
#print("...")
#time.sleep(1)
#print("*The narrator attacks*")
#print("*Battle music starts to play*")
#battle(hero1, narrator)





