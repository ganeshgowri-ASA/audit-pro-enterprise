"""
PV Chamber Configurator - Main Streamlit Application
UV+TC+HF+DH Combined Environmental Chamber Configuration System
"""

import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

# Import modules
from modules.chamber_design import ChamberDesign
from modules.cfd_simulation import CFDSimulation
from modules.uv_optical import UVOpticalSystem
from modules.thermal_management import ThermalManagement
from modules.quote_generator import QuoteGenerator
from modules.supplier_db import SupplierDatabase
from visualizations import ChamberVisualization

# Page configuration
st.set_page_config(
    page_title="PV Chamber Configurator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ff7f0e;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application"""

    # Title
    st.markdown('<h1 class="main-header">🔬 PV Test Equipment Configurator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">UV+TC+HF+DH Combined Environmental Chamber Configuration & Quote Generation System</p>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Module",
        [
            "🏠 Home & Overview",
            "🏗️ Chamber Design",
            "🌬️ CFD Simulation",
            "💡 UV Optical System",
            "🌡️ Thermal Management",
            "💰 Quote Generator",
            "🏭 Supplier Database",
            "📊 3D Visualization",
            "📄 Reports & Export"
        ]
    )

    # Initialize session state
    if 'config' not in st.session_state:
        st.session_state.config = {
            'interior_material': 'SS304',
            'uv_lamp_type': 'UV_LED',
            'target_irradiance': 60,
            'include_robot': True,
            'warranty_months': 24,
            'payment_schedule': '30-40-30'
        }

    # Route to selected page
    if page == "🏠 Home & Overview":
        show_home_page()
    elif page == "🏗️ Chamber Design":
        show_chamber_design_page()
    elif page == "🌬️ CFD Simulation":
        show_cfd_simulation_page()
    elif page == "💡 UV Optical System":
        show_uv_optical_page()
    elif page == "🌡️ Thermal Management":
        show_thermal_management_page()
    elif page == "💰 Quote Generator":
        show_quote_generator_page()
    elif page == "🏭 Supplier Database":
        show_supplier_database_page()
    elif page == "📊 3D Visualization":
        show_visualization_page()
    elif page == "📄 Reports & Export":
        show_reports_page()


def show_home_page():
    """Home page with overview and quick stats"""
    st.markdown('<h2 class="section-header">System Overview</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Chamber Size", "3.2m × 2.1m × 2.2m")
    with col2:
        st.metric("Temperature Range", "-45°C to +105°C")
    with col3:
        st.metric("UV Irradiance", "25-250 W/m²")
    with col4:
        st.metric("PV Module Capacity", "2 modules")

    # System capabilities
    st.markdown('<h2 class="section-header">Key Capabilities</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Environmental Testing:**
        - Temperature: -45°C to +105°C, ±2°C uniformity
        - Humidity: 40-95% RH, ±3% uniformity
        - UV: 280-400nm, ±10% uniformity
        - Ramp rate: 1.6-3.5°C/min

        **IEC Compliance:**
        - IEC 61215 (PV module qualification)
        - IEC 61730 (PV safety qualification)
        - IEC 60068 (Environmental testing)
        - IEC 60904-9 (Solar simulator standards)
        - ISO 17025 (Calibration requirements)
        """)

    with col2:
        st.markdown("""
        **System Features:**
        - Dual PV module testing (3.2m × 2.1m)
        - UV LED/Metal Halide/Fluorescent options
        - Cascade refrigeration system
        - Automated uniformity measurement
        - Real-time monitoring & control
        - NABL-traceable calibration

        **Applications:**
        - UV conditioning tests (UV15, UV60, UV180)
        - Thermal cycling (TC200, TC600)
        - Damp heat testing (DH1000, DH2000)
        - Combined stress testing
        """)

    # Standards compliance
    st.markdown('<h2 class="section-header">Standards Compliance</h2>', unsafe_allow_html=True)

    standards_data = {
        'Standard': ['IEC 61215', 'IEC 61730', 'IEC 60068-3-5', 'IEC 60904-9', 'ISO 17025'],
        'Title': [
            'Terrestrial PV Modules - Design Qualification',
            'PV Module Safety Qualification',
            'Environmental Testing Guidance',
            'Solar Simulator Performance Requirements',
            'Testing and Calibration Laboratories'
        ],
        'Application': [
            'Module qualification testing',
            'Safety and construction tests',
            'Temperature, humidity testing',
            'UV uniformity requirements',
            'Calibration procedures'
        ]
    }

    st.dataframe(pd.DataFrame(standards_data), use_container_width=True)

    # Quick configuration
    st.markdown('<h2 class="section-header">Quick Configuration</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.config['interior_material'] = st.selectbox(
            "Interior Material",
            options=['SS304', 'SS316'],
            index=0 if st.session_state.config['interior_material'] == 'SS304' else 1
        )

    with col2:
        st.session_state.config['uv_lamp_type'] = st.selectbox(
            "UV Lamp Type",
            options=['UV_LED', 'Metal_Halide', 'Fluorescent_UVA'],
            index=['UV_LED', 'Metal_Halide', 'Fluorescent_UVA'].index(st.session_state.config['uv_lamp_type'])
        )

    with col3:
        st.session_state.config['target_irradiance'] = st.number_input(
            "Target UV Irradiance (W/m²)",
            min_value=25,
            max_value=250,
            value=st.session_state.config['target_irradiance']
        )

    # Quick cost estimate
    quote_gen = QuoteGenerator()
    quick_cost = quote_gen.calculate_system_cost(st.session_state.config)

    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown(f"""
    **Estimated System Cost:** ₹{quick_cost['total_lakhs']:.2f} Lakhs (₹{quick_cost['total_inr']:,.0f})

    *Including: Chamber, UV system, Refrigeration, Controls, Installation, Calibration*
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def show_chamber_design_page():
    """Chamber design configuration page"""
    st.markdown('<h2 class="section-header">Chamber Design Specification</h2>', unsafe_allow_html=True)

    chamber = ChamberDesign()

    # Configuration options
    col1, col2 = st.columns(2)

    with col1:
        interior_material = st.selectbox(
            "Interior Material",
            options=['SS304', 'SS316'],
            help="SS316 provides superior corrosion resistance"
        )
        st.session_state.config['interior_material'] = interior_material

    with col2:
        with_legs = st.checkbox("Include Legs/Casters", value=True)

    # Get design summary
    summary = chamber.get_design_summary(interior_material)

    # Display dimensions
    st.markdown("### Chamber Dimensions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Internal Length", f"{summary['dimensions']['internal'][0]} mm")
        st.metric("Internal Width", f"{summary['dimensions']['internal'][1]} mm")
        st.metric("Internal Height", f"{summary['dimensions']['internal'][2]} mm")

    with col2:
        st.metric("External Length", f"{summary['dimensions']['external'][0]} mm")
        st.metric("External Width", f"{summary['dimensions']['external'][1]} mm")
        st.metric("External Height", f"{summary['dimensions']['external'][2]} mm")

    with col3:
        height_result = chamber.calculate_total_height(with_legs)
        st.metric("Total Height", f"{height_result['total_height_m']:.2f} m")
        st.metric("Clearance Available", f"{height_result['clearance_m']:.2f} m")

        if height_result['is_valid']:
            st.success("✅ Height constraint (<3m) satisfied")
        else:
            st.error("❌ Exceeds 3m height limit")

    # Floor loading
    st.markdown("### Floor Loading Analysis")

    loading = summary['loading']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("PV Modules Weight", f"{loading['pv_modules_weight_kg']} kg")
        st.metric("Rack System Weight", f"{loading['rack_weight_kg']} kg")
        st.metric("Structure Weight", f"{loading['structure_weight_kg']} kg")

    with col2:
        st.metric("Total Weight", f"{loading['total_weight_kg']} kg")
        st.metric("Footprint Area", f"{loading['footprint_m2']:.2f} m²")

    with col3:
        st.metric("Floor Loading", f"{loading['floor_loading_kg_per_m2']:.1f} kg/m²")
        st.metric("Safety Margin", f"{loading['safety_margin_percent']:.1f}%")

        if loading['is_valid']:
            st.success("✅ Floor loading (<400 kg/m²) satisfied")
        else:
            st.error("❌ Exceeds 400 kg/m² limit")

    # Materials
    st.markdown("### Material Specifications")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Interior: {summary['materials']['interior']['name']}**
        - Corrosion Resistance: {summary['materials']['interior']['corrosion_resistance']}
        - Thermal Conductivity: {summary['materials']['interior']['thermal_conductivity']} W/(m·K)
        - Description: {summary['materials']['interior']['description']}
        """)

    with col2:
        st.markdown(f"""
        **Insulation: {summary['materials']['insulation']['material']}**
        - Thickness: {summary['materials']['insulation']['thickness_mm']} mm
        - Density: {summary['materials']['insulation']['density']} kg/m³
        - Thermal Conductivity: {summary['materials']['insulation']['thermal_conductivity']} W/(m·K)
        - Description: {summary['materials']['insulation']['description']}
        """)

    # Rack system
    st.markdown("### Extensible Sliding Rack System")

    rack = summary['rack_system']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Configuration:**
        - Rack Levels: {rack['rack_levels']}
        - PV Module Capacity: {rack['capacity']}
        - Rail Material: {rack['rail_material']}
        - Rail Profile: {rack['rail_profile']}
        """)

    with col2:
        st.markdown(f"""
        **Sliding Mechanism:**
        - Slide Travel: {rack['slide_travel_mm']} mm
        - Slide Type: {rack['slide_type']}
        - Load per Slide: {rack['load_per_slide_kg']:.1f} kg
        - Extension: {rack['extension']}
        """)

    # Cost estimate
    st.markdown("### Cost Estimate")

    cost = summary['cost_estimate']
    st.metric("Chamber System Cost", f"₹{cost['total_chamber_cost_lakhs']:.2f} Lakhs",
              help=f"Base cost: ₹{cost['base_cost_inr']:,.0f}, Cost factor: {cost['cost_factor']}")


def show_cfd_simulation_page():
    """CFD simulation page"""
    st.markdown('<h2 class="section-header">CFD Simulation & Airflow Analysis</h2>', unsafe_allow_html=True)

    cfd = CFDSimulation()

    # Get simulation results
    summary = cfd.get_simulation_summary()

    # Heat load analysis
    st.markdown("### Heat Load Analysis")

    heat_load = summary['heat_load_analysis']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("UV Lamp Heat", f"{heat_load['uv_lamp_heat_w']:.0f} W")
    with col2:
        st.metric("Sample Heat", f"{heat_load['sample_heat_w']:.0f} W")
    with col3:
        st.metric("Infiltration", f"{heat_load['ambient_infiltration_w']:.0f} W")
    with col4:
        st.metric("Total Heat Load", f"{heat_load['total_heat_load_kw']:.2f} kW")

    # Heat load breakdown chart
    viz = ChamberVisualization()
    breakdown_chart = viz.create_cost_breakdown_chart(heat_load['breakdown_percent'])
    st.plotly_chart(breakdown_chart, use_container_width=True)

    # Airflow design
    st.markdown("### Airflow Design")

    airflow = summary['airflow_design']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Required Airflow", f"{airflow['airflow_m3_h']:.0f} m³/h")
        st.metric("Air Velocity", f"{airflow['air_velocity_m_s']:.2f} m/s")

    with col2:
        st.metric("Air Changes/Hour", f"{airflow['air_changes_per_hour']:.1f} ACH")
        st.metric("Delta-T", f"{airflow['delta_t_degC']}°C")

    with col3:
        if airflow['is_velocity_acceptable']:
            st.success("✅ Velocity within recommended range")
        else:
            st.warning("⚠️ Velocity outside recommended range")
        st.info(f"Recommended: {airflow['recommended_velocity_range']}")

    # Blower sizing
    st.markdown("### Blower/Fan Sizing")

    blowers = summary['blower_sizing']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        **Airflow Requirements:**
        - Design Airflow: {blowers['design_airflow_m3_h']:.0f} m³/h
        - Design Pressure: {blowers['design_pressure_pa']:.0f} Pa
        - Airflow per Blower: {blowers['airflow_per_blower_m3_h']:.0f} m³/h
        """)

    with col2:
        st.markdown(f"""
        **Blower Specifications:**
        - Number of Blowers: {blowers['number_of_blowers']}
        - Motor Power: {blowers['selected_motor_kw']:.2f} kW ({blowers['selected_motor_hp']:.1f} HP)
        - Efficiency: {blowers['blower_efficiency']*100:.0f}%
        """)

    with col3:
        st.markdown(f"""
        **Configuration:**
        - Type: {blowers['blower_type']}
        - Motor: {blowers['motor_type']}
        - Redundancy: {blowers['redundancy']}
        """)

    # Temperature distribution
    st.markdown("### Temperature Distribution Simulation")

    temp_dist = summary['temperature_distribution']

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Mean Temperature", f"{temp_dist['mean_temperature_degC']:.2f}°C")
        st.metric("Temperature Uniformity", f"±{temp_dist['uniformity_degC']:.2f}°C")

        if temp_dist['is_iec_compliant']:
            st.success(f"✅ IEC compliant (target: ±{temp_dist['target_uniformity_degC']}°C)")
        else:
            st.error(f"❌ Exceeds IEC limit (target: ±{temp_dist['target_uniformity_degC']}°C)")

    with col2:
        # Temperature heatmap
        temp_heatmap = viz.create_temperature_distribution_heatmap(temp_dist['temperature_field'])
        st.plotly_chart(temp_heatmap, use_container_width=True)

    # Airflow visualization
    st.markdown("### Airflow Pattern Visualization")
    airflow_viz = viz.create_airflow_vectors()
    st.plotly_chart(airflow_viz, use_container_width=True)


def show_uv_optical_page():
    """UV optical system page"""
    st.markdown('<h2 class="section-header">UV Optical System Design</h2>', unsafe_allow_html=True)

    uv_system = UVOpticalSystem()

    # Configuration
    col1, col2 = st.columns(2)

    with col1:
        lamp_type = st.selectbox(
            "UV Lamp Type",
            options=['UV_LED', 'Metal_Halide', 'Fluorescent_UVA'],
            format_func=lambda x: uv_system.lamp_types[x].type
        )
        st.session_state.config['uv_lamp_type'] = lamp_type

    with col2:
        target_irradiance = st.slider(
            "Target Irradiance (W/m²)",
            min_value=25,
            max_value=250,
            value=st.session_state.config['target_irradiance']
        )
        st.session_state.config['target_irradiance'] = target_irradiance

    # Get UV system summary
    summary = uv_system.get_uv_system_summary(lamp_type, target_irradiance)

    # Lamp selection
    st.markdown("### Lamp Selection & Configuration")

    lamp_sel = summary['lamp_selection']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Number of Lamps", lamp_sel['number_of_lamps'])
        st.metric("Total Electrical Power", f"{lamp_sel['total_electrical_power_kw']:.2f} kW")

    with col2:
        st.metric("UV Output per Lamp", f"{lamp_sel['uv_output_per_lamp_w']:.1f} W")
        st.metric("Total UV Output", f"{lamp_sel['total_uv_output_w']:.0f} W")

    with col3:
        st.metric("Actual Irradiance", f"{lamp_sel['actual_irradiance_w_m2']:.1f} W/m²")
        st.metric("Irradiance Margin", f"{lamp_sel['irradiance_margin_percent']:.1f}%")

    # Optical design
    st.markdown("### Optical Design & Lamp Positioning")

    optical = summary['optical_design']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Array Configuration:**
        - Configuration: {optical['array_configuration']}
        - Number of Rows: {optical['num_rows']}
        - Number of Columns: {optical['num_cols']}
        - Lamp Spacing (X): {optical['lamp_spacing_x_m']:.2f} m
        - Lamp Spacing (Y): {optical['lamp_spacing_y_m']:.2f} m
        """)

    with col2:
        st.markdown(f"""
        **Lamp-to-Test-Plane Distance:**
        - Optimal Distance: {optical['optimal_distance_mm']:.0f} mm
        - Distance Range: {optical['distance_range_mm'][0]}-{optical['distance_range_mm'][1]} mm
        - Required Beam Angle: {optical['required_beam_angle_deg']:.1f}°
        - Recommended: {optical['recommended_beam_angle']}
        """)

    # Uniformity analysis
    st.markdown("### Uniformity Analysis")

    uniformity = summary['uniformity_analysis']

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Mean Irradiance", f"{uniformity['mean_irradiance_w_m2']:.1f} W/m²")
        st.metric("Non-Uniformity", f"{uniformity['non_uniformity_percent']:.2f}%")
        st.metric("IEC Classification", uniformity['iec_classification'])

        if uniformity['is_iec_compliant']:
            st.success(f"✅ IEC compliant (target: ±{uniformity['target_uniformity_percent']}%)")
        else:
            st.warning(f"⚠️ Exceeds IEC limit (target: ±{uniformity['target_uniformity_percent']}%)")

    with col2:
        # UV uniformity map
        viz = ChamberVisualization()
        uv_map = viz.create_uv_uniformity_map(uniformity['irradiance_map'])
        st.plotly_chart(uv_map, use_container_width=True)

    # Spectral compliance
    st.markdown("### Spectral Compliance")

    spectral = summary['spectral_compliance']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("UVA Content", f"{spectral['uva_percent']:.1f}%")
        st.metric("UVB Content", f"{spectral['uvb_percent']:.1f}%")

    with col2:
        st.metric("Warm-up Time", f"{spectral['warm_up_time_min']} min")
        st.metric("Spectral Stability", spectral['spectral_stability'])

    with col3:
        st.metric("Compliance Status", spectral['compliance_status'])
        if spectral['compliance_status'] == 'PASS':
            st.success("✅ Spectral requirements met")
        else:
            st.error("❌ Spectral requirements not met")

    # Cost analysis
    st.markdown("### UV System Cost Analysis")

    cost = summary['cost_analysis']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Capital Costs:**")
        for item, value in cost['capital_costs'].items():
            if item not in ['total_capital_inr', 'total_capital_lakhs']:
                st.text(f"{item.replace('_', ' ').title()}: ₹{value:,.0f}")
        st.markdown(f"**Total: ₹{cost['capital_costs']['total_capital_lakhs']:.2f} Lakhs**")

    with col2:
        st.markdown("**Annual Operating Costs:**")
        st.text(f"Lamp Replacements: ₹{cost['operating_costs_annual']['lamp_replacements_inr']:,.0f}")
        st.text(f"Energy Cost: ₹{cost['operating_costs_annual']['energy_cost_inr']:,.0f}")
        st.text(f"Energy Consumption: {cost['operating_costs_annual']['energy_consumption_kwh']:,.0f} kWh/year")
        st.markdown(f"**Total Annual: ₹{cost['operating_costs_annual']['total_operating_inr']:,.0f}**")


def show_thermal_management_page():
    """Thermal management page"""
    st.markdown('<h2 class="section-header">Thermal Management System</h2>', unsafe_allow_html=True)

    thermal = ThermalManagement()

    # Configuration
    col1, col2 = st.columns(2)

    with col1:
        chamber_temp = st.slider("Chamber Temperature (°C)", -45, 105, 85)

    with col2:
        ambient_temp = st.slider("Ambient Temperature (°C)", 20, 45, 35)

    # Get thermal summary
    summary = thermal.get_thermal_summary(chamber_temp, ambient_temp)

    # Specifications
    st.markdown("### System Specifications")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Temperature Range", f"{summary['specifications']['temperature_range'][0]}°C to {summary['specifications']['temperature_range'][1]}°C")

    with col2:
        st.metric("Uniformity", summary['specifications']['uniformity'])

    with col3:
        st.metric("Ramp Rate", summary['specifications']['ramp_rate'])

    # Heat load
    st.markdown("### Heat Load Analysis")

    heat_load = summary['heat_load_analysis']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Sample Heat", f"{heat_load['sample_heat_w']:.0f} W")

    with col2:
        st.metric("UV Heat", f"{heat_load['uv_lamp_heat_w']:.0f} W")

    with col3:
        st.metric("Infiltration", f"{heat_load['ambient_infiltration_w']:.0f} W")

    with col4:
        st.metric("Total Heat Load", f"{heat_load['total_heat_load_kw']:.2f} kW")

    # Refrigeration system
    st.markdown("### Refrigeration System")

    refrig = summary['refrigeration_system']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Capacity:**
        - Design Capacity: {refrig['design_capacity_kw']:.2f} kW ({refrig['capacity_tr']:.2f} TR)
        - Safety Factor: {refrig['safety_factor']*100:.0f}%
        - Configuration: {refrig['stage_configuration']}
        """)

    with col2:
        st.markdown(f"""
        **Compressor:**
        - Power: {refrig['compressor_power_kw']:.2f} kW ({refrig['compressor_power_hp']:.1f} HP)
        - Estimated COP: {refrig['estimated_cop']:.1f}
        - Refrigerant: {refrig['refrigerant_recommended']}
        """)

    # Chiller system
    st.markdown("### Process Cooling Water (PCW) Chiller")

    chiller = summary['chiller_system']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Chiller Capacity", f"{chiller['chiller_capacity_tr']:.2f} TR")
        st.metric("PCW Flow Rate", f"{chiller['pcw_flow_m3_h']:.2f} m³/h")

    with col2:
        st.metric("Supply Temperature", f"{chiller['pcw_supply_temp_degC']}°C")
        st.metric("Return Temperature", f"{chiller['pcw_return_temp_degC']}°C")

    with col3:
        st.metric("Delta-T", f"{chiller['pcw_delta_t_degC']}°C")
        st.metric("Pump Power", f"{chiller['pump_power_kw']:.2f} kW")

    # Cost estimate
    st.markdown("### Thermal System Cost")

    cost = summary['cost_estimate']

    st.markdown("**Component Costs:**")

    cost_df = pd.DataFrame([
        {"Component": k.replace('_', ' ').title(), "Cost (INR)": f"₹{v:,.0f}"}
        for k, v in cost['component_costs_inr'].items()
    ])

    st.dataframe(cost_df, use_container_width=True)

    st.metric("Total Thermal System Cost", f"₹{cost['total_lakhs']:.2f} Lakhs")


def show_quote_generator_page():
    """Quote generation page"""
    st.markdown('<h2 class="section-header">Commercial Quote Generator</h2>', unsafe_allow_html=True)

    quote_gen = QuoteGenerator()

    # Customer information
    st.markdown("### Customer Information")

    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name", "ABC Solar Pvt Ltd")
        customer_address = st.text_area("Customer Address", "123 Industrial Area, Bangalore - 560001, Karnataka, India")

    with col2:
        payment_schedule = st.selectbox("Payment Schedule", ['30-40-30', '40-30-30', '50-50'])
        st.session_state.config['payment_schedule'] = payment_schedule

        warranty_months = st.selectbox("Warranty Period", [24, 36, 48, 60], index=0)
        st.session_state.config['warranty_months'] = warranty_months

    # Configuration
    st.markdown("### System Configuration")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.config['interior_material'] = st.selectbox("Interior Material", ['SS304', 'SS316'])

    with col2:
        st.session_state.config['uv_lamp_type'] = st.selectbox(
            "UV Lamp Type",
            ['UV_LED', 'Metal_Halide', 'Fluorescent_UVA']
        )

    with col3:
        st.session_state.config['include_robot'] = st.checkbox("Include Uniformity Robot", value=True)

    # Generate quote
    if st.button("Generate Quote", type="primary"):
        quote = quote_gen.generate_complete_quote(
            customer_name=customer_name,
            customer_address=customer_address,
            options=st.session_state.config,
            payment_schedule=payment_schedule,
            warranty_months=warranty_months
        )

        st.session_state.quote = quote

        # Display quote
        st.success("✅ Quote generated successfully!")

        st.markdown("### Quote Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            **Quote Number:** {quote['quote_header']['quote_number']}

            **Quote Date:** {quote['quote_header']['quote_date']}

            **Valid Until:** {quote['quote_header']['valid_until']}

            **Customer:** {quote['quote_header']['customer_name']}
            """)

        with col2:
            st.markdown(f"""
            **System:** {quote['system_description']['title']}

            **Model:** {quote['system_description']['model']}

            **Capacity:** {quote['system_description']['capacity']}
            """)

        # Cost breakdown
        st.markdown("### Cost Breakdown")

        cost_df = quote_gen.export_quote_to_dict(quote)
        st.dataframe(cost_df, use_container_width=True)

        # Payment terms
        st.markdown("### Payment Terms")

        payment_df = pd.DataFrame(quote['payment_terms']['payment_milestones'])
        st.dataframe(payment_df, use_container_width=True)

        # Delivery timeline
        st.markdown("### Delivery Timeline")

        st.metric("Total Duration", f"{quote['delivery_timeline']['total_duration_weeks']} weeks ({quote['delivery_timeline']['total_duration_months']} months)")

        timeline_df = pd.DataFrame(quote['delivery_timeline']['milestones'])
        st.dataframe(timeline_df, use_container_width=True)

        # Visualize timeline
        viz = ChamberVisualization()
        timeline_chart = viz.create_timeline_gantt(quote['delivery_timeline']['milestones'])
        st.plotly_chart(timeline_chart, use_container_width=True)


