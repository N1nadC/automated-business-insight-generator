import plotly.graph_objects as go


def customer_distribution_chart(df, metric='customers'):
    """
    Creates a donut chart for customer distribution by region.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
        - region (str): Region/state abbreviation
        - customers (int): Number of customers in the region
    metric : str, default 'customers'
        Label for the metric being displayed

    Returns
    -------
    plotly.graph_objects.Figure
    """
    colors = ['#0068c9', '#83c9ff', '#ff2b2b', '#ffabab', '#29b09d',
              '#7defa1', '#ff8700', '#ffd16a', '#6d3fc0', '#d5dae5']

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=df['region'],
        values=df['customers'],
        hole=0.4,
        marker=dict(
            colors=colors[:len(df)],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} (' + metric + ')<br>%{percent}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='Customer Distribution',
            font=dict(size=20, color='#1f1f1f'),
            x=0.5
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=30, r=30, t=80, b=30),
        height=450,
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5
        ),
        annotations=[dict(
            text=metric.title(),
            x=0.5, y=0.5,
            font_size=14,
            showarrow=False
        )]
    )

    return fig
