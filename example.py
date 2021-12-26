import ccftk

dbEN=ccftk.DataBase("data/DataMapEN.json")
print("Anubis (EN)")
print(dbEN.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10'))
print("")

dbFR=ccftk.DataBase("data/DataMapFR.json")
print("Anubis (FR)")
print(dbFR.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10'))
print("")
