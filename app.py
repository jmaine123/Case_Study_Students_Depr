import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv('./Student Depression Dataset.csv')
depressed_students = df.query('Depression == 1')
non_depressed_students = df.query('Depression == 0')

degree_depressed = depressed_students.groupby('Degree').size()
# degree_depressed.plot(kind='bar', title='Count of depressed students based on their degree')

depressed_and_suicidal = depressed_students.groupby('Have you ever had suicidal thoughts ?').size()

# depressed_and_suicidal.plot(kind="pie",autopct='%1.1f%%', title='Depressed with Suicidal thoughts')

#Data for students who are depressed, separating categories based on Age
older_depressed_df = df.query('Depression ==1 and Age >=30').groupby('Gender').size()
younger_depressed_df = df.query('Depression ==1 and Age <30').groupby('Gender').size()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Define custom colors
pie_colors = ['#0bbdab', '#f14655']

# dash colors

dash_colors = {
    'background': '#1053ad',
    'text': '#8ff9ff'
}

# Define the layout of the dashboard
app.layout = dbc.Container([
    html.Div(children=[
        html.Div(
            html.H1(children='Study On How Depression Effects Students', style={ 'textAlign': 'center', 'color': dash_colors['text'], 'font_size': '70px', 'padding-top': '20px'}),
            
        ),

        html.Div(
            dcc.Dropdown(
                id='status-dropdown',
                options=[
                    {'label': 'Depressed', 'value': 'Depressed'},
                    {'label': 'Not Depressed', 'value': 'Not Depressed'}
                ],
                value='Not Depressed',
                clearable=False,
                style={'width': '150px', 'backgroundColor': dash_colors['text'], 'font_color': dash_colors['background'], 'border': '1px solid', 'border_color': dash_colors['background']}
            ), style={'padding-top': '70px'}
        ),

            dcc.Graph(id='depress-eating-graph'),
        
        html.Div(children=[
            html.H2(children='Count of Depressed Students Based on their Degree', style={ 'textAlign': 'center', 'color': dash_colors['text']}),
            
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='bar-chart', figure=px.bar(degree_depressed).update_layout(paper_bgcolor=dash_colors['background'], plot_bgcolor=dash_colors['text'], font_color=dash_colors['text'], showlegend=False)),
                    width={'size': 6, 'offset': 3},
                    
                ),
            )
        ], style={'margin-top': '20px'}),
        
        html.Div(children=[
            html.H2(children='Depressed with Suicidal thoughts', style={ 'textAlign': 'center', 'color': dash_colors['text']}),
            
            dbc.Row([
                dbc.Col(dcc.Graph(id='dep-sui-chart', figure=px.pie(depressed_and_suicidal, names=depressed_and_suicidal.index, values=depressed_and_suicidal.values, title="Depressed with Suicidal Thoughts (Yes/No)", color_discrete_sequence=pie_colors).update_layout(paper_bgcolor=dash_colors['background'], font_color=dash_colors['text'])), width={'size': 6, 'offset': 3}, style={'backgroundColor': dash_colors['text'], 'padding': '2px', 'textAlign':'center'})
      
            ]),
            
        ], style={'padding-top': '50px'}),
        
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='older_dep', figure=px.pie(older_depressed_df, names=older_depressed_df.index, values=older_depressed_df.values, title="Depressed Students Over The Age Of 30", color_discrete_sequence=pie_colors).update_layout(paper_bgcolor=dash_colors['background'], plot_bgcolor=dash_colors['text'], font_color=dash_colors['text'])),
                width=5,
                style={'backgroundColor': dash_colors['text'], 'padding': '1px'}
            ),
            dbc.Col(
                dcc.Graph(id='young_dep', figure=px.pie(younger_depressed_df, names=younger_depressed_df.index, values=younger_depressed_df.values, title="Depressed Students Under The Age Of 30", color_discrete_sequence=pie_colors).update_layout(paper_bgcolor=dash_colors['background'], plot_bgcolor=dash_colors['text'], font_color=dash_colors['text'])),
                width=5,
                style={'backgroundColor': dash_colors['text'], 'padding': '1px', 'text-align': 'center'}
            )
        ],style={ 'width':'75%', 'margin': '30px 20%'}),
    ])
], style={'background-color': dash_colors['background'], 'font-family': 'san-serif', 'padding':'20px'})



# Define callback to update graph
@app.callback(
    Output('depress-eating-graph', 'figure'),
    Input('status-dropdown', 'value')
)
def update_graph(selected_status):
    filtered_df = depressed_students if selected_status != "Not Depressed" else non_depressed_students
    sleep_to_diet = filtered_df.groupby(['Sleep Duration', 'Dietary Habits']).size().reset_index()
    sleep_to_diet.rename(columns={0:"Count"}, inplace=True)
    table = pd.pivot_table(sleep_to_diet, index='Sleep Duration', columns='Dietary Habits', values='Count').reset_index()
    sleep_to_diet
    table
    figure = px.bar(sleep_to_diet, x='Sleep Duration', y='Count', color='Dietary Habits', barmode='group' ,title=f'Sleep Duration Compared to Eating Habit - {selected_status}').update_layout(plot_bgcolor="#222222", paper_bgcolor=dash_colors['background'], font_color=dash_colors['text'], title_font_size=27)
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
