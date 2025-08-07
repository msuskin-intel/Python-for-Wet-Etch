import pandas as pd
import matplotlib.pyplot as plt
import io
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid

from functools import reduce

class report:

    def __init__(self, elements:dict):
       """This class is designed to manage generating reports that can be e-mailed. Instantiate it by passing a dictionary. Keys are names that you use for reference with the class methods, and values are objects that you want to include in the report. """
       self.elements = elements
       self.msg = MIMEMultipart()
       self.html_str = ""
         
    def add_table(self, tables, cols=None, join_type:str='outer', join_on:str=None, styler_func:pd.DataFrame.style = None):
        """Add an HTML table to the report. 
        Behavior for tables argument:
        Pass a string --> The table with a matching nickname will be used.
        Pass a list of strings --> The tables with matching nicknames will be joined as specified in the join_type parameter.
        Pass a pd.Dataframe --> It will be added directly to the report. 
        Pass a list of pd.Dataframes --> They will be joined and added to the report. 
        
        Behavior for the cols argument:
        Ignore this parameter --> All columns of the selected tables will be used. 
        Pass a string --> Only the column with the header matching this string will be shown
        Pass a list of strings --> Any column with a header matching these strings will be shown
        
        Behavior for join type argument:
        If multiple tables are selected, this specifies how they will be joined. Options are 'outer', 'inner', 'left', 'right', and 'cross'. Default is outer, does nothing if there is only one table selected. 
        
        Behavior for join_on argument:
        Select which column to join the tables by. 

        Advanced usage: Pass a function for the styler object for the pd.Dataframe. Ignore if you don't know what this means. """
        
        if type(tables) == str:
            try:
                base = self.elements[tables]
            except:
                raise ValueError(f"Couldn't find table {tables} in report elements!")
        elif type(tables) == list[str]:
            try:
                base = self.elements[tables[0]]
            except:
                raise ValueError(f"Couldn't find table {tables[0]} in report elements!")
            for table in tables[1:]:
                try:
                    if not table.empty:
                        base = base.join(table, on=join_on, how=join_type, sort=True)
                except:
                    raise ValueError(f"Couldn't find table {table} in report elements!")
        elif type(tables) == pd.DataFrame:
            base = tables
        elif type(tables) == list[pd.DataFrame]:
            base = reduce(lambda x1, x2: x1.join(x2, on=join_on, how=join_type, sort=True), tables)
        else:
            raise TypeError("report.add_table() couldn't understand the arguments passed to it. See docstring for allowed arguments.")

        if styler_func is not None:
            s = base.style.pipe(styler_func)
        else:
            s=base
        
        
        self.html_str += s.to_html(index=True)
     
    def add_plot(self, tables, x_axis:str, y_axis:str, join_type='inner', join_on:str=None, **kwargs):
        """Generates a plot using the pyplot package. 
        
        Behavior for tables argument:
        Pass a string --> The table with a matching nickname will be used.
        Pass a list of strings --> The tables with matching nicknames will be joined as specified in the join_type parameter.
        Pass a pd.Dataframe --> It will be added directly to the report. 
        Pass a list of pd.Dataframes --> They will be joined and added to the report. 

        For x_axis and y_axis, pass the name of the column for each axis. 
        
        Behavior for join type argument:
        If multiple tables are selected, this specifies how they will be joined. Options are 'outer', 'inner', 'left', 'right', and 'cross'. Default is outer, does nothing if there is only one table selected. 
        
        Behavior for join_on argument:
        Select which column to join the tables by. 
        
        Pass PyPlot options to kwargs as a dict. For example, if you want axis labels to be rotated by 45 degrees, pass {"xrot" : 45}. 
        """
        #generate plot and feed it to buffer:
        
        if type(tables) == str:
            try:
                base = self.elements[tables]
            except:
                raise ValueError(f"Couldn't find table {tables} in report elements!")
        elif type(tables) == list[str]:
            try:
                base = self.elements[tables[0]]
            except:
                raise ValueError(f"Couldn't find table {tables[0]} in report elements!")
            for table in tables[1:]:
                try:
                    if not table.empty:
                        base = base.join(table, on=join_on, how=join_type, sort=True)
                except:
                    raise ValueError(f"Couldn't find table {table} in report elements!")
        elif type(tables) == pd.DataFrame:
            base = tables
        elif type(tables) == list[pd.DataFrame]:
            base = reduce(lambda x1, x2: x1.join(x2, on=join_on, how=join_type, sort=True), tables)
        else:
            raise TypeError("report.add_plot() couldn't understand the arguments passed to it. See docstring for allowed arguments.")
        
        buf = io.BytesIO()
        
        base.plot(x=x_axis, y=y_axis, **kwargs)
        plt.title(kwargs.get('name', ''))
        plt.xlabel(kwargs.get('xname', x_axis))
        plt.ylabel(kwargs.get('yname', y_axis))

        plt.savefig(buf, format='jpeg')

        buf.seek(0)

        #Create e-mail attachment and HTML part: 

        label = make_msgid()

        img = MIMEImage(buf.read())
        img.add_header('Content-ID', label[1:-1])
        
        txt = f"""
    <html>
        <body>
            <p><img src="cid:{label[1:-1]}"></p>
        </body>
    </html>
    """
        self.html_str += txt
        self.msg.attach(img)

        buf.close()     

    def add_text(self, header:str, body:str, **kwargs):
        """Add text to the e-mail. Takes a header and a body. Pass empty string to ignore either of these. header_size to change the font size"""
        h_size = kwargs.get('header_size', 2)
        
        self.html_str += f"""<html><h{h_size}>{header}</h{h_size}><body><p>{body}</p></body></html>"""
    
    def add_image(self, image):
        """Pass a path, nickname, or bytes object to image. Will also accept any list  of these types. """
        def append_image(img:MIMEImage):
            label = make_msgid()
            img.add_header('Content-ID', label[1:-1])
        
            txt = f"""
    <html>
        <body>
            <p><img src="cid:{label[1:-1]}"></p>
        </body>
    </html>
    """
            self.html_str += txt
            self.msg.attach(img)
        
        if not isinstance(image, list):
            image = [image]
        
        lst = [self.elements[s] if s in self.elements.keys() else s for s in image]
        
        for l in lst:
            if isinstance(l, str):
                try:
                    with open(l, 'rb') as f:
                        append_image(MIMEImage(f.read()))
                except:
                    raise FileNotFoundError(f"Could not open image at {l}!")
            elif isinstance(l, bytes | bytearray):
                try: 
                    append_image(MIMEImage(f))
                except:
                    raise TypeError("Could not interpret images as bytes or bytearray!")

    def __str__(self) -> str:
        return "\n".join([p.get_content_type() for p in self.msg.walk()])
    
    def email_report(self, subject:str, sender:str, recipients:list[str]):

        """Use the SMTP server to send the report. This only sends the EmailMessage object, so errors you encounter here might have originated earlier.  """

        self.msg['Subject'] = subject
        self.msg['From'] = sender
        self.msg['To'] = ', '.join(recipients)

        self.msg.attach(MIMEText(self.html_str, 'html'))
        
        with smtplib.SMTP('mail.intel.com') as s:
            s.send_message(self.msg)