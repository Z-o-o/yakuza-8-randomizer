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
import skill_data

_SKILL_AMOUNT = 2746
_IGNORED_IDS = [960, 1078, 1325, 1326, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1572, 2517, 2519, 2521, 1510, #Tag Team Skills
                1285, 1286, 1287, 253, 254, 255, 256 # Trenchcoat harraser moves
                ]

# We need to store our current location to generate the RMM folder structure where the .exe
# was run from, since the .exe uses the root's temp folder for processing.
def open_data_file():
    os.chdir(sys._MEIPASS)
    file = open(r'rpg_skill.bin.json', r'r', encoding="utf8")
    return file


def parse_skills():
    # skills = []
    # for skill_id in range(_SKILL_AMOUNT):
    #     # if ((skill_id/_SKILL_AMOUNT) * 100) % 10 == 0:
    #     #     print(str((skill_id/_SKILL_AMOUNT) * 100) + "% Complete")
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
    skills = skill_data.skills
    return skills

def shuffle_skills(skills, seed_value=None):
    random.seed(seed_value)
    mp_cost_og = []
    for skill in skills:
        mp_cost_og.append(skill.stats['need_heat'])

    valid_skills = []
    valid_skills_indexes = []
    for skill in skills:
        if skill.stats['reARMP_isValid'] == '1' and 'name' in skill.stats and skill.stats['category'] != 11 and skill.stats['use_cond'] != 30 and _IGNORED_IDS.count(int(skill.id)) == 0 and skill.stats['category'] != 8:
            valid_skills.append(skill.copy())
            valid_skills_indexes.append(skill.id)

    random.shuffle(valid_skills)
    return mp_cost_og,valid_skills,valid_skills_indexes

def get_skills_list(skills, valid_skills, valid_skills_indexes, mp_cost_og, empty_explain=False):
    skills_list = []

    for i in range(_SKILL_AMOUNT):
        if valid_skills_indexes.count(str(i)) != 0:
            next_skill = valid_skills.pop()
            skills_list.append(next_skill)
        else:
            skills_list.append(skills[i])
        
    for i in range(len(skills_list)):
        if mp_cost_og[i] == 0:
            skills_list[i].stats['need_heat'] = 0
        if mp_cost_og[i] > 0 and skills_list[i].stats['need_heat'] == 0:
            skills_list[i].stats['need_heat'] = random.randrange(5, 70)

    for skill in skills_list:
        skill.stats = skill.stats.copy()

    for skill in skills_list:
        if skill.stats['icon_pattern_id'] < 33:
            skill.stats['ui_category'] = 1
        elif skill.stats['icon_pattern_id'] > 32 and skill.stats['icon_pattern_id'] < 52 or skill.stats['icon_pattern_id'] > 58:
            skill.stats['ui_category'] = 3
            skill.stats["prohibit_equip_item_add_attribute"] = 1
        else:
            skill.stats['ui_category'] = 2
            skill.stats["prohibit_equip_item_add_attribute"] = 1

    if empty_explain:
        for skill in skills_list:
            skill.stats['explain'] = ''

    return skills_list

def generate_JSON(skills_list):
    file_read = open(r'rpg_skill.bin.json', r'r', encoding="utf8")
    file_write = open(r'rpg_skill.json', r'w', encoding="utf8")

    line = ""
    while True:
        line = file_read.readline()
        if "\"0\": {" in line:
            break
        file_write.write(line)
    file_read.close()
    for i in range(_SKILL_AMOUNT):
        end_comma = ",\n"
        if i == _SKILL_AMOUNT - 1:
             end_comma = "\n"
        data = str(skills_list[i].stats).replace("'", '"').replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false")
        data = data.replace('""Lights, camera, traction!"', '"\\"Lights, camera, traction!\\"')
        data = data.replace('true Grit', 'True Grit')
        data = '"' + str(skills_list[i].name) + "\": {\n      " + data[1:]
        data = data[:-1] + "\n    }\n  }"
        data = data.replace(',"', ',\n      "')
        file_write.write("  \"" + str(i) + "\": {\n    " + data + end_comma)
    file_write.write("}")
    file_write.close()

def repackage():
    import SkillreARMP
    SkillreARMP.rebuildFile()

def generate_RMM(current_directory, seed):
    seeded_name = f'Skill Randomizer seed - {seed}/'
    seeded_name = os.path.join(seeded_name, 'db.elvis.en/')
    # seeded_name = os.path.join(seeded_name, 'en/')
    current_directory = os.path.join(current_directory, seeded_name)
    os.makedirs(current_directory)
    shutil.copy(os.path.join(sys._MEIPASS, r"rpg_skill.bin"), os.path.join(current_directory, r"rpg_skill.bin"))