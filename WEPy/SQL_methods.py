"""Perform SQL Querries and return them for use in Python. This is mainly a wrapper for the PyUber package. """
import PyUber
import pandas as pd
from warnings import filterwarnings
from itertools import chain
from functools import reduce

def get_SQL(*args):
    """Pull one or multiple queries from the XEUS database by passing a string, list of strings, or dictionary to this function.
    --> If you pass a string, the pd.Dataframe will be returned directly. 
    --> If you pass multiple strings, a list of strings, or multiple lists of strings, the corresponding pd.Dataframes will be returned in a list in the same order.
    --> If you pass a dictionary, or multiple dictionaries, a dictionary will be returned where the keys are the keys you give and the values are the pd.Dataframes. 
     
    Do not pass lists of lists or dicts of dicts or dicts of lists or lists of dicts."""
    if len(set(map(lambda x: type(x), args))) > 1:
        raise TypeError("All arguments must be of the same type in get_SQL!")
    if len(set(map(lambda x: type(x), args))) == 0:
        raise TypeError("Must pass at least one argument to get_SQL!")
    
    filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')
    conn = PyUber.connect(datasource="D1D_PROD_XEUS", TimeOutInSeconds = 600)

    if len(args) == 1 & isinstance(args[0], str): #If only a string is passed
        return pd.read_sql_query(args[0], conn)
    elif (len(args) > 1) & all(map(lambda x : isinstance(x, str), args)): #If multiple strings are passed directly
        return [pd.read_sql_query(s, conn) for s in args]
    elif (len(args) >= 1) & all(map(lambda x : isinstance(x, list), args)):#If one or multiple lists of strings are passed
        return [pd.read_sql_query(s, conn) for s in chain(*args)]
    elif (len(args) >= 1) & all(map(lambda x : isinstance(x, dict), args)): #If one or more dicts are passed
        return {u : pd.read_sql_query(v, conn) for u,v in reduce(lambda x1, x2: x1 | x2, args).items()}
    else:
        raise TypeError("get_SQL() couldn't understand the arguments passed to it. See docstring for allowed arguments.")
    