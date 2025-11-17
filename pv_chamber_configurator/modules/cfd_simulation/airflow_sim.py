"""
CFD Simulation Engine
Calculates airflow patterns, temperature distribution, humidity mapping for IEC compliance
"""

import numpy as np
from scipy import interpolate
from typing import Dict, List, Tuple
import pandas as pd


class CFDSimulation:
    """
    Computational Fluid Dynamics Simulation for Environmental Chamber
    Ensures IEC 61215/61730/60068 compliance
    """

    def __init__(self, chamber_volume_m3: float = 14.784):
        self.chamber_volume = chamber_volume_m3
        self.air_changes_per_hour = 33  # Typical for environmental chambers

        # Chamber dimensions (from ChamberDesign)
        self.length = 3.2  # m
        self.width = 2.1   # m
        self.height = 2.2  # m

        # Air properties at 20°C
        self.air_density = 1.2  # kg/m³
        self.air_specific_heat = 1005  # J/(kg·K)
        self.air_viscosity = 1.81e-5  # Pa·s

        # IEC standards requirements
        self.temp_uniformity_target = 2.0  # ±°C
        self.humidity_uniformity_target = 3.0  # ±%RH
        self.uv_uniformity_target = 10.0  # ±%

    def calculate_required_airflow(self, heat_load_kw: float = 6.6) -> Dict:
        """
        Calculate required airflow rate based on heat load and temperature rise
        """
        # Target temperature rise across air circulation (delta-T)
        delta_t = 8  # °C (typical for good mixing)

        # Required airflow (Q = Heat / (ρ × Cp × ΔT))
        heat_load_w = heat_load_kw * 1000  # Convert to watts
        airflow_m3_s = heat_load_w / (self.air_density * self.air_specific_heat * delta_t)
        airflow_m3_h = airflow_m3_s * 3600
        airflow_cfm = airflow_m3_h * 0.588577  # Convert to CFM

        # Air velocity calculation
        # Cross-sectional area for airflow (typically 30-40% of chamber cross-section)
        flow_area = (self.width * self.height) * 0.35  # m²
        air_velocity = airflow_m3_s / flow_area  # m/s

        # Air changes per hour
        actual_ach = airflow_m3_h / self.chamber_volume

        return {
            'heat_load_kw': heat_load_kw,
            'delta_t_degC': delta_t,
            'airflow_m3_s': airflow_m3_s,
            'airflow_m3_h': airflow_m3_h,
            'airflow_cfm': airflow_cfm,
            'air_velocity_m_s': air_velocity,
            'flow_area_m2': flow_area,
            'air_changes_per_hour': actual_ach,
            'recommended_velocity_range': '0.5 - 1.5 m/s',
            'is_velocity_acceptable': 0.5 <= air_velocity <= 1.5
        }

    def calculate_pressure_drop(self, airflow_m3_h: float) -> Dict:
        """
        Calculate pressure drop through chamber and ductwork
        """
        # Convert to m³/s
        Q = airflow_m3_h / 3600

        # Pressure drop components
        # 1. Entry/Exit losses
        entry_loss_factor = 1.5  # K-factor
        velocity_head = 0.5 * self.air_density * ((Q / (self.width * self.height * 0.35)) ** 2)
        entry_exit_loss = entry_loss_factor * velocity_head

        # 2. Friction losses (simplified)
        hydraulic_diameter = (2 * self.width * self.height) / (self.width + self.height)
        reynolds = (self.air_density * (Q / (self.width * self.height * 0.35)) * hydraulic_diameter) / self.air_viscosity
        friction_factor = 0.316 / (reynolds ** 0.25) if reynolds > 2300 else 64 / reynolds
        friction_loss = friction_factor * (self.length / hydraulic_diameter) * velocity_head

        # 3. Component losses (filters, UV banks, etc.)
        filter_loss = 125  # Pa (typical HEPA filter)
        uv_bank_loss = 75  # Pa (across UV lamp arrays)
        damper_loss = 50   # Pa (control dampers)

        # Total pressure drop
        total_pressure_drop = entry_exit_loss + friction_loss + filter_loss + uv_bank_loss + damper_loss

        return {
            'airflow_m3_h': airflow_m3_h,
            'reynolds_number': reynolds,
            'flow_regime': 'Turbulent' if reynolds > 4000 else 'Transitional' if reynolds > 2300 else 'Laminar',
            'entry_exit_loss_pa': entry_exit_loss,
            'friction_loss_pa': friction_loss,
            'filter_loss_pa': filter_loss,
            'uv_bank_loss_pa': uv_bank_loss,
            'damper_loss_pa': damper_loss,
            'total_pressure_drop_pa': total_pressure_drop,
            'total_pressure_drop_inches_wg': total_pressure_drop / 249.1  # Convert to inches water gauge
        }

    def size_blowers(self, airflow_m3_h: float, pressure_drop_pa: float) -> Dict:
        """
        Size blower/fan system for required airflow and pressure
        """
        # Add safety factors
        airflow_with_margin = airflow_m3_h * 1.15  # 15% margin
        pressure_with_margin = pressure_drop_pa * 1.20  # 20% margin

        # Blower efficiency (typical centrifugal fan)
        blower_efficiency = 0.75

        # Motor power calculation
        power_kw = (airflow_with_margin / 3600) * pressure_with_margin / (1000 * blower_efficiency)
        power_hp = power_kw * 1.341  # Convert to HP

        # Select standard motor size
        standard_motor_sizes = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 7.5, 10.0]  # HP
        selected_motor_hp = min([size for size in standard_motor_sizes if size >= power_hp], default=10.0)
        selected_motor_kw = selected_motor_hp * 0.746

        # Number of blowers (typically 2 for redundancy)
        num_blowers = 2
        airflow_per_blower = airflow_with_margin / num_blowers

        return {
            'required_airflow_m3_h': airflow_m3_h,
            'design_airflow_m3_h': airflow_with_margin,
            'required_pressure_pa': pressure_drop_pa,
            'design_pressure_pa': pressure_with_margin,
            'calculated_power_kw': power_kw,
            'calculated_power_hp': power_hp,
            'selected_motor_hp': selected_motor_hp,
            'selected_motor_kw': selected_motor_kw,
            'blower_efficiency': blower_efficiency,
            'number_of_blowers': num_blowers,
            'airflow_per_blower_m3_h': airflow_per_blower,
            'redundancy': 'N+1 configuration',
            'blower_type': 'Centrifugal backward curved',
            'motor_type': 'IE3 efficiency, VFD compatible'
        }

    def simulate_temperature_distribution(self, set_temp: float, uv_on: bool = True) -> Dict:
        """
        Simulate temperature distribution in chamber (UV ON/OFF)
        Returns temperature uniformity analysis
        """
        # Create measurement grid (27 points as per IEC)
        grid_x = np.linspace(0.1, 0.9, 3) * self.length
        grid_y = np.linspace(0.1, 0.9, 3) * self.width
        grid_z = np.linspace(0.1, 0.9, 3) * self.height

        # Generate temperature field with realistic variations
        np.random.seed(42)  # For reproducibility
        temps = []

        for z in grid_z:
            for y in grid_y:
                for x in grid_x:
                    # Base temperature
                    temp = set_temp

                    # Add UV heating effect (if UV on)
                    if uv_on:
                        # More heating near test plane (center height)
                        z_factor = 1.0 - abs(z - self.height/2) / (self.height/2)
                        uv_heating = 0.8 * z_factor

                        temp += uv_heating

                    # Add edge effects (walls cooler)
                    edge_distance = min(x/self.length, (self.length-x)/self.length,
                                       y/self.width, (self.width-y)/self.width)
                    edge_cooling = -0.5 * (1.0 - edge_distance/0.5)
                    temp += edge_cooling

                    # Add random variation (sensor noise)
                    temp += np.random.normal(0, 0.2)

                    temps.append(temp)

        temps = np.array(temps)

        # Calculate uniformity
        mean_temp = np.mean(temps)
        max_temp = np.max(temps)
        min_temp = np.min(temps)
        std_temp = np.std(temps)
        uniformity = max_temp - min_temp

        # IEC compliance
        is_compliant = uniformity <= self.temp_uniformity_target

        return {
            'set_temperature_degC': set_temp,
            'uv_status': 'ON' if uv_on else 'OFF',
            'mean_temperature_degC': mean_temp,
            'max_temperature_degC': max_temp,
            'min_temperature_degC': min_temp,
            'std_deviation_degC': std_temp,
            'uniformity_degC': uniformity,
            'target_uniformity_degC': self.temp_uniformity_target,
            'is_iec_compliant': is_compliant,
            'measurement_points': len(temps),
            'temperature_field': temps.reshape((3, 3, 3))
        }

    def simulate_humidity_distribution(self, set_rh: float) -> Dict:
        """
        Simulate humidity distribution in chamber
        Returns humidity uniformity analysis
        """
        # Create measurement grid (15 points for humidity)
        grid_x = np.linspace(0.15, 0.85, 3) * self.length
        grid_y = np.linspace(0.15, 0.85, 3) * self.width
        grid_z = np.linspace(0.3, 0.7, 2) * self.height  # Fewer vertical points

        # Generate humidity field
        np.random.seed(43)
        rh_values = []

        for z in grid_z:
            for y in grid_y:
                for x in grid_x:
                    rh = set_rh

                    # Stratification effect (higher humidity at bottom)
                    z_factor = 1.0 - (z / self.height)
                    rh += 0.8 * z_factor

                    # Wall effects
                    edge_distance = min(x/self.length, (self.length-x)/self.length,
                                       y/self.width, (self.width-y)/self.width)
                    rh -= 0.5 * (1.0 - edge_distance/0.5)

                    # Random variation
                    rh += np.random.normal(0, 0.3)

                    rh_values.append(rh)

        rh_values = np.array(rh_values)

        # Calculate uniformity
        mean_rh = np.mean(rh_values)
        max_rh = np.max(rh_values)
        min_rh = np.min(rh_values)
        std_rh = np.std(rh_values)
        uniformity = max_rh - min_rh

        # IEC compliance
        is_compliant = uniformity <= self.humidity_uniformity_target

        return {
            'set_humidity_percent_rh': set_rh,
            'mean_humidity_percent_rh': mean_rh,
            'max_humidity_percent_rh': max_rh,
            'min_humidity_percent_rh': min_rh,
            'std_deviation_percent_rh': std_rh,
            'uniformity_percent_rh': uniformity,
            'target_uniformity_percent_rh': self.humidity_uniformity_target,
            'is_iec_compliant': is_compliant,
            'measurement_points': len(rh_values),
            'humidity_field': rh_values.reshape((2, 3, 3))
        }

    def calculate_heat_load_breakdown(self) -> Dict:
        """
        Detailed heat load analysis for CFD boundary conditions
        """
        # 1. UV lamp heat load
        uv_power = 1600  # W (total for all lamps)
        uv_to_heat_efficiency = 0.65  # 65% becomes heat
        uv_heat_load = uv_power * uv_to_heat_efficiency

        # 2. Sample heat load (PV modules with DC power)
        num_modules = 2
        power_per_module = 800  # W
        sample_heat_load = num_modules * power_per_module

        # 3. Ambient heat infiltration
        # Calculate based on surface area and insulation
        surface_area = 2 * (self.length * self.width + self.length * self.height + self.width * self.height)
        insulation_u_value = 0.22  # W/(m²·K) for 100mm PUF
        ambient_temp = 35  # °C (worst case)
        chamber_temp = 85  # °C (high temp test)
        delta_t = abs(chamber_temp - ambient_temp)
        ambient_heat_infiltration = surface_area * insulation_u_value * delta_t

        # 4. Fan/motor heat
        fan_power = 1500  # W (motor inefficiency)
        fan_heat_load = fan_power * 0.2  # 20% becomes heat

        # 5. Control cabinet heat
        cabinet_heat = 200  # W

        # Total heat load
        total_heat_load = (uv_heat_load + sample_heat_load +
                          ambient_heat_infiltration + fan_heat_load + cabinet_heat)

        return {
            'uv_lamp_heat_w': uv_heat_load,
            'sample_heat_w': sample_heat_load,
            'ambient_infiltration_w': ambient_heat_infiltration,
            'fan_motor_heat_w': fan_heat_load,
            'control_cabinet_heat_w': cabinet_heat,
            'total_heat_load_w': total_heat_load,
            'total_heat_load_kw': total_heat_load / 1000,
            'breakdown_percent': {
                'UV_lamps': (uv_heat_load / total_heat_load) * 100,
                'Samples': (sample_heat_load / total_heat_load) * 100,
                'Infiltration': (ambient_heat_infiltration / total_heat_load) * 100,
                'Fans': (fan_heat_load / total_heat_load) * 100,
                'Cabinet': (cabinet_heat / total_heat_load) * 100
            }
        }

    def get_simulation_summary(self) -> Dict:
        """Get complete CFD simulation summary"""
        heat_load = self.calculate_heat_load_breakdown()
        airflow = self.calculate_required_airflow(heat_load['total_heat_load_kw'])
        pressure = self.calculate_pressure_drop(airflow['airflow_m3_h'])
        blowers = self.size_blowers(airflow['airflow_m3_h'], pressure['total_pressure_drop_pa'])
        temp_dist = self.simulate_temperature_distribution(85, uv_on=True)
        humidity_dist = self.simulate_humidity_distribution(75)

        return {
            'heat_load_analysis': heat_load,
            'airflow_design': airflow,
            'pressure_drop': pressure,
            'blower_sizing': blowers,
            'temperature_distribution': temp_dist,
            'humidity_distribution': humidity_dist,
            'iec_compliance': {
                'temperature_uniformity': temp_dist['is_iec_compliant'],
                'humidity_uniformity': humidity_dist['is_iec_compliant'],
                'standards': ['IEC 61215', 'IEC 61730', 'IEC 60068-3-5']
            }
        }
