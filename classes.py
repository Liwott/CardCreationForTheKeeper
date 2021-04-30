import math

class TextArg(object):
    """Used as argument for text formatting"""
    formatters={'s':{'1':'','2':'s'}}

    def __init__(self,number:int):
        self.number=number

    def __str__(self):
        return str(self.number)

    def __getattr__(self,attr):
        if attr in TextArg.formatters:
            if self.number == 1:
                return TextArg.formatters[attr]['1']
            else:
                return TextArg.formatters[attr]['2']
        else:
            return '{{'+attr+'}}'

class Component(object):
    def __init__(self,text:str,cost,*args):
        self.args=args
        self.cost=cost(*args)
        textArgs=map(TextArg,list(args))
        # argument 0 is empty and sould not be used in formatting
        self.text=text.format(None,*textArgs)+' '

class NoComponent(object):
    def __init__(self):
        self.args=[None]
        self.cost=0
        self.text=""
noComponent=NoComponent()

class EffectModel(object):
    def __init__(self,text:str,cost,*args):
        self.text=text
        self.cost=cost
        self.args=args

class Effect(object):
    def __init__(self,effectModel,targetSelection=noComponent):
        args=effectModel.args
        self.args=args
        self.cost=effectModel.cost(targetSelection.cost,*args)
        textModel=effectModel.text
        # the first argument of the targetSelection is considered to be the number of targets
        textArgs=map(TextArg,[targetSelection.args[0]]+list(args))
        self.text=textModel.format(*textArgs)

class Ability(object):
    def __init__(self, actCondition=noComponent,actCost=noComponent,targetSelection=noComponent, *effectModels):
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

class BareCreatureCard(object):
    def __init__(self,offense:int,defense:int,caveat=noComponent,*abilities):
        self.offense=offense
        self.defense=defense
        self.caveat=caveat
        self.abilities=abilities
        cost=max(0,offense+(defense/5)-caveat.cost)
        for ability in abilities:
            cost+=ability.cost
        self.cost=max(1,math.ceil(cost))
