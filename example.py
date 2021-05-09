import classes as c
import refProcessing as r
import json
r.createTypes("data/DataMapEN.json")

print("Anubis")
anubis=r.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10')
print("cost : ",anubis.cost)
print("caveat : ",anubis.caveat.text)
print("1 : ",anubis.abilities[0].text)
print("2 : ",anubis.abilities[1].text)
