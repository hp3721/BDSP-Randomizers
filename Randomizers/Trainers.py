import UnityPy
import random
from PyQt5.QtWidgets import QTextEdit
import os
from pathlib import Path

#PathIDs inside Unity
#DO NOT CHANGE UNLESS GAME IS UPDATED
Trainer_Table = 676024375065692598
modPath = "romfs/Data/StreamingAssets/AssetAssistant/Dpr"
yuzuModPath = "StreamingAssets/AssetAssistant/Dpr"
pathList = [Trainer_Table]

#Level Increase
LevelIncrease = 1

##Gym Leaders, Rival 3rd fight onwards, E4, Champion, Galactic Admins
rivalBattles = [351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 481, 493, 494, 663, 664, 665, 666, 667, 668]
gymLeaders = [175, 179, 240, 241, 242, 243, 244, 245, 676, 677, 678, 679, 680, 681, 682, 683]
eliteFour = [185, 186, 187, 188, 696, 697, 698, 699, 701, 702, 703, 704]
champion = [191, 700, 705]
galacticAdmins = [220, 308, 309, 310, 311, 312, 313, 314, 401]

importantList = rivalBattles + gymLeaders + eliteFour + champion + galacticAdmins


def getAbilityList():
    
    filepath = "Resources//ability.txt"
    with open(filepath, "r") as f:
        return f.read().splitlines()
    
def getMoveList():
    
    filepath = "Resources//moves.txt"
    tempFilepath = "Resources//tempMoveIndex.txt"
    if os.path.exists(tempFilepath):
        with open(tempFilepath, "r") as f:
            return f.read().splitlines()
    else:
        with open(filepath, "r") as f:
            return f.read().splitlines()
        
def getAverageLevel(trainer):
    levelList = []
    for pokeNum in range(1, 7):
        level = trainer["P"f"{pokeNum}Level"]
        if level > 0:
            levelList.append(level)
    if len(levelList) > 0:
        return sum(levelList)/len(levelList)
    else:
        return 0

def RandomizeTrainers(text, minImportant, minBasic, romFSPath, scaleWithLevel=True):
    # make sure masterdatas is in same folder
    cwd = os.getcwd()
    
    abilityList = getAbilityList()
    moveList = getMoveList()
    
    src = "masterdatas"
    
    outputPath = os.path.join(cwd, "mods", modPath)

    if os.path.exists(outputPath) and os.path.isfile(os.path.join(outputPath, src)):
        os.chdir(outputPath)
        env = UnityPy.load(os.path.join(outputPath, src))
        
    elif os.path.exists(os.path.join(romFSPath, yuzuModPath)) and os.path.isfile(os.path.join(romFSPath, yuzuModPath, src)):
        os.chdir(romFSPath)
        env = UnityPy.load(os.path.join(romFSPath, yuzuModPath, src))
    else:
        text.append("ERROR: masterdatas not found ")
        return

    extract_dir = "Walker"
    text.append("Trainers Loaded.")
    
    
    for obj in env.objects:
        if obj.path_id in pathList:
            tree = obj.read_typetree()

            #TrainerPoke
            if tree['m_Name'] == "TrainerTable":
                for dic in tree['TrainerPoke']:
                    
                    trainerID = dic["ID"]
                    
                    ##Used to increase the amount of pokemon in party
                    if scaleWithLevel:
                        averageLevel = getAverageLevel(dic)
                        if trainerID in importantList:
                            pokeAmount = minImportant
                        else:
                            pokeAmount = max(int(averageLevel/10), minBasic)
                            pokeAmount = min(pokeAmount, 6) ##Max at 6 pokemon
                        ##For all pokemon under the average level, adds a new pokemon
                        for pokeNum in range(1, pokeAmount + 1):
                            if dic["P"f"{pokeNum}Level"] < averageLevel:
                                dic["P"f"{pokeNum}Level"] = averageLevel
                    
                    for pokeNum in range(1, 7):
                        # print(dic["P"f"{pokeNum}Level"])
                        level = dic["P"f"{pokeNum}Level"]
                        if level > 0:
                            #Increases level by 50% with a cap at level 100
                            dic["P"f"{pokeNum}Level"] = int(dic["P"f"{pokeNum}Level"] * LevelIncrease)
                            if dic["P"f"{pokeNum}Level"] > 100:
                                dic["P"f"{pokeNum}Level"] = 100
                            newPokemon = random.randint(1,493)
                            dic["P"f"{pokeNum}MonsNo"] = newPokemon
                            
                            ##Ability Selection
                            dic["P"f"{pokeNum}Tokusei"] = int(random.choice(abilityList[newPokemon-1].split(",")[1:]))
                            
                            possibleMoves = []
                            monMoveList = moveList[newPokemon-1].split(",")
                            for i in range(int(len(monMoveList)/2)):
                                if int(monMoveList[i*2]) < dic["P"f"{pokeNum}Level"]:
                                    possibleMoves.append(int(monMoveList[i*2 + 1]))
                                    
                            # print(possibleMoves)
                            ##Moves 1 through 4
                            amountOfMoves = min(4, len(possibleMoves))
                            for moveNum in range(1, amountOfMoves + 1):
                                dic["P"f"{pokeNum}Waza"f"{moveNum}"] = possibleMoves[-moveNum]
                                
                            #Sets the rest of the pokemons moves to 0
                            for moveNum in range(amountOfMoves + 1, 5):
                                dic["P"f"{pokeNum}Waza"f"{moveNum}"] = 0
                            
                            # Set all IVs to 31 for maximum difficulty :P
                            dic["P"f"{pokeNum}TalentHp"] = 31
                            dic["P"f"{pokeNum}TalentAtk"] = 31
                            dic["P"f"{pokeNum}TalentDef"] = 31
                            dic["P"f"{pokeNum}TalentSpAtk"] = 31
                            dic["P"f"{pokeNum}TalentSpDef"] = 31
                            dic["P"f"{pokeNum}TalentAgi"] = 31
                               
                obj.save_typetree(tree)
                
            else:
                print("Error use different path_id")
                
                
    text.append("Trainers Randomized.")                
    # saving an edited file
    # apply modifications to the objects
    # don't forget to use data.save()
        # ...
        # 
        # 
    #This output is compressed, thanks to Copycat#8110        
    # outputPath = os.path.join(cwd, "mods", modPath)
    
    if not os.path.exists(outputPath):
        os.makedirs(outputPath, 0o666)
        
    os.chdir(outputPath)
    
    with open("masterdatas", "wb") as f:
        f.write(env.file.save(packer = (64,2)))
    text.append("Trainers Saved.")
    
    os.chdir(cwd)
                

