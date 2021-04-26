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

class DataModel(object):
    def __init__(self,cost,text:str,formatters:dict={}):
        self.cost = cost
        self.text=text+' '
        self.formatters=formatters

class Data(object):
    def __init__(self,dataModel,*args):
        self.dataModel=dataModel
        self.args=args
        self.cost=dataModel.cost(*args)
        self.text={}
        textArgs=[""]
        textModel=self.dataModel.text
        formatters=self.dataModel.formatters
        for arg in self.args:
            textArg=TextArg(arg)
            for key in formatters:
                setattr(textArg,key,formatters[key](arg))
            textArgs.append(textArg)
        self.text=textModel.format(*textArgs)

class NoData(object):
    def __init__(self):
        self.args=[None]
        self.cost=0
        self.text=""
        self.formatters={}
noData=NoData()

class EffectModel(object):
    def __init__(self,dataModel,*args):
        self.dataModel=dataModel
        self.args=args

class Effect(object):
    def __init__(self,effectModel,targetting=noData):
        dataModel=effectModel.dataModel
        self.dataModel=dataModel
        args=effectModel.args
        self.args=args
        self.targetting=targetting
        self.cost=dataModel.cost(targetting.cost,*args)
        textModel=self.dataModel.text
        formatters=self.dataModel.formatters
        textArgs=[]
        # the last argument of the targetting is considered to be the number of targets
        args=[self.targetting.args[-1]]+list(self.args)
        for arg in args:
            textArg=TextArg(arg)
            for key in formatters:
                setattr(textArg,key,formatters[key](arg))
            textArgs.append(textArg)
        self.text=textModel.format(*textArgs)

class Ability(object):
    def __init__(self, actCondition=noData,actCost=noData,targetting=noData, *effectModels):
        self.actCondition=actCondition
        self.actCost=actCost
        self.targetting=targetting
        effects=[]
        cost=0
        for effectModel in effectModels:
            effect=Effect(effectModel,targetting)
            effects.append(effect)
            cost+=effect.cost
        self.effects=effects
        cost-=actCondition.cost
        cost-=actCost.cost
        self.cost=cost
        text=""
        text+=self.actCondition.text
        text+=self.actCost.text
        text+=self.targetting.text
        for effect in self.effects:
            text+=effect.text
        self.text=text
