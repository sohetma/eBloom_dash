# Author : Sohet Maxime
# NOMA : 7655-1300
# creation : 15/02/2019
# eBloom : Memoire CPME - EPL 

###############################################################
###############              IMPORT            ################
############################################################### 
from import_eBloom import *

###############################################################
###############              DATASET           ################
############################################################### 

""" USERNAME + PASSWORD """
# Keep this out of source code repository - save in a file or a database
USERNAME_PASSWORD = [['username', 'password'], ['maxime', '1111'], ['eBloom', 'Be4'], ['promoteur', 'promoteur']]


""" READ THE DATASET """
path = './data/'

filename = 'socio-demo.csv'
filename2 = 'risque2.csv'
filename3 = 'risque-average.csv'
filename4 = 'heatmap.csv'
filename5 = 'score.csv'
filename6 = 'kpi.csv'
filename7 = 'socio-demo2.csv'
  

dataset = pd.read_csv(path + filename , encoding = "ISO-8859-1", delimiter=';')
dataset2 = pd.read_csv(path + filename2 , encoding = "ISO-8859-1", delimiter=';')
dataset3 = pd.read_csv(path + filename3 , encoding = "ISO-8859-1", delimiter=';')
dataset4 = pd.read_csv(path + filename4 , encoding = "ISO-8859-1", delimiter=';')
dataset5 = pd.read_csv(path + filename5 , encoding = "ISO-8859-1", delimiter=';')
dataset6 = pd.read_csv(path + filename6 , encoding = "ISO-8859-1", delimiter=';')
dataset7 = pd.read_csv(path + filename7 , encoding = "ISO-8859-1", delimiter=';')



###############################################################
#####      COMPONONENTS AND MANIPULATION OF DATA        #######
############################################################### 


""" ORGANISE DROPDOWN 1 """
options_age_sexe = []
count = 0
for variables in dataset['Variables'].unique():
    count += 1  
    options_age_sexe.append({'label' : str(variables) , 'value': int(count) })
options_age_sexe = options_age_sexe[1:107]

features = dataset.columns[4:9]
#print(features)


""" ORGANISE DROPDOWN 2 """
options_test2= []
for variables in dataset2['DIVISION'].unique():
    options_test2.append({'label' : str(variables) , 'value': str(variables)}) #-2
    
options_test2 = options_test2[2:14]


""" ORGANISE DROPDOWN 3 """
options_test3= []
for variables in dataset2['TEAM'].unique():
    options_test3.append({'label' : str(variables) , 'value': str(variables)}) #-1 
    
options_test3 = options_test3[1:652]


""" ORGANISE DROPDOWN 4 """
options_test4 = [{'label' : 'Engagement', 'value' : 'Engagement'},
				 {'label' : 'Stress', 'value' : 'Stress'},
				 {'label' : 'Satisfaction', 'value' : 'Satisfaction'},
				 {'label' : 'Loyauté', 'value' : 'Loyauté'}]


""" DATA HEATMAP """
features_heatmap = list(dataset4.columns.values)
features_heatmap = features_heatmap[1:]
variables_heatmap = list(dataset4['DIVISION'].values)
dataset4 = dataset4.iloc[:,1:]
M = dataset4.as_matrix()/10000


""" Data score """
average, scores, reference, info_teams, dataset5_bis, features_dataset5 = cleaningAndOrganise_scores(dataset5)
teams = info_teams.iloc[:,2]
feat_data = features_dataset5[0:104]
dataset5_bis.columns = feat_data

""" ORGANISE DROPDOWN 5 """
count = 0
options_test5 = []
for variables in dataset5_bis['TEAM'].unique():
    options_test5.append({'label' : str(variables) , 'value': int(count)}) 
    count += 1 
 

""" ORGANISE DROPDOWN 6 """
options_test6 = []
options6 = average.columns.values
for variables in options6:
    options_test6.append({'label' : str(variables) , 'value': str(variables)}) 


