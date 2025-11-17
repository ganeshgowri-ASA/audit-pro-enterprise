"""
UV System Design - Optical Calculations & LED Configuration
==========================================================

UV uniformity calculations, spectral analysis, and LED configuration optimization
for environmental test chambers with UV aging capabilities.

Integration Points:
------------------
- Dependencies: engineering_core, chamber_design
- Used by: quote_generator, supplier_manager (LED vendors)
- Merge Priority: 6

Author: Audit-Pro Enterprise
Version: 1.0.0
"""

from typing import Dict, List
from dataclasses import dataclass
import math


@dataclass
class UVLEDSpec:
    """UV LED specifications"""
    wavelength_nm: int  # 340, 365, 385, 405
    power_per_led_W: float
    irradiance_W_m2: float
    viewing_angle_deg: int
    lifespan_hours: int
    cost_per_unit: float


class UVSystemDesigner:
    """UV system design and calculations"""

    # Common UV LED specifications
    LED_SPECS = {
        340: UVLEDSpec(340, 5, 25, 120, 10000, 45.0),
        365: UVLEDSpec(365, 10, 50, 120, 20000, 35.0),
        385: UVLEDSpec(385, 15, 75, 120, 25000, 30.0),
        405: UVLEDSpec(405, 20, 100, 120, 30000, 25.0),
    }

    def __init__(self, test_area_m2: float, target_irradiance: float, wavelength: int = 365):
        """
        Initialize UV system designer

        Args:
            test_area_m2: Test surface area
            target_irradiance: Target irradiance (W/m²)
            wavelength: UV wavelength (nm)
        """
        self.test_area = test_area_m2
        self.target_irradiance = target_irradiance
        self.wavelength = wavelength
        self.led_spec = self.LED_SPECS.get(wavelength, self.LED_SPECS[365])

    def calculate_led_count(self) -> Dict:
        """Calculate required number of LEDs"""
        # Account for uniformity factor (typically 1.5x)
        uniformity_factor = 1.5

        # Calculate required total irradiance
        total_power_required = self.test_area * self.target_irradiance * uniformity_factor

        # Number of LEDs needed
        led_count = math.ceil(total_power_required / self.led_spec.irradiance_W_m2)

        # Calculate actual irradiance achieved
        actual_irradiance = (led_count * self.led_spec.irradiance_W_m2) / (self.test_area * uniformity_factor)

        return {
            'led_count': led_count,
            'target_irradiance_W_m2': self.target_irradiance,
            'actual_irradiance_W_m2': round(actual_irradiance, 2),
            'total_power_W': led_count * self.led_spec.power_per_led_W,
            'wavelength_nm': self.wavelength,
            'estimated_cost': led_count * self.led_spec.cost_per_unit,
            'lifespan_hours': self.led_spec.lifespan_hours
        }

    def calculate_led_array_layout(self, chamber_width: float, chamber_length: float) -> Dict:
        """Calculate optimal LED array layout"""
        led_data = self.calculate_led_count()
        led_count = led_data['led_count']

        # Calculate grid layout
        aspect_ratio = chamber_length / chamber_width
        cols = math.ceil(math.sqrt(led_count / aspect_ratio))
        rows = math.ceil(led_count / cols)

        # Spacing between LEDs
        spacing_length = chamber_length / (cols + 1)
        spacing_width = chamber_width / (rows + 1)

        return {
            'rows': rows,
            'columns': cols,
            'total_leds': rows * cols,
            'spacing_length_m': round(spacing_length, 3),
            'spacing_width_m': round(spacing_width, 3),
            'mounting_height_recommendation_m': 0.5,
            'uniformity_expected': '±10%'
        }

    def calculate_power_requirements(self) -> Dict:
        """Calculate electrical requirements for UV system"""
        led_data = self.calculate_led_count()

        total_power_W = led_data['total_power_W']
        # Add driver losses (10%)
        driver_efficiency = 0.90
        total_power_with_driver = total_power_W / driver_efficiency

        # Calculate current at various voltages
        current_24V = total_power_with_driver / 24
        current_48V = total_power_with_driver / 48

        return {
            'led_power_W': total_power_W,
            'driver_losses_W': round(total_power_with_driver - total_power_W, 2),
            'total_system_power_W': round(total_power_with_driver, 2),
            'current_24V_A': round(current_24V, 2),
            'current_48V_A': round(current_48V, 2),
            'recommended_voltage': '48V DC',
            'power_supply_rating_W': math.ceil(total_power_with_driver * 1.2)  # 20% safety margin
        }

    def generate_uv_system_spec(self, chamber_width: float, chamber_length: float) -> Dict:
        """Generate complete UV system specification"""
        led_count = self.calculate_led_count()
        layout = self.calculate_led_array_layout(chamber_width, chamber_length)
        power = self.calculate_power_requirements()

        return {
            'wavelength_nm': self.wavelength,
            'led_configuration': led_count,
            'array_layout': layout,
            'electrical': power,
            'control_features': {
                'intensity_control': '0-100% PWM dimming',
                'timer_function': 'Programmable on/off cycles',
                'safety_interlock': 'Door-open cutoff',
                'monitoring': 'Real-time irradiance measurement'
            }
        }


# Example usage
if __name__ == "__main__":
    print("=== UV System Design Tests ===\n")

    designer = UVSystemDesigner(test_area_m2=2.0, target_irradiance=50, wavelength=365)

    print("1. LED Count Calculation:")
    led_count = designer.calculate_led_count()
    print(f"   LEDs required: {led_count['led_count']}")
    print(f"   Total power: {led_count['total_power_W']} W")
    print(f"   Estimated cost: ${led_count['estimated_cost']:.2f}")

    print("\n2. Array Layout:")
    layout = designer.calculate_led_array_layout(chamber_width=1.5, chamber_length=2.0)
    print(f"   Grid: {layout['rows']} × {layout['columns']}")
    print(f"   Spacing: {layout['spacing_length_m']}m × {layout['spacing_width_m']}m")

    print("\n✅ UV system module ready!")
