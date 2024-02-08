#!/usr/bin/env python3
import ijson
import json
import re
import random
import sys
import msvcrt as m
import os
import shutil
import time
import enemy_data

_ENEMY_AMOUNT = 5047
_IGNORED_IDS = [
                ]

# We need to store our current location to generate the RMM folder structure where the .exe
# was run from, since the .exe uses the root's temp folder for processing.
def open_data_file():
    os.chdir(sys._MEIPASS)


def parse_enemies():
    # skills = []
    # for skill_id in range(_ENEMY_AMOUNT):
    #     # if ((skill_id/_ENEMY_AMOUNT) * 100) % 10 == 0:
    #     #     print(str((skill_id/_ENEMY_AMOUNT) * 100) + "% Complete")
    #     f.seek(0)
    #     skill = Skill('', '', {})
    #     objects = ijson.items(f, str(skill_id))
    #     for stat in objects:
    #         print("Skill ID = " + str(skill_id) + ": \n")
    #         skill.id = skill_id
    #         skill.name = list(stat.keys())[0]
    #         """replace(": '", ": \"").replace("',", '\",')"""
    #         data = str(stat[list(stat.keys())[0]]).replace("'", '"').replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false")
    #         data = data.replace('""Lights, camera, traction!"', '"\\"Lights, camera, traction!\\"')
    #         print(data + '\n\n')
    #         # data = data.replace('""We Are the Globe""', '"\\"We Are the Globe\\""').replace('""Scar Me""', '"\\"Scar Me\\""').replace('""Relax""', '"\\"Relax\\""').replace('""Your Wackiest Dreams""', '"\\"Your Wackiest Dreams\\""').replace('""Endless Desire""', '"\\"Endless Desire\\""').replace('""Those Who Protect""', '"\\"Those Who Protect\\""').replace('""Be My Shelter""', '"\\"Be My Shelter\\""')
    #         skill.stats = json.loads(data)
    #         #print("This didn't fail")
    #     skills.append(skill)
    # f.close()
    enemies = enemy_data.enemies
    return enemies

def shuffle_enemies(enemies, seed_value=None):
    random.seed(seed_value)

    valid_enemies = []
    valid_enemy_indexes = []
    for enemy in enemies:
        if enemy.stats['reARMP_isValid'] == '1' and _IGNORED_IDS.count(int(enemy.id)) == 0:
            valid_enemies.append(enemy.copy())
            valid_enemy_indexes.append(enemy.id)

    random.shuffle(valid_enemies)
    return valid_enemies,valid_enemy_indexes

def get_enemy_list(enemies, valid_enemies, valid_enemy_indexes):
    enemy_list = []

    scales = ["mission",
              "group",
              "enemy_level", 
              "hp_ratio", 
              "hp", "mp", 
              "attack", "defence", "sp_attack", "sp_def", 
              "dodge", "accuracy", "base_wait", 
              "exp_point", "job_exp_point", "money_point", "money_drop_ratio", 
              "first_wait_ratio",
              "enemy_level_2",
              "hp_ratio_2",
              "exp_point_2",
              "job_exp_point_2",
              "enemy_level_3",
              "hp_ratio_3",
              "exp_point_3",
              "job_exp_point_3"]

    for i in range(_ENEMY_AMOUNT):
        if valid_enemy_indexes.count(str(i)) != 0:
            next_enemy = valid_enemies.pop()
            enemy_list.append(next_enemy.copy())
        else:
            enemy_list.append(enemies[i].copy())

    for enemy in enemy_list:
        enemy.stats = enemy.stats.copy()

    for i in range(len(enemy_list)):
        for scale in scales:
            enemy_list[i].stats[scale] = enemies[i].stats[scale]

    return enemy_list

def generate_JSON(enemy_list):
    file_read = open(r'character_npc_soldier_personal_data.bin.json', r'r', encoding="utf8")
    file_write = open(r'character_npc_soldier_personal_data.json', r'w', encoding="utf8")

    line = ""
    while True:
        line = file_read.readline()
        if "\"0\": {" in line:
            break
        file_write.write(line)
    file_read.close()
    for i in range(_ENEMY_AMOUNT):
        end_comma = ",\n"
        if i == _ENEMY_AMOUNT - 1:
             end_comma = "\n"
        data = str(enemy_list[i].stats).replace("'", '"').replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false")
        data = '"' + str(enemy_list[i].name) + "\": {\n      " + data[1:]
        data = data[:-1] + "\n    }\n  }"
        data = data.replace(',"', ',\n      "')
        file_write.write("  \"" + str(i) + "\": {\n    " + data + end_comma)
    file_write.write("}")
    file_write.close()

def repackage():
    import EnemyreARMP
    EnemyreARMP.rebuildFile()

def generate_RMM(current_directory, seed):
    seeded_name = f'Enemy Randomizer seed - {seed}/'
    seeded_name = os.path.join(seeded_name, 'db.elvis.en/')
    # seeded_name = os.path.join(seeded_name, 'en/')
    current_directory = os.path.join(current_directory, seeded_name)
    os.makedirs(current_directory)
    shutil.copy(os.path.join(sys._MEIPASS, r"character_npc_soldier_personal_data.bin"), os.path.join(current_directory, r"character_npc_soldier_personal_data.bin"))