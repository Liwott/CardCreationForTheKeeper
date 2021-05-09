import classes as c
import json
from lambdify import lambdify

def createTypes(dataMapFile):
    global types
    types={}
    file=open(dataMapFile)
    data=json.load(file)
    file.close()
    for compo in ["Caveat","ActCondition","ActCost","TargetSelection","Effect"]:
        types[compo]=ComponentType(compo,data[compo],data[compo+"Text"])

class ComponentType(object):
    def __init__(self,name,dataFile,textFile):
        self.name=name
        file=open(dataFile)
        self.data=json.load(file)
        file.close()
        file=open(textFile)
        self.text=json.load(file)
        file.close()
        self.isEffect=name=="Effect"

    def refComponent(self,ref):
        model,*strArgs=ref.split('.')
        data=self.data[model]
        vars=data['vars']
        if len(strArgs)!=len(vars):
            raise ValueError(self.name+' '+ref)
        args=map(int,strArgs)
        if self.isEffect:
            vars=[data['targetCost']]+vars
        cost=lambdify(vars,data["cost"])
        text=self.text[model]
        if self.isEffect:
            return c.EffectModel(text,cost,*args)
        else:
            return c.Component(text,cost,*args)

def refAbility(ref):
    actConditionRef,actCostRef,targetSelectionRef,*effectModelRefs=ref.split('-')
    arguments=[]
    arguments.append(types["ActCondition"].refComponent(actConditionRef))
    arguments.append(types["ActCost"].refComponent(actCostRef))
    arguments.append(types["TargetSelection"].refComponent(targetSelectionRef))
    for effectModelRef in effectModelRefs:
        arguments.append(types["Effect"].refComponent(effectModelRef))
    return c.Ability(*arguments)

def refBareCard(ref):
    if ref[0]=='S':
        ability=refAbility(ref[2:])
        return c.BareSpellCard(ability)
    elif ref[0]=='C':
        disableCreatureRef,*abilityRefs=ref.split('/')
        abilities=[]
        for abilityRef in abilityRefs:
            abilities.append(refAbility(abilityRef))
        fighting,caveatRef=disableCreatureRef.split('-')
        C,offense,defense=fighting.split('.')
        caveat=types["Caveat"].refComponent(caveatRef)
        return c.BareCreatureCard(int(offense),int(defense),caveat,*abilities)
    else:
        raise ValueError(ref[0]+" is not a valid card type")