""" Data Table """
dataset7 = orgadata(dataset7)



""" DATA KPI """
X,Y,features_kpi,locations = cleanAndOrganize_kpi(dataset6)
row, col = X.shape
mean_indicateur = []
for i in range(0,row):
  mean_indicateur.append(mean(X.iloc[i,:].values))
#mean_indicateur.columns = ['moyenne']
output = Y.iloc[:,12].values/10000
output_dataFrame = pd.DataFrame(output)
#XY = pd.concat([X, output_dataFrame], axis = 1)

mean_indicateur = pd.DataFrame(mean_indicateur)  
data_mean = pd.concat([mean_indicateur, output_dataFrame], axis = 1)
data_mean.columns = ['mean_indicateur', 'absenteisme']

cout = cout_manque_bien_etre(data_mean, 30000, pourcentage =  0.10 , salaire_moyen = 45000) 
print(cout)




######################################################################################################
######################################################################################################
############                          DASHBOARD APPLICATION                          #################
######################################################################################################
######################################################################################################

#ADD CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'eBloom'

#AUTHORISATION
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD)

#SERVER
server = app.server


#COLORS
colors = {
			'background' : 'FFFFFF', #62bfe2
			'blanc' : '#FFFFFF',
			'blancV' : '#F0FFF0',
			'blancBleu' : '#E8F6F3',
			'gris' : '#DCDCDC',
			'text' : '#74b9ff',
			'text2' : '#A0E362',  #00cec9
			'text3' : '#66C5BA',
			'noir' : '#000000',
			'bleu' : 'rgb(49,130,189)',
			'bleuciel' : '#E0F7FA',
			'bleubleu' : '#29B6F6',
			'vertpomme' : 'rgb(50,230,100)',
			'vertfonce' :  'rgb(70,200,150)',
			'vertstyle' : 'rgb(90,250,190)',
         }


###############################################################
###############           SOME DATA             ###############
############################################################### 

indicateurs = ['Engagement', 'Stressklachten' , 'Satisfaction','Loyalty','Taakbelasting','Taakmotivatoren','Relaties team','Organisat. steun']
indicateurs2 = ['Engagement', 'Stressklachten' , 'Satisfaction','Loyalty','Taakbelasting','Taakmotivatoren','Relaties team','Organisat. steun', 'Engagement']
indicateurs3 = ['Stress', 'Engagement', 'Loyauté' , 'Satisfaction', 'Charges et équilibre','Developpement perso','Relation en équipe','Avis employeur', 'Stressklachten']
index_moyen_entreprise = [4.74,3.51,4.49,4.81,4.26,4.68,5.29,4.04]
index_moyen_benchmark = [5.1,3.09,4.62,5.26,4.62,4.92,5.54,4.44]
index_moyen_benchmark_polar = [3.09, 5.1,5.26, 4.62, 4.62,4.92,5.54,4.44]

#index_moyen_benchmark_bis = [5.1,? , ? ,3.09,4.62,5.26,4.62,4.92,5.54,4.44]

trace0 = go.Bar(x = indicateurs, y = index_moyen_entreprise, name = "Moyenne", marker = go.bar.Marker(color='rgb(78,221,180)'))
trace1 = go.Bar(x = indicateurs, y = index_moyen_benchmark, name = 'Benchmark', marker = go.bar.Marker(color='rgb(49,130,189)'))        													
dat = [trace0, trace1]




###############################################################
###############               LAYOUT           ################
############################################################### 

