import requests, sqlite3
from tkinter import *
from tkinter import ttk
 
base_url = '*DATAFEED REDACTED MUST REPLACE THIS*'

def getData(*args): 
    
    try:
        initial_zip = zipcodes_entry.get()
        zipcodes = initial_zip.split(",")
        start = int(daysprior.get())
        end =  1
    except ValueError:
        pass
 
    conn = sqlite3.connect( 'Weather.db' )
    c = conn.cursor()
 
    for i in zipcodes:
        processing.set("Currently processing: " + str(i))
        query={'location': i,'startdate':start,'enddate':end,'applicationtype':'RESTAPI','useremail':'*USERNAME REDACTED FOR PUBLICATION*'}
        my_url = base_url + 'location=' + str(query['location']) +'&' + 'startdate=' + str(query['startdate']) + '&' +'enddate=' + str(query['enddate']) + '&' + 'applicationtype=' + str(query['applicationtype']) + '&' + 'useremail=' + str(query['useremail'])
        req = requests.get( my_url )
        my_json = req.json()
        actual_days = len(my_json["Data"])
        statement1 = 'CREATE TABLE IF NOT EXISTS Zip' + str(i) + ' (Date TEXT NOT NULL UNIQUE, Average_Temp REAL, Dew_Point REAL, Sea_Level_Pressure REAL, Station_Level_Pressure REAL, Mean_Visibility REAL, Mean_Wind_Speed REAL, Max_Sustained_Wind_Speed REAL, Max_Gust REAL, Max_Temp REAL, Min_Temp REAL, Total_Precipitation REAL, Snow_Depth REAL)'
        c.execute(statement1)
        for day in range(actual_days):
            statement2 = 'INSERT INTO Zip' + str(i) + ' VALUES (\"' + str(my_json['Data'][day]['Date']) + '\", ' + str(my_json['Data'][day]['TEMP']) + ', ' + str(my_json['Data'][day]['DewPoint']) + ', ' + str(my_json['Data'][day]['SeaLevelPressure']) + ', ' + str(my_json['Data'][day]['StationLevelPressure']) + ', ' + str(my_json['Data'][day]['MeanVisibility']) + ', ' + str(my_json['Data'][day]['MeanWindSpeed']) + ', ' + str(my_json['Data'][day]['MaximumSsustainedWindSpeed_x0020_']) + ', ' + str(my_json['Data'][day]['MaximumWindGust_x0020_'] + ', ' + str(my_json['Data'][day]['MaxTemperature'])) + ', ' + str(my_json['Data'][day]['MinimumTemperature']) + ', ' + str(my_json['Data'][day]['TotalPrecipitation']) + ', ' + str(my_json['Data'][day]['SnowDepth']) + ')'
            c.execute(statement2)
 
    processing.set("Done!")
    conn.commit()
    conn.close()

root = Tk()
root.title("Mindshare Weather")
root.iconbitmap(default='favicon.ico')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

daysprior = StringVar()
zipcodes = StringVar()
processing = StringVar()
processing.set('Waiting...')

daysprior_entry = ttk.Entry(mainframe, width=7, textvariable=daysprior)
daysprior_entry.grid(column=3, row=1, sticky=(W, E))

zipcodes_entry = ttk.Entry(mainframe, width=25, textvariable=zipcodes)
zipcodes_entry.grid(column=1, row=1, sticky=E)

ttk.Label(mainframe, textvariable=processing).grid(column=2, row=3, sticky=(W, E))
ttk.Button(mainframe, text="Start", command=getData).grid(column=2, row=4, sticky=S)

ttk.Label(mainframe, text="# Days Prior").grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Comma Delimited Zip Codes").grid(column=1, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

daysprior_entry.focus()
root.bind('<Return>', getData)

root.mainloop()