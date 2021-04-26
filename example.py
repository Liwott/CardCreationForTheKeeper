import classes as c

print("Spell Card : Black Death")
# print("Activation Condition")
def format_are(n):
    if n==1:
        return "is"
    else:
        return "are"
exActConditionModel=c.DataModel(lambda x : x,"Activate when at least {1} of your cards in play (excluding this card) {1.are} destroyed.",{"are":format_are})
exActCondition=c.Data(exActConditionModel,1)
# print("cost : ",exActCondition.cost)
# print("EN : ",exActCondition.text)

# print("Activation Cost")
exActCostModel=c.DataModel(lambda x: 6*x,"Sacrifice {1} card{1.s} in play chosen by an opponent of your choice.")
exActCost=c.Data(exActCostModel,2)
# print("cost : ",exActCost.cost)
# print("EN : ",exActCost.text)

# print("Targetting")
exTargettingModel=c.DataModel(lambda x: x/2,"Target up to {1} exhausted card{1.s} in play.")
exTargetting=c.Data(exTargettingModel,4)
# print("cost : ",exTargetting.cost)
# print("EN : ",exTargetting.text)

# print("Effect")
def format_alltargets(n):
    if n==1:
        return "the target"
    else:
        return "all targets"
exEffectDataModel=c.DataModel(lambda x: 8*x,"Destroy {0.alltargets}.",{"alltargets":format_alltargets})
exEffectModel=c.EffectModel(exEffectDataModel)
exEffect=c.Effect(exEffectModel,exTargetting)
# print("cost : ",exEffect.cost)
# print("EN : ",exEffect.text)

# print("Ability")
exAbility=c.Ability(exActCondition,exActCost,exTargetting,exEffectModel)
print("cost : ",exAbility.cost)
print(exAbility.text)

print("Spell Card : Free Black Death")
exAbility=c.Ability(c.noData,c.noData,exTargetting,exEffectModel)
print("cost : ",exAbility.cost)
print(exAbility.text)
