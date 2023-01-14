import base64
import io
import dash
import subprocess
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import timedelta,datetime
from flask import Flask
app = Flask(__name__)

lines = []
tables = []
table = []
makespan = []
with open(r'C:\\Users\\Fujitsu\\Downloads\\boite noire\\boite noire\\AMYK\\ResultatSolution.txt', 'r') as f:
    for line in f:
        lines.append(line)
        if line[0] == ' ':
            table.append(line.strip("\n"))
        elif line[0] == 'M':
            makespan.append(line.split()[-1])
        else:
            if len(table) > 1:
                tables.append(table)
                table = []
    tables.append(table)
dataframes = []
for Table in tables:
    rows = [line.split(maxsplit=5) for i, line in enumerate(
        Table) if i != 1 and i != len(Table)-1]
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.iloc[:, :-1] = df.iloc[:, :-1].astype(int)
    dataframes.append(df)

start_time = (df['Start'] / 1440).apply(timedelta).apply(lambda x: datetime.today() + x).apply(
        lambda x: x.strftime('%Y-%m-%d %H:%M'))
finish_time = (df['Finish'] / 1440).apply(timedelta).apply(lambda x: datetime.today() + x).apply(
        lambda x: x.strftime('%Y-%m-%d %H:%M'))
df["Start"] = pd.to_datetime(start_time)
df["Finish"] = pd.to_datetime(finish_time)
print(df["Start"])
data = px.timeline(df,x_start="Start" ,x_end="Finish", y="Task")

data.show()
# layout = go.Layout(title='Time Series Plot', xaxis={'title': 'Date'}, yaxis={'title': 'Value'})

# fig = go.Figure(data=data, layout=layout)

# app.layout = html.Div([
#     dcc.Graph(id='time-series-plot', figure=fig)
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)





