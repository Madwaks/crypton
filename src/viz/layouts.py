import dash_html_components as html

layout = html.Div(
    [
        html.Label("Symbol"),
        # dcc.Dropdown(
        #     id="symbol_select",
        #     options=[{"label": symbol.name, "value": symbol.name} for symbol in Symbol.objects.all()],
        #     value="ETHBTC",
        # ),
        # html.Div(id='graph', children=dcc.Graph(id='symbol_quotes_graph')),
        # html.Label('Moving averages'),
        # dcc.Checklist(id="indicators_list",
        #               options=INDICATORS_CHECKLIST, labelStyle=STYLE_MM_CHECKLIST
        #               ),
        # html.Label("Support & Resistances"),
        # dcc.Checklist(id="key_levels",
        #               options=[{"label": "Yes", "value": "True"}], labelStyle=STYLE_MM_CHECKLIST
        #               )
    ]
)
