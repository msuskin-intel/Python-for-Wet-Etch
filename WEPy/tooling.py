"""Script that allows you to write Python scripts referring directly to your tools as objects, and to incorporate them into logic. This class has a recursive instantiation so please do not call it without passing a proper argument."""
import PyUber
import pandas as pd
from warnings import filterwarnings

class tool:

    def __init__(self, name:str, isTool:bool):
        """Instantiate with string representing the tool or toolset name. Also use isTool to specify whether or not the string reflects an actual tool. 
        For example, you can make a tool object with name AUR, but you would set isTool to false in that case because 'AUR' is not the name of a specific tool. This is done to prevent the code from trying to find a status for 'AUR' in XEUS, for example."""
        self.name = name
        self.isTool = isTool

        self.children = self.getChildrenXEUS()
        
    def getChildrenXEUS(self) -> list | None:
        """Used to detect child entities in XEUS. Do not use this function in your code as it will accrue unnecessary overhead. """
        self.conn = PyUber.connect(datasource="D1D_PROD_XEUS", TimeOutInSeconds = 600)
        filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

        s = f"""SELECT 
          e.entity AS entity
FROM 
F_ENTITY e
WHERE
              e.entity_deleted_flag = 'N' 
 AND      e.entity Like '{self.name}%' """
        df = pd.read_sql_query(s, self.conn)
        if len(df) <= 1:
            return None
        else:
            c = set(df['ENTITY']) - {self.name}
            return [tool(x, isTool=True) for x in c]

    def __str__(self, lv=0) -> str:
        s = lv*"--> " + self.name + '\n'
        if self.children is not None:
            for x in self.children:
                s += x.__str__(lv=lv+1)
        else:
            pass

        return s
    
    def get_state(self) -> str:
        if not self.isTool: raise ValueError("get_state() was called on a tool object with isTool == False! This could have resulted in a bad SQL query. ")

        self.conn = PyUber.connect(datasource="D1D_PROD_XEUS", TimeOutInSeconds = 600)
        filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

        s = f"""SELECT 
          e.state AS state
FROM 
F_ENTITY e
WHERE
              e.entity_deleted_flag = 'N' 
 AND      e.entity = '{self.name}' """
        
        df = pd.read_sql_query(s, self.conn)
        return str(df['STATE'].values[0])

    def isCu(self) -> bool:
        if not self.isTool: raise ValueError("isCu() was called on a tool object with isTool == False! This could have resulted in a bad SQL query. ")

        self.conn = PyUber.connect(datasource="D1D_PROD_XEUS", TimeOutInSeconds = 600)
        filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

        s = f"""SELECT 
          e.cu_flag AS cu_flag
FROM 
F_ENTITY e
WHERE
              e.entity_deleted_flag = 'N' 
 AND      e.entity = '{self.name}' """
        
        df = pd.read_sql_query(s, self.conn)
        return str(df['CU_FLAG'].values[0]) == 'Y'

    def isPb(self) -> bool:
        if not self.isTool: raise ValueError("isPb() was called on a tool object with isTool == False! This could have resulted in a bad SQL query. ")
        self.conn = PyUber.connect(datasource="D1D_PROD_XEUS", TimeOutInSeconds = 600)
        filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

        s = f"""SELECT 
          e.pb_flag AS pb_flag
FROM 
F_ENTITY e
WHERE
              e.entity_deleted_flag = 'N' 
 AND      e.entity = '{self.name}' """
        
        df = pd.read_sql_query(s, self.conn)
        return str(df['PB_FLAG'].values[0]) == 'Y'

    def isAu(self) -> bool:
        if not self.isTool: raise ValueError("isAu() was called on a tool object with isTool == False! This could have resulted in a bad SQL query. ")
        self.conn = PyUber.connect(datasource="D1D_PROD_XEUS", TimeOutInSeconds = 600)
        filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

        s = f"""SELECT 
          e.au_flag AS au_flag
FROM 
F_ENTITY e
WHERE
              e.entity_deleted_flag = 'N' 
 AND      e.entity = '{self.name}' """
        
        df = pd.read_sql_query(s, self.conn)
        return str(df['AU_FLAG'].values[0]) == 'Y'

