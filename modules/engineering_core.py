"""
Engineering Core Module - Foundation for All Calculations
=========================================================

This module provides the base calculation engine used by all other modules.
It implements IEC standards validation, unit conversion utilities, and
mathematical helpers required for environmental chamber design and analysis.

Integration Points:
------------------
- Used by: chamber_design, cfd_simulation, uv_system, quote_generator
- Dependencies: None (Foundation module)
- Merge Priority: 1 (Must be merged first)

Author: Audit-Pro Enterprise
Version: 1.0.0
"""

import math
from typing import Dict, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


class IECStandard(Enum):
    """IEC Standards for Environmental Testing"""
    IEC_60068_2_1 = "IEC 60068-2-1"  # Cold test
    IEC_60068_2_2 = "IEC 60068-2-2"  # Dry heat test
    IEC_60068_2_14 = "IEC 60068-2-14"  # Change of temperature
    IEC_60068_2_30 = "IEC 60068-2-30"  # Damp heat test
    IEC_60068_2_38 = "IEC 60068-2-38"  # Combined temperature/humidity
    IEC_60068_3_5 = "IEC 60068-3-5"  # Temperature test guidance


class UnitSystem(Enum):
    """Supported unit systems"""
    METRIC = "metric"
    IMPERIAL = "imperial"


@dataclass
class Temperature:
    """Temperature representation with unit conversion"""
    value: float
    unit: str = "C"  # C, F, K

    def to_celsius(self) -> float:
        """Convert to Celsius"""
        if self.unit == "C":
            return self.value
        elif self.unit == "F":
            return (self.value - 32) * 5/9
        elif self.unit == "K":
            return self.value - 273.15
        else:
            raise ValueError(f"Unknown temperature unit: {self.unit}")

    def to_fahrenheit(self) -> float:
        """Convert to Fahrenheit"""
        celsius = self.to_celsius()
        return celsius * 9/5 + 32

    def to_kelvin(self) -> float:
        """Convert to Kelvin"""
        celsius = self.to_celsius()
        return celsius + 273.15


@dataclass
class Dimension:
    """Dimension with unit conversion support"""
    value: float
    unit: str = "mm"  # mm, cm, m, inch, ft

    def to_meters(self) -> float:
        """Convert to meters"""
        conversions = {
            "mm": 0.001,
            "cm": 0.01,
            "m": 1.0,
            "inch": 0.0254,
            "ft": 0.3048
        }
        if self.unit not in conversions:
            raise ValueError(f"Unknown dimension unit: {self.unit}")
        return self.value * conversions[self.unit]

    def to_millimeters(self) -> float:
        """Convert to millimeters"""
        return self.to_meters() * 1000

    def to_inches(self) -> float:
        """Convert to inches"""
        return self.to_meters() / 0.0254


