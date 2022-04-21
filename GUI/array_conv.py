import json


with open("out.json","r") as fp:
    obj = json.load(fp)

p1 = []
p2 = []

for i in range(len(obj)):
    if i % 2 == 0:
        p1.append(obj[i])
    else:
        p2.append(obj[i])

print(p1,p2)

new_list = {"p1":p1,"p2":p2}

with open("formatted_pos.json","w+") as fp:
    json.dump(new_list,fp)
