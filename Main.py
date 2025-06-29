from dash import Dash, dcc, html, Input, Output, callback
from Display import Display_Data
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
display_data = Display_Data()

graphing_data = display_data.get_plottable_vectors()


#plotting with a sample dataframe
df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "Sources" : ["src1", "src2", 'src3', 'src4'],
    "Startup": ["startup1", "startup2", 'startup3', 'startup4'],
    "Sector": ["apple", "apple", "orange", "orange"],
    "Summary" : ['summary1' , 'summary2', 'Summary3' , 'Summary4']
})

#creating scatter plot and adding lasso functionality
fig = px.scatter(df, x="x", y="y", color="Sector", hover_data=['Sources' , "Startup" , "Sector", "Summary"], custom_data=['Startup' ,'Sector', 'Summary' , 'Sources'])
fig.update_layout(dragmode='lasso', clickmode="event+select") #responsible for 

#setting layout of the app
app.layout=html.Div(
        [
    html.H1('Startup Graph'),
    dcc.Graph(id='Graph' , figure=fig),
    html.Div(id='display-points' , children=None)
        ],
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
                html.H1(custom_data[0]),
                html.Ul(
                    [
                    html.Li(id='Sector', children=custom_data[1], style={'color' : 'black'}),
                    html.Li(id='Summary',children=custom_data[2], style={'color': 'red'}),
                    html.Li(id='Sources', children=custom_data[3], style={'color' : 'yellow'})
                    ]
                )
            ]
        ) #saving elements in required html structure in this list for display

        preserved_points.append([point['x'], point['y'], custom_data[0], custom_data[1], custom_data[2], custom_data[3]]) #saving raw point data
    display_data.preserve_lasso(preserved_points) #saving raw points in Display object in case user wants to export

    return elemsList

if __name__ == '__main__':
    app.run(debug=True)