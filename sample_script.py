"""Here's a sample script that showcases some of the functionalities of the WEPy package. """

from WEPy.File_methods import get_excel, get_csv
from WEPy.SQL_methods import get_SQL
from WEPy.report import report

favorites = get_excel("Example Data/Favorites.xlsx") #This is an example Excel file

pirate_data = get_csv("Example Data/Data.csv") #This is an example CSV file

SQL_string = """SELECT 
          z1.stockroom AS stockroom
         ,z1.item_id AS item_id
         ,z1.qty_avail AS qty_avail
FROM 
F_WIINGS_INVENTORY z1
WHERE
              z1.item_id = 500195515"""

screw_data = get_SQL(SQL_string) #This line of code will query the WIINGs database using the SQL query defined in SQL_string

print(screw_data)

#Now we want to generate a report and email it.
your_email = "maiyan.suskin@intel.com" #<-- replace with your email

#Declare a dictionary holding our data and nicknames for our data
data = {'pirate' : pirate_data,
        'favorites' : favorites}

r = report(data)

#Add a title, and the favorite dinosaur of everyone.
r.add_text("Favorite Dinosaurs", "Favorite dinosaurs but the text is smaller")
r.add_table('favorites', ['Name', 'Favorite Dinosaur']) #We are only using one table so we don't need to include any join parameters

#Add more text and and image. We can pass an empty string to add_text if we want only a title or only body text
r.add_text("", "Look at this dog!!")
r.add_image("Example Data/dog.jpg")

#Add a plot generated from Data.csv
r.add_text("Here is some data. This is header text.", "")
r.add_plot('pirate', 'Month', 'Profit (doubloons)')

#We are ready to send this email. 
recipients = [your_email]
r.email_report("Sample report", your_email, recipients=recipients)