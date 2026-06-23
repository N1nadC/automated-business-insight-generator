import plotly.graph_objects as go


def delivery_gauge(avg_days, target=10, min_val=0, max_val=30):
    """
    Creates a gauge chart for delivery KPI visualization with
    color-coded performance zones.

    Parameters
    ----------
    avg_days : float or pandas.DataFrame
        Average delivery days value. If a DataFrame is passed,
        the first value will be extracted automatically.
    target : float, default 10
        Target delivery days (threshold line)
    min_val : float, default 0
        Minimum value for gauge scale
    max_val : float, default 30
        Maximum value for gauge scale

    Returns
    -------
    plotly.graph_objects.Figure
    """
    # Handle DataFrame input (extract scalar value)
    if hasattr(avg_days, 'iloc'):
        avg_days = float(avg_days.iloc[0, 0])
    else:
        avg_days = float(avg_days)

    if avg_days <= target:
        bar_color = '#29b09d'  # Green - good
    elif avg_days <= target * 1.5:
        bar_color = '#ff8700'  # Orange - warning
    else:
        bar_color = '#ff2b2b'  # Red - critical

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode='gauge+number+delta',
        value=avg_days,
        number=dict(
            suffix=' days',
            font=dict(size=36, color='#1f1f1f')
        ),
        delta=dict(
            reference=target,
            relative=False,
            valueformat='.1f',
            suffix=' vs target',
            font=dict(size=14)
        ),
        gauge=dict(
            axis=dict(
                range=[min_val, max_val],
                tickwidth=1,
                tickcolor='#1f1f1f'
            ),
            bar=dict(color=bar_color, thickness=0.75),
            bgcolor='white',
            borderwidth=2,
            bordercolor='#1f1f1f',
            steps=[
                dict(range=[min_val, target], color='#e8f5e9'),
                dict(range=[target, target * 1.5], color='#fff3e0'),
                dict(range=[target * 1.5, max_val], color='#ffebee')
            ],
            threshold=dict(
                line=dict(color='#ff2b2b', width=4),
                thickness=0.8,
                value=target
            )
        ),
        title=dict(
            text='Average Delivery Time',
            font=dict(size=18, color='#1f1f1f')
        )
    ))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=30, r=30, t=80, b=30),
        height=400
    )

    return fig
