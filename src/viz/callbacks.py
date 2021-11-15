import plotly.graph_objs as go
from dash.dependencies import Output, Input

from crypto.models import Quote
from viz.plotly_apps import app
from viz.utils import build_candle_lists, add_moving_avg_figure, add_key_levels_figure


@app.callback(
    Output(component_id="symbol_quotes_graph", component_property="figure"),
    [
        Input(component_id="symbol_select", component_property="value"),
        Input(component_id="indicators_list", component_property="value"),
        Input(component_id="key_levels", component_property="value"),
    ],
)
def build_graph(symbol_name, indicators_list, key_levels) -> go.Figure:
    quotes = Quote.objects.filter(symbol__name=symbol_name)

    timestamp, open_, high, low, close = build_candle_lists(quotes)

    fig = go.Figure(
        data=[go.Candlestick(x=timestamp, open=open_, high=high, low=low, close=close)]
    )

    fig.update_layout(xaxis_rangeslider_visible=False)

    if indicators_list is not None:
        fig = add_moving_avg_figure(
            indicators_list=indicators_list,
            symbol_name=symbol_name,
            fig=fig,
            ind_repo=IR,
            timestamps=timestamp,
        )

    if key_levels is not None:
        fig = add_key_levels_figure(symbol=symbol_name, fig=fig, repo=IR)

    return fig
