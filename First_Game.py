#Game
import time
import random


class Hero():
    def __init__(self, name, level=1, health=100, strength=10, items = {'healing potion': 2}):
        self.name = name 
        self.level = level
        self.health = health
        self.strength = strength
        self.items = items

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
    def use_item(self):
        count = 0
        full_health = self.health 
        while True:
            print("Choose one of your items {}".format(self.items))
            item_used = input()
            if item_used in self.items and self.items[item_used] != 0:
                while self.items[item_used] > 0 and count == 0:                             
                    if item_used == 'healing potion':
                        self.health += 20
                        self.items['healing potion'] -= 1
                        print("+20 health, Total Hero health: {}".format(self.health))
                        count += 1
                        continue                                       
                break

            elif item_used in self.items and self.items[item_used] == 0:
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
    

    

class Enemy():
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
    pass

#Introduction to the game setting
print('Enter you name, Hero:')
x = input()
hero1 = Hero(x,)
print(hero1)
narrator = Enemy('narrator',)

print(x + ", huh, well that's a dumb name")
#time.sleep(3)
print("...")
#time.sleep(3)
print("*The narrator attacks*")
print("*Battle music starts to play*")


# Loop or series of statements in order to battle enemies 
def battle(hero, enemy): # function was fixed using chat gpt
    action_list = ['attack', 'use item', 'standby']
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
            

# main reason for using chatgpt was to fix the use item function           
                

battle(hero1, narrator)





