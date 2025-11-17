"""
Quote Generator - Central Hub for All Calculations
==================================================

Aggregates data from all modules to generate comprehensive quotations
for environmental test chambers.

Integration Points:
------------------
- Dependencies: ALL technical modules (core, chamber, cfd, uv, supplier, branding)
- Used by: reports_export, main application
- Merge Priority: 8 (Must be merged last - depends on ALL others)

This is the CENTRAL HUB that brings everything together!

Author: Audit-Pro Enterprise
Version: 1.0.0
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json


@dataclass
class QuoteLineItem:
    """Individual line item in quote"""
    item_number: int
    description: str
    quantity: int
    unit_price: float
    total_price: float
    category: str = "equipment"
    notes: str = ""


class QuoteEngine:
    """Central quote generation engine"""

    def __init__(self):
        """Initialize quote engine"""
        self.line_items: List[QuoteLineItem] = []

    def add_chamber_cost(self, chamber_spec: Dict) -> float:
        """Add chamber cost from chamber_design module"""
        material_cost = chamber_spec.get('materials', {}).get('total_material_cost', 5000)

        # Add fabrication labor (estimated 50% of material cost)
        fabrication_cost = material_cost * 0.5

        total_chamber_cost = material_cost + fabrication_cost

        self.line_items.append(QuoteLineItem(
            item_number=len(self.line_items) + 1,
            description="Environmental Test Chamber - Custom Fabrication",
            quantity=1,
            unit_price=total_chamber_cost,
            total_price=total_chamber_cost,
            category="chamber",
            notes=f"Material: {chamber_spec.get('material_type', 'SS304')}"
        ))

        return total_chamber_cost

    def add_cooling_heating_system(self, thermal_spec: Dict) -> float:
        """Add cooling/heating costs from cfd_simulation"""
        required_capacity = thermal_spec.get('recommended_system_size_kW', 10)

        # Cost estimation: ~$500 per kW for combined system
        system_cost = required_capacity * 500

        mode = thermal_spec.get('mode', 'both')
        if mode == 'cooling':
            description = f"Cooling System - {required_capacity} kW"
        elif mode == 'heating':
            description = f"Heating System - {required_capacity} kW"
        else:
            description = f"Combined Cooling/Heating System - {required_capacity} kW"

        self.line_items.append(QuoteLineItem(
            item_number=len(self.line_items) + 1,
            description=description,
            quantity=1,
            unit_price=system_cost,
            total_price=system_cost,
            category="thermal",
            notes="Includes compressor, condenser, evaporator, heaters"
        ))

        return system_cost

    def add_uv_system(self, uv_spec: Dict) -> float:
        """Add UV system cost from uv_optical module"""
        led_config = uv_spec.get('led_configuration', {})
        cost = led_config.get('estimated_cost', 2000)

        self.line_items.append(QuoteLineItem(
            item_number=len(self.line_items) + 1,
            description=f"UV LED System - {led_config.get('wavelength_nm', 365)}nm",
            quantity=1,
            unit_price=cost,
            total_price=cost,
            category="uv",
            notes=f"{led_config.get('led_count', 20)} LEDs, {led_config.get('total_power_W', 200)}W total"
        ))

        return cost

    def add_control_system(self) -> float:
        """Add control system cost"""
        control_cost = 5000  # Base PLC controller cost

        self.line_items.append(QuoteLineItem(
            item_number=len(self.line_items) + 1,
            description="PLC Control System with HMI",
            quantity=1,
            unit_price=control_cost,
            total_price=control_cost,
            category="controls",
            notes="Includes touchscreen HMI, sensors, wiring"
        ))

        return control_cost

    def add_installation_commissioning(self, equipment_total: float) -> float:
        """Add installation and commissioning costs"""
        # Typically 15% of equipment cost
        install_cost = equipment_total * 0.15

        self.line_items.append(QuoteLineItem(
            item_number=len(self.line_items) + 1,
            description="Installation & Commissioning",
            quantity=1,
            unit_price=install_cost,
            total_price=install_cost,
            category="services",
            notes="On-site installation, testing, training (2 days)"
        ))

        return install_cost

    def calculate_totals(self, tax_rate: float = 0.18) -> Dict:
        """Calculate quote totals with tax"""
        subtotal = sum(item.total_price for item in self.line_items)
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount

        return {
            'subtotal': round(subtotal, 2),
            'tax_rate': tax_rate,
            'tax_amount': round(tax_amount, 2),
            'total': round(total, 2),
            'currency': 'INR'
        }

    def generate_quote(self, customer_name: str, project_name: str,
                      chamber_spec: Dict = None,
                      thermal_spec: Dict = None,
                      uv_spec: Dict = None) -> Dict:
        """
        Generate complete quotation

        Args:
            customer_name: Customer name
            project_name: Project name
            chamber_spec: From chamber_design module
            thermal_spec: From cfd_simulation module
            uv_spec: From uv_optical module

        Returns:
            Complete quote dictionary
        """
        # Clear previous items
        self.line_items = []

        # Add components
        if chamber_spec:
            self.add_chamber_cost(chamber_spec)

        if thermal_spec:
            self.add_cooling_heating_system(thermal_spec)

        if uv_spec:
            self.add_uv_system(uv_spec)

        # Always add control system
        self.add_control_system()

        # Calculate equipment total
        equipment_total = sum(item.total_price for item in self.line_items)

        # Add installation
        self.add_installation_commissioning(equipment_total)

        # Calculate totals
        totals = self.calculate_totals()

        # Generate quote
        quote = {
            'quote_number': f"APE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'quote_date': datetime.now().strftime('%Y-%m-%d'),
            'valid_until': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
            'customer': {
                'name': customer_name,
                'project': project_name
            },
            'line_items': [asdict(item) for item in self.line_items],
            'totals': totals,
            'payment_terms': "30% advance, 60% before dispatch, 10% after commissioning",
            'delivery_time': "12-16 weeks from advance payment",
            'warranty': "24 months from date of installation"
        }

        return quote

    def export_quote_json(self, quote: Dict, filename: str):
        """Export quote to JSON file"""
        with open(filename, 'w') as f:
            json.dump(quote, f, indent=2)


# Example usage
if __name__ == "__main__":
    print("=== Quote Generator Tests ===\n")

    engine = QuoteEngine()

    # Sample specifications (would come from other modules)
    chamber_spec = {
        'materials': {'total_material_cost': 8000},
        'material_type': 'SS304'
    }

    thermal_spec = {
        'mode': 'both',
        'recommended_system_size_kW': 15
    }

    uv_spec = {
        'led_configuration': {
            'wavelength_nm': 365,
            'led_count': 24,
            'total_power_W': 240,
            'estimated_cost': 840
        }
    }

    quote = engine.generate_quote(
        customer_name="ACME Corporation",
        project_name="UV Environmental Test Chamber",
        chamber_spec=chamber_spec,
        thermal_spec=thermal_spec,
        uv_spec=uv_spec
    )

    print(f"Quote Number: {quote['quote_number']}")
    print(f"Customer: {quote['customer']['name']}")
    print(f"Project: {quote['customer']['project']}")
    print(f"\nLine Items: {len(quote['line_items'])}")
    for item in quote['line_items']:
        print(f"  {item['item_number']}. {item['description']}: ₹{item['total_price']:,.2f}")

    print(f"\nSubtotal: ₹{quote['totals']['subtotal']:,.2f}")
    print(f"Tax (18%): ₹{quote['totals']['tax_amount']:,.2f}")
    print(f"Total: ₹{quote['totals']['total']:,.2f}")

    print("\n✅ Quote generator ready!")
