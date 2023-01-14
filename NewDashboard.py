import base64
import io
import dash
import subprocess
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash()

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'marginTop': '30%',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
    html.Div(id='output'),
    dcc.Graph(id="Graph"),
    dcc.Slider(id='slider', 
               min=1,
               max=30,
               value=1,
               marks={i: str(i) for i in range(1,31)},step=1)
])

def alpha(i,d):
    try :
        result = (i<len(d))*(d["tableau"+str(i)][0]==" ")
    except Exception : 
        result = 0
    return result

def parse_file(contents,filename):
    
    content_type, content_string = contents.split(',')

    decoded_string = base64.b64decode(content_string)
    if decoded_string is not None :
        try:
            D = pd.read_csv(io.StringIO(decoded_string.decode('utf-8')))
        except Exception:
            return html.Div(['There was an error processing this file.'])
    return D

@app.callback([Input('upload','contents'),
               Input('upload','filename'),
               Input('slider','value')])
def update_output(contents, filename,value):
    html.Div(id='output'),
    dcc.Graph(id="Graph"),
    dcc.Slider(id='slider', 
               min=1,
               max=30,
               value=1,
               marks={i: str(i) for i in range(1,31)},step=1)
    fig = go.Figure()
    if contents is not None :
        D = parse_file(contents, filename)
        D.to_csv('1.txt',index=False)
        d={}
    f = open('C:\\Users\\Fujitsu\\Downloads\\boite noire\\boite noire\\AMYK\\ResultatSolution.txt')
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
        H['graph'+str(i)] = O 
    print(H)
    fig = go.Figure(    
            data = [go.Sankey(
        node=dict(
        label=list(set(H['graph'+str(value)]['From'].tolist()+H['graph'+str(value)]['To'].tolist()))
        ),
        link=dict(
            source=H['graph'+str(value)]['From'],
            target=H['graph'+str(value)]['To'],
            value=L["Table"+str(value)]['time lapse']
            ))],
            layout = go.Layout(
                height = 900
                ))    
    return fig



if __name__ == '__main__':
    app.run_server(debug=False)
