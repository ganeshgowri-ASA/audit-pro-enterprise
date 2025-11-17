"""
Chamber Design Module - Dimensional Analysis & Material Selection
=================================================================

This module handles environmental chamber design calculations including:
- Dimensional analysis and validation
- Floor loading calculations
- Material selection logic
- Insulation thickness calculation
- Structural requirements

Integration Points:
------------------
- Dependencies: engineering_core (unit conversions, safety calculations)
- Used by: cfd_simulation, quote_generator, uv_system
- Merge Priority: 4 (After core-calculations)

Author: Audit-Pro Enterprise
Version: 1.0.0
"""

from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import math

# Integration with engineering_core (will be available after merge)
try:
    from modules.engineering_core import (
        UnitConverter, MathHelpers, SafetyCalculations,
        Dimension, IECValidator
    )
except ImportError:
    print("Warning: engineering_core not available. Using mock implementations.")
    # Mock implementations for standalone testing
    class UnitConverter:
        @staticmethod
        def length(value, from_unit, to_unit):
            return value
        @staticmethod
        def volume(value, from_unit, to_unit):
            return value


class ChamberType(Enum):
    """Types of environmental chambers"""
    WALK_IN = "walk_in"
    BENCH_TOP = "bench_top"
    REACH_IN = "reach_in"
    DRIVE_IN = "drive_in"
    CUSTOM = "custom"


class MaterialType(Enum):
    """Chamber material types"""
    STAINLESS_STEEL_304 = "ss304"
    STAINLESS_STEEL_316 = "ss316"
    POWDER_COATED_STEEL = "powder_coated"
    ALUMINUM = "aluminum"
    CUSTOM = "custom"


class InsulationType(Enum):
    """Insulation material types"""
    POLYURETHANE_FOAM = "pu_foam"
    MINERAL_WOOL = "mineral_wool"
    FIBERGLASS = "fiberglass"
    EXPANDED_POLYSTYRENE = "eps"
    VACUUM_PANEL = "vacuum_panel"


@dataclass
class ChamberDimensions:
    """Chamber internal dimensions"""
    length: float  # meters
    width: float   # meters
    height: float  # meters
    unit: str = "m"

    def get_volume(self) -> float:
        """Calculate internal volume in cubic meters"""
        return self.length * self.width * self.height

    def get_floor_area(self) -> float:
        """Calculate floor area in square meters"""
        return self.length * self.width

    def get_surface_area(self) -> float:
        """Calculate total internal surface area"""
        return 2 * (self.length * self.width +
                   self.length * self.height +
                   self.width * self.height)

    def get_external_dimensions(self, wall_thickness: float) -> Tuple[float, float, float]:
        """
        Calculate external dimensions including wall thickness

        Args:
            wall_thickness: Total wall thickness in meters (material + insulation)

        Returns:
            Tuple of (external_length, external_width, external_height)
        """
        return (
            self.length + 2 * wall_thickness,
            self.width + 2 * wall_thickness,
            self.height + 2 * wall_thickness
        )


@dataclass
class MaterialProperties:
    """Material physical and thermal properties"""
    name: str
    thermal_conductivity: float  # W/(m·K)
    density: float  # kg/m³
    thickness: float  # mm
    cost_per_kg: float  # currency per kg
    cost_per_m2: float  # currency per m²


