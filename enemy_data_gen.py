import ijson
import json
import time

_ENEMYCOUNT = 5047

class Enemy:
    def __init__(self, id, name, stats):
        self.id = id
        self.name = name
        self.stats = stats
    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

start = time.time()

f = open(r'character_npc_soldier_personal_data.bin.json', r'r', encoding="utf8")

enemies = []
last_percent = 0
for enemy_id in range(_ENEMYCOUNT):
    if int((enemy_id/_ENEMYCOUNT) * 100) > last_percent:
        last_percent = int((enemy_id/_ENEMYCOUNT) * 100)
        if last_percent % 10 == 0:
            print(str(last_percent) + "% Complete\n")
    f.seek(0)
    enemy = Enemy('', '', {})
    objects = ijson.items(f, str(enemy_id))
    data = ""
    for stat in objects:
        enemy.id = enemy_id
        enemy.name = list(stat.keys())[0]
        data = str(stat[list(stat.keys())[0]]).replace("'", '"').replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false")
        enemy.stats = json.loads(data)
    enemy = "Enemy(\""+str(enemy.id) + "\", \"" + str(enemy.name) + "\", " + str(data) + ")"
    enemies.append(enemy)
f.close()

print("Done Parsing.")

file_write = open(r'enemy_data.py', r'w', encoding="utf8")

file_write.write("class Enemy:\n\tdef __init__(self, id, name, stats):\n\t\tself.id = id\n\t\tself.name = name\n\t\tself.stats = stats\n\tdef __copy__(self):\n\t\tobj = type(self).__new__(self.__class__)\n\t\tobj.__dict__.update(self.__dict__)\n\t\treturn obj\n\n")
file_write.write("enemy0 = [\n\t")
enemy_lists = []
for i in range(_ENEMYCOUNT):
    if i % 100 == 0:
        file_write.write(']\n\nenemy' + str(i) + " = [\n\t")
        enemy_lists.append(i)
    file_write.write(str(enemies[i]) + ",\n\t")
file_write.write(']')

file_write.write('enemies = ')

for enemy in enemy_lists:
    file_write.write('enemy' + str(enemy) + " + ")

file_write.close()

total_time = time.time() - start

print("Done after " + str(int(total_time / 60)) + "minutes")