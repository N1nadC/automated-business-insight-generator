import plotly.graph_objects as go
import numpy as np


def monthly_revenue_chart(df):
    """
    Creates a production-quality line chart for monthly revenue trend
    with trend line overlay.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
        - month (datetime): Month period
        - revenue (numeric): Total revenue for the month

    Returns
    -------
    plotly.graph_objects.Figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['revenue'],
        mode='lines+markers',
        name='Monthly Revenue',
        line=dict(color='#0068c9', width=3),
        marker=dict(size=8, color='#0068c9', line=dict(width=2, color='white')),
        hovertemplate='<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
    ))

    # Add linear trend line
    if len(df) > 2:
        z = np.polyfit(range(len(df)), df['revenue'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=df['month'],
            y=p(range(len(df))),
            mode='lines',
            name='Trend',
            line=dict(color='#ff2b2b', width=2, dash='dash'),
            hovertemplate='Trend: $%{y:,.2f}<extra></extra>'
        ))

    fig.update_layout(
        title=dict(
            text='Monthly Revenue Trend',
            font=dict(size=20, color='#1f1f1f'),
            x=0.5
        ),
        xaxis=dict(
            title='Month',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickformat='%b %Y'
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
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=60, r=30, t=80, b=60),
        height=450
    )

    return fig
