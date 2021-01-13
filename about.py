import dash_core_components as dcc
import dash_html_components as html


def get_layout():
    layout = html.Div([
        html.Div([
            html.Div([
                html.H1('Comissão de Monitoramento Epidemiológico'),
                html.Hr(),
                html.P('Este sistema foi desenvolvimento pela Comissão de Monitoramento Epidemiológico do Multicampi UPE.'),
                html.P('Os dados foram obtidos dos boletins epidemiológicos das cidades monitoradas pela equipe.'),
                html.P('A Comissão de Monitoramento Epidemiológico é composta pelos integrantes listados abaixo.'),
                html.Br(),
                html.P('UPE Campus Garanhuns:'),
                html.Ul([
                    html.Li('Prof. Carlo Marcelo Revoredo da Silva'),
                    html.Li('Prof. Dâmocles Aurélio Nascimento da Silva Alves'),
                    html.Li('Prof. Daniel Dantas Moreira Gomes'),
                    html.Li('Prof. Emanoel Francisco Spósito Barreiros'),
                    html.Li('Prof. Iaponan Cardins de Sousa Almeida'),
                    html.Li('Prof. Iwelton Madson Celestino Pereira'),
                    html.Li('Profa. Régia Maria Batista Leite'),
                    html.Li('Profa. Rosângela Estevão Alves Falcão'),
                    html.Li('Dherfferson Montini Barros'),
                    html.Li('José Edgleyson Ferreira de Paula'),
                    html.Li('José Thiago Sampaio Luna'),
                    html.Li('Kelvin Vascondelos Alencar'),
                    html.Li('Luiz Gustavo Gomes de Oliveira Matias'),
                    html.Li('Muryllo Pimenta de Oliveira'),
                    html.Li('Sávio Santos de Araújo'),
                ]),
                html.P('UPE Campus Salgueiro:'),
                html.Ul([
                    html.Li('Profa. Eryka Fernanda Miranda Sobral'),
                    html.Li('Profa. Josiete da Silva Mendes'),
                    html.Li('Prof. Wanderberg Salves Brandão'),
                ]),
                html.P('UFPE:'),
                html.Ul([
                    html.Li('Getúlio Valdemir Batista'),
                ])
            ], className='col-12')
        ], className='row'),
        html.Div([
            html.Div([
                html.Div([
                    html.P('Dados atualizados em 07/01/2021 às 15h51.')
                ], className='col-12')
            ])
        ], className='row')
    ])

    return layout
