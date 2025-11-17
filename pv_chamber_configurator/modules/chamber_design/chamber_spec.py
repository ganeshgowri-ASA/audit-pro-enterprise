"""
Chamber Design Specification Module
Handles chamber dimensions, materials, loading calculations, and design validation
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class PVModuleSpec:
    """PV Module Specifications"""
    length: float = 3.2  # meters
    width: float = 2.1   # meters
    thickness: float = 0.05  # meters
    weight: float = 62   # kg


@dataclass
class ChamberDimensions:
    """Chamber Internal Dimensions"""
    length: float = 3200  # mm
    width: float = 2100   # mm
    height: float = 2200  # mm


class ChamberDesign:
    """
    Chamber Design and Specification Calculator
    Handles chamber sizing, material selection, and loading validation
    """

    def __init__(self):
        self.dimensions = ChamberDimensions()
        self.pv_module = PVModuleSpec()
        self.capacity = 2  # Number of PV modules

        # Material options
        self.interior_materials = {
            'SS304': {
                'name': 'Stainless Steel 304',
                'corrosion_resistance': 'Good',
                'cost_factor': 1.0,
                'thermal_conductivity': 16.2,  # W/(m·K)
                'description': 'Standard grade, good for most applications'
            },
            'SS316': {
                'name': 'Stainless Steel 316',
                'corrosion_resistance': 'Excellent',
                'cost_factor': 1.35,
                'thermal_conductivity': 16.3,  # W/(m·K)
                'description': 'Superior corrosion resistance, marine grade'
            }
        }

        self.exterior_materials = {
            'Galvanized': {
                'name': 'Galvanized Steel',
                'finish': 'Powder coated RAL 7035',
                'cost_factor': 1.0,
                'description': 'Standard industrial finish'
            }
        }

        # Insulation specifications
        self.insulation = {
            'material': 'PUF (Polyurethane Foam)',
            'thickness_mm': 100,
            'density': 42,  # kg/m³
            'thermal_conductivity': 0.022,  # W/(m·K) at 10°C
            'description': 'High-density, CFC-free, fire retardant'
        }

    def calculate_floor_loading(self) -> Dict:
        """
        Calculate floor loading for chamber with PV modules
        Returns loading in kg/m² and validation status
        """
        # Chamber footprint
        footprint_m2 = (self.dimensions.length / 1000) * (self.dimensions.width / 1000)

        # Total weight
        pv_modules_weight = self.capacity * self.pv_module.weight  # kg
        rack_system_weight = 80  # kg (estimated for extensible sliding rack)
        chamber_structure_weight = 450  # kg (estimated for SS304 construction)

        total_weight = pv_modules_weight + rack_system_weight + chamber_structure_weight

        # Floor loading
        floor_loading = total_weight / footprint_m2

        # Validation (< 400 kg/m²)
        max_allowed = 400  # kg/m²
        is_valid = floor_loading < max_allowed
        safety_margin = ((max_allowed - floor_loading) / max_allowed) * 100

        return {
            'pv_modules_weight_kg': pv_modules_weight,
            'rack_weight_kg': rack_system_weight,
            'structure_weight_kg': chamber_structure_weight,
            'total_weight_kg': total_weight,
            'footprint_m2': footprint_m2,
            'floor_loading_kg_per_m2': floor_loading,
            'max_allowed_kg_per_m2': max_allowed,
            'is_valid': is_valid,
            'safety_margin_percent': safety_margin
        }

    def calculate_total_height(self, with_legs: bool = True) -> Dict:
        """
        Calculate total chamber height including legs/casters
        Validates against <3m constraint
        """
        internal_height = self.dimensions.height  # mm
        wall_thickness = 100  # mm (insulation + SS panels)
        leg_height = 150 if with_legs else 0  # mm

        total_height = internal_height + (2 * wall_thickness) + leg_height
        total_height_m = total_height / 1000

        # Validation (< 3m total)
        max_allowed_m = 3.0
        is_valid = total_height_m < max_allowed_m
        clearance = max_allowed_m - total_height_m

        return {
            'internal_height_mm': internal_height,
            'wall_thickness_mm': wall_thickness,
            'leg_height_mm': leg_height,
            'total_height_mm': total_height,
            'total_height_m': total_height_m,
            'max_allowed_m': max_allowed_m,
            'is_valid': is_valid,
            'clearance_m': clearance
        }

    def get_external_dimensions(self) -> Dict:
        """Calculate external dimensions including insulation"""
        insulation_thickness = self.insulation['thickness_mm']
        wall_thickness = insulation_thickness + 2  # mm (inner + outer panel)

        external_length = self.dimensions.length + (2 * wall_thickness)
        external_width = self.dimensions.width + (2 * wall_thickness)
        external_height = self.dimensions.height + (2 * wall_thickness)

        return {
            'internal_L_W_H_mm': (self.dimensions.length, self.dimensions.width, self.dimensions.height),
            'wall_thickness_mm': wall_thickness,
            'external_L_W_H_mm': (external_length, external_width, external_height),
            'external_L_W_H_m': (external_length/1000, external_width/1000, external_height/1000),
            'volume_m3': (external_length * external_width * external_height) / 1e9
        }

    def design_rack_system(self) -> Dict:
        """
        Design extensible sliding rack system for PV modules
        """
        # Rack specifications
        rack_levels = 2  # Two levels for 2 modules
        rail_material = 'SS304'
        rail_profile = '50x50x3mm square tube'

        # Sliding mechanism
        slide_travel = 800  # mm (80% of width for easy access)
        slide_type = 'Heavy-duty ball bearing slides'
        load_per_slide = self.pv_module.weight / 2  # kg (2 slides per module)

        # Support structure
        support_points = 4  # per module
        load_per_support = self.pv_module.weight / support_points

        return {
            'rack_levels': rack_levels,
            'capacity': self.capacity,
            'rail_material': rail_material,
            'rail_profile': rail_profile,
            'slide_travel_mm': slide_travel,
            'slide_type': slide_type,
            'load_per_slide_kg': load_per_slide,
            'support_points_per_module': support_points,
            'load_per_support_kg': load_per_support,
            'tilting_capability': 'Optional 0-45° adjustment',
            'extension': 'Fully extendable for loading/unloading'
        }

    def design_portholes(self, num_portholes: int = 4) -> List[Dict]:
        """
        Design portholes for external connections (wiring, sensors, cooling)
        """
        porthole_specs = []

        # Standard porthole configurations
        configs = [
            {
                'name': 'Power & Signal',
                'diameter_mm': 100,
                'location': 'Left side wall',
                'purpose': 'DC power cables, sensor wiring',
                'seal_type': 'Silicone grommet with cable glands',
                'rating': 'IP65'
            },
            {
                'name': 'Cooling Water',
                'diameter_mm': 50,
                'location': 'Rear wall',
                'purpose': 'Process cooling water in/out',
                'seal_type': 'Compression fittings',
                'rating': 'IP65'
            },
            {
                'name': 'Exhaust/Vent',
                'diameter_mm': 75,
                'location': 'Top panel',
                'purpose': 'Emergency pressure relief',
                'seal_type': 'Spring-loaded damper',
                'rating': 'IP54'
            },
            {
                'name': 'Service Access',
                'diameter_mm': 150,
                'location': 'Right side wall',
                'purpose': 'Auxiliary connections, maintenance',
                'seal_type': 'Blanking plate with gasket',
                'rating': 'IP65'
            }
        ]

        return configs[:num_portholes]

    def calculate_surface_area(self) -> Dict:
        """Calculate internal surface area for heat transfer calculations"""
        L = self.dimensions.length / 1000  # m
        W = self.dimensions.width / 1000   # m
        H = self.dimensions.height / 1000  # m

        # Surface areas
        floor_area = L * W
        ceiling_area = L * W
        front_back_area = 2 * (L * H)
        side_area = 2 * (W * H)
        total_internal_area = floor_area + ceiling_area + front_back_area + side_area

        return {
            'floor_m2': floor_area,
            'ceiling_m2': ceiling_area,
            'front_back_m2': front_back_area,
            'sides_m2': side_area,
            'total_internal_m2': total_internal_area,
            'volume_m3': L * W * H
        }

    def get_material_cost_estimate(self, interior: str = 'SS304') -> Dict:
        """Estimate material costs based on selection"""
        base_cost = 350000  # INR (base chamber cost with SS304)

        interior_factor = self.interior_materials.get(interior, {}).get('cost_factor', 1.0)
        total_cost = base_cost * interior_factor

        return {
            'interior_material': interior,
            'base_cost_inr': base_cost,
            'cost_factor': interior_factor,
            'total_chamber_cost_inr': total_cost,
            'total_chamber_cost_lakhs': total_cost / 100000
        }

    def get_design_summary(self, interior: str = 'SS304') -> Dict:
        """Get complete chamber design summary"""
        return {
            'dimensions': {
                'internal': self.get_external_dimensions()['internal_L_W_H_mm'],
                'external': self.get_external_dimensions()['external_L_W_H_mm'],
            },
            'materials': {
                'interior': self.interior_materials[interior],
                'exterior': self.exterior_materials['Galvanized'],
                'insulation': self.insulation
            },
            'capacity': {
                'pv_modules': self.capacity,
                'module_size': f"{self.pv_module.length}m x {self.pv_module.width}m x {self.pv_module.thickness}m",
                'module_weight': f"{self.pv_module.weight} kg"
            },
            'loading': self.calculate_floor_loading(),
            'height': self.calculate_total_height(),
            'rack_system': self.design_rack_system(),
            'portholes': self.design_portholes(),
            'surface_area': self.calculate_surface_area(),
            'cost_estimate': self.get_material_cost_estimate(interior)
        }
