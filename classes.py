class TextArg(object):
    """Used as argument for text formatting"""
    def __init__(self,number:int):
        self.number=number
        if number == 1:
            self.s=""
        else:
            self.s="s"

    def __str__(self):
        return str(self.number)

class ComponentModel(object):
    def __init__(self,cost,text:str,formatters:dict={}):
        self.cost = cost
        self.text=text+' '
        self.formatters=formatters

class Component(object):
    def __init__(self,componentModel,*args):
        self.componentModel=componentModel
        self.args=args
        self.cost=componentModel.cost(*args)
        self.text={}
        textArgs=[""]
        textModel=self.componentModel.text
        formatters=self.componentModel.formatters
        for arg in self.args:
            textArg=TextArg(arg)
            for key in formatters:
                setattr(textArg,key,formatters[key](arg))
            textArgs.append(textArg)
        self.text=textModel.format(*textArgs)

class NoComponent(object):
    def __init__(self):
        self.args=[None]
        self.cost=0
        self.text=""
        self.formatters={}
noComponent=NoComponent()

class EffectModel(object):
    def __init__(self,componentModel,*args):
        self.componentModel=componentModel
        self.args=args

class Effect(object):
    def __init__(self,effectModel,targetSelection=noComponent):
        componentModel=effectModel.componentModel
        self.componentModel=componentModel
        args=effectModel.args
        self.args=args
        self.targetSelection=targetSelection
        self.cost=componentModel.cost(targetSelection.cost,*args)
        textModel=self.componentModel.text
        formatters=self.componentModel.formatters
        textArgs=[]
        # the last argument of the targetSelection is considered to be the number of targets
        args=[self.targetSelection.args[-1]]+list(self.args)
        for arg in args:
            textArg=TextArg(arg)
            for key in formatters:
                setattr(textArg,key,formatters[key](arg))
            textArgs.append(textArg)
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
        self.cost=cost
        text=""
        text+=self.actCondition.text
        text+=self.actCost.text
        text+=self.targetSelection.text
        for effect in self.effects:
            text+=effect.text
        self.text=text