app.layout = html.Div([

						###############################################################
 						###############         TITLE + VISION         ################
 						############################################################### 
						html.Div(
							style={'backgroundColor' : colors['blancV'], }, #, 'width' : '100%', 'border' : '2px solid', 'color' : colors['vertfonce']
							children=[
    								#html.H1(
    								#		children='eBloom',
    								#		style={'textAlign': 'center','color': colors['text2'], 'font-style' : 'italic'}
    								#	   ),
    								html.Img(src = app.get_asset_url('ebloom.png'), style = {'height' : 100, 'textAlign' : 'center'}), # 'data:image/png;base64,{}'.format(encoded_image)
    								html.H2(
    										children = "Promoting well-being enhancement everyday",
    										style={'textAlign': 'center','color': colors['bleu'], 'font-style' : 'normal'}
    									   ),
    								html.P(children = "DASHBOARD", style = {'textAlign': 'center','color': colors['bleu'], 'font-style' : 'normal', 'font-size' : '18pt'}) ,
    								html.P(style = {'height' : 5}),
					  				 ],
					  	),
					  	 

						html.Div(children = [
							html.Div([
								html.Div([
									html.P('Dernière mise à jour des données : 25-05-2019',  style = {'textAlign' : 'center', 'color' : colors['noir'], 'width' : '100%' , 'height' : '30', 'font-size' : '15pt'})
								],
								style = { 'border' : '10px solid', 'color' : colors['blancBleu'],'backgroundColor' : colors['blanc'], 'textAlign' : 'center', 'width' : '30%' },
								className = 'four columns'),

								html.Div([
									html.P('Nombre de répondants : 15 153 sur 30 000', style = {'textAlign' : 'center', 'color' : colors['noir'], 'width' : '100%' , 'height' : '30', 'font-size' : '15pt'}),
								],
								style = { 'border' : '10px solid', 'color' : colors['blancBleu'],'backgroundColor' : colors['blanc'], 'textAlign' : 'center' ,'width' : '30%'},
								className = 'four columns' 
								),

								html.Div([
									html.P('Coût de manque en bien-être estimé à : 40 000 000 €/an', style = {'textAlign' : 'center', 'color' : colors['noir'], 'width' : '100%', 'height' : '30', 'font-size' : '15pt'}),
								],
								style = { 'border' : '10px solid', 'color' : colors['blancBleu'],'backgroundColor' : colors['blanc'], 'textAlign' : 'center' , 'width' : '32%'},
								className = 'four columns' 
								),
							],
							className = 'row'
							),

							html.Div([
								html.P(), #ICI
							],
							#style = { 'border' : '10px solid', 'color' : colors['blancBleu'],'backgroundColor' : colors['blanc'], 'textAlign' : 'center'  },
							className = 'six columns '
							),

						],
						style = {'color' : colors['noir'], 'textAlign' : 'center'},
						className = 'row'
						),	



						html.Div(children = [
							html.P(style = {'height' : 5}),
						    ###############################################################
	 						###############          FIRST STAGE           ################
	 						############################################################### 
							html.Div(children = [

								# PLOT 1
						  	 	html.Div([	


								   # BAR CHART : OVERVIEW FACTEURS
								  	dcc.Graph(
		        						    figure=go.Figure
		        						    (	
		        						    	data = dat, 	
		           								layout=go.Layout(
		           									 	xaxis=dict(tickangle=-45),
		           										barmode='group',           										 
		            									title='Global overview : moyennes par facteur',
		            									showlegend=True,
		            									yaxis=dict(range= [0,7],title='Score (1-7)',titlefont=dict(size=16,color='rgb(107, 107, 107)')), 
		            									#legend=go.layout.Legend(x=0,y=1.0),
		            									#margin=go.layout.Margin(l=40, r=0, t=40, b=30)
		        										)
		    								),
		    							    style={'height': 590 , 'display' :'inline-block', 'margin' : {'l' : 10 , 'b' : 20, 't' : 0, 'r' : 0}, 'width' : '80%', 'textAlign' :'center'},
		    								id='my-graph',	
									), 
							    ], 
							    style = { 'border' : '10px solid', 'color' : colors['blancBleu'],'backgroundColor' : colors['blanc'] },
							    className = "six columns",
							 	),


								#html.P('', style = {'height' : 30}),	
								#html.H1('Facteur du bien-être par tranche d âge', style = {'color' : colors['noir'], 'textAlign': 'center', 'font-size' : '18px', 'font-family' : 'arial', 'font-style' : 'normal'},),			

								# PLOT 2
								html.Div([
							  		#SPYDER CHART
									dcc.Dropdown(
							  				id = 'my-dropdown5',		
											options = options_test5,
											value = '2', 
											style = {'height' : '30','width' : '75%','textAlign': 'center',  'display': 'inline-block' }
							  		),

									dcc.Graph(
											#figure = go.Figure(
											#					data = [go.Scatterpolar(r = index_moyen_entreprise,theta = indicateurs2 ,fill = 'toself',name = 'Entreprise', line =  dict(color = '#74b9ff')), #, fillcolor = '#74b9ff'
    										#							go.Scatterpolar(r = index_moyen_benchmark,theta = indicateurs2 ,fill = 'toself',name = 'Benchmark', line =  dict(color = '#A0E362')) #, fillcolor = '#A0E362'
    										#						   ],
											#					layout = go.Layout(title='Indicateurs : Team & Benchmark',   polar = dict(radialaxis = dict(visible = True, range = [2, 6])), showlegend = True)
											#	              ),		
											id = 'graph4',
											style = {'textAlign' : 'center', 'border' : '10px solid', 'color' : colors['blancBleu'], 'backgroundColor' : colors['blanc'], 'width' : '100%', 'height' : 550}
											#className = "four columns",
											),
									],
									style = { 'textAlign' : 'center', 'display' : 'inline-block',  },
									className = "six columns", 
								),	

						  	], 
						  	style={'width': '100%', 'display': 'inline-block'}, 
						  	className = "row",
						  	),


							###############################################################
	 						###############          SECOND STAGE           ###############
	 						###############################################################	

							#PLOT 3
							html.Div(children = [
								
								html.Div([	
									html.Label('DIVISION'),				
									dcc.Dropdown(
										id = 'my-dropdown2',		
										options = options_test2,
										value = 'BIZ', 
										style = {'height' : '30','width' : '100%','textAlign': 'center',  'display': 'inline-block' }
									),
								], 
								className="four columns",
								#style = {'height' : '30','width' : '75%','textAlign': 'center',  'display': 'inline-block' }
								),

								
								html.Div([		
									html.Label('TEAM'),			
									dcc.Dropdown(
										id = 'my-dropdown3',		
										options = options_test3,
										value = ' SALES CENTER IN', 
										style = {'height' : '30','width' : '100%','textAlign': 'center',  'display': 'inline-block' }
									),
								], 
								className="four columns",
								#style = {'height' : '30','width' : '75%','textAlign': 'center',  'display': 'inline-block' }
								),

								
								html.Div([	
									html.Label('INDICATEUR'),				
									dcc.Dropdown(
										id = 'my-dropdown4',		
										options = options_test4,
										value = 'Engagement', 
										style = {'height' : '30','width' : '100%','textAlign': 'center',  'display': 'inline-block' }
									),
								], 
								className="four columns",
								#style = {'height' : '30','width' : '75%','textAlign': 'center',  'display': 'inline-block' }
								),
								html.Div(children = [
									dcc.Graph(id='graph3', style = {'height' : '500', 'display': 'inline-block', 'textAlign' : 'center'}, className = "six columns",),
									dcc.Graph(id='graph2', style = {'height' : '500', 'display': 'inline-block','textAlign' : 'center'}, className = "six columns", )
								],
								style = {'width' : '100%', 'textAlign' : 'center', 'display': 'inline-block', 'border' : '10px solid', 'color' : colors['blancBleu'], 'background' : colors['blanc']},
								#className = "four columns",
								),
							],
							className = "row", #row
							style = {'width' : '98%', 'height' : '600', 'textAlign' : 'center',},
							),	



							###############################################################
	 						###############          THIRD STAGE           ################
	 						###############################################################
	 						html.Div(children = [
							


								#PLOT 4 
								html.Div([					  			
								   		html.Label('Selectionne une variable dans la liste déroulante', style = {'height' : '30', 'width' : '75%','textAlign': 'center',  'display': 'inline-block' }),
										dcc.Dropdown(
											id = 'my-dropdown1',		
											options = options_age_sexe,
											value = '3', 
											className="app-header--title",
											style = {'height' : '30','width' : '75%','textAlign': 'center',  'display': 'inline-block' }
										),
											
										html.Div ([
												html.Label("Facteur du bien-être par tranche d'âge", style = {'height' : '30', 'width' : '75%','textAlign': 'center',  'display': 'inline-block', 'color' : colors['noir']}),

												#HISTO PER YEAR
												dcc.Graph(id='graph1', style = {'height' : '400', }),
										], style = {'border' : '10px solid ', 'color' : colors['blancBleu'], 'backgroundColor' : colors['blanc'],}),
							  	],
							  	style = { 'height': 590, 'textAlign': 'center', 'display' :'inline-block', }, #, 'display' :'inline-block', 'margin' : {'l' : 10 , 'b' : 20, 't' : 0, 'r' : 0},
							  	className = "six columns",
							  	),	

								#html.P(children = "" , style = {'height ' : 100}),

							  	#PLOT 5 
							  	html.Div([
							  		#HEATMAP
									dcc.Graph(
											figure = go.Figure(
																data = [go.Heatmap(
																				   z = M,
		                   														   x = features_heatmap,
		                   														   y = variables_heatmap,
		                   														   colorscale =  'Viridis'
		                   														   )
																		],
																layout = go.Layout(title='HeatMap : Indicateurs & Divsions',
																					xaxis = dict(ticks='', nticks=60),
    																				yaxis = dict(ticks='', nticks=100),
																					margin = dict(t=120, l=250, b=100, pad=4)
																				   ),
												              ),		
											id = 'heatmap',
											style = {'textAlign' : 'center', 'width' : '90%', 'height' : '500'},
											className = "four columns",
											),
									],
									style = { 'border' : '10px solid', 'color' : colors['blancBleu'], 'backgroundColor' : colors['blanc'] , 'textAlign': 'center', 'display' :'inline-block',},
									className = "six columns", 
								),		

							],
							style={ 'width' : '100%', 'display': 'inline-block',}, # 'textAlign' : 'center'
						  	className = "row",
						  	),

							###############################################################
	 						###############          4th STAGE           ##################
	 						###############################################################
	 						html.Div(children = [

	 							html.Div([
	 								html.Div( [
		 								dcc.Dropdown(
		 									id = 'my-dropdown6',		
											options = options_test6,
											value = 'Index stress moyen', 
											style = {'height' : '30','width' : '70%','textAlign': 'center',  'display': 'inline-block' }
		 								),
		 								dcc.Dropdown(
		 									id = 'my-dropdown7',		
											options = options_test6,
											value = 'Index engagement moyen', 
											style = {'height' : '30','width' : '70%','textAlign': 'center',  'display': 'inline-block' }
		 								),
		 								html.Button('Apply clustering', id ='clustering1', style = {'backgroundColor' : '#A0E362', 'height' : '40', 'width' : '40%'}),
		 								html.P(style = {'height' : '5'}),
	 								],
	 								#style = {},
	 								#className = 'Four columns'
	 								),
	 								dcc.Graph(id = 'graph5',
	 										  style = {'border' : '10px solid', 'color' : colors['blancBleu'], 'backgroundColor' : colors['blanc'] }	
	 								)
	 							],
	 							style = { 'textAlign': 'center', 'display' :'inline-block','height' : '500'},
	 							className = 'six columns'
	 							),


	 							html.Div([
	 								html.Div([ 
	 									html.P("Tableau des scores agrégés par question et par catégorie "), #, 
	 								],
	 								style = {'color' : colors['noir']}
	 								),
	 								#dcc.Dropdown(),
	 								#dcc.Graph(id = 'graph6')

	 								dash_table.DataTable(
	 									id = 'table1',
	 									columns = [{"name" : i, "id" : i} for i in dataset7.columns],
	 									data = dataset7.to_dict('records'),
	 									style_table={ 'minHeight' : '500px',  'maxHeight': '500px', 'minWidth' : '500px', 'overflowX': 'scroll'}, #
	 									style_cell={'minHeight' : '50px', 'minWidth': '70px', 'maxWidth': '200px','whiteSpace': 'normal', 'color' : colors['noir'], 'textAlign' : 'center'},
	 									style_header={'backgroundColor' : colors['bleuciel'], 'fontWeight': 'bold'},
	 									sorting=True,
	 									filtering=True,
	 									#row_selectable='multi',

	 									style_cell_conditional=[{
            								'if': {'row_index': 'odd'},
            								'backgroundColor' : colors['bleuciel']
            								#'backgroundColor': 'rgb(248, 248, 248)'
        								}],

	 									css=[{
        									'selector': '.dash-cell div.dash-cell-value',
        									'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;',
    									}],
	 								),
	 								#html.A('Download CSV', id = 'my-link'),
	 							],
	 							style = {'border' : '10px solid', 'color' : colors['blancBleu'], 'backgroundColor' : colors['blanc'] , 'textAlign': 'center', 'display' :'inline-block','height':'600', 'margin' : {'l' : 10 , 'b' : 20, 't' : 0, 'r' : 0}},
	 							className = 'six columns'
	 							),

	 						],
	 						style = { 'width' : '100%', 'display': 'inline-block'},
	 						className = "row"
	 						),



						],
						# STYLE DASH PLOTS
						style = {'color' : colors['text'] , 'width' : '98%', 'display' :'inline-block',  'border' : '10px ', 'textAlign' : 'center' }
						),



					], 
					# STYLE DIV GENERAL	
					 style = {'color' : colors['text'], 'textAlign' : 'center', 'backgroundColor' : colors['blancV']}
					)




