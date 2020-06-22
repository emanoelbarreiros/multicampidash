import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table as dt
import plotly.express as px


def get_layout(data, student_count):
    data_table, fig, multicampi_enrolled = get_data(data, student_count)

    layout = html.Div([
        html.H1('Dados Gerais do Multicampi'),
        html.Hr(),
        html.H3('Análise do quantitativo de estudantes que responderam ao formulário comparado ao número de estudantes matriculados no semestre corrente.'),
        html.Br(),
        dcc.Markdown('Total de estudantes matriculados no Multicampi: **{}**'.format(multicampi_enrolled)),
        dcc.Markdown('Total de estudantes que responderam ao formulário: **{} (~{:.1f}%)**'.format(data.index.to_numpy().size, data.index.to_numpy().size/multicampi_enrolled*100)),
        html.Br(),
        dcc.Graph(id='response-percentage', figure=fig),
        data_table,
    ])
    return layout


def get_data(data, student_count):
    multicampi_enrolled = 2519
    data_respondents = data.groupby('campus')['curso'].value_counts()
    df = data_respondents.to_frame(name='respostas')
    total_enrolled = []
    headers = []
    for val in data_respondents.index.values:
        total_enrolled.append(int(student_count[val[0] + '-' + val[1]]))
        headers.append(val[0] + '-' + val[1])
    df['matriculados'] = total_enrolled
    df['%'] = df['respostas'] / df['matriculados'] * 100
    chart_data = (df['respostas'] / df['matriculados'] * 100).values.tolist()
    source = pd.DataFrame({'Curso': headers,
                           'Porcentagem': chart_data})
    data_table = dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in source.columns],
        data=list(source.to_dict("index").values()),
    )
    fig = px.bar(source, x="Porcentagem", y="Curso", orientation='h')
    return data_table, fig, multicampi_enrolled