import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

from crypto.models import Quote, Symbol

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = DjangoDash("SimpleExample", external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        dcc.Dropdown(id="symbols", placeholder="Select symbol"),
        dcc.Checklist(
            id="toggle-rangeslider",
            options=[{"label": "Include Rangeslider", "value": "slider"}],
            value=["slider"],
        ),
        dcc.Graph(id="graph", animate=False),
        dcc.Interval(id="slider"),
    ]
)


@app.callback(Output("graph", "figure"), Input("symbols", "options"))
def get_available_symbols():
    breakpoint()


@app.callback(Output("graph", "figure"), [Input("toggle-rangeslider", "value")])
def display_candlestick(value):
    symbol = Symbol.objects.get(name="ETHBTC")
    time_unit = "1d"
    quotes = Quote.objects.filter(symbol=symbol, time_unit=time_unit).only(
        "open", "close", "high", "low"
    )

    fig = go.Figure(
        go.Candlestick(
            x=[quote.open_date for quote in quotes],
            open=[quote.open for quote in quotes],
            high=[quote.high for quote in quotes],
            low=[quote.low for quote in quotes],
            close=[quote.close for quote in quotes],
        )
    )
    fig.layout.yaxis.range = [
        min([quote.low for quote in quotes]),
        max([quote.high for quote in quotes]),
    ]

    fig.update_layout(xaxis_rangeslider_visible="slider" in value, height=700)

    return fig
