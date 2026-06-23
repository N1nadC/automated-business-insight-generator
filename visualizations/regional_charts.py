import plotly.graph_objects as go


def state_revenue_chart(df):
    """
    Creates a vertical bar chart for revenue by state.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
        - customer_state (str): Brazilian state abbreviation (e.g., 'SP', 'RJ')
        - revenue (numeric): Total revenue for the state

    Returns
    -------
    plotly.graph_objects.Figure
    """
    df_sorted = df.sort_values('revenue', ascending=False)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_sorted['customer_state'],
        y=df_sorted['revenue'],
        marker=dict(
            color='#29b09d',
            line=dict(color='rgba(0,0,0,0.1)', width=1)
        ),
        text=df_sorted['revenue'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        textfont=dict(size=11, color='#1f1f1f'),
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='Revenue by State',
            font=dict(size=20, color='#1f1f1f'),
            x=0.5
        ),
        xaxis=dict(
            title='State',
            showgrid=False,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title='Revenue ($)',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickprefix='$',
            tickformat=',.0f'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=30, t=80, b=80),
        height=450,
        showlegend=False
    )

    return fig