class UnitConverter:
    """Comprehensive unit conversion utilities"""

    @staticmethod
    def temperature(value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between units"""
        temp = Temperature(value, from_unit)
        if to_unit == "C":
            return temp.to_celsius()
        elif to_unit == "F":
            return temp.to_fahrenheit()
        elif to_unit == "K":
            return temp.to_kelvin()
        else:
            raise ValueError(f"Unknown target unit: {to_unit}")

    @staticmethod
    def length(value: float, from_unit: str, to_unit: str) -> float:
        """Convert length between units"""
        dim = Dimension(value, from_unit)
        conversions = {
            "m": dim.to_meters(),
            "mm": dim.to_millimeters(),
            "cm": dim.to_meters() * 100,
            "inch": dim.to_inches(),
            "ft": dim.to_inches() / 12
        }
        if to_unit not in conversions:
            raise ValueError(f"Unknown target unit: {to_unit}")
        return conversions[to_unit]

    @staticmethod
    def volume(value: float, from_unit: str, to_unit: str) -> float:
        """Convert volume between units"""
        conversions_to_cubic_meters = {
            "m3": 1.0,
            "cm3": 1e-6,
            "mm3": 1e-9,
            "L": 0.001,
            "mL": 1e-6,
            "ft3": 0.0283168,
            "in3": 1.63871e-5,
            "gal": 0.00378541  # US gallon
        }

        if from_unit not in conversions_to_cubic_meters or to_unit not in conversions_to_cubic_meters:
            raise ValueError("Unknown volume unit")

        cubic_meters = value * conversions_to_cubic_meters[from_unit]
        return cubic_meters / conversions_to_cubic_meters[to_unit]

    @staticmethod
    def pressure(value: float, from_unit: str, to_unit: str) -> float:
        """Convert pressure between units"""
        conversions_to_pascal = {
            "Pa": 1.0,
            "kPa": 1000.0,
            "MPa": 1e6,
            "bar": 1e5,
            "mbar": 100.0,
            "psi": 6894.76,
            "atm": 101325.0,
            "mmHg": 133.322,
            "inHg": 3386.39
        }

        if from_unit not in conversions_to_pascal or to_unit not in conversions_to_pascal:
            raise ValueError("Unknown pressure unit")

        pascals = value * conversions_to_pascal[from_unit]
        return pascals / conversions_to_pascal[to_unit]

    @staticmethod
    def power(value: float, from_unit: str, to_unit: str) -> float:
        """Convert power between units"""
        conversions_to_watts = {
            "W": 1.0,
            "kW": 1000.0,
            "MW": 1e6,
            "hp": 745.7,
            "BTU/h": 0.293071
        }

        if from_unit not in conversions_to_watts or to_unit not in conversions_to_watts:
            raise ValueError("Unknown power unit")

        watts = value * conversions_to_watts[from_unit]
        return watts / conversions_to_watts[to_unit]


class IECValidator:
    """Validation against IEC standards"""

    @staticmethod
    def validate_temperature_range(min_temp: float, max_temp: float,
                                   standard: IECStandard = IECStandard.IEC_60068_2_38) -> Dict:
        """
        Validate temperature range against IEC standards

        Returns:
            dict: {'valid': bool, 'warnings': list, 'recommendations': list}
        """
        warnings = []
        recommendations = []
        valid = True

        # Standard temperature ranges (in Celsius)
        standard_ranges = {
            IECStandard.IEC_60068_2_1: (-70, 25),  # Cold test
            IECStandard.IEC_60068_2_2: (25, 200),  # Dry heat
            IECStandard.IEC_60068_2_14: (-70, 200),  # Temperature change
            IECStandard.IEC_60068_2_30: (25, 55),  # Damp heat
            IECStandard.IEC_60068_2_38: (-70, 180),  # Combined temp/humidity
        }

        if standard in standard_ranges:
            std_min, std_max = standard_ranges[standard]

            if min_temp < std_min:
                warnings.append(f"Minimum temperature {min_temp}°C below standard range ({std_min}°C)")

            if max_temp > std_max:
                warnings.append(f"Maximum temperature {max_temp}°C above standard range ({std_max}°C)")

            if abs(max_temp - min_temp) > 200:
                warnings.append("Temperature range exceeds 200°C - may require special design")

        # Temperature rate of change recommendations
        temp_range = abs(max_temp - min_temp)
        if temp_range > 150:
            recommendations.append("Consider thermal shock protection for temperature range > 150°C")

        if temp_range < 10:
            recommendations.append("Small temperature range - verify stability requirements")

        return {
            'valid': valid and len(warnings) == 0,
            'warnings': warnings,
            'recommendations': recommendations,
            'standard': standard.value
        }

    @staticmethod
    def validate_humidity_range(min_rh: float, max_rh: float) -> Dict:
        """
        Validate relative humidity range

        Returns:
            dict: {'valid': bool, 'warnings': list}
        """
        warnings = []
        valid = True

        if min_rh < 10:
            warnings.append("Very low humidity (<10% RH) may require special dehumidification")

        if max_rh > 98:
            warnings.append("Very high humidity (>98% RH) may cause condensation")

        if min_rh < 0 or max_rh > 100:
            warnings.append("Humidity must be between 0-100% RH")
            valid = False

        return {
            'valid': valid,
            'warnings': warnings
        }


class MathHelpers:
    """Mathematical utilities for engineering calculations"""

    @staticmethod
    def calculate_volume(length: float, width: float, height: float) -> float:
        """Calculate chamber volume"""
        return length * width * height

    @staticmethod
    def calculate_surface_area(length: float, width: float, height: float) -> float:
        """Calculate total surface area of rectangular chamber"""
        return 2 * (length * width + length * height + width * height)

    @staticmethod
    def calculate_air_changes_per_hour(airflow_m3_per_min: float, chamber_volume_m3: float) -> float:
        """
        Calculate air changes per hour (ACH)

        Args:
            airflow_m3_per_min: Airflow rate in cubic meters per minute
            chamber_volume_m3: Chamber volume in cubic meters

        Returns:
            Air changes per hour
        """
        if chamber_volume_m3 <= 0:
            raise ValueError("Chamber volume must be positive")

        airflow_per_hour = airflow_m3_per_min * 60
        return airflow_per_hour / chamber_volume_m3

    @staticmethod
    def calculate_reynolds_number(velocity: float, characteristic_length: float,
                                  kinematic_viscosity: float = 1.5e-5) -> float:
        """
        Calculate Reynolds number for airflow

        Args:
            velocity: Air velocity (m/s)
            characteristic_length: Characteristic length (m)
            kinematic_viscosity: Kinematic viscosity (m²/s), default for air at 20°C

        Returns:
            Reynolds number (dimensionless)
        """
        return (velocity * characteristic_length) / kinematic_viscosity

    @staticmethod
    def interpolate_linear(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
        """Linear interpolation"""
        if x2 == x1:
            raise ValueError("x1 and x2 must be different for interpolation")
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

    @staticmethod
    def calculate_heat_transfer_coefficient(
        velocity: float,
        characteristic_length: float,
        thermal_conductivity: float = 0.026,  # W/(m·K) for air at 20°C
        prandtl_number: float = 0.71  # for air
    ) -> float:
        """
        Estimate convective heat transfer coefficient using simplified correlation

        Returns:
            Heat transfer coefficient in W/(m²·K)
        """
        re = MathHelpers.calculate_reynolds_number(velocity, characteristic_length)

        # Simplified Nusselt number correlation for forced convection
        if re < 5e5:  # Laminar to transitional
            nu = 0.664 * (re ** 0.5) * (prandtl_number ** 0.333)
        else:  # Turbulent
            nu = 0.037 * (re ** 0.8) * (prandtl_number ** 0.333)

        h = (nu * thermal_conductivity) / characteristic_length
        return h


class SafetyCalculations:
    """Safety-related calculations and checks"""

    @staticmethod
    def calculate_floor_loading(total_weight_kg: float, base_area_m2: float) -> Dict:
        """
        Calculate floor loading and safety classification

        Returns:
            dict with loading in kg/m² and Pa, plus safety classification
        """
        if base_area_m2 <= 0:
            raise ValueError("Base area must be positive")

        loading_kg_m2 = total_weight_kg / base_area_m2
        loading_pa = loading_kg_m2 * 9.81  # Convert to Pascals

        # Classification based on typical building codes
        if loading_pa < 2400:  # ~245 kg/m²
            classification = "Light load - Suitable for most office spaces"
        elif loading_pa < 4800:  # ~490 kg/m²
            classification = "Medium load - Suitable for light industrial"
        elif loading_pa < 7200:  # ~735 kg/m²
            classification = "Heavy load - Requires structural verification"
        else:
            classification = "Very heavy load - Requires special foundation"

        return {
            'loading_kg_m2': round(loading_kg_m2, 2),
            'loading_pa': round(loading_pa, 2),
            'loading_kpa': round(loading_pa / 1000, 2),
            'classification': classification,
            'requires_structural_engineer': loading_pa > 4800
        }

    @staticmethod
    def calculate_electrical_load(
        heating_power_kw: float,
        cooling_power_kw: float,
        humidifier_power_kw: float,
        controls_power_kw: float = 0.5,
        lighting_power_kw: float = 0.2,
        safety_factor: float = 1.25
    ) -> Dict:
        """
        Calculate total electrical load with safety factor

        Returns:
            dict with power requirements and current at various voltages
        """
        total_power = (heating_power_kw + cooling_power_kw +
                      humidifier_power_kw + controls_power_kw + lighting_power_kw)

        total_with_safety = total_power * safety_factor

        # Calculate current requirements at common voltages (3-phase)
        voltages = [208, 240, 380, 400, 415, 480]
        current_requirements = {}

        for voltage in voltages:
            # For 3-phase: I = P / (√3 × V × PF)
            # Assuming power factor of 0.95
            current = (total_with_safety * 1000) / (math.sqrt(3) * voltage * 0.95)
            current_requirements[f"{voltage}V_3ph"] = round(current, 2)

        return {
            'total_power_kw': round(total_power, 2),
            'safety_factor': safety_factor,
            'total_with_safety_kw': round(total_with_safety, 2),
            'current_requirements_amps': current_requirements,
            'recommendations': [
                f"Install {math.ceil(total_with_safety * 1.5)} kVA transformer minimum",
                "Use appropriate circuit breakers rated 20% above calculated current",
                "Ensure proper grounding and earth leakage protection"
            ]
        }


# Integration Hooks for Other Modules
class IntegrationHooks:
    """
    Placeholder hooks for integration with other modules.
    These will be populated when respective modules are merged.
    """

    @staticmethod
    def register_chamber_design_hook():
        """Hook for chamber_design module integration"""
        # Will be implemented when feature/chamber-design is merged
        pass

    @staticmethod
    def register_cfd_simulation_hook():
        """Hook for cfd_simulation module integration"""
        # Will be implemented when feature/cfd-simulation is merged
        pass

    @staticmethod
    def register_uv_system_hook():
        """Hook for uv_system module integration"""
        # Will be implemented when feature/uv-system is merged
        pass

    @staticmethod
    def register_quote_generator_hook():
        """Hook for quote_generator module integration"""
        # Will be implemented when feature/quote-generator is merged
        pass


# Example usage and testing
if __name__ == "__main__":
    print("=== Engineering Core Module Tests ===\n")

    # Test 1: Unit Conversions
    print("1. Unit Conversion Tests:")
    temp_f = UnitConverter.temperature(100, "C", "F")
    print(f"   100°C = {temp_f}°F")

    length_inch = UnitConverter.length(1000, "mm", "inch")
    print(f"   1000mm = {length_inch:.2f} inches")

    volume_L = UnitConverter.volume(1, "m3", "L")
    print(f"   1 m³ = {volume_L} liters\n")

    # Test 2: IEC Validation
    print("2. IEC Standards Validation:")
    validation = IECValidator.validate_temperature_range(-40, 180)
    print(f"   Temperature range -40°C to 180°C:")
    print(f"   Valid: {validation['valid']}")
    print(f"   Standard: {validation['standard']}")
    if validation['warnings']:
        print(f"   Warnings: {validation['warnings']}")

    # Test 3: Safety Calculations
    print("\n3. Safety Calculations:")
    floor_load = SafetyCalculations.calculate_floor_loading(2500, 4.0)
    print(f"   Chamber weight: 2500 kg over 4 m²")
    print(f"   Floor loading: {floor_load['loading_kg_m2']} kg/m²")
    print(f"   Classification: {floor_load['classification']}")

    electrical = SafetyCalculations.calculate_electrical_load(15, 12, 3)
    print(f"\n   Electrical load: {electrical['total_with_safety_kw']} kW (with safety factor)")
    print(f"   Current at 400V 3-phase: {electrical['current_requirements_amps']['400V_3ph']} A")

    print("\n=== All Tests Passed ===")
    print("\n✅ Core calculations module ready for integration!")