def show_supplier_database_page():
    """Supplier database page"""
    st.markdown('<h2 class="section-header">Supplier Database - India</h2>', unsafe_allow_html=True)

    supplier_db = SupplierDatabase()

    # Category selection
    category = st.selectbox(
        "Select Component Category",
        ['All'] + supplier_db.get_all_categories()
    )

    if category == 'All':
        # Show all suppliers
        st.markdown("### All Suppliers")
        df = supplier_db.export_to_dataframe()
        st.dataframe(df, use_container_width=True)

        # Summary
        st.markdown("### Database Summary")
        summary = supplier_db.get_database_summary()
        summary_df = pd.DataFrame([
            {
                'Category': cat,
                'Total Suppliers': data['total_suppliers'],
                'Tier 1 Count': data['tier1_count'],
                'Avg Lead Time (weeks)': f"{data['avg_lead_time_weeks']:.1f}"
            }
            for cat, data in summary.items()
        ])
        st.dataframe(summary_df, use_container_width=True)

    else:
        # Show category-specific suppliers
        suppliers = supplier_db.get_suppliers_by_category(category)

        for supplier in suppliers:
            with st.expander(f"**{supplier['company']}** - {supplier.get('rating', 'N/A')}"):
                col1, col2 = st.columns(2)

                with col1:
                    for key, value in supplier.items():
                        if key not in ['company', 'rating']:
                            st.text(f"{key.replace('_', ' ').title()}: {value}")

                with col2:
                    st.text(f"Rating: {supplier.get('rating', 'N/A')}")
                    st.text(f"Lead Time: {supplier.get('lead_time_weeks', 'N/A')} weeks")

    # Competitor comparison
    st.markdown("### International Competitor Comparison")

    competitors = supplier_db.get_competitor_comparison()

    comp_df = pd.DataFrame(competitors['competitors'])
    st.dataframe(comp_df, use_container_width=True)

    st.markdown("### Local Supplier Advantages")

    for key, value in competitors['local_advantage'].items():
        st.text(f"• {key.title()}: {value}")


