import pandas as pd
import numpy as np

import plotly.graph_objects as go

# Colors used by graphs
colors = [
    '#4182C8', '#2E94B2',
    '#39A791', '#6FB26C',
    '#C0C15C', '#F9BD24',
    '#F3903F', '#EC6546',
    '#7D4C94', '#5B61AE'
]

def degrees_to_cardinal(degree: float):
    """
    """
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((degree + 11.25)/22.5)
    return dirs[index % 16]


def get_values(df: object, column : str = 'direction'):
    """
    This function calculates what percentage of speed-range was from a given direction.
    For example 20% of all 10-15 m/s wind records was from North.
    """
    percentages = df[column].value_counts(normalize=True)
    result = percentages.multiply(other = 100)
    result = result.to_dict()
    #print(result)
    return result


def sorting(result: dict):
    """
    This function returns a list of the percentage values in the order defined in "dirs" list.
    """
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    lst = []      
    for direction in dirs:
        try:
            value = result[direction]
        except:
            value = 0
        lst.append(value)
    return lst

def export_csv(r_1: list, r_2: list, r_3: list, r_4: list):
    """
    Export extracted values to to CSV
    """
    export = {'r_1':r_1, 'r_2': r_2, 'r_3': r_3, 'r_4': r_4}
    df = pd.DataFrame.from_dict(export)
    df.to_csv('website/data/environment/air-temperature-wind/wind_data.csv',index=False)


def create_graph(r_1: list, r_2: list, r_3: list, r_4: list):
    """
    Create a standalone Graph object.
    Can be used for testing.
    """
    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=r_4,
        name='> 11 m/s',
        marker_color=colors[8]
    ))
    fig.add_trace(go.Barpolar(
        r=r_3,
        name='8-10 m/s',
        marker_color=colors[1]
    ))
    fig.add_trace(go.Barpolar(
        r=r_2,
        name='5-8 m/s',
        marker_color=colors[2]
    ))
    fig.add_trace(go.Barpolar(
        r=r_1,
        name='< 5 m/s',
        marker_color=colors[3]
    ))

    fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
    fig.update_layout(
        title='Wind Speed Distribution in Helsinki',
        font_size=16,
        legend_font_size=16,
        polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=90,

    )
    fig.show()


def main():
    """
    """
    df = pd.read_csv("website/data/environment/air-temperature-wind/raw_air_temp_and_wind.csv")
    df.dropna(inplace=True)

    df['direction'] = df['Wind direction (deg)'].apply(lambda row: degrees_to_cardinal(row))
    df['strength'] = df['Wind speed (m/s)'].astype(float)
    df['strength'] = df['strength'].apply(np.ceil)
    df['frequency'] = df['direction'].map(df['direction'].value_counts())
    
    bins = [-1, 5, 8, 10, 11]
    labels = ["< 5", "5-8", "8-10", "> 11"]
    df['binned_strength'] = pd.cut(df['strength'],  bins=bins, labels=labels)

    df_1 = df[df['binned_strength'] == "< 5"]
    df_2 = df[df['binned_strength'] == "5-8"]
    df_3 = df[df['binned_strength'] == "8-10"]
    df_4 = df[df['binned_strength'] == "> 11"]

    group_1 = get_values(df_1)
    group_2 = get_values(df_2)
    group_3 = get_values(df_3)
    group_4 = get_values(df_4)

    r_1 = sorting(group_1)
    r_2 = sorting(group_2)
    r_3 = sorting(group_3)
    r_4 = sorting(group_4)

    export_csv(r_1, r_2, r_3, r_4)
    create_graph(r_1, r_2, r_3, r_4)


if __name__=='__main__':
    main()