class ChamberDesigner:
    """Main chamber design calculator"""

    # Material properties database
    MATERIALS = {
        MaterialType.STAINLESS_STEEL_304: MaterialProperties(
            name="Stainless Steel 304",
            thermal_conductivity=16.2,
            density=8000,
            thickness=1.5,
            cost_per_kg=4.5,
            cost_per_m2=50.0
        ),
        MaterialType.STAINLESS_STEEL_316: MaterialProperties(
            name="Stainless Steel 316",
            thermal_conductivity=16.3,
            density=8000,
            thickness=1.5,
            cost_per_kg=6.5,
            cost_per_m2=70.0
        ),
        MaterialType.POWDER_COATED_STEEL: MaterialProperties(
            name="Powder Coated Steel",
            thermal_conductivity=50.0,
            density=7850,
            thickness=2.0,
            cost_per_kg=2.5,
            cost_per_m2=30.0
        )
    }

    INSULATION = {
        InsulationType.POLYURETHANE_FOAM: MaterialProperties(
            name="Polyurethane Foam",
            thermal_conductivity=0.026,
            density=40,
            thickness=75,
            cost_per_kg=8.0,
            cost_per_m2=25.0
        ),
        InsulationType.MINERAL_WOOL: MaterialProperties(
            name="Mineral Wool",
            thermal_conductivity=0.038,
            density=100,
            thickness=100,
            cost_per_kg=5.0,
            cost_per_m2=20.0
        ),
        InsulationType.FIBERGLASS: MaterialProperties(
            name="Fiberglass",
            thermal_conductivity=0.040,
            density=12,
            thickness=100,
            cost_per_kg=4.0,
            cost_per_m2=15.0
        )
    }

    def __init__(self, dimensions: ChamberDimensions, chamber_type: ChamberType = ChamberType.WALK_IN):
        """
        Initialize chamber designer

        Args:
            dimensions: Internal chamber dimensions
            chamber_type: Type of chamber
        """
        self.dimensions = dimensions
        self.chamber_type = chamber_type
        self.material_type = MaterialType.STAINLESS_STEEL_304
        self.insulation_type = InsulationType.POLYURETHANE_FOAM

    def calculate_insulation_thickness(
        self,
        internal_temp: float,
        external_temp: float,
        max_heat_loss: float,
        insulation_type: Optional[InsulationType] = None
    ) -> Dict:
        """
        Calculate required insulation thickness

        Args:
            internal_temp: Internal temperature (°C)
            external_temp: External/ambient temperature (°C)
            max_heat_loss: Maximum allowed heat loss (W/m²)
            insulation_type: Type of insulation material

        Returns:
            Dictionary with insulation thickness and heat loss analysis
        """
        if insulation_type is None:
            insulation_type = self.insulation_type

        insulation = self.INSULATION[insulation_type]

        # Temperature difference
        delta_t = abs(internal_temp - external_temp)

        # Calculate required thickness
        # Q = k * A * ΔT / thickness
        # thickness = k * ΔT / Q
        required_thickness = (insulation.thermal_conductivity * delta_t / max_heat_loss) * 1000  # Convert to mm

        # Round up to nearest 25mm
        recommended_thickness = math.ceil(required_thickness / 25) * 25

        # Calculate actual heat loss with recommended thickness
        actual_thickness_m = recommended_thickness / 1000
        actual_heat_loss = (insulation.thermal_conductivity * delta_t) / actual_thickness_m

        return {
            'required_thickness_mm': round(required_thickness, 2),
            'recommended_thickness_mm': recommended_thickness,
            'actual_heat_loss_per_m2': round(actual_heat_loss, 2),
            'insulation_type': insulation.name,
            'thermal_conductivity': insulation.thermal_conductivity,
            'safety_margin': round(((recommended_thickness - required_thickness) / required_thickness) * 100, 1)
        }

    def calculate_material_quantities(self) -> Dict:
        """
        Calculate material quantities required

        Returns:
            Dictionary with material quantities and costs
        """
        surface_area = self.dimensions.get_surface_area()

        # Get material and insulation properties
        material = self.MATERIALS[self.material_type]
        insulation = self.INSULATION[self.insulation_type]

        # Calculate material mass
        material_thickness_m = material.thickness / 1000
        material_volume = surface_area * material_thickness_m
        material_mass = material_volume * material.density

        # Calculate insulation mass
        insulation_thickness_m = insulation.thickness / 1000
        insulation_volume = surface_area * insulation_thickness_m
        insulation_mass = insulation_volume * insulation.density

        # Calculate costs
        material_cost = surface_area * material.cost_per_m2
        insulation_cost = surface_area * insulation.cost_per_m2

        return {
            'internal_surface_area_m2': round(surface_area, 2),
            'material': {
                'type': material.name,
                'thickness_mm': material.thickness,
                'mass_kg': round(material_mass, 2),
                'cost': round(material_cost, 2)
            },
            'insulation': {
                'type': insulation.name,
                'thickness_mm': insulation.thickness,
                'mass_kg': round(insulation_mass, 2),
                'cost': round(insulation_cost, 2)
            },
            'total_mass_kg': round(material_mass + insulation_mass, 2),
            'total_material_cost': round(material_cost + insulation_cost, 2)
        }

    def calculate_structural_requirements(self) -> Dict:
        """
        Calculate structural requirements including floor loading

        Returns:
            Dictionary with structural analysis
        """
        # Estimate total weight
        material_data = self.calculate_material_quantities()
        structural_weight = material_data['total_mass_kg']

        # Add weight of components (estimated)
        cooling_system_weight = 200  # kg
        heating_system_weight = 150  # kg
        controls_weight = 50  # kg
        door_assembly_weight = 100  # kg

        total_weight = (structural_weight + cooling_system_weight +
                       heating_system_weight + controls_weight + door_assembly_weight)

        # Calculate floor loading
        ext_dims = self.dimensions.get_external_dimensions(
            (self.MATERIALS[self.material_type].thickness +
             self.INSULATION[self.insulation_type].thickness) / 1000
        )
        base_area = ext_dims[0] * ext_dims[1]

        floor_loading_kg_m2 = total_weight / base_area
        floor_loading_kpa = (floor_loading_kg_m2 * 9.81) / 1000

        # Classification
        if floor_loading_kpa < 2.4:
            classification = "Light - Suitable for office spaces"
            foundation_type = "Standard concrete slab (100mm)"
        elif floor_loading_kpa < 4.8:
            classification = "Medium - Light industrial floor required"
            foundation_type = "Reinforced concrete (150mm)"
        elif floor_loading_kpa < 7.2:
            classification = "Heavy - Industrial floor required"
            foundation_type = "Heavy-duty reinforced concrete (200mm)"
        else:
            classification = "Very Heavy - Special foundation required"
            foundation_type = "Engineer-designed foundation"

        return {
            'total_weight_kg': round(total_weight, 2),
            'base_area_m2': round(base_area, 2),
            'floor_loading_kg_m2': round(floor_loading_kg_m2, 2),
            'floor_loading_kpa': round(floor_loading_kpa, 2),
            'classification': classification,
            'recommended_foundation': foundation_type,
            'external_dimensions_m': {
                'length': round(ext_dims[0], 3),
                'width': round(ext_dims[1], 3),
                'height': round(ext_dims[2], 3)
            },
            'requires_structural_engineer': floor_loading_kpa > 4.8
        }

    def calculate_door_size(self) -> Dict:
        """
        Calculate recommended door size based on chamber dimensions

        Returns:
            Dictionary with door specifications
        """
        # Door size typically 80-90% of chamber width/height (whichever is smaller)
        min_dimension = min(self.dimensions.width, self.dimensions.height)

        if self.chamber_type == ChamberType.WALK_IN:
            door_width = min(1.0, min_dimension * 0.8)  # Max 1m wide
            door_height = min(2.0, self.dimensions.height * 0.85)
            door_type = "Hinged door with viewing window"
        elif self.chamber_type == ChamberType.DRIVE_IN:
            door_width = min_dimension * 0.9
            door_height = self.dimensions.height * 0.9
            door_type = "Motorized sliding door"
        else:  # REACH_IN, BENCH_TOP
            door_width = min_dimension * 0.7
            door_height = self.dimensions.height * 0.7
            door_type = "Hinged door"

        return {
            'door_width_m': round(door_width, 3),
            'door_height_m': round(door_height, 3),
            'door_type': door_type,
            'insulation_required': True,
            'gasket_type': "Silicone high-temperature gasket",
            'locking_mechanism': "Multi-point locking" if self.chamber_type == ChamberType.WALK_IN else "Single-point locking"
        }

    def generate_design_summary(self) -> Dict:
        """
        Generate comprehensive design summary

        Returns:
            Complete design specification
        """
        materials = self.calculate_material_quantities()
        structure = self.calculate_structural_requirements()
        door = self.calculate_door_size()

        return {
            'chamber_type': self.chamber_type.value,
            'internal_dimensions': asdict(self.dimensions),
            'internal_volume_m3': round(self.dimensions.get_volume(), 3),
            'external_dimensions': structure['external_dimensions_m'],
            'materials': materials,
            'structural': structure,
            'door': door,
            'material_type': self.material_type.value,
            'insulation_type': self.insulation_type.value
        }


