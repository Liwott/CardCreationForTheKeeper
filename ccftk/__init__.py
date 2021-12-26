import math
import json

class DataBase(object):
    def __init__(self,dataMapFile):
        types={}
        file=open(dataMapFile)
        data=json.load(file)
        file.close()
        file=open(data["Formatters"])
        formatters=json.load(file)
        file.close()
        for compo in ["Caveat","ActCondition","ActCost","TargetSelection","Effect"]:
            file=open(data[compo])
            dataDict=json.load(file)
            file.close()
            file=open(data[compo+"Text"])
            textDict=json.load(file)
            file.close()
            types[compo]=ComponentType(compo,dataDict,textDict,formatters)
        self.types=types

    def refAbility(self,ref):
        actConditionRef,actCostRef,targetSelectionRef,*effectModelRefs=ref.split('-')
        arguments=[]
        arguments.append(self.types["ActCondition"].refComponent(actConditionRef))
        arguments.append(self.types["ActCost"].refComponent(actCostRef))
        arguments.append(self.types["TargetSelection"].refComponent(targetSelectionRef))
        for effectModelRef in effectModelRefs:
            arguments.append(self.types["Effect"].refComponent(effectModelRef))
        return Ability(*arguments)

    def refBareCard(self,ref):
        if ref[0]=='S':
            ability=self.refAbility(ref[2:])
            return BareSpellCard(ability)
        elif ref[0]=='C':
            disabledCreatureRef,*abilityRefs=ref.split('/')
            abilities=[]
            for abilityRef in abilityRefs:
                abilities.append(self.refAbility(abilityRef))
            fighting,caveatRef=disabledCreatureRef.split('-')
            C,offense,defense=fighting.split('.')
            caveat=self.types["Caveat"].refComponent(caveatRef)
            return BareCreatureCard(int(offense),int(defense),caveat,*abilities)
        else:
            raise ValueError(ref[0]+" is not a valid card type")

class ComponentType(object):
    def __init__(self,name,dataDict,textDict,formatters):
        self.data=dataDict
        self.text=textDict
        self.formatters=formatters
        self.isEffect=name=="Effect"

    def refComponent(self,ref):
        model,*strArgs=ref.split('.')
        cost=self.data[model]['cost']
        text=self.text[model]
        args=map(int,strArgs)
        if self.isEffect:
            return EffectModel(text,self.formatters,cost,*args)
        else:
            return Component(text,self.formatters,cost,*args)

class Component(object):
    def __init__(self,text:str,formatters:dict,cost:str,*args):
        self.args=args
        self.cost=evaluate(cost,None,*args)
        textArgs=map(lambda x:TextArg(x,formatters),list(args))
        if text=="":
            # avoid too much space
            self.text=text
        else:
            # argument 0 is empty and sould not be used in formatting
            self.text=text.format(None,*textArgs)+' '

class EffectModel(object):
    def __init__(self,text:str,formatters:dict,cost,*args):
        self.text=text
        self.formatters=formatters
        self.cost=cost
        self.args=args

class Effect(object):
    def __init__(self,effectModel,targetSelection):
        args=effectModel.args
        self.args=args
        self.cost=evaluate(effectModel.cost,targetSelection.cost,*args)
        textModel=effectModel.text
        formatters=effectModel.formatters
        if len(targetSelection.args)==0:
            # produces a non-empty argument for targets that should crash if it is called
            textArgs=[None]+list(map(lambda x:TextArg(x,formatters),list(args)))
        else:
            # the first argument of the targetSelection is considered to be the number of targets
            textArgs=map(lambda x:TextArg(x,formatters),[targetSelection.args[0]]+list(args))
        self.text=textModel.format(*textArgs)

class Ability(object):
    def __init__(self, actCondition,actCost,targetSelection, *effectModels):
        self.actCondition=actCondition
        self.actCost=actCost
        self.targetSelection=targetSelection
        effects=[]
        cost=0
        for effectModel in effectModels:
            effect=Effect(effectModel,targetSelection)
            effects.append(effect)
            cost+=effect.cost
        self.effects=effects
        cost-=actCondition.cost
        cost-=actCost.cost
        self.cost=max(1,cost)
        text=""
        text+=self.actCondition.text
        text+=self.actCost.text
        text+=self.targetSelection.text
        for effect in self.effects:
            text+=effect.text
        self.text=text

class BareSpellCard(object):
    def __init__(self,ability):
        self.ability=ability
        self.cost=max(1,math.ceil(ability.cost))

    def __str__(self):
        return "cost : "+str(self.cost)+"\n"+self.ability.text

class BareCreatureCard(object):
    def __init__(self,offense:int,defense:int,caveat,*abilities):
        self.offense=offense
        self.defense=defense
        self.caveat=caveat
        self.abilities=abilities
        cost=max(0,offense+(defense/5)-caveat.cost)
        for ability in abilities:
            cost+=ability.cost
        self.cost=max(1,math.ceil(cost))

    def __str__(self):
        string="cost : "+str(self.cost)+"\noffense : "+str(self.offense)+"\ndefense : "+str(self.defense)+"\n"
        if self.caveat.text=="":
            string+="no caveat"
        else:
            string+="caveat : "+self.caveat.text
        n=0
        for ability in self.abilities:
            n+=1
            string+="\nability "+str(n)+" : "+ability.text
        if n==0:
            string+="\nno ability"
        return string

class TextArg(object):
    """Used as argument for text formatting"""

    def __init__(self,number:int,formatters:dict={}):
        self.number=number
        self.formatters=formatters

    def __str__(self):
        return str(self.number)

    def __getattr__(self,attr):
        if attr in self.formatters:
            if self.number == 1:
                return self.formatters[attr]['1']
            else:
                return self.formatters[attr]['2']
        else:
            return '{{'+attr+'}}'

def evaluate(function:str,*mathArgs):
    res=function.format(*mathArgs)
    # what follows is to be replaced with a parser
    for carac in res:
        if carac not in ' 0123456789+-*/.()':
            raise ValueError(carac,function,vars,args)
    return eval(res)
