import classes as c
import refProcessing as r
r.setLocale('EN')
import json
formattersFile=open('Formatters/EN.json')
c.TextArg.formatters=json.load(formattersFile)
formattersFile.close()

# print("Ability : Black Death")
# exActCondition=c.Component("Activate when at least {1} of your cards in play (excluding this card) {1.are} destroyed.",lambda x : x,1)
# exActCost=c.Component("Sacrifice {1} card{1.s} in play chosen by an opponent of your choice.",lambda x: 6*x,2)
# exTargetSelection=c.Component("Target up to {1} exhausted card{1.s} in play.",lambda x: x/2,4)
# exEffectModel=c.EffectModel("Destroy {0.all_targets}.",lambda t: 8*t)
# exEffect=c.Effect(exEffectModel,exTargetSelection)
# exAbility=c.Ability(exActCondition,exActCost,exTargetSelection,exEffectModel)
# print("cost : ",exAbility.cost)
# print(exAbility.text)
#
# print("Ability : Free Black Death")
# freeAbility=c.Ability(c.noComponent,c.noComponent,exTargetSelection,exEffectModel)
# print("cost : ",freeAbility.cost)
# print(freeAbility.text)
#
# print("Bare Spell Card : Black Death")
# exBareSpellCard=c.BareSpellCard(exAbility)
# print("cost : ",exBareSpellCard.cost)
#
# print("Bare Creature Card : Black Killer")
# exBareCreatureCard=c.BareCreatureCard(6,20,c.noComponent,exAbility)
# print("cost : ",exBareCreatureCard.cost)

print("Anubis")
anubis=r.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10')
print("cost : ",anubis.cost)
print("caveat : ",anubis.caveat.text)
print("1 : ",anubis.abilities[0].text)
print("2 : ",anubis.abilities[1].text)
