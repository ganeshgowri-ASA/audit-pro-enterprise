# Engineering Core Module - Integration Guide

## Overview
The `engineering_core.py` module is the **foundation** for all calculation modules in the Audit-Pro-Enterprise system. It must be merged to `main` **FIRST** before any other technical modules.

## What This Module Provides

### 1. Unit Conversion System
```python
from modules.engineering_core import UnitConverter

# Temperature conversions
temp_f = UnitConverter.temperature(25, "C", "F")  # 77°F

# Length conversions
length_m = UnitConverter.length(1000, "mm", "m")  # 1.0 m

# Volume, pressure, power conversions
volume_L = UnitConverter.volume(1, "m3", "L")  # 1000 L
pressure_psi = UnitConverter.pressure(1, "bar", "psi")  # 14.5 psi
power_hp = UnitConverter.power(1, "kW", "hp")  # 1.34 hp
```

### 2. IEC Standards Validation
```python
from modules.engineering_core import IECValidator, IECStandard

# Validate temperature range against IEC standards
result = IECValidator.validate_temperature_range(
    min_temp=-40,
    max_temp=180,
    standard=IECStandard.IEC_60068_2_38
)

if result['valid']:
    print("✅ Compliant with IEC 60068-2-38")
else:
    print(f"⚠️ Warnings: {result['warnings']}")
```

### 3. Mathematical Helpers
```python
from modules.engineering_core import MathHelpers

# Calculate air changes per hour
ach = MathHelpers.calculate_air_changes_per_hour(
    airflow_m3_per_min=50,
    chamber_volume_m3=10
)

# Calculate Reynolds number for airflow analysis
re = MathHelpers.calculate_reynolds_number(
    velocity=2.5,  # m/s
    characteristic_length=1.0  # m
)

# Heat transfer coefficient estimation
h = MathHelpers.calculate_heat_transfer_coefficient(
    velocity=2.5,
    characteristic_length=1.0
)
```

### 4. Safety Calculations
```python
from modules.engineering_core import SafetyCalculations

# Floor loading calculations
floor_load = SafetyCalculations.calculate_floor_loading(
    total_weight_kg=2500,
    base_area_m2=4.0
)
print(f"Floor loading: {floor_load['loading_kg_m2']} kg/m²")
print(f"Classification: {floor_load['classification']}")

# Electrical load calculations
electrical = SafetyCalculations.calculate_electrical_load(
    heating_power_kw=15,
    cooling_power_kw=12,
    humidifier_power_kw=3
)
print(f"Total load: {electrical['total_with_safety_kw']} kW")
print(f"Current @ 400V: {electrical['current_requirements_amps']['400V_3ph']} A")
```

## Integration Points

### Modules That Depend on This:
1. ✅ **chamber_design** - Uses unit conversions and dimensional calculations
2. ✅ **cfd_simulation** - Uses Reynolds number, heat transfer, ACH calculations
3. ✅ **uv_system** - Uses unit conversions and mathematical helpers
4. ✅ **quote_generator** - Uses all calculation utilities for validation
5. ✅ **virtual_hmi** - Uses IEC validation and safety calculations

### How to Import:
```python
# In other modules after this is merged to main
from modules.engineering_core import (
    UnitConverter,
    IECValidator,
    IECStandard,
    MathHelpers,
    SafetyCalculations,
    Temperature,
    Dimension
)
```

## Testing
Run the module directly to execute built-in tests:
```bash
python modules/engineering_core.py
```

Expected output:
```
=== Engineering Core Module Tests ===

1. Unit Conversion Tests:
   100°C = 212.0°F
   1000mm = 39.37 inches
   1 m³ = 1000.0 liters

2. IEC Standards Validation:
   Temperature range -40°C to 180°C:
   Valid: True
   Standard: IEC 60068-2-38

3. Safety Calculations:
   Chamber weight: 2500 kg over 4 m²
   Floor loading: 625.0 kg/m²
   Classification: Medium load - Suitable for light industrial

   Electrical load: 37.5 kW (with safety factor)
   Current at 400V 3-phase: 55.45 A

=== All Tests Passed ===
```

## Merge Requirements

### Prerequisites:
- None (Foundation module)

### Merge Order:
- **Priority: 1** (Merge this FIRST)

### After Merging:
The following branches can proceed:
- `feature/chamber-design`
- `feature/cfd-simulation`
- `feature/uv-system`
- `feature/quote-generator`

## Future Extensions

### Planned Enhancements:
1. **Material Properties Database**
   - Thermal conductivity tables
   - Specific heat capacity data
   - Density values for common materials

2. **Advanced Fluid Dynamics**
   - Turbulence models
   - Buoyancy calculations
   - Stratification analysis

3. **Energy Efficiency Metrics**
   - COP (Coefficient of Performance) calculations
   - Energy consumption predictions
   - Carbon footprint estimation

4. **Multi-Standard Support**
   - ASTM standards
   - MIL-STD specifications
   - Custom test profiles

### Extension Points:
```python
# Add new conversion types
class UnitConverter:
    @staticmethod
    def energy(value, from_unit, to_unit):
        # Implementation for Joules, BTU, kWh, etc.
        pass

# Add new validators
class StandardValidator:
    @staticmethod
    def validate_astm_compliance(...):
        # ASTM standard validation
        pass
```

## API Stability
- ✅ All public methods in this module are considered **STABLE**
- ✅ Breaking changes will require major version bump
- ✅ New features will be added as new methods (non-breaking)

## Support
For integration questions or issues:
1. Check this documentation
2. Review inline docstrings in `engineering_core.py`
3. Run built-in tests for examples
4. Contact: Audit-Pro Enterprise Development Team

---

**Version:** 1.0.0
**Status:** Ready for Production
**Last Updated:** 2025-11-17
