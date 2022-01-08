import math
import json

class DataBase(object):
    def __init__(self,dataMapFile):
        types={}
        file=open(dataMapFile)
        data=json.load(file)
        file.close()
        file=open(data["Formatters"])
        self.formatters=json.load(file)
        file.close()
        for compo in ["Caveat","ActCondition","ActCost","TargetSelection","Effect"]:
            file=open(data[compo])
            dataDict=json.load(file)
            file.close()
            file=open(data[compo+"Text"])
            textDict=json.load(file)
            file.close()
            types[compo]=ComponentType(compo,dataDict,textDict,self.formatters)
        self.types=types
        
    # building from reference

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
        
    # building from cli input
    
    # issues to be addressed :
    # - language
    # - checking validity of effectModel
    # - checking arguments
    # - quitting
    # - confirming
    
    def inputBool(self,question):
        # will be relevantly in the class with language
        answer=input(question+"\n(type 'y' for yes and 'n' for no) ")
        if answer=='y':
            return True
        elif answer=='n':
            return False
        else:
            print("Must be 'y' or 'n'.")
            return inputBool(question)

    def inputInt(self,question):
        # will be relevantly in the class with language
        try:
            return int(input(question+" "))
        except:
            print("Must be an integer.")
            return inputInt(question)
        
    def inputAbility(self,welcome=True):
        if welcome:
            print("Welcome to the ability creation helper, that will guide you through choosing the components that make up the ability. Take in front of you the list of referenced components.")
        else:
            print("Choose the components of the ability one by one.")
        print("Choose an activation condition.")
        actCondition=self.types["ActCondition"].inputComponent()
        print("Choose an activation cost.")
        actCost=self.types["ActCost"].inputComponent()
        print("Choose the rule of selection of the targets on which the effects will be applied.")
        targetSelection=self.types["TargetSelection"].inputComponent()
        print("Choose the effects one by one.")
        effectModels=self.types["Effect"].inputEffectModels()
        return Ability(actCondition,actCost,targetSelection,*effectModels)
        
    def inputBareSpellCard(self,welcome=True):
        if welcome:
            print("Welcome to the bare card creation helper, that will guide you through choosing the components that make up the card. Take in front of you the list of referenced components.")
        print("A spell consists in exactly one ability.")
        return BareSpellCard(self.inputAbility(welcome=False))

    def inputBareCreatureCard(self,welcome=True):
        if welcome:
            print("Welcome to the bare card creation helper, that will guide you through choosing the components that make up the card. Take in front of you the list of referenced components.")
        print("A creature consists in fighting skills, possibly one caveat and possibly one or more abilities.")
        offense=self.inputInt("What is the offense?")
        defense=self.inputInt("What is the defense?")
        print("Choose a caveat.")
        caveat=self.types["Caveat"].inputComponent()
        abilities=[]
        abilityCount=TextArg(1,self.formatters)
        plural=TextArg(2,self.formatters)
        # this supposes the existence of an "_other" formatter, the question will go altogether in a language-specific file in a future version
        while self.inputBool("Is there at least one{0._other} ability?".format(abilityCount)):
            abilities.append(self.inputAbility(welcome=False))
            abilityCount=plural
        return BareCreatureCard(offense,defense,caveat,*abilities)

    def inputBareCard(self,welcome=True):
        if welcome:
            print("Welcome to the bare card creation helper, that will guide you through choosing the components that make up the card. Take in front of you the list of referenced components.")
        if self.inputBool("Is it a spell card?"):
            return self.inputBareSpellCard(welcome=False)
        else:
            return self.inputBareCreatureCard(welcome=False)


class ComponentType(object):
    def __init__(self,name,dataDict,textDict,formatters):
        self.data=dataDict
        self.text=textDict
        self.formatters=formatters
        self.isTargetSelection=name=="TargetSelection"
        self.isEffect=name=="Effect"
        
    # building from reference

    def refComponent(self,ref):
        model,*strArgs=ref.split('.')
        cost=self.data[model]['cost']
        text=self.text[model]
        args=map(int,strArgs)
        if self.isEffect:
            return EffectModel(text,self.formatters,cost,*args)
        elif self.isTargetSelection and ref=="1":
            # "this card" means there is one target
            return Component(text,self.formatters,cost,1)
        else:
            return Component(text,self.formatters,cost,*args)
            
    # building from cli input
    
    def inputComponent(self):
        while True:
            ref=input("What is the reference? ")
            try:
                return self.refComponent(ref)
            except:
                print(ref+" is not a valid reference.")
                
    def inputEffectModels(self):
        print("Choose the first effect.")
        effectModels=[self.inputComponent()]
        effectRef=""
        while effectRef!="0":
            while True:
                print("Choose the next effect (or give '0' as a reference is there is no other effect).")
                effectRef=input("What is the reference? ")
                try:
                    effect=self.refComponent(effectRef)
                    effectModels.append(effect)
                    break
                except:
                    if effectRef=="0":
                        break
                    print(effectRef+" is not a valid reference.")
        return effectModels

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
            
    def __str__(self):
        return "cost : "+str(self.cost)+"\n"+self.text

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
        self.text=textModel.format(*textArgs)+' '
        
    def __str__(self):
        return "cost : "+str(self.cost)+"\n"+self.text

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
        
    def __str__(self):
        return "cost : "+str(self.cost)+"\n"+self.text

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
