"""
UV Optical System Design
Handles lamp selection, uniformity optimization, and spectral compliance for PV testing
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class LampSpecification:
    """UV Lamp Specifications"""
    type: str
    power_w: int
    wavelength_range_nm: Tuple[int, int]
    uva_percent: float
    uvb_percent: float
    lifetime_hours: int
    cost_inr: int
    spectral_stability: str
    dimmability: str


class UVOpticalSystem:
    """
    UV Optical System Design and Analysis
    Ensures IEC 60904-9 compliance for solar simulators
    """

    def __init__(self):
        # Test area
        self.test_area_length = 3.2  # m
        self.test_area_width = 2.1   # m
        self.test_area_m2 = self.test_area_length * self.test_area_width

        # IEC requirements
        self.target_irradiance_min = 25   # W/m²
        self.target_irradiance_max = 250  # W/m²
        self.target_irradiance_typical = 60  # W/m² (IEC 61215)
        self.uniformity_target = 10  # ±% (IEC requirement)

        # Uniformity measurement grid (24-30 points)
        self.grid_points = 30

        # Lamp database
        self.lamp_types = self._initialize_lamp_database()

    def _initialize_lamp_database(self) -> Dict:
        """Initialize UV lamp options database"""
        return {
            'UV_LED': LampSpecification(
                type='UV LED Array',
                power_w=100,
                wavelength_range_nm=(280, 400),
                uva_percent=95.0,
                uvb_percent=5.0,
                lifetime_hours=50000,
                cost_inr=180000,
                spectral_stability='Excellent (±2%)',
                dimmability='0-100% continuous'
            ),
            'Metal_Halide': LampSpecification(
                type='Metal Halide',
                power_w=400,
                wavelength_range_nm=(290, 400),
                uva_percent=92.0,
                uvb_percent=8.0,
                lifetime_hours=5000,
                cost_inr=45000,
                spectral_stability='Good (±5%)',
                dimmability='50-100% (ballast dependent)'
            ),
            'Fluorescent_UVA': LampSpecification(
                type='Fluorescent UVA',
                power_w=80,
                wavelength_range_nm=(315, 400),
                uva_percent=97.0,
                uvb_percent=3.0,
                lifetime_hours=8000,
                cost_inr=25000,
                spectral_stability='Moderate (±7%)',
                dimmability='Not recommended'
            )
        }

    def calculate_lamp_count(self, lamp_type: str, target_irradiance: float = 60) -> Dict:
        """
        Calculate number of lamps required for target irradiance
        """
        lamp_spec = self.lamp_types[lamp_type]

        # UV efficiency (electrical power to UV output)
        uv_efficiency = {
            'UV_LED': 0.35,        # 35% electrical to UV
            'Metal_Halide': 0.25,  # 25% electrical to UV
            'Fluorescent_UVA': 0.30  # 30% electrical to UV
        }

        efficiency = uv_efficiency.get(lamp_type, 0.25)

        # UV power output per lamp
        uv_output_per_lamp = lamp_spec.power_w * efficiency  # W

        # Total UV power required
        total_uv_required = target_irradiance * self.test_area_m2  # W

        # Number of lamps (with 20% margin for aging and uniformity)
        num_lamps_calc = (total_uv_required * 1.2) / uv_output_per_lamp
        num_lamps = int(np.ceil(num_lamps_calc))

        # Make even number for symmetry
        if num_lamps % 2 != 0:
            num_lamps += 1

        # Total electrical power
        total_electrical_power = num_lamps * lamp_spec.power_w

        # Total UV output
        total_uv_output = num_lamps * uv_output_per_lamp

        # Actual irradiance achieved
        actual_irradiance = total_uv_output / self.test_area_m2

        return {
            'lamp_type': lamp_spec.type,
            'lamp_power_w': lamp_spec.power_w,
            'uv_efficiency_percent': efficiency * 100,
            'uv_output_per_lamp_w': uv_output_per_lamp,
            'target_irradiance_w_m2': target_irradiance,
            'test_area_m2': self.test_area_m2,
            'total_uv_required_w': total_uv_required,
            'number_of_lamps': num_lamps,
            'total_electrical_power_w': total_electrical_power,
            'total_electrical_power_kw': total_electrical_power / 1000,
            'total_uv_output_w': total_uv_output,
            'actual_irradiance_w_m2': actual_irradiance,
            'irradiance_margin_percent': ((actual_irradiance - target_irradiance) / target_irradiance) * 100
        }

    def optimize_lamp_distance(self, lamp_type: str, num_lamps: int) -> Dict:
        """
        Optimize lamp-to-test-plane distance for uniformity
        Range: 300-800mm
        """
        # Lamp arrangement (rectangular array)
        # For rectangular test area, optimize rows and columns
        aspect_ratio = self.test_area_length / self.test_area_width
        num_cols = int(np.ceil(np.sqrt(num_lamps * aspect_ratio)))
        num_rows = int(np.ceil(num_lamps / num_cols))

        # Adjust if needed
        while num_rows * num_cols < num_lamps:
            num_cols += 1

        # Lamp spacing
        lamp_spacing_x = self.test_area_length / num_cols  # m
        lamp_spacing_y = self.test_area_width / num_rows   # m

        # Optimal distance calculation (based on beam angle and spacing)
        # For good uniformity: distance ≈ 0.5 × diagonal spacing
        diagonal_spacing = np.sqrt(lamp_spacing_x**2 + lamp_spacing_y**2)
        optimal_distance_m = 0.5 * diagonal_spacing

        # Constrain to 300-800mm range
        optimal_distance_m = np.clip(optimal_distance_m, 0.3, 0.8)
        optimal_distance_mm = optimal_distance_m * 1000

        # Beam angle requirement
        required_beam_angle = 2 * np.arctan((diagonal_spacing / 2) / optimal_distance_m) * (180 / np.pi)

        return {
            'num_lamps': num_lamps,
            'array_configuration': f"{num_rows} × {num_cols}",
            'num_rows': num_rows,
            'num_cols': num_cols,
            'lamp_spacing_x_m': lamp_spacing_x,
            'lamp_spacing_y_m': lamp_spacing_y,
            'diagonal_spacing_m': diagonal_spacing,
            'optimal_distance_m': optimal_distance_m,
            'optimal_distance_mm': optimal_distance_mm,
            'distance_range_mm': (300, 800),
            'required_beam_angle_deg': required_beam_angle,
            'recommended_beam_angle': '90-120° for uniform coverage'
        }

    def simulate_uniformity(self, lamp_type: str, num_lamps: int, distance_mm: float) -> Dict:
        """
        Simulate UV uniformity across test plane
        24-30 measurement points as per IEC 60904-9
        """
        distance_m = distance_mm / 1000

        # Get lamp configuration
        config = self.optimize_lamp_distance(lamp_type, num_lamps)
        num_rows = config['num_rows']
        num_cols = config['num_cols']

        # Create measurement grid (5×6 = 30 points)
        meas_x = np.linspace(0.1, 0.9, 6) * self.test_area_length
        meas_y = np.linspace(0.1, 0.9, 5) * self.test_area_width

        # Lamp positions
        lamp_x = np.linspace(0, self.test_area_length, num_cols)
        lamp_y = np.linspace(0, self.test_area_width, num_rows)

        # Calculate irradiance at each measurement point
        irradiance_map = np.zeros((len(meas_y), len(meas_x)))

        for i, y_m in enumerate(meas_y):
            for j, x_m in enumerate(meas_x):
                total_irradiance = 0

                # Sum contribution from all lamps (inverse square law + cosine effect)
                for lx in lamp_x:
                    for ly in lamp_y:
                        # Distance from lamp to measurement point
                        r = np.sqrt((x_m - lx)**2 + (y_m - ly)**2 + distance_m**2)

                        # Cosine effect (angle from normal)
                        cos_angle = distance_m / r

                        # Irradiance contribution (simplified model)
                        # I = I0 * cos³(θ) / r²
                        lamp_contribution = (100 / num_lamps) * (cos_angle**3) / (r**2)

                        total_irradiance += lamp_contribution

                irradiance_map[i, j] = total_irradiance

        # Normalize to target irradiance
        irradiance_map = irradiance_map * (self.target_irradiance_typical / np.mean(irradiance_map))

        # Calculate uniformity metrics
        mean_irradiance = np.mean(irradiance_map)
        max_irradiance = np.max(irradiance_map)
        min_irradiance = np.min(irradiance_map)
        std_irradiance = np.std(irradiance_map)

        # Non-uniformity (as per IEC 60904-9)
        non_uniformity = ((max_irradiance - min_irradiance) / mean_irradiance) * 100

        # IEC compliance
        is_compliant = non_uniformity <= self.uniformity_target

        return {
            'lamp_configuration': config['array_configuration'],
            'distance_mm': distance_mm,
            'measurement_points': len(meas_x) * len(meas_y),
            'grid_size': f"{len(meas_y)} × {len(meas_x)}",
            'mean_irradiance_w_m2': mean_irradiance,
            'max_irradiance_w_m2': max_irradiance,
            'min_irradiance_w_m2': min_irradiance,
            'std_irradiance_w_m2': std_irradiance,
            'non_uniformity_percent': non_uniformity,
            'target_uniformity_percent': self.uniformity_target,
            'is_iec_compliant': is_compliant,
            'irradiance_map': irradiance_map,
            'iec_classification': 'Class A' if non_uniformity <= 2 else 'Class B' if non_uniformity <= 5 else 'Class C'
        }

    def analyze_spectral_compliance(self, lamp_type: str) -> Dict:
        """
        Analyze spectral composition compliance with IEC requirements
        """
        lamp_spec = self.lamp_types[lamp_type]

        # IEC requirements for UV testing
        # UVA: 315-400nm (should be 90-97%)
        # UVB: 280-315nm (should be 3-10%)
        # UVC: <280nm (should be minimal)

        uva_compliant = 90 <= lamp_spec.uva_percent <= 97
        uvb_compliant = 3 <= lamp_spec.uvb_percent <= 10
        total_compliant = abs((lamp_spec.uva_percent + lamp_spec.uvb_percent) - 100) < 1

        # Spectral drift analysis
        # Estimate drift over time and temperature
        drift_factors = {
            'UV_LED': {
                'temp_drift_percent_per_degC': 0.02,
                'aging_drift_percent_per_1000h': 0.5,
                'warm_up_time_min': 0.5
            },
            'Metal_Halide': {
                'temp_drift_percent_per_degC': 0.15,
                'aging_drift_percent_per_1000h': 3.0,
                'warm_up_time_min': 15
            },
            'Fluorescent_UVA': {
                'temp_drift_percent_per_degC': 0.25,
                'aging_drift_percent_per_1000h': 5.0,
                'warm_up_time_min': 5
            }
        }

        drift = drift_factors.get(lamp_type, drift_factors['UV_LED'])

        return {
            'lamp_type': lamp_spec.type,
            'wavelength_range_nm': lamp_spec.wavelength_range_nm,
            'uva_percent': lamp_spec.uva_percent,
            'uvb_percent': lamp_spec.uvb_percent,
            'uva_compliant': uva_compliant,
            'uvb_compliant': uvb_compliant,
            'total_compliant': total_compliant,
            'spectral_stability': lamp_spec.spectral_stability,
            'temp_drift_percent_per_degC': drift['temp_drift_percent_per_degC'],
            'aging_drift_percent_per_1000h': drift['aging_drift_percent_per_1000h'],
            'warm_up_time_min': drift['warm_up_time_min'],
            'calibration_frequency_hours': lamp_spec.lifetime_hours / 10,
            'iec_standard': 'IEC 60904-9',
            'compliance_status': 'PASS' if (uva_compliant and uvb_compliant) else 'FAIL'
        }

    def specify_glass_requirements(self) -> Dict:
        """
        Specify glass requirements for UV chamber windows
        """
        return {
            'window_purpose': 'UV transmission to test plane',
            'material': 'Solar toughened glass',
            'thickness_mm': 8,
            'uv_transmission': '>90% for 280-400nm',
            'thermal_properties': {
                'heat_insulation': 'Low-E coating optional',
                'max_temperature_degC': 150,
                'thermal_expansion_coeff': '9.0×10⁻⁶ /°C'
            },
            'mechanical_properties': {
                'impact_resistance': 'Toughened to IEC 60068-2-75',
                'safety': 'Breaks into small granular chunks',
                'edge_treatment': 'Polished edges'
            },
            'optical_properties': {
                'surface_quality': 'Low haze, minimal distortion',
                'anti_reflection_coating': 'Optional for >95% transmission',
                'wavelength_cutoff': '<280nm (blocks UVC)'
            },
            'mounting': {
                'frame_material': 'Aluminum with silicone gaskets',
                'seal_rating': 'IP65',
                'replacement_interval': 'Every 5 years or as needed'
            }
        }

    def calculate_system_cost(self, lamp_type: str, num_lamps: int) -> Dict:
        """
        Calculate total UV system cost
        """
        lamp_spec = self.lamp_types[lamp_type]

        # Component costs (INR)
        lamp_cost = num_lamps * lamp_spec.cost_inr
        ballast_cost = num_lamps * 15000  # Per ballast/driver
        reflector_cost = num_lamps * 8000  # Reflectors
        mounting_frame_cost = 150000  # Complete mounting structure
        glass_window_cost = 80000  # UV-transmitting glass
        control_system_cost = 120000  # Dimming controls, monitoring
        wiring_sensors_cost = 80000  # Electrical wiring and UV sensors

        total_cost = (lamp_cost + ballast_cost + reflector_cost +
                     mounting_frame_cost + glass_window_cost +
                     control_system_cost + wiring_sensors_cost)

        # Operating cost (per year)
        operating_hours_per_year = 2000  # Estimated usage
        lamp_replacements_per_year = (operating_hours_per_year * num_lamps) / lamp_spec.lifetime_hours
        annual_lamp_cost = lamp_replacements_per_year * lamp_spec.cost_inr

        # Energy cost
        power_kw = (num_lamps * lamp_spec.power_w) / 1000
        energy_kwh_per_year = power_kw * operating_hours_per_year
        electricity_rate_inr_per_kwh = 8  # Industrial rate
        annual_energy_cost = energy_kwh_per_year * electricity_rate_inr_per_kwh

        total_annual_operating_cost = annual_lamp_cost + annual_energy_cost

        return {
            'capital_costs': {
                'lamps': lamp_cost,
                'ballasts_drivers': ballast_cost,
                'reflectors': reflector_cost,
                'mounting_frame': mounting_frame_cost,
                'glass_windows': glass_window_cost,
                'controls': control_system_cost,
                'wiring_sensors': wiring_sensors_cost,
                'total_capital_inr': total_cost,
                'total_capital_lakhs': total_cost / 100000
            },
            'operating_costs_annual': {
                'lamp_replacements_inr': annual_lamp_cost,
                'energy_cost_inr': annual_energy_cost,
                'total_operating_inr': total_annual_operating_cost,
                'operating_hours': operating_hours_per_year,
                'power_consumption_kw': power_kw,
                'energy_consumption_kwh': energy_kwh_per_year
            },
            'lifetime_analysis': {
                'lamp_lifetime_hours': lamp_spec.lifetime_hours,
                'replacements_per_year': lamp_replacements_per_year,
                'system_lifetime_years': 10,
                'total_10year_cost_inr': total_cost + (total_annual_operating_cost * 10),
                'total_10year_cost_lakhs': (total_cost + (total_annual_operating_cost * 10)) / 100000
            }
        }

    def get_uv_system_summary(self, lamp_type: str = 'UV_LED', target_irradiance: float = 60) -> Dict:
        """Get complete UV optical system summary"""
        lamp_count = self.calculate_lamp_count(lamp_type, target_irradiance)
        num_lamps = lamp_count['number_of_lamps']
        distance_opt = self.optimize_lamp_distance(lamp_type, num_lamps)
        uniformity = self.simulate_uniformity(lamp_type, num_lamps, distance_opt['optimal_distance_mm'])
        spectral = self.analyze_spectral_compliance(lamp_type)
        glass_spec = self.specify_glass_requirements()
        cost = self.calculate_system_cost(lamp_type, num_lamps)

        return {
            'lamp_selection': lamp_count,
            'optical_design': distance_opt,
            'uniformity_analysis': uniformity,
            'spectral_compliance': spectral,
            'glass_specifications': glass_spec,
            'cost_analysis': cost,
            'iec_compliance_summary': {
                'uniformity': uniformity['is_iec_compliant'],
                'spectral': spectral['compliance_status'] == 'PASS',
                'standards': ['IEC 60904-9', 'IEC 61215', 'IEC 61730']
            }
        }