#ADD EXTERNAL CSS
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

"""
for val in options_age_sexe : 
    if(selected_variable == val.get('value')):
     	row = val.get('value')
"""



##############################################################
########    CALLBACKS + Functions of GRAPHS        ###########
##############################################################

#CALLBACK PLOT2
@app.callback(Output('graph1','figure'),
			 [Input('my-dropdown1', 'value')])

def update_figure(selected_variable):
	#print ('test')
	return { 'data' : [ go.Bar( 
								y = features, 
								x = dataset.iloc[int(selected_variable)-1,4:9]/100 , 
								orientation = 'h', 
								name = 'Moyenne des indices de l entreprise', 
								marker = go.bar.Marker(color='rgb(78,221,180)')
								)
					  ],

			 'layout ' : go.Layout(
			 					title = "Facteur du bien-être par tranche d'âge ",
			 					yaxis=dict(range= [0,7],title='Score (1-7)',titlefont=dict(size=16,color='rgb(107, 107, 107)')),
			 					  )
			}



#CALLBACK PLOT3 
@app.callback(Output('graph2','figure'),
			 [Input('my-dropdown2', 'value'),
			  Input('my-dropdown3', 'value'),
			  Input('my-dropdown4', 'value')])

def update_graph2(dropdown2, dropdown3, dropdown4): 

  if (lessThan10(dropdown2, dropdown3) == False ):
  	#print('error')
  	return {
			'data' :  [go.Pie(
							 	values = [0] ,
								labels = ['< 10 Réponses'] ,
								#name = " % ", 
								#hoverinfo = "label+percent",
								marker = dict(colors=['rgb(200,220,75)']),
								)
						 ],
			'layout' : go.Layout(
								title='Evaluation des risques par équipe et par indicateur ',
								annotations = [{"showarrow": False, 'text' : 'PAS DE GRAPHE','x': 0.73, 'y': 0.5}],
								)

			}
  else : 

	  filtered = dataset2[dataset2['DIVISION'] == dropdown2 ]
	  #filtered = dataset2
	  liste = []

	  for var in filtered['TEAM'].unique():
	    filtered = filtered[filtered['TEAM'] == dropdown3]
			#filtered_by_TEAM = filtered[filtered['TEAM'] == dropdown3]
				
	  for i in range(4,16):
	    results = filtered.iloc[:,i].values
	    results = list(map(int, results))
	    t = results[0]
	    liste.append(t)


	  if (dropdown4 == 'Engagement'): 
	    x = liste[0:3]
	  elif (dropdown4 == 'Stress'):
	    x = liste[3:6]
	  elif (dropdown4 == 'Satisfaction'):
	    x = liste[6:9]
	  elif (dropdown4 == 'Loyauté'):
	    x = liste[9:12]

	  label = ['Peu de risque', 'Risque moyen', 'Haut risque']

	  nbRep = lessThan10(dropdown2, dropdown3) 
	  text = "{}{}".format(round(nbRep,0)," réponses")
	  text2 = "{}{}{}{}".format(dropdown3, "&\n\n",  round(nbRep,0)," réponses")
	  title = 'Evaluation des risques par équipe et par indicateur '
	  title2 = "{}{}{}".format(title, " : ", dropdown3)

	  return {
				'data' :  [go.Pie(
									values = x ,
									labels = label ,
									#name = " % ", 
									hoverinfo = "label+percent",
									marker = dict(colors=['rgb(50,230,100)', 'rgb(70,200,150)', 'rgb(90,250,190)' ]),
									hole = 0.5

								),
						 ],
				'layout' : go.Layout(title= title2, annotations = [{"showarrow": False, 'text' : text ,'x': 0.5, 'y': 0.5}],)

			   }

