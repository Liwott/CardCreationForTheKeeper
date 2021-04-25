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
    def __init__(self,cost):
        self.cost = cost
        self.text={}
        self.formatters={}

    def add_text(self,locale:str,text:str,formatters:list=[]):
        self.text[locale]=text+' '
        self.formatters[locale]=formatters

class Data(object):
    def __init__(self,dataModel,*args):
        self.dataModel=dataModel
        self.args=args
        self.cost=dataModel.cost(*args)
        self.create_text()

    def create_text(self):
        self.text={}
        for locale in self.dataModel.text:
            textArgs=[""]
            textModel=self.dataModel.text[locale]
            formatters=self.dataModel.formatters[locale]
            for arg in self.args:
                textArg=TextArg(arg)
                for key in formatters:
                    setattr(textArg,key,formatters[key](arg))
                textArgs.append(textArg)
            self.text[locale]=textModel.format(*textArgs)

class NoData(object):
    def __init__(self):
        self.cost=None
        self.args=[None]
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
        self.create_text()

    def create_text(self):
        self.text={}
        for locale in self.dataModel.text:
            textModel=self.dataModel.text[locale]
            formatters=self.dataModel.formatters[locale]
            textArgs=[]
            # the last argument of the targetting is onsidered to be the number of targets
            args=[self.targetting.args[-1]]+list(self.args)
            for arg in args:
                textArg=TextArg(arg)
                for key in formatters:
                    setattr(textArg,key,formatters[key](arg))
                textArgs.append(textArg)
            self.text[locale]=textModel.format(*textArgs)

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
        self.text={}

    def create_text(self,locale):
        text=""
        text+=self.actCondition.text[locale]
        text+=self.actCost.text[locale]
        text+=self.targetting.text[locale]
        for effect in self.effects:
            text+=effect.text[locale]
        self.text[locale]=text
