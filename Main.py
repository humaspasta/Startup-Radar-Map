import dash
from dash import Dash, dcc, html, Input, Output, callback, no_update
from Display import Display_Data
import dash_bootstrap_components as dbc
import plotly.express as px
import os
import pandas as pd

external_stylesheets = [dbc.themes.DARKLY , 'https://codepen.io/chriddyp/pen/bWLwgP.css']
display_data = Display_Data(data_path=os.path.join('.' , 'startups.csv'))
display_data.scrape_all_links()
vectors = display_data.get_plottable_vectors()

app = Dash(__name__ , external_stylesheets=external_stylesheets)


#graphing_data = display_data.get_plottable_vectors()



#plotting with a sample dataframe
# df = pd.DataFrame({
#     "x": [1,2,1,2],
#     "y": [1,2,3,4],
#     "Sources" : ["src1", "src2", 'src3', 'src4'],
#     "Startup": ["startup1", "startup2", 'startup3', 'startup4'],
#     "Sector": ["Cybersecurity", "Cybersecurity", "Ecommerce", "Logistics"],
#     "Summary" : ['summary1' , 'summary2', 'Summary3' , 'Summary4']
# })

#creating scatter plot and adding lasso functionality
fig = px.scatter(vectors, x="x", y="y", color="Sector", hover_data=["Name" , "Sector", 'Summary', "Funding_Stage"], custom_data=['Name' ,'Sector', 'Funding_Stage', 'Summary'], template='plotly_dark')
fig.update_layout(dragmode='lasso', clickmode="event+select") #responsible for 
#setting layout of the app
app.layout= html.Div(
        [
            html.Div #this div contains the graph and the header
            ( 
                [
                    html.H1('Startup Radar Map' , style={'color' : 'white'}),
                    dcc.Graph(id='Graph' , figure=fig),
                ]
            )
            ,
              html.Div #this div contains the button and anything that will help with downloading
            (
                [
                    html.Button(id='export-button', children='Export Data', n_clicks=None , style={'marginTop' : '20px' , 'marginLeft' : '10px'}),
                    dcc.Download(id='download-helper')
                ]
            )
        ,
            html.Div
            ( #this div contains the points that will be displayed when inside the lasso's bounds
                [
                    
                    html.Div(
                         id='display-points' , children=None , style={
                        'display' : 'flex',
                        'alignItems' : 'center',
                        'flexWrap' : 'wrap',
                        'gap' : '20px'
                    } , 
                   ),
                ]
            )
        ]
        ,
        style={'color' : 'black'}
    )

#function for displaying data
@callback(
    Output(component_id='display-points' , component_property='children'), #will set the children of the element with display-points to the points
    Input(component_id='Graph' , component_property='selectedData') #reads input from the lasso
)
def display_selected_points(selectedData):
    '''
    returns a list of selected elements in html form for display. Returns in the following format:
    [
    html.H1(children='StartupName'),
    html.UL(
        html.Li(id='Sector' , children = ""),
        html.Li(id='Summary', children = ""),
        html.Li(id='Sources', children = "")
    )
])
    '''
    
    preserved_points = [] #points to preserve

    if selectedData == None:
        return []
    
    
    elemsList = [] #elements to save

    for point in selectedData['points']:
        custom_data = point['customdata'] #retrieving the relevant point data to display
  
        elemsList.extend(
            [
                html.Div(
                    [
                html.H1(custom_data[0] , style={'color' : 'white'}),
                html.Ul(
                    [
                    html.Li(id='Sector', children=custom_data[1], style={'color' : 'White'}),
                    html.Li(id='Summary',children=custom_data[2], style={'color': 'lightblue'}),
                    html.Li(id='Sources', children=custom_data[3], style={'color' : 'darkgreen'})
                    ]
                )
                    ]
                , style={'background' : 'black' , 'padding' : '10px', 'borderRadius' : '30px' , 'marginLeft' : '10px' , 'marginRight' : '10px', 'marginTop' : '20px'}) #styling each information box
            ]
        ) #saving elements in required html structure in this list for display

        preserved_points.append([point['x'], point['y'], custom_data[0], custom_data[1], custom_data[2], custom_data[3]]) #saving raw point data
    display_data.preserve_lasso(preserved_points) #saving raw points in Display object in case user wants to export

    return elemsList

@callback(
        Output(component_id='download-helper' , component_property='data'),
        Output(component_id='export-button' , component_property='n_clicks'),
        Input(component_id='export-button' , component_property='n_clicks'),
        prevent_initial_call = True
)
def export_points(n_clicks):

    if n_clicks:
        return display_data.export_lasso() , None
    return no_update , no_update




if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)