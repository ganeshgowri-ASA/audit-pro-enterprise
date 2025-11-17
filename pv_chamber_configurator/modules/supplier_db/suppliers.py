"""
Supplier Database for India
Comprehensive list of suppliers for PV chamber components
"""

from typing import Dict, List
import pandas as pd


class SupplierDatabase:
    """
    Database of Indian suppliers for PV chamber components
    """

    def __init__(self):
        self.suppliers = self._initialize_supplier_database()

    def _initialize_supplier_database(self) -> Dict:
        """Initialize comprehensive supplier database"""
        return {
            'UV_LEDs': [
                {
                    'company': 'OSRAM Opto Semiconductors India',
                    'location': 'Bangalore, Karnataka',
                    'products': 'UV LED chips, modules, arrays',
                    'wavelength_range': '280-400nm',
                    'contact': 'www.osram.in',
                    'rating': 'Tier 1 - Premium',
                    'lead_time_weeks': 8,
                    'min_order_value': '₹5 Lakhs'
                },
                {
                    'company': 'Excelitas Technologies India',
                    'location': 'Pune, Maharashtra',
                    'products': 'UV LEDs, UV sensors, photodetectors',
                    'wavelength_range': '250-400nm',
                    'contact': 'www.excelitas.com',
                    'rating': 'Tier 1 - Premium',
                    'lead_time_weeks': 6,
                    'min_order_value': '₹3 Lakhs'
                },
                {
                    'company': 'Violumas (Crystal IS distributor)',
                    'location': 'Mumbai, Maharashtra',
                    'products': 'Deep UV LEDs, UVB/UVC modules',
                    'wavelength_range': '255-310nm',
                    'contact': 'info@violumas.com',
                    'rating': 'Tier 1 - Specialized',
                    'lead_time_weeks': 10,
                    'min_order_value': '₹8 Lakhs'
                }
            ],
            'Chambers': [
                {
                    'company': 'HIACC Environmental Chambers',
                    'location': 'Chennai, Tamil Nadu',
                    'products': 'Custom environmental chambers, temperature/humidity chambers',
                    'specialization': 'IEC certified chambers, automotive',
                    'contact': 'www.hiacc.in',
                    'rating': 'Tier 1 - Local Leader',
                    'lead_time_weeks': 12,
                    'typical_capacity': 'Up to 10m³'
                },
                {
                    'company': 'Envisys Technologies',
                    'location': 'Hyderabad, Telangana',
                    'products': 'Environmental test chambers, thermal shock chambers',
                    'specialization': 'Electronics, defense',
                    'contact': 'www.envisystech.com',
                    'rating': 'Tier 1',
                    'lead_time_weeks': 14,
                    'typical_capacity': 'Up to 15m³'
                },
                {
                    'company': 'Testronix Instruments',
                    'location': 'New Delhi',
                    'products': 'Walk-in chambers, stability chambers',
                    'specialization': 'Pharma, packaging',
                    'contact': 'www.testronixinstruments.com',
                    'rating': 'Tier 2',
                    'lead_time_weeks': 10,
                    'typical_capacity': 'Up to 20m³'
                }
            ],
            'Refrigeration': [
                {
                    'company': 'Bitzer India Pvt Ltd',
                    'location': 'Pune, Maharashtra',
                    'products': 'Compressors (reciprocating, screw, scroll)',
                    'refrigerants': 'R404A, R449A, R452A',
                    'contact': 'www.bitzer.in',
                    'rating': 'Tier 1 - Premium',
                    'lead_time_weeks': 4,
                    'support': 'Nationwide service network'
                },
                {
                    'company': 'Emerson Climate Technologies India',
                    'location': 'Pune, Maharashtra',
                    'products': 'Copeland compressors, controls, condensing units',
                    'refrigerants': 'R404A, R449A, R452A, R472B',
                    'contact': 'www.emerson.com',
                    'rating': 'Tier 1 - Premium',
                    'lead_time_weeks': 3,
                    'support': 'Excellent technical support'
                },
                {
                    'company': 'Danfoss India',
                    'location': 'Chennai, Tamil Nadu',
                    'products': 'Compressors, expansion valves, controls',
                    'refrigerants': 'All major refrigerants',
                    'contact': 'www.danfoss.com',
                    'rating': 'Tier 1',
                    'lead_time_weeks': 4,
                    'support': 'Good spare parts availability'
                }
            ],
            'Controls_Automation': [
                {
                    'company': 'Siemens India',
                    'location': 'Multiple locations',
                    'products': 'PLCs, HMIs, drives, sensors',
                    'platforms': 'Simatic S7-1200/1500, WinCC',
                    'contact': 'www.siemens.co.in',
                    'rating': 'Tier 1 - Premium',
                    'lead_time_weeks': 6,
                    'support': 'Excellent, nationwide'
                },
                {
                    'company': 'Schneider Electric India',
                    'location': 'Multiple locations',
                    'products': 'PLCs, HMIs, VFDs, temperature controllers',
                    'platforms': 'Modicon M221/M241, Vijeo Designer',
                    'contact': 'www.se.com',
                    'rating': 'Tier 1',
                    'lead_time_weeks': 4,
                    'support': 'Very good'
                },
                {
                    'company': 'Allen Bradley (Rockwell Automation) India',
                    'location': 'Bangalore, Pune',
                    'products': 'PLCs, HMIs, drives, I/O modules',
                    'platforms': 'CompactLogix, PanelView',
                    'contact': 'www.rockwellautomation.com',
                    'rating': 'Tier 1 - Premium',
                    'lead_time_weeks': 8,
                    'support': 'Good'
                }
            ],
            'Sensors_Instruments': [
                {
                    'company': 'EKO Instruments (India representative)',
                    'location': 'Mumbai, Maharashtra',
                    'products': 'UV radiometers, pyranometers, solar sensors',
                    'accuracy': 'IEC 60904-9 compliant',
                    'contact': 'www.eko-india.com',
                    'rating': 'Tier 1 - Specialized',
                    'lead_time_weeks': 8,
                    'calibration': 'NABL traceable'
                },
                {
                    'company': 'Gigahertz Optik India',
                    'location': 'Bangalore, Karnataka',
                    'products': 'UV sensors, spectroradiometers, light meters',
                    'accuracy': 'ISO 17025 certified',
                    'contact': 'www.gigahertz-optik.com',
                    'rating': 'Tier 1',
                    'lead_time_weeks': 10,
                    'calibration': 'DAkkS/NABL'
                },
                {
                    'company': 'Aplab Limited',
                    'location': 'Mumbai, Maharashtra',
                    'products': 'Temperature sensors, humidity sensors, data loggers',
                    'accuracy': 'Class A RTDs, ±0.1°C',
                    'contact': 'www.aplab.com',
                    'rating': 'Tier 2 - Good value',
                    'lead_time_weeks': 3,
                    'calibration': 'NABL available'
                }
            ],
            'Calibration_Labs': [
                {
                    'company': 'National Physical Laboratory (NPL)',
                    'location': 'New Delhi',
                    'services': 'Primary calibration standards',
                    'accreditation': 'National Standards Body',
                    'parameters': 'Temperature, humidity, UV, electrical',
                    'contact': 'www.nplindia.org',
                    'rating': 'Primary Standard',
                    'lead_time_weeks': 6,
                    'cost_level': 'High'
                },
                {
                    'company': 'CSIR-National Aerospace Laboratories (NAL)',
                    'location': 'Bangalore, Karnataka',
                    'services': 'Environmental testing, calibration',
                    'accreditation': 'NABL ISO 17025',
                    'parameters': 'Temperature, pressure, humidity, altitude',
                    'contact': 'www.nal.res.in',
                    'rating': 'Tier 1',
                    'lead_time_weeks': 4,
                    'cost_level': 'Medium-High'
                },
                {
                    'company': 'TÜV SÜD South Asia',
                    'location': 'Mumbai, Bangalore, Chennai',
                    'services': 'Calibration, testing, certification',
                    'accreditation': 'NABL, DAkkS, ISO 17025',
                    'parameters': 'All environmental parameters',
                    'contact': 'www.tuvsud.com',
                    'rating': 'Tier 1 - International',
                    'lead_time_weeks': 3,
                    'cost_level': 'Medium'
                },
                {
                    'company': 'SGS India',
                    'location': 'Multiple locations',
                    'services': 'Testing, inspection, calibration',
                    'accreditation': 'NABL ISO 17025',
                    'parameters': 'Environmental, electrical, dimensional',
                    'contact': 'www.sgs.in',
                    'rating': 'Tier 1 - International',
                    'lead_time_weeks': 2,
                    'cost_level': 'Medium'
                }
            ],
            'DC_Power_Supplies': [
                {
                    'company': 'Aplab Limited',
                    'location': 'Mumbai, Maharashtra',
                    'products': 'Programmable DC power supplies, electronic loads',
                    'specifications': '0-80V, 0-30A, 800W per channel',
                    'contact': 'www.aplab.com',
                    'rating': 'Tier 2 - Good value',
                    'lead_time_weeks': 4,
                    'warranty_years': 2
                },
                {
                    'company': 'Electro Dynamic Works (EDW)',
                    'location': 'Bangalore, Karnataka',
                    'products': 'High power DC supplies, custom solutions',
                    'specifications': 'Up to 100V, 50A, modular',
                    'contact': 'www.edwindia.com',
                    'rating': 'Tier 2',
                    'lead_time_weeks': 6,
                    'warranty_years': 1
                },
                {
                    'company': 'Keysight Technologies India',
                    'location': 'Bangalore, Maharashtra',
                    'products': 'Precision DC sources, SMUs, electronic loads',
                    'specifications': 'High accuracy ±0.02%, programmable',
                    'contact': 'www.keysight.com',
                    'rating': 'Tier 1 - Premium',
                    'lead_time_weeks': 8,
                    'warranty_years': 3
                }
            ],
            'Water_Treatment': [
                {
                    'company': 'Ion Exchange India Ltd',
                    'location': 'Multiple locations',
                    'products': 'DM plants, RO systems, water treatment',
                    'capacity': 'From 100 LPH to 10000 LPH',
                    'contact': 'www.ionexchangeglobal.com',
                    'rating': 'Tier 1 - Market Leader',
                    'lead_time_weeks': 4,
                    'support': 'Excellent nationwide'
                },
                {
                    'company': 'Thermax India',
                    'location': 'Pune, Maharashtra',
                    'products': 'Water treatment plants, ion exchange',
                    'capacity': 'Industrial scale',
                    'contact': 'www.thermaxglobal.com',
                    'rating': 'Tier 1',
                    'lead_time_weeks': 6,
                    'support': 'Very good'
                },
                {
                    'company': 'Aquaguard Engineers',
                    'location': 'Multiple locations',
                    'products': 'RO/DI systems, lab water purification',
                    'capacity': '50 LPH to 1000 LPH',
                    'contact': 'www.aquaguardindia.com',
                    'rating': 'Tier 2 - Good value',
                    'lead_time_weeks': 3,
                    'support': 'Good'
                }
            ]
        }

    def get_suppliers_by_category(self, category: str) -> List[Dict]:
        """Get all suppliers for a specific category"""
        return self.suppliers.get(category, [])

    def get_all_categories(self) -> List[str]:
        """Get list of all supplier categories"""
        return list(self.suppliers.keys())

    def search_suppliers(self, keyword: str) -> Dict:
        """Search suppliers by keyword"""
        results = {}

        keyword_lower = keyword.lower()

        for category, suppliers in self.suppliers.items():
            matching = [
                s for s in suppliers
                if keyword_lower in s.get('company', '').lower() or
                   keyword_lower in s.get('products', '').lower() or
                   keyword_lower in s.get('location', '').lower()
            ]

            if matching:
                results[category] = matching

        return results

    def get_tier1_suppliers(self) -> Dict:
        """Get all Tier 1 suppliers"""
        tier1 = {}

        for category, suppliers in self.suppliers.items():
            tier1_suppliers = [
                s for s in suppliers
                if 'Tier 1' in s.get('rating', '')
            ]

            if tier1_suppliers:
                tier1[category] = tier1_suppliers

        return tier1

    def export_to_dataframe(self, category: str = None) -> pd.DataFrame:
        """Export supplier database to pandas DataFrame"""
        all_suppliers = []

        categories = [category] if category else self.get_all_categories()

        for cat in categories:
            suppliers = self.get_suppliers_by_category(cat)
            for supplier in suppliers:
                supplier_data = supplier.copy()
                supplier_data['category'] = cat
                all_suppliers.append(supplier_data)

        return pd.DataFrame(all_suppliers)

    def get_competitor_comparison(self) -> Dict:
        """Get comparison of major international competitors"""
        return {
            'competitors': [
                {
                    'company': 'ATT (Associated Environmental Systems)',
                    'country': 'Italy',
                    'specialization': 'Large environmental chambers',
                    'strengths': ['European quality', 'Wide temp range', 'Customization'],
                    'weaknesses': ['High cost', 'Long lead time', 'Import duties'],
                    'typical_cost_premium': '40-50% vs local',
                    'delivery_weeks': 28
                },
                {
                    'company': 'CME (Climate & Environment)',
                    'country': 'Germany',
                    'specialization': 'Precision environmental testing',
                    'strengths': ['High precision', 'Excellent documentation', 'CE marked'],
                    'weaknesses': ['Very expensive', 'Complex service', 'Spare parts costly'],
                    'typical_cost_premium': '50-60% vs local',
                    'delivery_weeks': 32
                },
                {
                    'company': 'Arvispec',
                    'country': 'Spain',
                    'specialization': 'PV testing equipment',
                    'strengths': ['PV specialized', 'Good UV systems', 'EU standards'],
                    'weaknesses': ['Limited India presence', 'Forex risk', 'Shipping'],
                    'typical_cost_premium': '35-45% vs local',
                    'delivery_weeks': 24
                },
                {
                    'company': 'UFE (Ultimate Force Engineering)',
                    'country': 'Singapore',
                    'specialization': 'Environmental chambers',
                    'strengths': ['Good quality', 'Closer to India', 'English speaking'],
                    'weaknesses': ['Still expensive', 'Moderate lead time', 'Limited customization'],
                    'typical_cost_premium': '25-35% vs local',
                    'delivery_weeks': 20
                },
                {
                    'company': 'Stech',
                    'country': 'China',
                    'specialization': 'Environmental test equipment',
                    'strengths': ['Competitive pricing', 'Fast delivery', 'Good enough quality'],
                    'weaknesses': ['Quality concerns', 'Service support', 'Documentation'],
                    'typical_cost_premium': '-10 to +10% vs local',
                    'delivery_weeks': 16
                }
            ],
            'local_advantage': {
                'cost': '20-50% lower than imports',
                'delivery': '40-50% faster',
                'service': 'On-site support available',
                'customization': 'Easy modification',
                'payment': 'Rupee transactions, no forex risk',
                'warranty': 'Easier warranty claims'
            }
        }

    def get_database_summary(self) -> Dict:
        """Get summary of supplier database"""
        summary = {}

        for category in self.get_all_categories():
            suppliers = self.get_suppliers_by_category(category)
            summary[category] = {
                'total_suppliers': len(suppliers),
                'tier1_count': len([s for s in suppliers if 'Tier 1' in s.get('rating', '')]),
                'avg_lead_time_weeks': sum([s.get('lead_time_weeks', 0) for s in suppliers]) / len(suppliers) if suppliers else 0,
                'locations': list(set([s.get('location', '') for s in suppliers]))
            }

        return summary
