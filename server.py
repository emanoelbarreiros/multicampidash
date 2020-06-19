from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

server = Flask('multicampidash')
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)