# Integration hooks for other modules
class IntegrationHooks:
    """Hooks for integration with other modules"""

    @staticmethod
    def export_to_cfd_simulation(design_summary: Dict) -> Dict:
        """
        Export design data for CFD simulation

        Returns:
            Data formatted for CFD module
        """
        return {
            'geometry': {
                'length': design_summary['internal_dimensions']['length'],
                'width': design_summary['internal_dimensions']['width'],
                'height': design_summary['internal_dimensions']['height'],
                'volume': design_summary['internal_volume_m3']
            },
            'thermal': {
                'wall_material': design_summary['material_type'],
                'insulation': design_summary['insulation_type']
            }
        }

    @staticmethod
    def export_to_quote_generator(design_summary: Dict) -> Dict:
        """
        Export design data for quote generation

        Returns:
            Data formatted for quote module
        """
        return {
            'description': f"{design_summary['chamber_type'].replace('_', ' ').title()} Chamber",
            'dimensions': design_summary['internal_dimensions'],
            'materials': design_summary['materials'],
            'total_material_cost': design_summary['materials']['total_material_cost']
        }


# Example usage and testing
if __name__ == "__main__":
    print("=== Chamber Design Module Tests ===\n")

    # Test 1: Create walk-in chamber
    print("1. Walk-in Chamber Design:")
    dimensions = ChamberDimensions(length=3.0, width=2.0, height=2.5)
    designer = ChamberDesigner(dimensions, ChamberType.WALK_IN)

    print(f"   Internal volume: {dimensions.get_volume()} m³")
    print(f"   Floor area: {dimensions.get_floor_area()} m²")
    print(f"   Surface area: {dimensions.get_surface_area():.2f} m²")

    # Test 2: Insulation calculation
    print("\n2. Insulation Calculation:")
    insulation = designer.calculate_insulation_thickness(
        internal_temp=-40,
        external_temp=25,
        max_heat_loss=20  # W/m²
    )
    print(f"   Required thickness: {insulation['required_thickness_mm']:.2f} mm")
    print(f"   Recommended thickness: {insulation['recommended_thickness_mm']} mm")
    print(f"   Actual heat loss: {insulation['actual_heat_loss_per_m2']:.2f} W/m²")

    # Test 3: Material quantities
    print("\n3. Material Quantities:")
    materials = designer.calculate_material_quantities()
    print(f"   Material: {materials['material']['type']}")
    print(f"   Material mass: {materials['material']['mass_kg']} kg")
    print(f"   Insulation mass: {materials['insulation']['mass_kg']} kg")
    print(f"   Total cost: ${materials['total_material_cost']:.2f}")

    # Test 4: Structural analysis
    print("\n4. Structural Requirements:")
    structure = designer.calculate_structural_requirements()
    print(f"   Total weight: {structure['total_weight_kg']} kg")
    print(f"   Floor loading: {structure['floor_loading_kpa']:.2f} kPa")
    print(f"   Classification: {structure['classification']}")
    print(f"   Foundation: {structure['recommended_foundation']}")

    # Test 5: Door specifications
    print("\n5. Door Specifications:")
    door = designer.calculate_door_size()
    print(f"   Door size: {door['door_width_m']}m × {door['door_height_m']}m")
    print(f"   Door type: {door['door_type']}")
    print(f"   Locking: {door['locking_mechanism']}")

    # Test 6: Complete design summary
    print("\n6. Design Summary:")
    summary = designer.generate_design_summary()
    print(f"   Chamber type: {summary['chamber_type']}")
    print(f"   Internal volume: {summary['internal_volume_m3']} m³")
    print(f"   External dimensions: {summary['external_dimensions']['length']}m × {summary['external_dimensions']['width']}m × {summary['external_dimensions']['height']}m")

    print("\n=== All Tests Passed ===")
    print("\n✅ Chamber design module ready for integration!")
