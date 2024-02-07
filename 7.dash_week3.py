# Import required libraries
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
Launch_Site_1 =spacex_df['Launch Site'].unique()
Launch_Site = np.insert(Launch_Site_1, 0, 'ALL')
df = pd.DataFrame(spacex_df)
df_grouped = df.groupby('Launch Site')['class'].value_counts().unstack().fillna(0)
df_grouped['Total'] = df_grouped.sum(axis=1)
df_grouped['Exitoso (%)'] = (df_grouped[1] / df_grouped['Total']) * 100
df_grouped['Fallido (%)'] = (df_grouped[0] / df_grouped['Total']) * 100
df_grouped['Places']=Launch_Site_1
# Create a dash application
app = dash.Dash(__name__)
print('inicio')
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([#TASK 2.2: Add two dropdown menus
                                    html.Label("Select Statistics:"),
                                    dcc.Dropdown(id='site-dropdown',  options=[{'label': i, 'value': i} for i in Launch_Site],
                                                 placeholder='Select a Launch Site here',
                                                 searchable=True)
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    html.P("Payload range (Kg):"),
                                    dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                    100: '100'},
                                    value=[min_payload, max_payload]),
                                ]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(df_grouped , values='Exitoso (%)', 
        names='Places', 
        title='total successful launches count for all sites')
        return fig

    else:
        valores_fila = pd.DataFrame(df_grouped.loc[entered_site])
        #valores_fila_2 = valores_fila.groupby('Exitoso (%)')['Fallido (%)'].value_counts()
        valores_fila.drop(index=['Total', 'Places',1,0], inplace=True)
        fig = px.pie(valores_fila , values=str(entered_site), 
        names=valores_fila.index, 
        title=f'the Success vs. Failed counts {entered_site}')
        return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site,range):
    if entered_site == 'ALL':
        datos_filtrados = spacex_df[(spacex_df['Payload Mass (kg)'] >= range[0]) & (spacex_df['Payload Mass (kg)'] <= range[1])]
        print(entered_site)
        fig = px.scatter(datos_filtrados, x='Payload Mass (kg)', y='class', title='correlation between payload and launch success')
        return fig
    else: 
        #print(datos_limitados.size)
        otro = spacex_df[spacex_df['Launch Site'] == entered_site]
        datos_filtrados = otro [(otro ['Payload Mass (kg)'] >= range[0]) & (otro['Payload Mass (kg)'] <= range[1])]
        fig = px.scatter(datos_filtrados, x='Payload Mass (kg)', y='class', title=f'correlation between payload and launch success {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
