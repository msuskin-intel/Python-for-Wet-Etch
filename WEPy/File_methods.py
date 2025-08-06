"""Various methods for efficiently handling one or more static files from the host machine. """
import pandas as pd
from itertools import chain
from functools import reduce

def get_csv(*args):
    if len(set(map(lambda x: type(x), args))) > 1:
        raise TypeError("All arguments must be of the same type in get_csv!")
    if len(set(map(lambda x: type(x), args))) == 0:
        raise TypeError("Must pass at least one argument to get_csv!")
    
    
    if len(args) == 1 & isinstance(args[0], str): #If only a string is passed
        return pd.read_csv(args[0])
    elif (len(args) > 1) & all(map(lambda x : isinstance(x, str), args)): #If multiple strings are passed directly
        return [pd.read_csv(s) for s in args]
    elif (len(args) >= 1) & all(map(lambda x : isinstance(x, list), args)):#If one or multiple lists of strings are passed
        return [pd.read_csv(s) for s in chain(*args)]
    elif (len(args) >= 1) & all(map(lambda x : isinstance(x, dict), args)): #If one or more dicts are passed
        return {u : pd.read_csv(v) for u,v in reduce(lambda x1, x2: x1 | x2, args).items()}
    else:
        raise TypeError("get_csv() couldn't understand the arguments passed to it. See docstring for allowed arguments.")

def get_excel(*args):
    if len(set(map(lambda x: type(x), args))) > 1:
        raise TypeError("All arguments must be of the same type in get_excel!")
    if len(set(map(lambda x: type(x), args))) == 0:
        raise TypeError("Must pass at least one argument to get_excel!")
    
    
    if len(args) == 1 & isinstance(args[0], str): #If only a string is passed
        return pd.read_excel(args[0])
    elif (len(args) > 1) & all(map(lambda x : isinstance(x, str), args)): #If multiple strings are passed directly
        return [pd.read_excel(s) for s in args]
    elif (len(args) >= 1) & all(map(lambda x : isinstance(x, list), args)):#If one or multiple lists of strings are passed
        return [pd.read_excel(s) for s in chain(*args)]
    elif (len(args) >= 1) & all(map(lambda x : isinstance(x, dict), args)): #If one or more dicts are passed
        return {u : pd.read_excel(v) for u,v in reduce(lambda x1, x2: x1 | x2, args).items()}
    else:
        raise TypeError("get_excel() couldn't understand the arguments passed to it. See docstring for allowed arguments.")