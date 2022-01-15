import pandas as pd
import plotly.graph_objects as go

# Colors used by graphs
colors = [
    '#4182C8', '#2E94B2',
    '#39A791', '#6FB26C',
    '#C0C15C', '#F9BD24',
    '#F3903F', '#EC6546',
    '#7D4C94', '#5B61AE'
]


def cleaner():
    """
    """
    df = pd.read_csv("website/data/environment/air-quality/air_quality_2020.csv")

    df = df.rename(columns={'Year': 'year', 'm': 'month', 'd': 'day'})
    df = df[df['year'] == 2020]
    df['Date'] = pd.to_datetime(df[['year', 'month', 'day']])

    df.drop(['year', 'month', 'day'], axis=1, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    x = df.groupby(df.Date.dt.date).mean().reset_index()
    print(x.describe())
    x.to_csv('website/data/environment/air-quality/air_quality_2020_clean.csv', index=False)
    return x


def create_temp_graph(df):
    """
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Nitrogen dioxide (ug/m3)'],
        mode='lines',
        line_shape='spline',
        name='Nitrogen dioxide (ug/m3)'
        )
    )

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Nitrogen monoxide (ug/m3)'],
        mode='lines',
        line_shape='spline',
        name='Nitrogen monoxide (ug/m3)'
        )
    )

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Particulate matter < 10 µm (ug/m3)'],
        mode='lines',
        line_shape='spline',
        name='Particulate matter < 10 µm (ug/m3)'
        )
    )
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Particulate matter < 2.5 µm (ug/m3)'],
        mode='lines',
        line_shape='spline',
        name='Particulate matter < 2.5 µm (ug/m3)'
        )
    )

    fig.update_layout(
        font=dict(size=14, color="#fff"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
        ),
        legend_font_size=12,
        paper_bgcolor='#1E1E1E', 
        plot_bgcolor='#1E1E1E', 
        margin={"r": 30, "t": 30, "l": 30, "b": 30},
        autosize=True
    )
    fig.show()


def main():
    """
    """
    df = cleaner()
    create_temp_graph(df)


main()
