from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)


app.layout = html.Div([
    html.H2('Analysing Sales of Pink Morsel'),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        # options=["north", "south", "east","west"],
        value=["north", "south", "east","west"],
        inline=True
    ),
])


@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"))


def update_line_chart(sales):
    df = pd.read_csv('output.csv') # replace with your own data source
    df['Date'] = pd.to_datetime(df['Date'])
    # mask = df.continent.isin(continents)
    fig = px.line(df, x="Date", y="Sales", height=600, color='Region')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



