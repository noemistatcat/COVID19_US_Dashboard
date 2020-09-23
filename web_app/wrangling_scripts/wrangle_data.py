import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import us

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`
# Read the datasets
# Confirmed Cases
df_confirmed = pd.read_csv('data/time_series_covid19_confirmed_US.csv')
df_deaths = pd.read_csv('data/time_series_covid19_deaths_US.csv')

# Transform the data from wide to long
df_deaths = pd.melt(df_deaths.drop(columns=['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 
                    'Country_Region','Combined_Key', 'Lat', 'Long_'], axis=1),
            id_vars=['UID', 'Population','Province_State'],var_name='date', value_name='deaths')

df_confirmed = pd.melt(df_confirmed.drop(columns=['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 
                    'Country_Region','Combined_Key', 'Lat', 'Long_'], axis=1),
            id_vars=['UID', 'Province_State'],var_name='date', value_name='confirmed')

df = df_deaths.merge(df_confirmed[['UID','date','confirmed']], on = ['UID', 'date'])

# Group by State
df = df[['date','Province_State','Population','deaths','confirmed']].groupby(['date','Province_State']).sum().reset_index()

# Filter out 'Diamond Princess', 'Grand Princess'
df = df[~df.Province_State.isin(['Diamond Princess', 'Grand Princess'])]

# Get the state code for each US State
df['State_Code'] = [us.states.lookup(x).abbr for x in df['Province_State']]

def return_figures():
    """Creates plotly visualization

    Args:
        None

    Returns:
        list (dict): list the four plotly visualization

    """
    figure = px.choropleth(
        df,  # Input Pandas DataFrame
        locations="State_Code",  # DataFrame column with locations
        color="confirmed",  # DataFrame column with color values
        range_color=(0, df['confirmed'].max()),
        color_continuous_scale=px.colors.sequential.Bluyl,
        hover_name="Province_State", # DataFrame column hover info
        locationmode = "USA-states",  # Set to plot as US States
        animation_frame="date")
  

    layout_one = figure.update_layout(
        title_text = None, # Create a Title         
        geo_scope='usa',  # Plot only the USA instead of globe
        )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines')
                    )
    
    layout_two = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    graph_three.append(
      go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_three = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    graph_four.append(
      go.Scatter(
      x = [20, 40, 60, 80],
      y = [10, 20, 30, 40],
      mode = 'markers'
      )
    )

    layout_four = dict(title = 'Chart Four',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=figure, layout=layout_one))
#    figures.append(dict(data=figure, layout=layout_two))
#     figures.append(dict(data=graph_three, layout=layout_three))
#     figures.append(dict(data=graph_four, layout=layout_four))

    return figures