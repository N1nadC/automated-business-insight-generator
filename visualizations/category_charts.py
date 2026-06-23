import plotly.graph_objects as go


def category_performance_chart(df):
    """
    Creates a horizontal bar chart for category performance.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
        - product_category_name_english (str): Product category name
        - revenue (numeric): Revenue for the category

    Returns
    -------
    plotly.graph_objects.Figure
    """
    df_sorted = df.sort_values('revenue', ascending=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_sorted['product_category_name_english'],
        x=df_sorted['revenue'],
        orientation='h',
        marker=dict(
            color=df_sorted['revenue'],
            colorscale='Blues',
            line=dict(color='rgba(0,0,0,0.1)', width=1)
        ),
        text=df_sorted['revenue'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        textfont=dict(size=11, color='#1f1f1f'),
        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='Category Performance',
            font=dict(size=20, color='#1f1f1f'),
            x=0.5
        ),
        xaxis=dict(
            title='Revenue ($)',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickprefix='$',
            tickformat=',.0f'
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            tickfont=dict(size=12)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=200, r=80, t=80, b=60),
        height=max(400, len(df) * 35),
        showlegend=False
    )

    return fig