#CALLBACK PLOT3 
@app.callback(Output('graph3', 'figure'),
			 [Input('my-dropdown2', 'value'),
			  Input('my-dropdown4', 'value')])

def update_graph3(dropdown2, dropdown4):
	filtered = dataset3[dataset3['DIVISION'] == dropdown2 ]

	l,c = filtered.shape
	#print('taille l', l)	
	if (l==0) : 	
  		return {
			'data' :  [go.Pie(
							 	values = [0] ,
								labels = ['< 10 Réponses'] ,
								#name = " % ", 
								#hoverinfo = "label+percent",
								marker = dict(colors=['rgb(200,220,75)']),
								)
						 ],
			'layout' : go.Layout(
								title='Evaluation des risques par Divsion',
								annotations = [{"showarrow": False, 'text' : 'PAS DE GRAPHE','x': 0.73, 'y': 0.5}],
								)
			}

	liste = []
	for i in range(2,14):
	    results = filtered.iloc[:,i].values
	    results = list(map(int, results))
	    t = results[0]
	    liste.append(t)

	if (dropdown4 == 'Engagement'): 
    		x = liste[0:3]
	elif (dropdown4 == 'Stress'):
    		x = liste[3:6]
	elif (dropdown4 == 'Satisfaction'):
    		x = liste[6:9]
	elif (dropdown4 == 'Loyauté'):
    		x = liste[9:12]


  	#print ('taille' , l)
	nbRep = filtered['Totaal # responses'].values[0] 

	text = "{}{}{}{}".format(dropdown2, ' &\n',  round(nbRep,0)," réponses")
	text2 = "{}".format(dropdown2)
	text3 = "{}{}".format(round(nbRep,0)," réponses")
	title = 'Evaluation des risques par Divsion '
	title2 = "{}{}{}".format(title, " : ", dropdown2)
  		
	label = ['Peu de risque', 'Risque moyen', 'Haut risque']

	return {
			'data' :  [go.Pie(
								values = x ,
								labels = label ,
								#name = " % ", 
								hoverinfo = "label+percent",
								marker = dict(colors=['rgb(50,230,100)', 'rgb(70,200,150)', 'rgb(90,250,190)']),
								hole = 0.5
								),
						 ],
			'layout' : go.Layout(title= title2, annotations = [{"showarrow": False, 'text' : text3 ,'x': 0.5, 'y': 0.5}],)

			}



