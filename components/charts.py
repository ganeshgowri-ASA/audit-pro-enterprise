"""
Chart Components
AuditPro Enterprise - Reusable chart visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config.settings import CHART_COLORS


def status_pie_chart(data: dict, title: str = "Status Distribution"):
    """
    Create pie chart for status distribution

    Args:
        data: Dictionary with status as key and count as value
        title: Chart title

    Returns:
        plotly figure
    """
    if not data:
        return None

    labels = list(data.keys())
    values = list(data.values())

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        )
    )])

    fig.update_layout(
        title=title,
        showlegend=True,
        height=400
    )

    return fig


def severity_bar_chart(data: dict, title: str = "NC/OFI by Severity"):
    """
    Create bar chart for severity distribution

    Args:
        data: Dictionary with severity as key and count as value
        title: Chart title

    Returns:
        plotly figure
    """
    if not data:
        return None

    df = pd.DataFrame(list(data.items()), columns=['Severity', 'Count'])

    color_map = {
        'Critical': '#d32f2f',
        'Major': '#f57c00',
        'Minor': '#fbc02d',
        'Observation': '#0288d1'
    }

    fig = px.bar(
        df,
        x='Severity',
        y='Count',
        title=title,
        color='Severity',
        color_discrete_map=color_map
    )

    fig.update_layout(
        showlegend=False,
        height=400
    )

    return fig


def trend_line_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str = "Trend Analysis"):
    """
    Create line chart for trend analysis

    Args:
        data: DataFrame with data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title

    Returns:
        plotly figure
    """
    if data.empty:
        return None

    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        title=title,
        markers=True
    )

    fig.update_layout(
        height=400,
        showlegend=True
    )

    return fig


def kpi_gauge_chart(value: float, max_value: float = 100, title: str = "Performance"):
    """
    Create gauge chart for KPI

    Args:
        value: Current value
        max_value: Maximum value
        title: Chart title

    Returns:
        plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': max_value * 0.8},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': CHART_COLORS['primary']},
            'steps': [
                {'range': [0, max_value * 0.6], 'color': '#ffebee'},
                {'range': [max_value * 0.6, max_value * 0.8], 'color': '#fff3e0'},
                {'range': [max_value * 0.8, max_value], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))

    fig.update_layout(height=300)

    return fig


def stacked_bar_chart(data: pd.DataFrame, x_col: str, y_cols: list, title: str = "Comparison"):
    """
    Create stacked bar chart

    Args:
        data: DataFrame with data
        x_col: Column name for x-axis
        y_cols: List of column names to stack
        title: Chart title

    Returns:
        plotly figure
    """
    if data.empty:
        return None

    fig = go.Figure()

    for col in y_cols:
        fig.add_trace(go.Bar(
            name=col,
            x=data[x_col],
            y=data[col]
        ))

    fig.update_layout(
        barmode='stack',
        title=title,
        height=400
    )

    return fig


def audit_score_chart(scores: dict, title: str = "Audit Scores"):
    """
    Create horizontal bar chart for audit scores

    Args:
        scores: Dictionary with audit name as key and score as value
        title: Chart title

    Returns:
        plotly figure
    """
    if not scores:
        return None

    df = pd.DataFrame(list(scores.items()), columns=['Audit', 'Score'])
    df = df.sort_values('Score', ascending=True)

    # Color based on score
    colors = ['#d32f2f' if s < 70 else '#f57c00' if s < 85 else '#2ca02c' for s in df['Score']]

    fig = go.Figure(go.Bar(
        x=df['Score'],
        y=df['Audit'],
        orientation='h',
        marker=dict(color=colors)
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Score (%)",
        yaxis_title="",
        height=max(300, len(scores) * 40)
    )

    return fig


def timeline_chart(data: pd.DataFrame, start_col: str, end_col: str, name_col: str, title: str = "Timeline"):
    """
    Create Gantt-style timeline chart

    Args:
        data: DataFrame with timeline data
        start_col: Column name for start date
        end_col: Column name for end date
        name_col: Column name for task/item name
        title: Chart title

    Returns:
        plotly figure
    """
    if data.empty:
        return None

    fig = px.timeline(
        data,
        x_start=start_col,
        x_end=end_col,
        y=name_col,
        title=title
    )

    fig.update_layout(height=max(300, len(data) * 40))

    return fig
