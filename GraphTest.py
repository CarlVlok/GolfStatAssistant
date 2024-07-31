from typing import List
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os
import pandas as pd
import sqlite3

# Load the Excel file
file_path = 'data/Fshot_data1.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Load the DataFrame into the SQLite database
df.to_sql('excel_data', conn, index=False, if_exists='replace')

# Execute SQL queries and return results
def execute_sql(query):
    return pd.read_sql_query(query, conn)
pd.set_option('display.max_rows', None)

#Helper Function | Converts DataFrame to String
def dataToString(x):
    output = x.iloc[:, 0].tolist()
    return output

c = ["D", "3W", "5W", "3i", "4i", "5i", "6i", "7i", "8i", "9i", "PW", "GP", "SW", "LW"]
clubs = ["Driver", "3 Wood", "5 Wood", "3 iron", "4 iron", "5 iron", "6 iron", "7 iron", "8 iron", "9 iron", "Pitching Wedge", "Gap Wedge", "Sand Wedge", "Lob Wedge"]

allClubs = [
    {"Driver": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"3 Wood": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"5 Wood": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"3 iron": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"4 iron": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"5 iron": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"6 iron": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"7 iron": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"8 iron": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"9 iron": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"Pitching Wedge": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"Gap Wedge": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"Sand Wedge": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}, 
    {"Lob Wedge": {'CarryDist': [], 'FlatCarryDist': [], 'TotalDist': [], 'BallSpeed': [], 'LaunchAngle': [], 'Curve': []}}
]


def loadAll(folder_path):
    names = os.listdir(folder_path)
    
    for name in names:
        file_path = os.path.join(folder_path, name)
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, sheet_name='Sheet1')  # Replace 'Sheet1' with the name of your sheet
            df.to_sql('excel_data', conn, index=False, if_exists='replace')
            #print(f"Processing file: {name}")
            
            for i in range(len(clubs)):
                club = c[i]
                #print(f"Processing club: {club}")

                CarryDist = f'SELECT CarryDistPremium FROM excel_data WHERE Club = "{club}"'
                Carry = execute_sql(CarryDist)
                carry = dataToString(Carry)

                FlatCarryDist = f'SELECT FlatCarryDistPremium FROM excel_data WHERE Club = "{club}"'  
                FlatCarry = execute_sql(FlatCarryDist)
                fc = dataToString(FlatCarry)

                TotalDist = f'SELECT TotalDistPremium FROM excel_data WHERE Club = "{club}"'
                Total = execute_sql(TotalDist)
                t = dataToString(Total)

                BallSpeed = f'SELECT BallSpeedPremium FROM excel_data WHERE Club = "{club}"'
                Bspeed = execute_sql(BallSpeed)
                bs = dataToString(Bspeed)

                LaunchAnglePremium = f'SELECT LaunchAnglePremium FROM excel_data WHERE Club = "{club}"'
                Launch = execute_sql(LaunchAnglePremium)
                l = dataToString(Launch)

                Curve = f'SELECT Curve FROM excel_data WHERE Club = "{club}"'
                Cur = execute_sql(Curve)
                cu = dataToString(Cur)
            
                allClubs[i][clubs[i]]['CarryDist'].extend(carry)
                allClubs[i][clubs[i]]['FlatCarryDist'].extend(fc)
                allClubs[i][clubs[i]]['TotalDist'].extend(t)
                allClubs[i][clubs[i]]['BallSpeed'].extend(bs)
                allClubs[i][clubs[i]]['LaunchAngle'].extend(l)
                allClubs[i][clubs[i]]['Curve'].extend(cu)
            # print("===================")
    
    return allClubs
folder_path = "data/"
data = loadAll(folder_path)


def getAngle(ang):
    angle = ''.join(filter(str.isdigit, ang))
    # Convert the numeric part to an integer
    return int(angle)

def getSpinRate(club, BallSpeed, LaunchAngle):
    # Driver, Wood, Long Iron, Mid Iron, Short Iron, PW+GW, SW, LW
    launchSpinFactor = [1.4, 1.2, 1.2, 1.1, 1.1, 1.1, 1.0, 1.0, 0.9, 0.9, 0.7, 0.6, 0.5, 0.4]
    rpmList = []
    for i in range(len(BallSpeed)):
        top = BallSpeed[i]**2 * launchSpinFactor[club] 
        rpmList.append(top/getAngle(LaunchAngle[i]))
    return rpmList

def calcAverage(list):
    total = 0
    for num in list:
        total+=num
    if len(list)==0:
        output = 0
    else:
        output = round(total/len(list))
    return output

def carryChart():
    x = clubs
    y1 = []
    y2 = []
    y3 = []
    for i in range(len(clubs)):
        y1.append(calcAverage(data[i][clubs[i]]['CarryDist']))
        y2.append(calcAverage(data[i][clubs[i]]['FlatCarryDist']) - calcAverage(data[i][clubs[i]]['CarryDist']))
        y3.append(calcAverage(data[i][clubs[i]]['TotalDist']) - calcAverage(data[i][clubs[i]]['CarryDist']))

    fig, ax = plt.subplots()

    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)


    bar1 = plt.bar(x, y1, color='r', label="Carry")
    bar2 = plt.bar(x, y2, bottom=y1, color='b', label="Flat Carry")
    bar3 = plt.bar(x, y3, bottom=np.array(y1) + np.array(y2), label="Total")
    plt.xlabel("Club")
    plt.ylabel("Distance in meters")
    plt.title("Carry Distance, Flat Distance and Total Distance for each club")
    plt.xticks(x, x, rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()

    for i in range(len(x)):
        total_height = y1[i] + y2[i] + y3[i]
        ax.annotate(f'{total_height:.2f}',
                    xy=(i, total_height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    plt.show()  

def rpmChart():
    x =clubs
    y1 = []
    for i in range(len(x)):
        y1.append(calcAverage(getSpinRate(i, data[i][clubs[i]]['BallSpeed'], data[i][clubs[i]]['LaunchAngle'])))
    plt.bar(x, y1, color='r', label="Carry")
    fig, ax = plt.subplots()
    for i in range(len(x)):
        total_height = y1[i]
        ax.annotate(f'{total_height:.2f}',
                    xy=(i, total_height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    plt.show()

def sortCurve(arr: List[str]) -> List[str]:
    def key_func(s: str):
        if s.endswith('L'):
            return int(s[:-1])
        elif s.endswith('R'):
            return int(s[:-1]) + 1000  # Add a large number to ensure 'R' values are sorted after 'L' values
        return float('inf')  # Ensure '0' (or any unexpected format) comes at the end
    return sorted(arr, key=key_func)
    
    
def scatterPlot(db):
    y = db[7]["7 iron"]["CarryDist"]
    x = sortCurve(db[7]["7 iron"]["Curve"])

    # Check if lengths match after processing
    if len(y) != len(x):
        raise ValueError("The lengths of 'CarryDist' and 'Curve' lists do not match after processing.")

    # Create the scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', marker='o')
    plt.title('Basic Scatter Plot')
    plt.xlabel('Curve')
    plt.ylabel('Carry Distance')
    plt.grid(True)
    plt.show()

    
carryChart()
rpmChart()
scatterPlot(data)     




