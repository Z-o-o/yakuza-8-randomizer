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
_IGNORED_IDS = ['1689', '3947', # Ink Sac
                '1848', '4531', '4532', # Sujimon 3 starters
                '1632', '1686', # Giant Shark/Squid
                '1717', '1708', # Support Bryce
                '1820', # Ebina 1st phase
                '1870', '1992', # Sojimaru
                '4754' # Jo Amon intended loss
                ]
bosses = []

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

    boss_ids = [
        '1006', # Sasaki
        '1009', # Tanaka
        '1017', '1884', '1885', '1886', # Asakura
        '1067', # Seiryu Ch. 1 Long Battle Boss - Kuwaki
        '1075', # Tomizawa
        '1081', '1226', '1255', '1325', '1381', '4559', # Yamai
        '1097', '4140', # Roman
        '1104', # Jose
        '1150', '1552', '1559', # Dwight
        '1238', # Wong Tou
        '1406', '1407', '1408', '1409', # Sawashiro
        '1482', # Daigo
        '1480', # Majima
        '1481', # Saejima
        '1509', # Arai (Ch.12 Long battle)
        '1504', # Makino (Ch.12 Long battle)
        '1518', # Narasaki
        '1547', # Takada
        '1686', # Giant Squid
        '1719', '1720', # Bryce
        '4757', # Ebina Sword Phase
        '1446', '1445', # Excavators
        '1977', # Komaki
        '1978', # Chau Ka Long
        '3338', '3341', '3343', '3342', '3344', '3345', # The Robo Michios
        '3357', # Utamaru
        '1912', # UFO Sojimaru
        '3362', '3363', '3364', '3361'  # Amons (Kazuya, Jiro, Sango, Jo)
    ]

    valid_enemies = []
    valid_enemy_indexes = []
    for enemy in enemies:
        if enemy.stats['reARMP_isValid'] == '1' and _IGNORED_IDS.count(enemy.id) == 0:
            valid_enemies.append(enemy.copy())
            valid_enemy_indexes.append(enemy.id)
        if boss_ids.count(enemy.id) != 0:
            new_enemy = enemy.copy()
            new_enemy.stats = enemy.stats.copy()
            bosses.append(new_enemy)

    random.shuffle(valid_enemies)
    return valid_enemies,valid_enemy_indexes

def get_enemy_list(enemies, valid_enemies, valid_enemy_indexes, boss_weight):
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
    
    boss_names = {}
    boss_names.update(dict.fromkeys(['1017', '1884', '1885', '1886'], 'Asakura'))
    boss_names.update(dict.fromkeys(['1081', '1226', '1255', '1325', '1381', '4559'], 'Yamai'))
    boss_names.update(dict.fromkeys(['1097', '4140'], 'Roman'))
    boss_names.update(dict.fromkeys(['1150', '1552', '1559'], 'Dwight'))
    boss_names.update(dict.fromkeys(['1406', '1407', '1408', '1409'], 'Sawashiro'))
    boss_names.update(dict.fromkeys(['1719', '1720'], 'Bryce'))
    boss_names.update(dict.fromkeys(['1446', '1445'], 'Excavators'))
    boss_names.update(dict.fromkeys(['3338', '3341', '3343', '3342', '3344', '3345'], 'Robo Michio'))
    boss_names.update(dict.fromkeys(['3362', '3363', '3364', '3361'], 'Amon'))
    boss_names['1067'] = 'Kuwaki'
    boss_names['1075'] = 'Tomizawa'
    boss_names['1104'] = 'Jose'
    boss_names['1238'] = 'Wong'
    boss_names['1482'] = 'Daigo'
    boss_names['1480'] = 'Majima'
    boss_names['1481'] = 'Saejima'
    boss_names['1518'] = 'Narasaki'
    boss_names['1547'] = 'Takada'
    boss_names['1686'] = 'Giant Squid'
    boss_names['4757'] = 'Ebina'
    boss_names['1977'] = 'Komaki'
    boss_names['1978'] = 'Chau Ka Long'
    boss_names['3357'] = 'Utamaru'
    boss_names['1912'] = 'UFO Sujimaru'
    boss_names['1509'] = 'Arai'
    boss_names['1006'] = 'Sasaki'
    boss_names['1009'] = 'Tanaka'
    boss_names['1504'] = 'Makino'
    # boss_names['3362'] = 'Kazuya Amon'
    # boss_names['3363'] = 'Jiro Amon'
    # boss_names['3364'] = 'Sango Amon'
    # boss_names['3361'] = 'Jo Amon'

    bosses_copy = bosses.copy()
    for i in range(_ENEMY_AMOUNT):
        if len(bosses_copy) == 0:
            # print('OUTTA BOSSES, RECHARGING\n')
            bosses_copy = bosses.copy()
        if valid_enemy_indexes.count(str(i)) != 0:
            next_enemy = None
            if random.randint(1, 100) <= boss_weight:
                next_enemy = bosses_copy.pop(random.randrange(-1, len(bosses_copy) - 1))
                # print("\nWE GOT BOSS: " + boss_names[next_enemy.id])
                for b in bosses_copy.copy():
                    if boss_names[b.id].__eq__(boss_names[next_enemy.id]):
                        # print("REMOVING: " + boss_names[b.id])
                        bosses_copy.pop(bosses_copy.index(b))
            else:
                next_enemy = valid_enemies.pop()
            enemy_list.append(next_enemy.copy())
        else:
            enemy_list.append(enemies[i].copy())

    for enemy in enemy_list:
        enemy.stats = enemy.stats.copy()


    for i in range(len(enemy_list)):
        enemy_list[i].stats['call_enemy_id'] = 0
        for scale in scales:
            enemy_list[i].stats[scale] = enemies[i].stats[scale]

    for enemy in enemy_list:
        if enemy.stats['call_enemy_id'] != 0:
            for e in enemy_list:
                if e.stats['enemy_level'] > (enemy.stats['enemy_level'] - 3) and e.stats['enemy_level'] < (enemy.stats['enemy_level'] + 1):
                    enemy.stats['call_enemy_id'] == int(e.id)

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
    languages = [r'de', r'en', r'es', r'fr', r'it', r'ja', r'ko', r'pt', r'ru', r'zh', r'zhs']
    for lang in languages:
        seeded_name = f'Enemy Randomizer seed - {seed}/'
        lang_directory = current_directory
        seeded_name = os.path.join(seeded_name, f'db.elvis.{lang}/')
        # seeded_name = os.path.join(seeded_name, 'en/')
        lang_directory = os.path.join(lang_directory, seeded_name)
        os.makedirs(lang_directory)
        shutil.copy(os.path.join(sys._MEIPASS, r"character_npc_soldier_personal_data.bin"), os.path.join(lang_directory, r"character_npc_soldier_personal_data.bin"))