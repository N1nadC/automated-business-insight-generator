import plotly.graph_objects as go


def top_products_chart(df, top_n=10):
    """
    Creates a horizontal bar chart for top N products by revenue.

    Parameters
    ----------
    df : pandas.DataFrame
        Columns:
        - product_id (str): Product identifier
        - revenue (numeric): Revenue for the product
    top_n : int, default 10
        Number of top products to display

    Returns
    -------
    plotly.graph_objects.Figure
    """
    df_top = df.nlargest(top_n, 'revenue').sort_values('revenue', ascending=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_top['product_id'],
        x=df_top['revenue'],
        orientation='h',
        marker=dict(
            color='#ff8700',
            line=dict(color='rgba(0,0,0,0.1)', width=1)
        ),
        text=df_top['revenue'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        textfont=dict(size=11, color='#1f1f1f'),
        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text=f'Top {top_n} Products by Revenue',
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
            tickfont=dict(size=11)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=200, r=80, t=80, b=60),
        height=max(400, top_n * 40),
        showlegend=False
    )

    return fig
