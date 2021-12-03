import numpy as np
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



app = dash.Dash(__name__)

app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.H1("COVID-19 VACCINE PROGRESSION", style={'text-align':'center','color':'black','backgroundColor':'white'}),
    html.P(dcc.Link('Enter Dashboard', href='/page-1'),style={'text-align':'center','color':'white'}),
    html.Div(id='page-content'),
])


df=pd.read_csv(r"D:\S4\DV\Covid Progression\country_vaccinations.csv")

df['iso_code'] = df['iso_code'].fillna('Unknown')
df = df.fillna(0)

vaccine = df.groupby(["country","vaccines"])['total_vaccinations','total_vaccinations_per_hundred', 'daily_vaccinations','daily_vaccinations_per_million'].max().reset_index()
#vaccine = df

fig1=px.choropleth(vaccine, locations='country',locationmode='country names', color='total_vaccinations')

fig2=px.choropleth(vaccine, locations='country',locationmode='country names', color='daily_vaccinations')

fig3=px.choropleth(vaccine, locations='country',locationmode = 'country names', color='vaccines')

fig4=px.treemap(vaccine,path=['country','vaccines'],values='total_vaccinations')

adf=vaccine.sort_values(by='total_vaccinations',ascending=False).head(10)

fig5 = px.sunburst(adf, path=['country', 'vaccines'], values='total_vaccinations')

adf=vaccine.sort_values(by='total_vaccinations')

fig6 = px.sunburst(adf, path=['country', 'vaccines'], values='total_vaccinations')

fig7 = px.scatter_matrix(df, dimensions=['total_vaccinations','daily_vaccinations','people_vaccinated'], color="vaccines")

fig8 = px.imshow(df.corr()).update_layout(title='CORRELATION')

fig9 = px.area(df, x="date", y="daily_vaccinations", color='country')

fig10 = px.line(df, x="date", y="total_vaccinations", color='country')



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname=='/page-1':

            return html.Div(children=[
            html.Div(
                    [
                        html.A(
                            html.Button("Colab link", id="learn-more-button"),
                            href="https://colab.research.google.com/drive/1oXkGNcX8Pd-uC7gzWfHuZRhGSO-cCbBU?usp=sharing",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            # All elements from the top of the page
            html.Div([
                html.Div([
                    html.H1(children='TOTAL VACCINATION',style={'text-align':'center','backgroundColor':'white'}),
                    
                    dcc.Graph(
                        id='graph1',
                        figure=fig1
                    ),  
                    html.Div(children='''
                        INFERENCE: From the above choropleth graph, it can be inferred that the United States has the highest rate on Total Vaccinations.
                '''),
                ], className='six columns'),
                html.Div([
                    html.H1(children='Daily Vaccination',style={'text-align':'center','backgroundColor':'white'}),

                    dcc.Graph(
                        id='graph2',
                        figure=fig2
                    ),  
                     html.Div(children='''
                        INFERENCE: From the above choropleth graph, it can be inferred that the country China has the highest rate of daily vaccinations.
                '''),
                ], className='six columns'),
            ], className='row'),
            # New Div for all elements in the new 'row' of the page
            html.Div([
                html.Br(),
                html.H1(children='Vaccine In Action',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph3',
                    figure=fig3
                ),  
                html.Div(children='''
                        INFERENCE: From the above graph, it can be inferred that various countries use different types of vaccines and each color denotes the different vaccine used by them
                '''),
            ], className='row'),

            html.Div([
                html.Br(),
                html.H1(children='Tree Map based on Total Vaccinations',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph4',
                    figure=fig4
                ),  
                html.Div(children='''
                    
                '''),
            ], className='row'),

            html.Div([
                html.Br(),
                html.H1(children='Top Total Vaccinated Countries and Vaccines Used',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph5',
                    figure=fig5
                ),  
                html.Div(children='''
                        INFERENCE: US took first place in total vaccination and they use Moderna, Pfizer/BioNTech and China took second position and the vaccine used by them is Sinopharm/Beijing, Sinopharm/Wuhan, Sinovac.
                '''),
            ], className='row'),

            html.Div([
                html.Br(),
                html.H1(children='Less Total Vaccinated Countries and Vaccines Used by them',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph6',
                    figure=fig6
                ),  
                html.Div(children='''
                        INFERENCE: Saint Helena took first position in less total vaccinations and they use Oxford/AstraZeneca.
                '''),
            ], className='row'),

            html.Div([
                html.Br(),
                html.H1(children='Scatter plot Martrix',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph7',
                    figure=fig7
                ),  
                html.Div(children='''
                        INFERENCE: From the above scatter plot matrix, relationship between various features can be identified.
                '''),
            ], className='row'),

            html.Div([
                html.Br(),
                html.H1(children='Daily Vaccination Trend',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph9',
                    figure=fig9
                ),  
                html.Div(children='''
                        INFERENCE: From the above graph, US has the highest trend among countries
                '''),
            ], className='row'),

            html.Div([
                html.Br(),
                html.H1(children='Total Vaccination Trend',style={'text-align':'center','backgroundColor':'white'}),


                dcc.Graph(
                    id='graph10',
                    figure=fig10
                ),  
                html.Div(children='''
                        INFERENCE: From the above graph, US has the highest trend among countries.
                '''),
            ], className='row'),
        ])
    

if __name__ == '__main__':
    app.run_server(debug=True)