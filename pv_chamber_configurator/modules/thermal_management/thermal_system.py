"""
Thermal Management System Design
Calculates refrigeration requirements, chiller sizing, and cooling water specifications
"""

import numpy as np
from typing import Dict, List, Tuple


class ThermalManagement:
    """
    Thermal Management System for Environmental Chamber
    Handles heating, cooling, and temperature control design
    """

    def __init__(self):
        # Temperature specifications
        self.temp_min = -45  # °C
        self.temp_max = 105  # °C (with UV ON)
        self.temp_uniformity = 2.0  # ±°C
        self.ramp_rate_min = 1.6  # °C/min
        self.ramp_rate_max = 3.5  # °C/min

        # Refrigerant options
        self.refrigerants = {
            'R449A': {
                'name': 'R449A (Opteon™ XP40)',
                'gwp': 1397,
                'ozone_depletion': 0,
                'temp_range': (-50, 60),
                'application': 'Low and medium temp',
                'replaces': 'R404A, R507',
                'availability': 'Widely available in India'
            },
            'R472B': {
                'name': 'R472B (Forane® 472B)',
                'gwp': 2146,
                'ozone_depletion': 0,
                'temp_range': (-60, 50),
                'application': 'Low temp applications',
                'replaces': 'R404A',
                'availability': 'Available'
            }
        }

    def calculate_heat_load(self, chamber_temp: float, ambient_temp: float = 35) -> Dict:
        """
        Calculate total heat load for refrigeration sizing
        """
        # Chamber dimensions
        length, width, height = 3.2, 2.1, 2.2  # m

        # 1. Sample heat load (PV modules with DC power)
        sample_power = 800  # W per module
        num_modules = 2
        sample_heat = sample_power * num_modules  # W

        # 2. UV lamp heat (when UV is ON)
        uv_lamps_power = 1600  # W total
        uv_to_heat = 0.65  # 65% becomes heat
        uv_heat = uv_lamps_power * uv_to_heat if chamber_temp > 0 else 0  # W

        # 3. Ambient heat infiltration through walls
        # Surface area
        surface_area = 2 * (length*width + length*height + width*height)  # m²

        # U-value for 100mm PUF insulation
        u_value = 0.22  # W/(m²·K)

        # Temperature difference
        delta_t = abs(chamber_temp - ambient_temp)

        # Heat infiltration
        ambient_heat = surface_area * u_value * delta_t  # W

        # 4. Air circulation fan/blower heat
        fan_power = 1500  # W (motor power)
        fan_efficiency = 0.75
        fan_heat = fan_power * (1 - fan_efficiency)  # W

        # 5. Humidity system heat (when humidifying)
        humidity_heat = 500  # W (steam generator / water heating)

        # 6. Control system and lighting heat
        controls_heat = 200  # W

        # 7. Door opening heat gain (periodic)
        door_heat = 150  # W (averaged over time)

        # Total heat load
        total_heat_load_w = (sample_heat + uv_heat + ambient_heat +
                            fan_heat + humidity_heat + controls_heat + door_heat)

        total_heat_load_kw = total_heat_load_w / 1000

        # Breakdown percentages
        breakdown = {
            'Sample/PV modules': (sample_heat / total_heat_load_w) * 100,
            'UV lamps': (uv_heat / total_heat_load_w) * 100,
            'Wall infiltration': (ambient_heat / total_heat_load_w) * 100,
            'Air circulation': (fan_heat / total_heat_load_w) * 100,
            'Humidity system': (humidity_heat / total_heat_load_w) * 100,
            'Controls/Lighting': (controls_heat / total_heat_load_w) * 100,
            'Door openings': (door_heat / total_heat_load_w) * 100
        }

        return {
            'chamber_temperature_degC': chamber_temp,
            'ambient_temperature_degC': ambient_temp,
            'sample_heat_w': sample_heat,
            'uv_lamp_heat_w': uv_heat,
            'ambient_infiltration_w': ambient_heat,
            'fan_motor_heat_w': fan_heat,
            'humidity_system_heat_w': humidity_heat,
            'controls_lighting_heat_w': controls_heat,
            'door_opening_heat_w': door_heat,
            'total_heat_load_w': total_heat_load_w,
            'total_heat_load_kw': total_heat_load_kw,
            'breakdown_percent': breakdown
        }

    def size_refrigeration_system(self, heat_load_kw: float) -> Dict:
        """
        Size refrigeration system based on heat load
        """
        # Add safety factor
        safety_factor = 1.25  # 25% safety margin
        design_capacity_kw = heat_load_kw * safety_factor

        # Convert to Tons of Refrigeration (TR)
        # 1 TR = 3.517 kW
        capacity_tr = design_capacity_kw / 3.517

        # Cascade refrigeration for wide temperature range (-45°C to +105°C)
        # Low stage: -45°C to -10°C
        # High stage: -10°C to +105°C

        # Number of compressor stages
        temp_range = self.temp_max - self.temp_min
        num_stages = 2 if temp_range > 100 else 1

        # Compressor power estimation
        # COP (Coefficient of Performance) varies with temperature
        # Low temp: COP ~ 1.5-2.0
        # High temp: COP ~ 2.5-3.5

        avg_cop = 2.2
        compressor_power_kw = design_capacity_kw / avg_cop

        return {
            'required_capacity_kw': heat_load_kw,
            'safety_factor': safety_factor,
            'design_capacity_kw': design_capacity_kw,
            'capacity_tr': capacity_tr,
            'capacity_btu_h': capacity_tr * 12000,
            'temperature_range_degC': (self.temp_min, self.temp_max),
            'num_compressor_stages': num_stages,
            'stage_configuration': 'Cascade (2-stage)' if num_stages == 2 else 'Single stage',
            'estimated_cop': avg_cop,
            'compressor_power_kw': compressor_power_kw,
            'compressor_power_hp': compressor_power_kw * 1.341,
            'refrigerant_recommended': 'R449A (primary) + R449A (cascade)' if num_stages == 2 else 'R449A'
        }

    def size_chiller(self, refrigeration_capacity_tr: float) -> Dict:
        """
        Size process cooling water chiller
        """
        # Chiller capacity (match refrigeration)
        chiller_capacity_tr = refrigeration_capacity_tr

        # Process cooling water specifications
        pcw_flow_gpm = chiller_capacity_tr * 2.4  # GPM (typical: 2-3 GPM per TR)
        pcw_flow_lpm = pcw_flow_gpm * 3.785  # LPM
        pcw_flow_m3_h = pcw_flow_lpm * 0.06  # m³/h

        # Temperature differential
        pcw_supply_temp = 10  # °C
        pcw_return_temp = 15  # °C
        delta_t = pcw_return_temp - pcw_supply_temp  # 5°C

        # Verify heat removal
        water_specific_heat = 4.186  # kJ/(kg·°C)
        water_density = 1000  # kg/m³
        heat_removed_kw = (pcw_flow_m3_h / 3600) * water_density * water_specific_heat * delta_t

        # Pump sizing
        # Head calculation (typical: 20-40m for closed loop)
        pump_head_m = 30  # m
        pump_power_kw = (pcw_flow_m3_h * pump_head_m * water_density * 9.81) / (3600 * 1000 * 0.75)

        return {
            'chiller_capacity_tr': chiller_capacity_tr,
            'chiller_capacity_kw': chiller_capacity_tr * 3.517,
            'pcw_flow_gpm': pcw_flow_gpm,
            'pcw_flow_lpm': pcw_flow_lpm,
            'pcw_flow_m3_h': pcw_flow_m3_h,
            'pcw_supply_temp_degC': pcw_supply_temp,
            'pcw_return_temp_degC': pcw_return_temp,
            'pcw_delta_t_degC': delta_t,
            'heat_removal_capacity_kw': heat_removed_kw,
            'pump_head_m': pump_head_m,
            'pump_power_kw': pump_power_kw,
            'pump_type': 'Centrifugal, SS316 wetted parts',
            'piping_size': 'DN50 (2") SCH40 SS304'
        }

    def size_evaporator_condenser(self, capacity_kw: float) -> Dict:
        """
        Size heat exchangers (evaporator and condenser)
        """
        # Evaporator sizing (inside chamber)
        # Heat transfer coefficient for forced air: 20-50 W/(m²·K)
        htc_evap = 35  # W/(m²·K)
        lmtd_evap = 10  # Log mean temperature difference, °C

        evap_area_m2 = capacity_kw * 1000 / (htc_evap * lmtd_evap)

        # Typical finned coil geometry
        fins_per_inch = 8
        fin_material = 'Aluminum'
        tube_material = 'Copper'

        # Condenser sizing (water-cooled)
        htc_cond = 800  # W/(m²·K) for water-cooled
        lmtd_cond = 5  # °C

        cond_area_m2 = capacity_kw * 1000 / (htc_cond * lmtd_cond)

        return {
            'evaporator': {
                'heat_transfer_area_m2': evap_area_m2,
                'heat_transfer_coefficient': htc_evap,
                'lmtd_degC': lmtd_evap,
                'capacity_kw': capacity_kw,
                'type': 'Finned coil evaporator',
                'fins_per_inch': fins_per_inch,
                'fin_material': fin_material,
                'tube_material': tube_material,
                'defrost_method': 'Electric + Hot gas bypass',
                'location': 'Chamber plenum'
            },
            'condenser': {
                'heat_transfer_area_m2': cond_area_m2,
                'heat_transfer_coefficient': htc_cond,
                'lmtd_degC': lmtd_cond,
                'capacity_kw': capacity_kw * 1.3,  # Includes compressor heat
                'type': 'Shell and tube',
                'tube_material': 'Copper/Cu-Ni',
                'shell_material': 'SS304',
                'cooling_medium': 'Process cooling water',
                'location': 'Refrigeration rack'
            }
        }

    def calculate_temperature_control(self) -> Dict:
        """
        Specify temperature control system
        """
        # PID control parameters
        # Tuned for environmental chamber dynamics

        return {
            'control_method': 'Cascade PID',
            'primary_loop': {
                'sensor': 'RTD Pt100 (Class A)',
                'location': 'Chamber center',
                'accuracy': '±0.1°C',
                'response_time': '5 seconds',
                'pid_parameters': {
                    'P': 5.0,
                    'I': 180,
                    'D': 30
                }
            },
            'secondary_loop': {
                'sensor': 'RTD Pt100 (Class A)',
                'location': 'Evaporator outlet',
                'accuracy': '±0.1°C',
                'response_time': '3 seconds',
                'pid_parameters': {
                    'P': 3.0,
                    'I': 120,
                    'D': 20
                }
            },
            'heating_control': {
                'method': 'SCR (Silicon Controlled Rectifier)',
                'heater_type': 'Finned tubular heaters, SS sheath',
                'total_power_kw': 6,
                'num_stages': 3,
                'modulation': '0-100% continuous'
            },
            'cooling_control': {
                'method': 'VFD on compressor + Hot gas bypass',
                'capacity_modulation': '10-100%',
                'response_time': '15 seconds',
                'defrost_cycle': 'Automatic based on pressure diff'
            },
            'safety_features': {
                'over_temp_cutout': 'Hardware limit at 110°C',
                'under_temp_cutout': 'Hardware limit at -50°C',
                'refrigerant_leak_detection': 'Yes',
                'pressure_relief': 'Automatic safety valves'
            }
        }

    def estimate_thermal_system_cost(self) -> Dict:
        """
        Estimate cost of thermal management system
        """
        costs = {
            'compressor_cascade_system': 350000,  # INR
            'evaporator_coils': 80000,
            'condenser': 60000,
            'expansion_valves': 40000,
            'refrigerant_charge': 35000,
            'heaters_scr': 55000,
            'chiller_3tr': 450000,
            'pcw_pump_piping': 85000,
            'controls_sensors': 120000,
            'installation_piping': 125000
        }

        total = sum(costs.values())

        return {
            'component_costs_inr': costs,
            'total_thermal_system_inr': total,
            'total_lakhs': total / 100000,
            'operating_cost_per_year_inr': 45000,  # Maintenance + refrigerant top-up
            'energy_cost_note': 'Calculated separately based on usage'
        }

    def get_thermal_summary(self, chamber_temp: float = 85, ambient_temp: float = 35) -> Dict:
        """Get complete thermal management summary"""
        heat_load = self.calculate_heat_load(chamber_temp, ambient_temp)
        refrigeration = self.size_refrigeration_system(heat_load['total_heat_load_kw'])
        chiller = self.size_chiller(refrigeration['capacity_tr'])
        heat_exchangers = self.size_evaporator_condenser(refrigeration['design_capacity_kw'])
        control = self.calculate_temperature_control()
        cost = self.estimate_thermal_system_cost()

        return {
            'specifications': {
                'temperature_range': (self.temp_min, self.temp_max),
                'uniformity': f"±{self.temp_uniformity}°C",
                'ramp_rate': f"{self.ramp_rate_min}-{self.ramp_rate_max}°C/min"
            },
            'heat_load_analysis': heat_load,
            'refrigeration_system': refrigeration,
            'chiller_system': chiller,
            'heat_exchangers': heat_exchangers,
            'temperature_control': control,
            'cost_estimate': cost,
            'refrigerant_selection': self.refrigerants['R449A']
        }