def show_visualization_page():
    """3D visualization page"""
    st.markdown('<h2 class="section-header">3D Visualization</h2>', unsafe_allow_html=True)

    viz = ChamberVisualization()

    # Chamber 3D view
    st.markdown("### 3D Chamber View")

    show_internals = st.checkbox("Show Internal Components", value=True)

    chamber_3d = viz.create_chamber_3d(show_internals=show_internals)
    st.plotly_chart(chamber_3d, use_container_width=True)

    # Additional visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Temperature Distribution")
        temp_map = viz.create_temperature_distribution_heatmap()
        st.plotly_chart(temp_map, use_container_width=True)

    with col2:
        st.markdown("### UV Uniformity Map")
        uv_map = viz.create_uv_uniformity_map()
        st.plotly_chart(uv_map, use_container_width=True)

    # Airflow visualization
    st.markdown("### Airflow Pattern")
    airflow_viz = viz.create_airflow_vectors()
    st.plotly_chart(airflow_viz, use_container_width=True)


def show_reports_page():
    """Reports and export page"""
    st.markdown('<h2 class="section-header">Reports & Export</h2>', unsafe_allow_html=True)

    st.markdown("""
    ### Available Export Options

    - **PDF Report**: Comprehensive technical specification document
    - **Excel Quote**: Detailed cost breakdown and quote
    - **Technical Datasheet**: Equipment specifications
    - **Installation Manual**: Site preparation and installation guide
    """)

    if 'quote' in st.session_state:
        quote = st.session_state.quote

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Download PDF Report"):
                st.info("PDF generation feature - to be implemented with reportlab")

        with col2:
            if st.button("Download Excel Quote"):
                quote_gen = QuoteGenerator()
                df = quote_gen.export_quote_to_dict(quote)

                # Convert to CSV for download
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Quote CSV",
                    data=csv,
                    file_name=f"pv_chamber_quote_{quote['quote_header']['quote_number']}.csv",
                    mime="text/csv"
                )

    else:
        st.warning("⚠️ Please generate a quote first in the Quote Generator module")

    # System specification summary
    st.markdown("### System Specification Summary")

    # Initialize all systems
    chamber = ChamberDesign()
    cfd = CFDSimulation()
    uv = UVOpticalSystem()
    thermal = ThermalManagement()

    spec_data = {
        'Parameter': [
            'Chamber Size (L×W×H)',
            'Temperature Range',
            'Humidity Range',
            'UV Irradiance',
            'PV Module Capacity',
            'Floor Loading',
            'Total System Cost'
        ],
        'Specification': [
            '3200mm × 2100mm × 2200mm',
            '-45°C to +105°C (±2°C uniformity)',
            '40-95% RH (±3% uniformity)',
            '25-250 W/m² (±10% uniformity)',
            '2 modules (3.2m × 2.1m)',
            '<400 kg/m²',
            f"₹{QuoteGenerator().calculate_system_cost()['total_lakhs']:.2f} Lakhs"
        ]
    }

    st.dataframe(pd.DataFrame(spec_data), use_container_width=True)


if __name__ == "__main__":
    main()
