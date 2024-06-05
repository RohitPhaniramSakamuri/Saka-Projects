import random

#charizard, tyranitar, pikachu, blastoise, venusaur, rayquaza, mewtwo  

class pokemon:
    def __init__(self, name, hp, moveList, attack, defense, speed, type1, type2=None):
        self.name = name
        self.hp = hp
        self.type1 = type1
        self.type2 = type2
        self.moveList = moveList
        self.attack = attack 
        self.defense = defense
        self.speed = speed
        self.status = None
    
    def __str__(self):
        return self.name
    
    def setStatus(self, status):
        self.status = status


class player:
    def __init__(self, name, pokeList):
        self.name = name
        self.pokeList = pokeList
        self.bag = []
        self.currentPoke = None

    def randomiser(self, max):
        return random.randint(0, max)
    
    def setCurrentPoke(self, pokeName):

        '''Takes a string as argument, typically the name of the pokemon concerned (pokemon.name)'''

        if pokeName == None:
            self.currentPoke = None
                                                    
        boolList = [x.name == pokeName for x in self.pokeList] #creates a list of booleans (eg: [True, False, False, False]) 
        if True in boolList: 
            self.currentPoke = self.pokeList[boolList.index(True)] #sets the current pokemon to the pokemon whose name has been passed as arg
        else:
            print(self.name, "doesn't have this Pokemon")
        # works as intended only if all pokemon in game are unique

    def switchPoke(self):
        selection = int(input(f"Choose your Pokemon:\n{[_.name for _ in self.pokeList ]}")) # change to accomodate all pokemon for the GUI
        return self.pokeList[selection]


    def doMoveAgainst(self, target, moveMade):
        global liveGame # boolean that is the game-running while loop condition.
        modifier = 1
        comment = ''
        willHit = self.randomiser(100) <= self.currentPoke.moveList[moveMade].accuracy # a boolean that checks if a random number <= 100 < the move's accuracy
        # self.currentPoke.moveList[moveMade] is the current move made
        if liveGame:
            if self.currentPoke.moveList[moveMade].pp == 0:  # checks if the chosen move have the pp remaining for it to be able to carry out the hit
                print(self.currentPoke.name, "does not have enough pp!")
                gameJunction()
            else:
                self.currentPoke.moveList[moveMade].pp -= 1 # 1 pp consumed per move
                if willHit:
                    if self.currentPoke.type1 == self.currentPoke.moveList[moveMade].type or (self.currentPoke.type2 == self.currentPoke.moveList[moveMade].type and self.currentPoke.type2 != None):
                        modifier *= 1.5 # STAB (Same Type Attack Boost) modifier

                    if target.currentPoke.type1 in AttackSuperEffective[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 2 
                        comment = 'Super Effective!'

                    if target.currentPoke.type2 in AttackSuperEffective[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 2 
                        if comment != 'Super Effective!':
                            comment = 'Super Effective!'

                    if target.currentPoke.type1 in AttackIneffective[self.currentPoke.moveList[moveMade].type] or target.currentPoke.type2 in AttackIneffective[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 0.5
                        comment = 'Not very Effective...'

                    if target.currentPoke.type1 in AttackNull[self.currentPoke.moveList[moveMade].type] or target.currentPoke.type2 in AttackNull[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 0
                        comment = f'Does not affect {target.currentPoke}...'

                    # the damage equation
                    damage = ((0.84*(self.currentPoke.moveList[moveMade].power)*(self.currentPoke.attack/target.currentPoke.defense)) + 2)*modifier

                    target.currentPoke.hp -= round(damage) #hit has landed, hp is subtracted by the damaged amount from the target(computer)'s current Pokemon

                    if target.currentPoke.hp <= 0: #if target's current pokemon hp is ded
                        target.currentPoke.hp = 0 #set it to zero
                        target.currentPoke.setStatus('fnt') #set its status effect to 'fnt'
                        comment += f' {target.currentPoke} fainted!' 
                        isAlive = [nextPoke.status != 'fnt' for nextPoke in target.pokeList] # a list of bools that has True if a pokemon's status != 'fnt' (pokeNotDed)
                        if True in isAlive: #checks if computer has any usable pokemon left
                            for _ in isAlive:
                                    target.setCurrentPoke(target.pokeList[isAlive.index(True)].name) #sets the first pokemon it finds alive from the left as computer's next pokemon.
                                    comment += f'\n{target.name} chose {target.currentPoke}!'
                                    break
                        else:
                            comment += f"\n\n{target.name} has no more usable pokemon remaining! {self.name} wins!"
                            liveGame = False
                            
                    print(f'{self.currentPoke} used {self.currentPoke.moveList[moveMade]}.\nDid {round(damage)}hp damage. ' + comment) # This is displayed when a hit lands.

                else:
                    print(print(f"{self.currentPoke}'s {self.currentPoke.moveList[moveMade]} missed!")) # This is displayed when a hit does not land.


class notPlayer(player): # a child of player class
    def doMoveAgainst(self, target, moveMade):
        global liveGame
        modifier = 1
        comment = ''
        willHit = self.randomiser(100) <= self.currentPoke.moveList[moveMade].accuracy # a boolean that checks if a random number <= 100 < the move's accuracy
        if liveGame:
            if self.currentPoke.moveList[moveMade] == 0: # same pp check as above
                print(self.currentPoke.name,"does not have enough pp")
                gameJunction()
            else:
                self.currentPoke.moveList[moveMade].pp -= 1
                if willHit:
                    if self.currentPoke.type1 == self.currentPoke.moveList[moveMade].type or (self.currentPoke.type2 == self.currentPoke.moveList[moveMade].type and self.currentPoke.type2 != None):
                        modifier *= 1.5

                    if target.currentPoke.type1 in AttackSuperEffective[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 2 
                        comment = 'Super Effective!'

                    if target.currentPoke.type2 in AttackSuperEffective[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 2 
                        if comment != 'Super Effective!':
                            comment = 'Super Effective!'

                    if target.currentPoke.type1 in AttackIneffective[self.currentPoke.moveList[moveMade].type] or target.currentPoke.type2 in AttackIneffective[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 0.5
                        comment = 'Not very Effective...'

                    if target.currentPoke.type1 in AttackNull[self.currentPoke.moveList[moveMade].type] or target.currentPoke.type2 in AttackNull[self.currentPoke.moveList[moveMade].type]:
                        modifier *= 0
                        comment = f'Does not affect {target.currentPoke}...'

                    damage = ((0.84*(self.currentPoke.moveList[moveMade].power)*(self.currentPoke.attack/target.currentPoke.defense)) + 2)*modifier

                    target.currentPoke.hp -= round(damage) # hit landed against the target (in this case, it is Saka (player)) damage is deducted from hp

                    if target.currentPoke.hp <= 0: # if pokeDed
                        target.currentPoke.hp = 0 # set hp to 0
                        target.currentPoke.setStatus('fnt') # set status to 'fnt'
                        comment += f' {target.currentPoke} fainted!'
                        print(f'{self.currentPoke} used {self.currentPoke.moveList[moveMade]}.\nDid {round(damage)}hp damage. ' + comment)
                        isAlive = [x for x in self.pokeList if x.status != 'fnt'] # a bool list which has True if pokeStatus != 'fnt'
                        if len(isAlive) == 0:
                            comment += f"\n\n{target.name} has no more usable pokemon remaining! {self.name} wins!"
                            liveGame = False

                        else:
                            Saka.setCurrentPoke(choicePokemon())
                    
                    else:
                        print(f'{self.currentPoke} used {self.currentPoke.moveList[moveMade]}.\nDid {round(damage)}hp damage. ' + comment)

                else:
                    print(f"{self.currentPoke}'s {self.currentPoke.moveList[moveMade]} missed!")


class move:
    def __init__(self, name, accuracy, type, pp, power=None, attInc=None, defInc=None, speedInc=None, hpInc=None, statChange=None):
        self.moveName = name
        self.accuracy = accuracy
        self.type = type
        self.pp = pp
        self.power = power
        self.attInc = attInc
        self.defInc = defInc
        self.speedInc = speedInc
        self.hpInc = hpInc
        self.statChange = statChange
        
    def __str__(self):
        return str(self.moveName)
    

class item:
    def __init__(self, name, count, statChange=None):
        self.name = name
        self.count = count
        self.statchange = statChange
    

def gameJunction():
    choice = int(input(f"What will {Saka.name} do?\n>> [Fight, Bag, Pokemon, Run]\n")) #matchcase
    if choice == 0:
        fight()

    elif choice == 1:
        chosenItem = int(input(f"Which item?\n{[items.name for items in Saka.bag]}\n"))
        chosenPoke = Saka.switchPoke()
        applyBagItem(chosenItem, chosenPoke)
        Computer.doMoveAgainst(Saka, compChoice)

    elif choice == 2:
        Saka.setCurrentPoke(choicePokemon())
        Computer.doMoveAgainst(Saka, compChoice)

    elif choice == 3:
        print("You can't run!")
        gameJunction()


def fight():
        moveMade = int(input(f"{[moves.moveName for moves in Saka.currentPoke.moveList]}\n"))
        if Saka.currentPoke.speed >= Computer.currentPoke.speed:
            Saka.doMoveAgainst(Computer, moveMade)
            Computer.doMoveAgainst(Saka, compChoice)
        else:
            Saka.doMoveAgainst(Computer, moveMade)
            Computer.doMoveAgainst(Saka, compChoice)


def doDamage():
    pass


def applyBagItem(itemChosen, pokeChosen):
    if Saka.bag[itemChosen].count > 0:
        if Saka.bag[itemChosen].name == "Hyper Potion":
            pokeChosen.hp += 200
            
        elif Saka.bag[itemChosen].name == "Super Potion":
            pokeChosen.hp += 50

        elif Saka.bag[itemChosen].name == "Potion":
            pokeChosen.hp += 20

        elif Saka.bag[itemChosen].name == "X Attack":
            pokeChosen.attack *= 3
            
        elif Saka.bag[itemChosen].name == "X Defense":
            pokeChosen.defense *= 3

        elif Saka.bag[itemChosen].name == "X Speed":
            pokeChosen.speed *= 3

        elif Saka.bag[itemChosen].name == "Ether":
            moveChosen = int(input(f"Which move will you apply the Ether on?\n{[_.name for _ in pokeChosen.moveList]}\n"))
            pokeChosen.moveList[moveChosen].pp += 10

        print(f"Applied {Saka.bag[itemChosen].name} to {pokeChosen}")
        Saka.bag[itemChosen].count -= 1
    else:
        print("You do not have enough of this item!")
        gameJunction()
    
    
def choicePokemon():
    pokePicked = Saka.switchPoke()
    if pokePicked.status == 'fnt':
        print(pokePicked,"cannot battle any longer")
        choicePokemon()

    elif pokePicked == Saka.currentPoke:
        print(Saka.currentPoke,"is already in battle!")
        choicePokemon()
    
    else:
        print(f"{Saka.name} chose {pokePicked.name}!")
        return(pokePicked.name)


#moves
#__init__(self, name, accuracy, type, pp, power=None, attInc=None, defInc=None, speedInc=None, hpInc=None, statChange=None)
Thunderbolt = move("Thunderbolt", 100, "Electric", 15, 90, statChange="Par")
Flamethrower = move("Flamethrower", 100, "Fire", 15, 90, statChange="Burn")
Slash = move("Slash", 100, "Normal", 20, 70)
Aerial_Ace = move("Aerial Ace", 100, "Flying", 20, 60)
Dragon_Claw = move("Dragon Claw", 100, "Dragon", 15, 80)
Extreme_Speed = move("Extreme Speed", 100, "Normal", 5, 80)
Assurance = move("Assurance", 100, "Dark", 10, 60)
Earthquake = move("Earthquake", 100, "Ground", 10, 100)
Rock_Slide = move("Rock Slide", 90, "Rock", 10, 75)
Brick_Break = move("Brick Break", 70, "Fighting", 10, 75)
Surf = move("Surf", 100, "Water", 15, 95)
Hydro_Pump = move("Hydro Pump", 80, "Water", 5, 110)
Skull_Bash = move("Skull Bash", 100, "Normal", 10, 100)
Shadow_Ball = move("Shadow Ball", 100, "Ghost", 15, 80)
Sludge_Bomb = move("Sludge Ball", 100, "Poison", 10, 90)
Psychic = move("Psychic", 100, "Psychic", 10, 90)
Solar_Beam = move("Solar Beam", 100, "Grass", 10, 120)
Body_Slam = move("Body Slam", 100, "Normal", 15, 85)
Hyper_Beam = move("Hyper Beam", 90, "Normal", 5, 90)
Wing_Attack = move("Wing Attack", 100, "Flying", 35, 60)
Ice_Beam = move("Ice Beam", 100, "Ice", 10, 90, statChange="Frz")
Splash = move("Splash", 100, "Normal", 40, 0)
Draco_Meteor = move("Draco Meteor", 90, "Dragon", 5, 130)
Leaf_Blade = move("Leaf Blade", 100, "Grass", 15, 90)


#pokemon hp = (max+min)*0.55
#__init__(self, name, hp, moveList, attack, defense, speed, type1, type2=None,)
Pikachu = pokemon("Pikachu", 249, [Thunderbolt, Extreme_Speed, Brick_Break, Splash], 55, 40, 90, "Electric")
Charizard = pokemon("Charizard", 344, [Flamethrower, Slash, Aerial_Ace, Dragon_Claw], 109, 78, 100, "Fire", "Flying")
Tyranitar = pokemon("Tyranitar", 392, [Assurance, Earthquake, Rock_Slide, Slash], 134, 110, 61, "Rock", "Dark")
Blastoise = pokemon("Blastoise", 346, [Surf, Hydro_Pump, Skull_Bash, Earthquake], 85, 100, 78, "Water")
Gengar = pokemon("Gengar", 304, [Shadow_Ball, Sludge_Bomb, Psychic, Splash], 130, 75, 110, "Ghost", "Poison")
Venusaur = pokemon("Venusaur", 349, [Skull_Bash, Sludge_Bomb, Solar_Beam, Splash], 100, 83, 80, "Grass", "Poison")
Snorlax = pokemon("Snorlax", 525, [Body_Slam, Hyper_Beam, Earthquake, Splash], 110, 110, 30, "Normal")
Dragonite = pokemon("Dragonite", 373, [Brick_Break, Wing_Attack, Splash, Dragon_Claw], 134, 100, 80, "Dragon", "Flying")
Mewtwo = pokemon("Mewtwo", 406, [Psychic, Brick_Break, Ice_Beam, Splash], 154, 90, 130, "Psychic")
Rayquaza = pokemon("Rayquaza", 404, [Aerial_Ace, Draco_Meteor, Earthquake, Ice_Beam], 150, 90, 95, "Dragon", "Flying")
Blaziken = pokemon("Blaziken", 349, [Flamethrower, Brick_Break, Aerial_Ace, Extreme_Speed], 120, 70, 80, "Fire", "Fighting")
Sceptile = pokemon("Sceptile", 327, [Leaf_Blade, Body_Slam, Brick_Break, Slash], 105, 85, 120, "Grass")


#items
hyperPot = item("Hyper Potion", 3)
superPot = item("Super Potion", 3)
potion = item("Potion", 3)
Xattack = item("X Attack", 1)
Xdefense = item("X Defense", 1)
Xspeed = item("X Speed", 1)
Ether = item("Ether", 1,)


#players
Saka = player(str(input("Enter your name: ")), [Blastoise, Pikachu, Venusaur, Dragonite, Mewtwo, Blaziken])
Computer = notPlayer("Computer", [Tyranitar, Charizard, Gengar, Snorlax, Sceptile, Rayquaza])

Saka.bag = [hyperPot, superPot, potion, Xattack, Xdefense, Xspeed, Ether]
#type-weakness dictionary

#attack effectiveness
#{"Normal":[], "Fire":[], 'Water':[], 'Electric':[], 'Grass':[], 'Ice':[], 'Fighting':[], 'Poison':[], 'Ground':[], 'Flying':[], 'Psychic':[], 'Bug':[], 'Rock':[], 'Ghost':[], 'Dragon':[], 'Dark':[], 'Steel':[]}

AttackSuperEffective = {"Normal":[], "Fire":['Grass', 'Ice', 'Bug', 'Steel'], 'Water':['Fire', 'Ground', 'Rock'], 'Electric':['Water', 'Flying'], 'Grass':['Water', 'Ground', 'Rock'], 'Ice':['Grass', 'Ground', 'Flying', 'Dragon'], 'Fighting':['Normal', 'Ice', 'Rock', 'Dark', 'Steel'], 'Poison':['Grass'], 'Ground':['Fire', 'Electric', 'Poison', 'Rock', 'Steel'], 'Flying':['Grass', 'Fighting', 'Bug'], 'Psychic':['Fighting', 'Poison'], 'Bug':['Grass', 'Psychic', 'Dark'], 'Rock':['Fire', 'Ice', 'Flying', 'Bug'], 'Ghost':['Psychic', 'Ghost'], 'Dragon':['Dragon'], 'Dark':['Psychic','Ghost'], 'Steel':['Ice', 'Rock']}
AttackIneffective = {"Normal":['Rock', 'Steel'], "Fire":["Fire",'Water', 'Rock', 'Dragon'], 'Water':['Water', 'Grass', 'Dragon'], 'Electric':['Electric', 'Grass', 'Dragon'], 'Grass':['Fire', 'Grass', 'Poison', 'Flying', 'Bug', 'Dragon', 'Steel'], 'Ice':['Ice', 'Fire', 'Water', 'Steel'], 'Fighting':['Poison', 'Flying', 'Psychic', 'Bug'],'Poison':['Poison', 'Ground', 'Rock', 'Ghost'],'Ground':['Grass', 'Bug'],'Flying':['Electric', 'Rock', 'Steel'], 'Psychic':['Psychic', 'Steel'], 'Bug':['Fire', 'Fighting', 'Poison', 'Flying', 'Ghost'], 'Rock':['Fighting', 'Ground', 'Steel'], 'Ghost':['Dark'], 'Dragon':['Steel'], 'Dark':['Fighting', 'Dark'], 'Steel':['Fire', 'Water', 'Electric', 'Steel']}
AttackNull = {"Normal":['Ghost'], "Fire":[], 'Water':[], 'Electric':['Ground'], 'Grass':[], 'Ice':[], 'Fighting':['Ghost'], 'Poison':['Steel'], 'Ground':['Flying'], 'Flying':[], 'Psychic':['Dark'], 'Bug':[], 'Rock':[], 'Ghost':['Normal'], 'Dragon':[], 'Dark':[], 'Steel':[]}

liveGame = True

while liveGame:
    if Computer.currentPoke == None:
        Computer.setCurrentPoke(str(Computer.pokeList[0]))

    if Saka.currentPoke == None:
        Saka.setCurrentPoke(Saka.pokeList[0].name)
        print(Saka.name, "chose", Saka.currentPoke)
        print(Computer.name, "chose", Computer.currentPoke)
        print(" ")

    else:
        compChoice = Computer.randomiser(3)
        if liveGame:
            gameJunction()
        else:
            break

