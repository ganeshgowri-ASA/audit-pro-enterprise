# PV Test Equipment Configurator & Quote Generation System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🔬 Overview

Comprehensive **UV+TC+HF+DH Combined Environmental Chamber** configuration and quote generation system for **PV (Photovoltaic) module testing**. This professional-grade application provides end-to-end system design, engineering calculations, cost estimation, and supplier management for environmental test chambers compliant with IEC standards.

### Key Features

- **Chamber Design**: Complete mechanical design with material selection, loading analysis, and dimensional validation
- **CFD Simulation**: Airflow modeling, temperature/humidity distribution, and blower sizing
- **UV Optical System**: Lamp selection, uniformity optimization, and spectral compliance verification
- **Thermal Management**: Refrigeration sizing, heat load analysis, and chiller specifications
- **Quote Generator**: Automated commercial quotations with payment terms and delivery timelines
- **Supplier Database**: Comprehensive database of 50+ Indian suppliers across all component categories
- **3D Visualization**: Interactive chamber views, temperature maps, UV uniformity plots, and airflow patterns
- **Standards Compliance**: Full compliance with IEC 61215, IEC 61730, IEC 60068, IEC 60904-9, ISO 17025

## 📋 Table of Contents

- [System Specifications](#system-specifications)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Core Modules](#core-modules)
- [Usage](#usage)
- [Engineering Calculations](#engineering-calculations)
- [Standards Compliance](#standards-compliance)
- [Supplier Database](#supplier-database)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 System Specifications

### Chamber Design
- **Internal Dimensions**: 3200mm (L) × 2100mm (W) × 2200mm (H)
- **Capacity**: 2 PV modules (3.2m × 2.1m × 0.05m, 62kg each)
- **Materials**: SS304/SS316 interior, galvanized steel exterior
- **Insulation**: 100-120mm PUF (Polyurethane Foam), CFC-free
- **Floor Loading**: <400 kg/m²
- **Total Height**: <3m (including legs)

### Environmental Specifications
- **Temperature Range**: -45°C to +105°C (with UV ON)
- **Temperature Uniformity**: ±2°C (IEC compliant)
- **Humidity Range**: 40-95% RH
- **Humidity Uniformity**: ±3% RH
- **UV Irradiance**: 25-250 W/m², adjustable
- **UV Uniformity**: ±10% (IEC 60904-9)
- **Ramp Rate**: 1.6-3.5°C/min

### UV Specifications
- **Wavelength Range**: 280-400nm
- **UVA Content**: 90-97%
- **UVB Content**: 3-10%
- **Lamp Options**: UV LED, Metal Halide, Fluorescent UVA
- **Measurement Grid**: 24-30 points
- **Spectral Stability**: ±2-7% depending on lamp type

### Refrigeration System
- **Heat Load**: 6.6 kW (typical)
- **Capacity**: 10.3 kW (2.9 TR)
- **Refrigerant**: R449A / R472B
- **Configuration**: Cascade (2-stage)
- **Compressor**: Multi-stage, VFD controlled

### Airflow & CFD
- **Airflow Rate**: 8137 m³/h
- **Air Velocity**: 0.78 m/s
- **Air Changes**: 33 ACH
- **Blower Configuration**: 2× centrifugal (N+1 redundancy)
- **Motor Power**: 1.5 kW each

### DC Power Supply
- **Channels**: Dual
- **Voltage Range**: 0-80V per channel
- **Current Range**: 0-30A per channel
- **Power**: 800W per module
- **Accuracy**: ±0.2% (V & I)
- **Modes**: CV, CI, CP, CR

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ganeshgowri-ASA/audit-pro-enterprise.git
   cd audit-pro-enterprise/pv_chamber_configurator
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv

   # Activate on Windows
   venv\Scripts\activate

   # Activate on Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd ..
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run pv_chamber_configurator/pv_configurator_app.py
   ```

5. **Access the application**
   - Open browser and navigate to: `http://localhost:8501`
   - The application will start with the Home & Overview page

## 📁 Project Structure

```
pv_chamber_configurator/
├── pv_configurator_app.py          # Main Streamlit application
├── README.md                        # This file
│
├── modules/                         # Core calculation modules
│   ├── __init__.py
│   ├── chamber_design/              # Chamber design & specifications
│   │   ├── __init__.py
│   │   └── chamber_spec.py
│   ├── cfd_simulation/              # CFD & airflow analysis
│   │   ├── __init__.py
│   │   └── airflow_sim.py
│   ├── uv_optical/                  # UV lamp system design
│   │   ├── __init__.py
│   │   └── uv_system.py
│   ├── thermal_management/          # Refrigeration & thermal control
│   │   ├── __init__.py
│   │   └── thermal_system.py
│   ├── quote_generator/             # Commercial quote generation
│   │   ├── __init__.py
│   │   └── quote_system.py
│   └── supplier_db/                 # Supplier database
│       ├── __init__.py
│       └── suppliers.py
│
├── visualizations/                  # 3D visualization components
│   ├── __init__.py
│   └── chamber_3d.py
│
├── components/                      # UI components (optional)
│   └── __init__.py
│
├── data/                            # Data storage
│   ├── quotes/                      # Generated quotes
│   ├── reports/                     # PDF reports
│   └── exports/                     # Excel exports
│
└── reports/                         # Report templates
    └── templates/
```

## 🧩 Core Modules

### 1. Chamber Design Module (`chamber_design/`)

**Purpose**: Complete mechanical design and specification

**Features**:
- Internal/external dimension calculations
- Material selection (SS304/SS316)
- Floor loading analysis (<400 kg/m²)
- Height validation (<3m)
- Extensible sliding rack system design
- Porthole specifications for external connections
- Cost estimation

**Classes**:
- `ChamberDesign`: Main design calculator
- `PVModuleSpec`: PV module specifications
- `ChamberDimensions`: Dimension management

### 2. CFD Simulation Module (`cfd_simulation/`)

**Purpose**: Computational fluid dynamics and airflow analysis

**Features**:
- Heat load breakdown (UV, samples, infiltration)
- Required airflow calculation
- Pressure drop analysis
- Blower/fan sizing
- Temperature distribution simulation (27-point grid)
- Humidity distribution simulation (15-point grid)
- IEC compliance verification

**Classes**:
- `CFDSimulation`: CFD calculation engine

**Key Calculations**:
- Airflow: Q = Heat / (ρ × Cp × ΔT)
- Reynolds number, friction factors
- Pressure drop components
- Blower power: P = Q × ΔP / (η × 1000)

### 3. UV Optical System Module (`uv_optical/`)

**Purpose**: UV lamp system design and uniformity optimization

**Features**:
- Lamp database (UV LED, Metal Halide, Fluorescent)
- Lamp count calculation for target irradiance
- Lamp-to-test-plane distance optimization (300-800mm)
- 24-30 point uniformity simulation
- Spectral compliance verification (UVA/UVB)
- Glass specification (solar toughened)
- Lifetime & cost analysis

**Classes**:
- `UVOpticalSystem`: UV system designer
- `LampSpecification`: Lamp data structure

**Lamp Options**:
| Type | Power | Wavelength | UVA/UVB | Lifetime | Cost |
|------|-------|------------|---------|----------|------|
| UV LED | 100W | 280-400nm | 95%/5% | 50000h | ₹1.8L |
| Metal Halide | 400W | 290-400nm | 92%/8% | 5000h | ₹0.45L |
| Fluorescent | 80W | 315-400nm | 97%/3% | 8000h | ₹0.25L |

### 4. Thermal Management Module (`thermal_management/`)

**Purpose**: Refrigeration system design and thermal control

**Features**:
- Heat load analysis (7 components)
- Refrigeration system sizing (cascade configuration)
- Chiller capacity calculation
- Evaporator/condenser sizing
- Process cooling water (PCW) specifications
- Temperature control (Cascade PID)
- Refrigerant selection (R449A/R472B)

**Classes**:
- `ThermalManagement`: Thermal system designer

**Heat Load Components**:
1. PV module power (800W × 2)
2. UV lamps (1600W × 65%)
3. Ambient infiltration (U-value × Area × ΔT)
4. Air circulation fans
5. Humidity system
6. Controls & lighting
7. Door openings

### 5. Quote Generator Module (`quote_generator/`)

**Purpose**: Commercial quotation generation

**Features**:
- Line-item cost breakdown
- GST calculation (18%)
- Payment terms (30-40-30, 40-30-30, 50-50)
- Warranty options (24-60 months)
- Delivery timeline (20-30 weeks)
- Terms & conditions
- Export to Excel/CSV

**Classes**:
- `QuoteGenerator`: Quote generation engine

**Typical Costs** (INR Lakhs):
- Chamber System: ₹35.0
- UV LED Arrays: ₹16.0
- Refrigeration: ₹8.0
- Controls/HMI: ₹7.0
- DC Power Supply: ₹6.0
- Uniformity Robot: ₹12.0
- Water Treatment: ₹6.3
- Installation: ₹5.0
- Calibration: ₹3.5
- **Total: ₹99.8 Lakhs** (approx. $120,000 USD)

### 6. Supplier Database Module (`supplier_db/`)

**Purpose**: Comprehensive India-based supplier management

**Features**:
- 50+ suppliers across 8 categories
- Tier 1/2 classification
- Lead time tracking
- Location mapping
- International competitor comparison
- Search and filter capabilities

**Categories**:
1. UV LEDs (OSRAM, Excelitas, Violumas)
2. Chambers (HIACC, Envisys, Testronix)
3. Refrigeration (Bitzer, Emerson, Danfoss)
4. Controls (Siemens, Schneider, Allen Bradley)
5. Sensors (EKO, Gigahertz Optik, Aplab)
6. Calibration (NPL, CSIR-NAL, TÜV SÜD, SGS)
7. DC Power (Aplab, EDW, Keysight)
8. Water Treatment (Ion Exchange, Thermax)

**Classes**:
- `SupplierDatabase`: Supplier management system

### 7. Visualization Module (`visualizations/`)

**Purpose**: 3D chamber visualization and data plotting

**Features**:
- 3D isometric chamber view
- Temperature distribution heatmaps
- UV uniformity maps
- Airflow vector fields
- Cost breakdown charts
- Project timeline Gantt charts
- Configuration comparison plots

**Classes**:
- `ChamberVisualization`: Plotly-based visualization engine

## 💻 Usage

### Basic Workflow

1. **Home & Overview**
   - Review system specifications
   - Quick configuration
   - Estimated cost preview

2. **Chamber Design**
   - Select interior material (SS304/SS316)
   - Review dimensions and loading
   - Verify height and floor constraints
   - View rack system design

3. **CFD Simulation**
   - Analyze heat load breakdown
   - Review airflow design
   - Check temperature/humidity uniformity
   - Verify IEC compliance

4. **UV Optical System**
   - Select lamp type
   - Set target irradiance (25-250 W/m²)
   - Optimize lamp distance
   - Check uniformity and spectral compliance
   - Review cost analysis

5. **Thermal Management**
   - Set operating conditions
   - Review refrigeration sizing
   - Check chiller specifications
   - Analyze cost breakdown

6. **Quote Generator**
   - Enter customer information
   - Configure system options
   - Generate complete quotation
   - Review payment terms and timeline
   - Download CSV export

7. **Supplier Database**
   - Browse suppliers by category
   - Compare Tier 1 suppliers
   - Review international competitors
   - Export supplier lists

8. **3D Visualization**
   - View 3D chamber model
   - Explore temperature/UV maps
   - Analyze airflow patterns
   - Generate presentation graphics

9. **Reports & Export**
   - Generate PDF technical reports
   - Export Excel quotations
   - Download specifications
   - Create installation manuals

### Example Configuration

```python
# Example: Configure and generate quote

from modules.chamber_design import ChamberDesign
from modules.uv_optical import UVOpticalSystem
from modules.quote_generator import QuoteGenerator

# 1. Design chamber
chamber = ChamberDesign()
design_summary = chamber.get_design_summary('SS304')

# 2. Configure UV system
uv_system = UVOpticalSystem()
uv_summary = uv_system.get_uv_system_summary('UV_LED', 60)

# 3. Generate quote
quote_gen = QuoteGenerator()
quote = quote_gen.generate_complete_quote(
    customer_name="ABC Solar Pvt Ltd",
    customer_address="Bangalore, India",
    options={'interior_material': 'SS304', 'uv_lamp_type': 'UV_LED'},
    payment_schedule='30-40-30',
    warranty_months=24
)

# 4. Export
quote_df = quote_gen.export_quote_to_dict(quote)
quote_df.to_excel('quote.xlsx')
```

## 🔬 Engineering Calculations

### Key Formulas

#### 1. Airflow Calculation
```
Q = Heat Load / (ρ × Cp × ΔT)

Where:
- Q = Airflow (m³/s)
- Heat Load = Total heat load (W)
- ρ = Air density (1.2 kg/m³)
- Cp = Specific heat (1005 J/kg·K)
- ΔT = Temperature rise (8°C)
```

#### 2. Refrigeration Capacity
```
Capacity (TR) = Heat Load (kW) / 3.517

COP = Cooling Capacity / Compressor Power
```

#### 3. UV Uniformity
```
Non-uniformity (%) = ((Imax - Imin) / Imean) × 100

IEC Requirement: ≤ 10%
```

#### 4. Floor Loading
```
Floor Loading (kg/m²) = Total Weight (kg) / Footprint (m²)

Constraint: < 400 kg/m²
```

#### 5. Heat Transfer
```
Q = U × A × ΔT

Where:
- Q = Heat transfer (W)
- U = U-value (0.22 W/m²·K for 100mm PUF)
- A = Surface area (m²)
- ΔT = Temperature difference (°C)
```

## 📜 Standards Compliance

### IEC 61215 - PV Module Design Qualification
- **UV Test (MQT 10.10)**: UV60 (60 kWh/m²), UV180 (180 kWh/m²)
- **Thermal Cycling (MQT 10.11)**: TC200 (200 cycles), TC600 (600 cycles)
- **Damp Heat (MQT 10.12)**: DH1000 (1000h at 85°C/85%RH), DH2000 (2000h)
- **Temperature Cycling**: -40°C to +85°C

### IEC 61730 - PV Module Safety Qualification
- **UV Conditioning**: UV15 (15 kWh/m²)
- **Thermal Cycling**: 50 cycles
- **Humidity-Freeze**: -40°C to +85°C with 85%RH

### IEC 60068 - Environmental Testing
- **Part 2-1**: Cold test (-45°C)
- **Part 2-2**: Dry heat test (+105°C)
- **Part 2-30**: Damp heat cyclic (85°C/85%RH)
- **Part 3-5**: Temperature test chamber performance
- **Part 3-6**: Humidity test chamber performance

### IEC 60904-9 - Solar Simulator Standards
- **Classification**: A (uniformity ≤2%), B (≤5%), C (≤10%)
- **Irradiance**: 1000 W/m² (AM1.5G) for solar simulation
- **UV Irradiance**: 25-250 W/m² for UV-only testing
- **Measurement Grid**: Minimum 24 points

### ISO 17025 - Testing and Calibration
- **Temperature**: NABL-traceable RTD calibration, ±0.1°C
- **Humidity**: NABL-traceable hygrometer, ±2%RH
- **UV**: NABL-traceable radiometer, ±3%
- **Calibration Frequency**: Annual

## 🏭 Supplier Database

### Indian Suppliers (50+ companies)

**UV LEDs & Lamps**:
- OSRAM Opto Semiconductors (Bangalore) - Tier 1 Premium
- Excelitas Technologies (Pune) - Tier 1 Premium
- Violumas/Crystal IS (Mumbai) - Tier 1 Specialized

**Environmental Chambers**:
- HIACC Environmental (Chennai) - Tier 1 Local Leader
- Envisys Technologies (Hyderabad) - Tier 1
- Testronix Instruments (Delhi) - Tier 2

**Refrigeration**:
- Bitzer India (Pune) - Tier 1 Premium
- Emerson Climate Technologies (Pune) - Tier 1 Premium
- Danfoss India (Chennai) - Tier 1

**Controls & Automation**:
- Siemens India - Tier 1 Premium (PLC, HMI, Drives)
- Schneider Electric India - Tier 1
- Allen Bradley/Rockwell - Tier 1 Premium

**Calibration Labs (NABL Accredited)**:
- National Physical Laboratory (NPL) - Delhi
- CSIR-NAL - Bangalore
- TÜV SÜD South Asia - Multiple locations
- SGS India - Multiple locations

### International Competitors

| Company | Country | Cost Premium | Delivery |
|---------|---------|--------------|----------|
| ATT | Italy | +40-50% | 28 weeks |
| CME | Germany | +50-60% | 32 weeks |
| Arvispec | Spain | +35-45% | 24 weeks |
| UFE | Singapore | +25-35% | 20 weeks |
| Stech | China | -10 to +10% | 16 weeks |

**Local Advantages**:
- 20-50% cost savings
- 40-50% faster delivery
- On-site support
- No forex risk
- Easy customization

## 📊 Technical Data

### Sensor Specifications

| Parameter | Sensor Type | Quantity | Accuracy | Location |
|-----------|-------------|----------|----------|----------|
| Temperature | RTD Pt100 Class A | 27 | ±0.1°C | Chamber grid |
| Humidity | Capacitive | 15 | ±2%RH | Chamber grid |
| UV Irradiance | Si Photodiode | 48 | ±3% | Test plane |
| Pressure | Piezoresistive | 4 | ±0.5% | Refrigeration |
| Airflow | Hot wire | 2 | ±3% | Ductwork |

### Electrical Specifications

| System | Voltage | Current | Power | Phase |
|--------|---------|---------|-------|-------|
| Main Supply | 415V | 50A | 35kW | 3-Ph |
| UV Lamps | 220V | 15A | 3.3kW | 1-Ph |
| Refrigeration | 415V | 25A | 18kW | 3-Ph |
| Controls | 230V | 5A | 1.2kW | 1-Ph |
| DC Power | 80V | 30A | 4.8kW | DC |

## 🛠️ Maintenance

### Regular Maintenance Schedule

**Weekly**:
- Visual inspection
- Check alarms and indicators
- Record calibration readings

**Monthly**:
- Clean filters
- Check UV lamp intensity
- Inspect door seals
- Test safety interlocks

**Quarterly**:
- Clean UV lamps and reflectors
- Check refrigerant levels
- Inspect electrical connections
- Verify temperature/humidity uniformity

**Annual**:
- NABL calibration (Temperature, Humidity, UV)
- Replace filters
- Deep clean chamber interior
- Check refrigeration system
- Verify all safety systems

**Every 2-3 Years**:
- Replace UV lamps (depending on type)
- Major refrigeration service
- PLC battery replacement

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Contact: [Your contact email]

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- CFD calculations powered by [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/)
- Visualizations by [Plotly](https://plotly.com/)
- Data management with [Pandas](https://pandas.pydata.org/)
- PDF reports via [ReportLab](https://www.reportlab.com/)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-17
**Status**: Production Ready
**Developed for**: PV Testing Industry, India
