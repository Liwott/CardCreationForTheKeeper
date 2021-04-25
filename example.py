import classes as c

# def cost0(x,y,z):
#     return x*y*z
# type0=DataModel(cost0)
# type0.add_text("EN","lmao{1.s} lmao{2.s} lmao{3.s}")
# type0.add_text("FR","mdr{1.s} mdr{2.s} mdr{3.s}")
# data0=Data(type0,2,1,3)
# print(data0.cost)
# print(data0.text)

print("Spell Card : Black Death")
print("Activation Condition")
exActConditionModel=c.DataModel(lambda x : x)
def format_are(n):
    if n==1:
        return "is"
    else:
        return "are"
exActConditionModel.add_text("EN","""
Activate when at least {1} of your cards in play (excluding this card) {1.are} destroyed.""",{"are":format_are})
exActCondition=c.Data(exActConditionModel,1)
print("cost : ",exActCondition.cost)
print("EN : ",exActCondition.text["EN"])

print("Activation Cost")
exActCostModel=c.DataModel(lambda x: 6*x)
exActCostModel.add_text("EN","Sacrifice {1} card{1.s} in play chosen by an opponent of your choice.")
exActCost=c.Data(exActCostModel,2)
print("cost : ",exActCost.cost)
print("EN : ",exActCost.text["EN"])

print("Targetting")
exTargettingModel=c.DataModel(lambda x: x/2)
exTargettingModel.add_text("EN","Target up to {1} exhausted card{1.s} in play.")
exTargetting=c.Data(exTargettingModel,4)
print("cost : ",exTargetting.cost)
print("EN : ",exTargetting.text["EN"])

print("Effect")
exEffectDataModel=c.DataModel(lambda x: 8*x)
def format_alltargets(n):
    if n==1:
        return "the target"
    else:
        return "all targets"
exEffectDataModel.add_text("EN","Destroy {0.alltargets}.",{"alltargets":format_alltargets})
exEffectModel=c.EffectModel(exEffectDataModel)
exEffect=c.Effect(exEffectModel,exTargetting)
print("cost : ",exEffect.cost)
print("EN : ",exEffect.text["EN"])

print("Ability")
exAbility=c.Ability(exActCondition,exActCost,exTargetting,exEffectModel)
exAbility.create_text("EN")
print("cost : ",exAbility.cost)
print("EN : ",exAbility.text["EN"])
