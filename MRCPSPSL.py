
import pandas as pd

pd.options.mode.chained_assignment = None
def alpha(i,d):
    try :
        result = (i<len(d))*(d["tableau"+str(i)][0]==" ")
    except Exception : 
        result = 0
    return result

d={}
d2={}
L2 = [0,0,0,0]
f2 = open('C:\\Users\\Fujitsu\\Downloads\\boite noire\\boite noire\\KADTAB'+r'\\kad.txt')
for i,line in enumerate(f2) :
    k = "tableau" + str(i)
    d2[k] = line
i=1  
p=1 
while i < len(d2):
    if len(d2["tableau" + str(i)])<2:
        i=i+1
    elif d2["tableau" + str(i)][0]=="M" :
        df2 = d2["tableau" + str(i)].split(None,4)
        L2[0] = df2[0] + " " + df2[1]
        for j in range(1,len(L2)):
            L2[j] = df2[j+1]
        i=i+1
    else :
        i=i+1      

f = open("C:\\Users\\Fujitsu\\Downloads\\boite noire\\boite noire\AMYK\\ResultatSolution.txt")
for i,line in enumerate(f) :
    k = "tableau" + str(i)
    d[k] = line
L = {}    
i=1  
p=1 



while i < len(d):
    if len(d["tableau" + str(i)])<2:
        i=i+1
    elif d["tableau" + str(i)][1]=="T" :
        df = []
        while alpha(i,d)==1 :
            df.append(d["tableau"+str(i)])
            i = i+1
        L["Table"+str(p)]= df
        p=p+1
        i=i+1
    else :
        i=i+1    
        
for i in range(1,len(L)+1):
    for j in range(0,len(L["Table"+str(i)])):
        if j == 0:
            L["Table"+str(i)][j] = L["Table"+str(i)][j].split()
        else :
            L["Table"+str(i)][j] = L["Table"+str(i)][j].split(None,5)
            if len( L["Table"+str(i)][j]) ==5 :
                L["Table"+str(i)][j].append(0)
    L["Table"+str(i)]=pd.DataFrame(L["Table"+str(i)][1:], columns =L["Table"+str(i)][0])
    
H={}
for i in range(1,len(L)+1):
    L["Table"+str(i)]['next task'] = [None]*len(L["Table"+str(i)])
    L["Table"+str(i)]['time lapse'] = [None]*len(L["Table"+str(i)])
    From=[]
    To=[]
    for j in range(0,len(L["Table"+str(i)])):
        L["Table"+str(i)]['time lapse'][j] = int(L["Table"+str(i)]['Finish'][j]) - int(L["Table"+str(i)]['Start'][j])
        P=[]
        for k in range(0,len(L["Table"+str(i)])):
                if L["Table"+str(i)]['Start'][k] == L["Table"+str(i)]['Finish'][j] :
                    P.append(k)
                    L["Table"+str(i)]["next task"][j] = P
                    From.append(j)
                    To.append(k)
    O = pd.DataFrame({'From':From,'To':To})
    print(O)

    H['graph'+str(i)] = O
    dcc.Textarea(
        id='input',
        value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '100%', 'height': 12})



# G = nx.from_pandas_edgelist()        
# nx.draw(G,)


# L["Table"+str(i)]

# import pandas as pd
# import os
# import io
# from io import StringIO

# # Open the text file and read it into a string
# with open(os.path.dirname(os.path.abspath(__file__))+r"\ResultatSolution.txt", 'r') as f:
#     data = f.read()

# # Split the string into a list of tables
# tables = data.split('**************************************************************************************************')
# del tables[0]
# del tables[2]
# # Create a list to store the dataframes
# dataframes = []

# # Iterate over the list of tables
# for table in tables:
#     # Read the table as a CSV file using pandas
#     tio = StringIO(table)
#     df = pd.read_csv(tio, delimiter='    ',engine="python")
    
#     # Add the dataframe to the list
#     dataframes.append(df)