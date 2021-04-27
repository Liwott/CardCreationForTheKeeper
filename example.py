import classes as c
c.TextArg.formatters={'s':{1:'',2:'s'},'are':{1:'is',2:'are'},'all_targets':{1:'the target',2:'all targets'}}

print("Spell Card : Black Death")
exActConditionModel=c.ComponentModel(lambda x : x,"Activate when at least {1} of your cards in play (excluding this card) {1.are} destroyed.")
exActCondition=c.Component(exActConditionModel,1)

exActCostModel=c.ComponentModel(lambda x: 6*x,"Sacrifice {1} card{1.s} in play chosen by an opponent of your choice.")
exActCost=c.Component(exActCostModel,2)

exTargetSelectionModel=c.ComponentModel(lambda x: x/2,"Target up to {1} exhausted card{1.s} in play.")
exTargetSelection=c.Component(exTargetSelectionModel,4)

exEffectComponentModel=c.ComponentModel(lambda x: 8*x,"Destroy {0.all_targets}.")
exEffectModel=c.EffectModel(exEffectComponentModel)
exEffect=c.Effect(exEffectModel,exTargetSelection)

exAbility=c.Ability(exActCondition,exActCost,exTargetSelection,exEffectModel)
print("cost : ",exAbility.cost)
print(exAbility.text)

print("Spell Card : Free Black Death")
exAbility=c.Ability(c.noComponent,c.noComponent,exTargetSelection,exEffectModel)
print("cost : ",exAbility.cost)
print(exAbility.text)
