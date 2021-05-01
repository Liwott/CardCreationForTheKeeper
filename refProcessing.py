import classes as c
import json

def lambdify(vars:list,function:str):
    """to be securised"""
    def lambdified(*args):
        res=function
        for var,arg in zip(vars,args):
            res=res.replace(var,str(arg))
        return evaluate(res)
    return lambdified

def evaluate(res:str):
    """to be replaced with a parser"""
    for carac in res:
        if carac not in ' 0123456789+-*/.()':
            raise ValueError(carac,function,vars,args)
    return eval(res)

def setLocale(locale):
    global typeCaveat, typeActCondition, typeActCost, typeTargetSelection, typeEffectModel
    typeCaveat=ComponentType('Caveat',locale)
    typeActCondition=ComponentType('ActCondition',locale)
    typeActCost=ComponentType('ActCost',locale)
    typeTargetSelection=ComponentType('TargetSelection',locale)
    typeEffectModel=ComponentType('Effect',locale)

class ComponentType(object):
    def __init__(self,name,locale):
        self.name=name
        file=open(name+'/data.json')
        self.data=json.load(file)
        file.close()
        file=open(name+'/'+locale+'.json')
        self.text=json.load(file)
        file.close()

    def refComponent(self,ref):
        model,*strArgs=ref.split('.')
        data=self.data[model]
        vars=data['vars']
        if len(strArgs)!=len(vars):
            print(strArgs,vars)
            raise ValueError(self.name+' '+ref)
        args=map(int,strArgs)
        cost=lambdify(vars,data["cost"])
        text=self.text[model]
        return c.Component(text,cost,*args)

    def refEffectModel(self,ref):
        model,*strArgs=ref.split('.')
        data=self.data[model]
        vars=data['vars']
        if len(strArgs)!=len(vars):
            raise ValueError(args)
        args=map(int,strArgs)
        vars=[data['targetCost']]+vars
        cost=lambdify(vars,data["cost"])
        text=self.text[model]
        return c.EffectModel(text,cost,*args)

class BareCardCreator(object):
    pass

def refAbility(ref):
    actConditionRef,actCostRef,targetSelectionRef,*effectModelRefs=ref.split('-')
    arguments=[]
    arguments.append(typeActCondition.refComponent(actConditionRef))
    arguments.append(typeActCost.refComponent(actCostRef))
    arguments.append(typeTargetSelection.refComponent(targetSelectionRef))
    for effectModelRef in effectModelRefs:
        arguments.append(typeEffectModel.refEffectModel(effectModelRef))
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
        caveat=typeCaveat.refComponent(caveatRef)
        return c.BareCreatureCard(int(offense),int(defense),caveat,*abilities)
    else:
        raise ValueError(ref[0]+" is not a valid card type")
