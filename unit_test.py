import ccftk
import json

dbEN=ccftk.DataBase("data/DataMapEN.json")

print("Caveat")
for i in range(35):
    for x in ["1","4"]:
        comp=str(i)+"."+x
        print(comp)
        ref="C.7.15-"+comp
        try:
            print(dbEN.refBareCard(ref))
        except:
            print("Fail")

print("ActCondition")
for i in range(23):
    for x in ["1","4"]:
        comp=str(i)+"."+x
        print(comp)
        ref="S/"+comp+"-0-0-0"
        try:
            print(dbEN.refBareCard(ref))
        except:
            print("Fail")

print("ActCost")
for i in range(21):
    for x in ["1","4"]:
        comp=str(i)+"."+x
        print(comp)
        ref="S/0-"+comp+"-0-0"
        try:
            print(dbEN.refBareCard(ref))
        except:
            print("Fail")

print("TargetSelection")
for i in range(20):
    for x in ["1","4"]:
        for y in ["1","4"]:
            comp=str(i)+"."+x+"."+y
            print(comp)
            ref="S/0-0-"+comp+"-0"
            try:
                print(dbEN.refBareCard(ref))
            except:
                print("Fail")

print("Effect")
for i in range(35):
    for t in ["1","4"]:
        for x in ["1","4"]:
            for y in ["1","4"]:
                comp=t+"-"+str(i)+"."+x+"."+y
                print(comp)
                ref="S/0-0-2."+comp
                try:
                    print(dbEN.refBareCard(ref))
                except:
                    print("Fail")
