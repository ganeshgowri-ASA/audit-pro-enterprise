"""
3D Chamber Visualization using Plotly
Creates isometric, elevation, top, and back views of the chamber
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Tuple


class ChamberVisualization:
    """
    3D Visualization for PV Environmental Chamber
    """

    def __init__(self, length_m: float = 3.2, width_m: float = 2.1, height_m: float = 2.2):
        self.length = length_m
        self.width = width_m
        self.height = height_m

    def create_chamber_3d(self, show_internals: bool = True) -> go.Figure:
        """
        Create 3D isometric view of chamber
        """
        # Chamber outline (wireframe)
        x = [0, self.length, self.length, 0, 0, 0, self.length, self.length, 0, 0, self.length, self.length, self.length, self.length, 0, 0]
        y = [0, 0, self.width, self.width, 0, 0, 0, self.width, self.width, 0, 0, 0, self.width, self.width, self.width, 0]
        z = [0, 0, 0, 0, 0, self.height, self.height, self.height, self.height, self.height, self.height, 0, 0, self.height, self.height, self.height]

        fig = go.Figure()

        # Chamber structure
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='darkblue', width=4),
            name='Chamber Structure',
            showlegend=True
        ))

        if show_internals:
            # PV modules (2 modules)
            module_thickness = 0.05
            module_z1 = 0.5  # First module height
            module_z2 = 1.2  # Second module height

            for i, module_z in enumerate([module_z1, module_z2]):
                # Module representation (rectangle)
                mx = [0.1, self.length-0.1, self.length-0.1, 0.1, 0.1]
                my = [0.1, 0.1, self.width-0.1, self.width-0.1, 0.1]
                mz = [module_z] * 5

                fig.add_trace(go.Scatter3d(
                    x=mx, y=my, z=mz,
                    mode='lines',
                    line=dict(color='orange', width=3),
                    name=f'PV Module {i+1}',
                    showlegend=True
                ))

                # Fill module surface
                fig.add_trace(go.Mesh3d(
                    x=[0.1, self.length-0.1, self.length-0.1, 0.1],
                    y=[0.1, 0.1, self.width-0.1, self.width-0.1],
                    z=[module_z, module_z, module_z, module_z],
                    i=[0, 0],
                    j=[1, 2],
                    k=[2, 3],
                    color='lightblue',
                    opacity=0.5,
                    name=f'PV Surface {i+1}',
                    showlegend=False
                ))

            # UV lamp array (top)
            lamp_z = self.height - 0.6  # 600mm from top
            num_lamps_x = 4
            num_lamps_y = 3

            for i in range(num_lamps_x):
                for j in range(num_lamps_y):
                    lx = (i + 0.5) * (self.length / num_lamps_x)
                    ly = (j + 0.5) * (self.width / num_lamps_y)

                    # Lamp representation (small cube)
                    lamp_size = 0.1
                    fig.add_trace(go.Scatter3d(
                        x=[lx],
                        y=[ly],
                        z=[lamp_z],
                        mode='markers',
                        marker=dict(size=8, color='yellow', symbol='square'),
                        name='UV Lamp' if i == 0 and j == 0 else None,
                        showlegend=(i == 0 and j == 0),
                        hovertext=f'UV Lamp ({i+1},{j+1})'
                    ))

            # Evaporator coil (side wall)
            evap_x = [0.05] * 5
            evap_y = [0.2, 0.2, self.width-0.2, self.width-0.2, 0.2]
            evap_z = [0.3, self.height-0.3, self.height-0.3, 0.3, 0.3]

            fig.add_trace(go.Scatter3d(
                x=evap_x, y=evap_y, z=evap_z,
                mode='lines',
                line=dict(color='cyan', width=3),
                name='Evaporator Coil',
                showlegend=True
            ))

        # Layout settings
        fig.update_layout(
            title='PV Environmental Chamber - 3D Isometric View',
            scene=dict(
                xaxis_title='Length (m)',
                yaxis_title='Width (m)',
                zaxis_title='Height (m)',
                xaxis=dict(range=[0, self.length]),
                yaxis=dict(range=[0, self.width]),
                zaxis=dict(range=[0, self.height]),
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.2)
                )
            ),
            width=800,
            height=600,
            showlegend=True
        )

        return fig

    def create_temperature_distribution_heatmap(self, temp_data: np.ndarray = None) -> go.Figure:
        """
        Create temperature distribution heatmap
        """
        if temp_data is None:
            # Generate sample data (3x3x3 grid)
            np.random.seed(42)
            temp_data = 85 + np.random.randn(3, 3, 3) * 1.2

        # Take middle z-slice for visualization
        middle_slice = temp_data[:, :, 1]

        # Create grid
        x = np.linspace(0, self.length, 3)
        y = np.linspace(0, self.width, 3)

        fig = go.Figure(data=go.Heatmap(
            z=middle_slice,
            x=x,
            y=y,
            colorscale='RdBu_r',
            colorbar=dict(title='Temperature (°C)'),
            hoverongaps=False
        ))

        fig.update_layout(
            title='Temperature Distribution (Mid-Height Plane)',
            xaxis_title='Length (m)',
            yaxis_title='Width (m)',
            width=600,
            height=500
        )

        return fig

    def create_uv_uniformity_map(self, irradiance_map: np.ndarray = None) -> go.Figure:
        """
        Create UV irradiance uniformity map
        """
        if irradiance_map is None:
            # Generate sample data (5x6 grid)
            np.random.seed(43)
            base = 60  # W/m²
            irradiance_map = base + np.random.randn(5, 6) * 3

        # Create grid
        x = np.linspace(0.1 * self.length, 0.9 * self.length, 6)
        y = np.linspace(0.1 * self.width, 0.9 * self.width, 5)

        fig = go.Figure(data=go.Heatmap(
            z=irradiance_map,
            x=x,
            y=y,
            colorscale='Viridis',
            colorbar=dict(title='Irradiance (W/m²)'),
            hoverongaps=False
        ))

        # Add measurement points
        xx, yy = np.meshgrid(x, y)
        fig.add_trace(go.Scatter(
            x=xx.flatten(),
            y=yy.flatten(),
            mode='markers',
            marker=dict(size=8, color='red', symbol='x'),
            name='Measurement Points',
            showlegend=True
        ))

        fig.update_layout(
            title='UV Irradiance Uniformity Map (Test Plane)',
            xaxis_title='Length (m)',
            yaxis_title='Width (m)',
            width=700,
            height=500
        )

        return fig

    def create_airflow_vectors(self) -> go.Figure:
        """
        Create airflow visualization with vector field
        """
        # Create grid
        x = np.linspace(0.2, self.length - 0.2, 8)
        y = np.linspace(0.2, self.width - 0.2, 6)
        z = np.linspace(0.3, self.height - 0.3, 5)

        # Generate sample airflow vectors (circular pattern)
        np.random.seed(44)

        fig = go.Figure()

        # Sample airflow (simplified circular convection)
        for zi in [0.5, 1.1, 1.7]:  # Three height levels
            vectors = []
            for xi in x[::2]:
                for yi in y[::2]:
                    # Circular flow pattern
                    cx, cy = self.length / 2, self.width / 2
                    dx = -(yi - cy) * 0.3
                    dy = (xi - cx) * 0.3
                    dz = 0.1

                    # Add vector
                    fig.add_trace(go.Cone(
                        x=[xi],
                        y=[yi],
                        z=[zi],
                        u=[dx],
                        v=[dy],
                        w=[dz],
                        colorscale='Blues',
                        sizemode='absolute',
                        sizeref=0.3,
                        showscale=False,
                        name=f'Airflow z={zi:.1f}m' if xi == x[0] and yi == y[0] else None,
                        showlegend=(xi == x[0] and yi == y[0])
                    ))

        # Add chamber outline
        x_outline = [0, self.length, self.length, 0, 0, 0, self.length, self.length, 0, 0, self.length, self.length, self.length, self.length, 0, 0]
        y_outline = [0, 0, self.width, self.width, 0, 0, 0, self.width, self.width, 0, 0, 0, self.width, self.width, self.width, 0]
        z_outline = [0, 0, 0, 0, 0, self.height, self.height, self.height, self.height, self.height, self.height, 0, 0, self.height, self.height, self.height]

        fig.add_trace(go.Scatter3d(
            x=x_outline,
            y=y_outline,
            z=z_outline,
            mode='lines',
            line=dict(color='gray', width=2),
            name='Chamber',
            showlegend=True
        ))

        fig.update_layout(
            title='Airflow Pattern (CFD Simulation)',
            scene=dict(
                xaxis_title='Length (m)',
                yaxis_title='Width (m)',
                zaxis_title='Height (m)',
                aspectmode='data',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            width=800,
            height=600
        )

        return fig

    def create_cost_breakdown_chart(self, costs: Dict) -> go.Figure:
        """
        Create cost breakdown pie chart
        """
        labels = [k.replace('_', ' ').title() for k in costs.keys()]
        values = list(costs.values())

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            marker=dict(colors=px.colors.qualitative.Set3)
        )])

        fig.update_layout(
            title='System Cost Breakdown (INR Lakhs)',
            width=700,
            height=500
        )

        return fig

    def create_timeline_gantt(self, milestones: List[Dict]) -> go.Figure:
        """
        Create project timeline Gantt chart
        """
        tasks = []

        for milestone in milestones:
            tasks.append(dict(
                Task=milestone['phase'],
                Start=milestone['start_date'],
                Finish=milestone['end_date'],
                Description=milestone.get('description', '')
            ))

        fig = px.timeline(
            tasks,
            x_start='Start',
            x_end='Finish',
            y='Task',
            title='Project Delivery Timeline',
            labels={'Task': 'Phase'},
            hover_data=['Description']
        )

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Project Phase',
            width=900,
            height=600,
            showlegend=False
        )

        fig.update_yaxes(categoryorder='total ascending')

        return fig

    def create_performance_comparison(self, config_options: List[Dict]) -> go.Figure:
        """
        Create configuration comparison bar chart
        """
        configs = [opt['name'] for opt in config_options]
        metrics = ['Cost', 'Performance', 'Efficiency', 'Reliability']

        fig = go.Figure()

        for i, metric in enumerate(metrics):
            values = [opt['scores'][metric] for opt in config_options]

            fig.add_trace(go.Bar(
                name=metric,
                x=configs,
                y=values,
                text=values,
                textposition='auto'
            ))

        fig.update_layout(
            title='Configuration Comparison',
            xaxis_title='Configuration',
            yaxis_title='Score (0-100)',
            barmode='group',
            width=800,
            height=500
        )

        return fig
