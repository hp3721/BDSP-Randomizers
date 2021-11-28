#py -m pip install UnityPy
import UnityPy
import random
from PyQt5.QtWidgets import QTextEdit
import os
from pathlib import Path

#PathIDs inside Unity
#DO NOT CHANGE UNLESS GAME IS UPDATED
shopTable = 5586546078177307292
modPath = "romfs/StreamingAssets/AssetAssistant/Dpr"
pathList = [shopTable]

def uselessItemRemover(itemNo):
    
    if itemNo > 428: ##Explorer kit
        return True
    elif itemNo >= 159 and itemNo <= 212: #Figy Berry to Rowap Berry
        return True
    elif itemNo >= 137 and itemNo <= 148: #Grass mail to Brick mail
        return True
    elif itemNo >= 113 and itemNo <= 134: #Braces and Arceus Plates
        return True
    elif itemNo in [236, 155, 70, 71]: #Light ball, Oran berry, Shoal Salt, and Shoal Shell
        return True
    elif itemNo >= 95 and itemNo <= 98: #Mulches for Berry Planting
        return True
    elif itemNo >= 256 and itemNo <= 264: #Lucky punch to Yellow scarf
        return True
    else:
        return False
    
def generateRandom():
    lowRange = 1
    highRange = 327
    
    itemNo = random.randrange(lowRange, highRange)
    ##while item is useless generate a different item
    while uselessItemRemover(itemNo):
        itemNo = random.randrange(lowRange, highRange)
    return itemNo
    
def RandomizeShops(text):


    # Checks if romfs path already exist
    cwd = os.getcwd()
    
    if os.path.exists(modPath) == True:
        if os.path.isfile(modPath + '/masterdatas') == True:
            os.chdir(modPath)
        
    src = "masterdatas"
    
    shopList = ["FS", "FixedShop"]
    
    env = UnityPy.load(src)
    extract_dir = "Walker"
    text.append("Items Shop Loaded.")

    for obj in env.objects:
        if obj.path_id in pathList:
            tree = obj.read_typetree()
            print(tree)
            if tree['m_Name'] == "ShopTable":
                for shop in shopList:
                    for item in tree[shop]:
                        item["ItemNo"] = generateRandom()
                    
            obj.save_typetree(tree)
        else:
            print("Error use different path_id")
            
    text.append("Items Shop Randomized.")                
    # saving an edited file
    # apply modifications to the objects
    # don't forget to use data.save()
        # ...
        # 
        # 
    #This output is compressed, thanks to Copycat#8110
    if cwd == os.getcwd():
        Path(modPath).mkdir(parents=True, exist_ok=True)
        os.chdir(modPath)
        
    with open("masterdatas", "wb") as f:
        f.write(env.file.save(packer = (64,2)))
    text.append("Trainers Saved.")
    
    os.chdir(cwd)