#CALLBACK PLOT4
@app.callback(Output('graph4','figure'),
			 [Input('my-dropdown5', 'value')])

def update_graph5(selected_variable):
	#print ('test')
	teams_polar = list(info_teams.iloc[:,2].values)
	return { 'data' : [ go.Scatterpolar( 
							r = average.iloc[int(selected_variable)],
							theta = indicateurs3,
							fill =  'toself',
							name = teams_polar[int(selected_variable)], #'Team',
							line = dict(color = '#74b9ff')
						),

						go.Scatterpolar(
							r = index_moyen_benchmark_polar,
							theta = indicateurs3 ,
							fill = 'toself',
							name = 'Benchmark', 
							line =  dict(color = '#A0E362')
						)
					  ],

			 'layout ' : go.Layout(
			 					title = 'Indicateurs : Team & Benchmark',
			 					polar = dict(radialaxis = dict(visible = True, range = [2, 6])),
			 					showlegend = True
			 					)
			}



#CALLBACK PLOT5
@app.callback(Output('graph5','figure'),
			 [Input('my-dropdown6', 'value'),
			 Input('my-dropdown7', 'value'),
			 Input('clustering1', 'n_clicks')])

def update_graph6(dropdown6, dropdown7, n_clicks):
	x = average[dropdown6].values
	y = average[dropdown7].values
	xx = pd.DataFrame(x) 
	yy = pd.DataFrame(y)
	X = pd.concat([xx,yy], axis = 1)
	row_average, col_average = average.shape
	#X = average.ix[:,dropdown6:dropdown7]

	cluster_init = []
	for i in range(0,row_average):
		cluster_init.append(1)

	if (col_average == 0):
		cluster = cluster_init

	elif (n_clicks is None):
		cluster = cluster_init

	elif (n_clicks%2 ==1 and col_average != 0):
		
		
		taille1 , taille2 = X.shape 
		if (taille2 == 0): 
			return 'Problem : try an other indicator'
		else: 
			#Clustering
			cluster = cluster_init
			#cluster = clustering_kmeans(X)
	else : 
		cluster = cluster_init



	return { 'data' : [ go.Scatter( 
									x = x, 
									y = y , 
									mode = 'markers',
									marker = dict(color = cluster, colorscale = 'Viridis'),
									text = teams
								)
					  ],

			 'layout ' : go.Layout(
			 					title = "Facteur du bien-être par tranche d'âge ",
			 					  )
			}



##############################################################
#############      OTHERS UTILS FUNCTIONS      ###############
##############################################################

def lessThan10(dropdown2, dropdown3): 
  filtered = dataset2[dataset2['DIVISION'] == dropdown2 ]
  liste = []

  for var in filtered['TEAM'].unique():
    filtered = filtered[filtered['TEAM'] == dropdown3]

  l,c = filtered.shape	
  if (l==0) : return False		
  #print ('taille' , l)
  nbRep = filtered['Totaal # responses'].values[0]  
  #print("Nbre de repondants", nbRep)

  if(nbRep < 10) :
  	return False
  else : 
  	return nbRep


#Applying k-means to the mall dataset
'''
def clustering_kmeans(X):
	kmeans = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
	y_kmeans = kmeans.fit_predict(X)
	return y_kmeans
'''
##############################################################
#############             RUN SERVER           ###############
##############################################################

if __name__ == '__main__':
	app.run_server(debug=True)