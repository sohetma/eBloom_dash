# Author : Sohet Maxime
# NOMA : 7655-1300
# creation : 15/02/2019
# eBloom : Memoire CPME - EPL 


import dash
import os
import copy
import time
import datetime
import base64
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
#from flask_caching import Cache
from dash.dependencies import Input, Output
import dash_auth
import dash

#from sklearn.cluster import KMeans
from statistics import mean 

from functions import cout_manque_bien_etre
from functions import cleanAndOrganize_kpi
from functions import zeroToAverage
from functions import meandata
from functions import cleaningAndOrganise_scores
from functions import orgadata