##Used for updating movesets when trainers aren't randomized                
def updateMovesets(text, romFSPath):
    
    moveList = getMoveList()
    
    src = "masterdatas"
    
    cwd = os.getcwd()
    
    outputPath = os.path.join(cwd, "mods", modPath)

    if os.path.exists(outputPath) and os.path.isfile(os.path.join(outputPath, src)):
        os.chdir(outputPath)
        env = UnityPy.load(os.path.join(outputPath, src))
        
    elif os.path.exists(os.path.join(romFSPath, yuzuModPath)) and os.path.isfile(os.path.join(romFSPath, yuzuModPath, src)):
        os.chdir(romFSPath)
        env = UnityPy.load(os.path.join(romFSPath, yuzuModPath, src))
    else:
        text.append("ERROR: masterdatas not found ")
        return
    
    for obj in env.objects:
        if obj.path_id in pathList:
            tree = obj.read_typetree()

            #TrainerPoke
            if tree['m_Name'] == "TrainerTable":
                for dic in tree['TrainerPoke']:
                    for pokeNum in range(1, 7):
                        level = dic["P"f"{pokeNum}Level"]
                        if level > 0:
                            newPokemon = dic["P"f"{pokeNum}MonsNo"]
                            
                            possibleMoves = []
                            monMoveList = moveList[newPokemon-1].split(",")
                            for i in range(int(len(monMoveList)/2)):
                                if int(monMoveList[i*2]) < dic["P"f"{pokeNum}Level"]:
                                    possibleMoves.append(int(monMoveList[i*2 + 1]))
                                    
                            # print(possibleMoves)
                            ##Moves 1 through 4
                            amountOfMoves = min(4, len(possibleMoves))
                            for moveNum in range(1, amountOfMoves + 1):
                                dic["P"f"{pokeNum}Waza"f"{moveNum}"] = possibleMoves[-moveNum]
                                
                            #Sets the rest of the pokemons moves to 0
                            for moveNum in range(amountOfMoves + 1, 5):
                                dic["P"f"{pokeNum}Waza"f"{moveNum}"] = 0  
                
                obj.save_typetree(tree)
                                  
    # saving an edited file
    # apply modifications to the objects
    # don't forget to use data.save()
        # ...
        # 
        # 
    #This output is compressed, thanks to Copycat#8110        
    # outputPath = os.path.join(cwd, "mods", modPath)
    
    if not os.path.exists(outputPath):
        os.makedirs(outputPath, 0o666)
        
    os.chdir(outputPath)
    
    with open("masterdatas", "wb") as f:
        f.write(env.file.save(packer = (64,2)))
    
    os.chdir(cwd)