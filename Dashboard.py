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
from datetime import timedelta, datetime

pd.options.mode.chained_assignment = None

colors = {"graphBackground": "#F5F5F5",
          "background": "#ffffff", "text": "#000000"}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Projet Boite noir ",
            style={
                'width': '100%',
                'height': '60px',
                'textAlign': 'center',
                'color': '#87ceeb',
            }),
    dcc.Upload(
        id='upload',
        children=html.Div([
            'Glisser-déposer ou  ',
            html.A('Séléctionner un fichier')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'color': '#00000',
        },
        multiple=False
    ),
    html.Div(id='output'),
    dcc.Graph(id="Graph", style={
        'width': '100%',
        'height': '100%'}),
    html.H2("ARGADI AYOUB   -   BOUMGHAIT CHERGUI Marouan   -           EL HAMRAOUI EL Mehdi    -           GNAOUAT Amine   -  HOUTTANE Mawan   -  TMaG Mouad", style={
            'width': '40%',
            'height': 'AUTO',
            'lineHeight': 'AUTO',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            ''
            'textAlign': 'center',
            'color': '#00000',
        },)],style={
            'textAlign': 'center'
        })


def alpha(i, d):
    try:
        result = (i < len(d))*(d["tableau"+str(i)][0] == " ")
    except Exception:
        result = 0
    return result


def parse_file(contents, filename):

    content_type, content_string = contents.split(',')

    decoded_string = base64.b64decode(content_string)
    if decoded_string is not None:
        try:
            D = pd.read_csv(io.StringIO(decoded_string.decode('utf-8')))
        except Exception:
            return html.Div(['There was an error processing this file.'])
    return D


@app.callback(Output('Graph', 'figure'),
              [Input('upload', 'contents'),
               Input('upload', 'filename')])
def update_output(contents, filename):
    fig = go.Figure()
    if contents is not None:
        D = parse_file(contents, filename)
        D.to_csv('1.txt', index=False)
        d = {}

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
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    # fig = go.Figure(data =[px.timeline(df, x_start="Start", x_end="Finish", y="Task")],layout = go.Layout(
    #             height = 900
    #             ))
    # link=dict(
    #     source=H['graph'+str(value)]['From'],
    #     target=H['graph'+str(value)]['To'],
    #     value=L["Table"+str(value)]['time lapse']
    #     ))],

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
