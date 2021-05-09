def lambdify(vars:list,function:str):
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
