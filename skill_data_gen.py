import ijson
import json

_SKILL_AMOUNT = 2746

class Skill:
    def __init__(self, id, name, stats):
        self.id = id
        self.name = name
        self.stats = stats
    def copy(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

f = open(r'rpg_skill.bin.json', r'r', encoding="utf8")

skills = []
for skill_id in range(_SKILL_AMOUNT):
    if int((skill_id/_SKILL_AMOUNT) * 100) % 10 == 0:
        print(str((skill_id/_SKILL_AMOUNT) * 100) + "% Complete\n")
    f.seek(0)
    skill = Skill('', '', {})
    objects = ijson.items(f, str(skill_id))
    data = ""
    for stat in objects:
        #print("Skill ID = " + str(skill_id) + ": \n")
        skill.id = skill_id
        skill.name = list(stat.keys())[0]
        """replace(": '", ": \"").replace("',", '\",')"""
        data = str(stat[list(stat.keys())[0]]).replace("'", '"').replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false")
        data = data.replace('""Lights, camera, traction!"', '"\\"Lights, camera, traction!\\"')
        #print(data + '\n\n')
        # data = data.replace('""We Are the Globe""', '"\\"We Are the Globe\\""').replace('""Scar Me""', '"\\"Scar Me\\""').replace('""Relax""', '"\\"Relax\\""').replace('""Your Wackiest Dreams""', '"\\"Your Wackiest Dreams\\""').replace('""Endless Desire""', '"\\"Endless Desire\\""').replace('""Those Who Protect""', '"\\"Those Who Protect\\""').replace('""Be My Shelter""', '"\\"Be My Shelter\\""')
        skill.stats = json.loads(data)
        #print("This didn't fail")
    skill = "Skill(\""+str(skill.id) + "\", \"" + str(skill.name) + "\", " + str(data) + ")"
    skills.append(skill)
f.close()

print("Done Parsing.")

file_write = open(r'skill_data.py', r'w', encoding="utf8")

file_write.write("class Skill:\n\tdef __init__(self, id, name, stats, new_stats):\n\t\tself.id = id\n\t\tself.name = name\n\t\tself.stats = stats\n\t\tself.new_stats = new_stats\n\tdef copy(self):\n\t\tobj = type(self).__new__(self.__class__)\n\t\tobj.__dict__.update(self.__dict__)\n\t\treturn obj\n\n")
file_write.write("skills0 = [\n\t")
for i in range(_SKILL_AMOUNT):
    if i % 100 == 0:
        file_write.write(']\n\nskills' + str(i) + " = [\n\t")
    file_write.write(str(skills[i]) + ",\n\t")
file_write.write(']')