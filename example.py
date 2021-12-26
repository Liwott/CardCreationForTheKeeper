import ccftk
import json

dbEN=ccftk.DataBase("data/DataMapEN.json")
print("Anubis (EN)")
print(dbEN.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10'))
print("")

dbEN=ccftk.DataBase("data/DataMapEN.json")
file=open("sets/cards.json")
set=json.load(file)
file.close()
for name,ref in set.items():
    print(name+ " (EN)")
    print(dbEN.refBareCard(ref))
    print("")

# print("Anubis (EN)")
# print(dbEN.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10'))
# print("")

dbFR=ccftk.DataBase("data/DataMapFR.json")
print("Anubis (FR)")
print(dbFR.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10'))
print("")
