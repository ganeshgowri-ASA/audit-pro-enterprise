"""
Commercial Quote Generation System
Handles pricing, payment terms, warranties, and delivery schedules
"""

from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd


class QuoteGenerator:
    """
    Commercial Quote Generator for PV Chamber System
    Generates comprehensive quotations with all cost breakdowns
    """

    def __init__(self):
        # Base costs (INR Lakhs)
        self.base_costs = {
            'chamber_system': 35.0,
            'uv_led_arrays': 16.0,
            'refrigeration_system': 8.0,
            'controls_hmi': 7.0,
            'dc_power_supply': 6.0,
            'uniformity_robot': 12.0,
            'water_treatment': 6.3,
            'installation': 5.0,
            'calibration': 3.5,
            'documentation': 1.2
        }

        # Currency
        self.currency = 'INR'

        # Tax rates
        self.gst_rate = 0.18  # 18% GST

    def calculate_system_cost(self, options: Dict = None) -> Dict:
        """
        Calculate total system cost with options
        """
        if options is None:
            options = {}

        # Base costs
        costs = self.base_costs.copy()

        # Apply option modifiers
        if options.get('interior_material') == 'SS316':
            costs['chamber_system'] *= 1.35  # 35% premium for SS316

        if options.get('uv_lamp_type') == 'Metal_Halide':
            costs['uv_led_arrays'] *= 0.5  # Metal halide is cheaper
        elif options.get('uv_lamp_type') == 'Fluorescent_UVA':
            costs['uv_led_arrays'] *= 0.35  # Fluorescent is cheapest

        if options.get('include_robot', True) == False:
            costs['uniformity_robot'] = 0

        if options.get('advanced_water_treatment', False):
            costs['water_treatment'] *= 1.4

        # Subtotal
        subtotal_lakhs = sum(costs.values())
        subtotal_inr = subtotal_lakhs * 100000

        # GST
        gst_inr = subtotal_inr * self.gst_rate

        # Total
        total_inr = subtotal_inr + gst_inr
        total_lakhs = total_inr / 100000

        return {
            'line_items_lakhs': costs,
            'subtotal_lakhs': subtotal_lakhs,
            'subtotal_inr': subtotal_inr,
            'gst_rate_percent': self.gst_rate * 100,
            'gst_inr': gst_inr,
            'gst_lakhs': gst_inr / 100000,
            'total_inr': total_inr,
            'total_lakhs': total_lakhs,
            'total_usd': total_inr / 83,  # Approximate conversion
            'currency': self.currency
        }

    def generate_payment_terms(self, total_amount: float, schedule: str = '30-40-30') -> Dict:
        """
        Generate payment schedule
        Supported schedules: 30-40-30, 40-30-30, 50-50
        """
        schedules = {
            '30-40-30': [
                {'milestone': 'Purchase Order', 'percent': 30},
                {'milestone': 'Pre-Dispatch Inspection', 'percent': 40},
                {'milestone': 'Installation & Commissioning', 'percent': 30}
            ],
            '40-30-30': [
                {'milestone': 'Purchase Order', 'percent': 40},
                {'milestone': 'Pre-Dispatch Inspection', 'percent': 30},
                {'milestone': 'Installation & Commissioning', 'percent': 30}
            ],
            '50-50': [
                {'milestone': 'Purchase Order', 'percent': 50},
                {'milestone': 'Installation & Commissioning', 'percent': 50}
            ]
        }

        payment_schedule = schedules.get(schedule, schedules['30-40-30'])

        # Calculate amounts
        for payment in payment_schedule:
            payment['amount_inr'] = total_amount * (payment['percent'] / 100)
            payment['amount_lakhs'] = payment['amount_inr'] / 100000

        return {
            'schedule_type': schedule,
            'total_amount_inr': total_amount,
            'payment_milestones': payment_schedule,
            'payment_method': 'Wire Transfer / RTGS / NEFT',
            'credit_period': 'As per milestone achievement',
            'advance_payment_mandatory': True
        }

    def generate_warranty_terms(self, warranty_months: int = 24) -> Dict:
        """
        Generate warranty and support terms
        """
        return {
            'comprehensive_warranty': {
                'duration_months': warranty_months,
                'coverage': 'All parts, labor, and service',
                'response_time': '24 hours for critical issues',
                'on_site_support': 'Available during warranty',
                'exclusions': ['Consumables', 'Misuse', 'Force majeure']
            },
            'extended_warranty_options': [
                {
                    'duration_months': 36,
                    'additional_cost_percent': 8,
                    'description': '3-year comprehensive coverage'
                },
                {
                    'duration_months': 48,
                    'additional_cost_percent': 15,
                    'description': '4-year comprehensive coverage'
                },
                {
                    'duration_months': 60,
                    'additional_cost_percent': 22,
                    'description': '5-year comprehensive coverage'
                }
            ],
            'calibration_support': {
                'first_calibration': 'Included during installation',
                'annual_calibration': 'Chargeable as per actuals',
                'nabl_accredited': True,
                'certificate_validity_months': 12
            },
            'software_updates': {
                'included_period_months': warranty_months,
                'update_frequency': 'Quarterly or as needed',
                'remote_support': 'Yes, via TeamViewer/AnyDesk'
            },
            'spare_parts': {
                'availability': '10+ years',
                'lead_time_weeks': '2-4 weeks',
                'pricing': 'List price at time of order'
            }
        }

    def generate_delivery_timeline(self, start_date: datetime = None) -> Dict:
        """
        Generate project delivery timeline
        """
        if start_date is None:
            start_date = datetime.now()

        # Timeline in weeks
        milestones = [
            {'phase': 'Engineering & Design', 'duration_weeks': 3, 'description': 'Detailed design drawings, CFD analysis'},
            {'phase': 'Procurement', 'duration_weeks': 6, 'description': 'Long-lead items, custom fabrication'},
            {'phase': 'Manufacturing', 'duration_weeks': 8, 'description': 'Chamber fabrication, system assembly'},
            {'phase': 'FAT (Factory Acceptance Test)', 'duration_weeks': 1, 'description': 'Performance verification at factory'},
            {'phase': 'Packing & Dispatch', 'duration_weeks': 1, 'description': 'Secure packaging, transportation'},
            {'phase': 'Site Installation', 'duration_weeks': 2, 'description': 'Unloading, positioning, connections'},
            {'phase': 'Commissioning & Testing', 'duration_weeks': 2, 'description': 'System startup, performance tests'},
            {'phase': 'Calibration & Documentation', 'duration_weeks': 1, 'description': 'NABL calibration, user training'},
            {'phase': 'Handover', 'duration_weeks': 1, 'description': 'Final acceptance, documentation transfer'}
        ]

        # Calculate dates
        current_date = start_date
        for milestone in milestones:
            milestone['start_date'] = current_date.strftime('%Y-%m-%d')
            end_date = current_date + timedelta(weeks=milestone['duration_weeks'])
            milestone['end_date'] = end_date.strftime('%Y-%m-%d')
            current_date = end_date

        total_weeks = sum([m['duration_weeks'] for m in milestones])
        total_months = total_weeks / 4.33

        return {
            'project_start_date': start_date.strftime('%Y-%m-%d'),
            'project_end_date': current_date.strftime('%Y-%m-%d'),
            'total_duration_weeks': total_weeks,
            'total_duration_months': round(total_months, 1),
            'milestones': milestones,
            'critical_path': ['Procurement', 'Manufacturing', 'Commissioning & Testing'],
            'dependencies': {
                'site_readiness': 'Customer to provide: Power (415V 3Ph, 50A), PCW (500 LPH), Floor (400kg/m²)',
                'access': 'Chamber access door minimum 2.5m x 2.5m',
                'approvals': 'Electrical and plumbing work permits'
            }
        }

    def generate_terms_conditions(self) -> Dict:
        """
        Generate standard terms and conditions
        """
        return {
            'validity': {
                'quote_validity_days': 90,
                'price_escalation_clause': 'Prices firm for 90 days from quote date'
            },
            'taxes_duties': {
                'gst': '18% applicable on all items',
                'customs_duty': 'Not applicable (domestic supply)',
                'other_levies': 'As applicable by law'
            },
            'delivery_terms': {
                'incoterms': 'DDP (Delivered Duty Paid) customer site',
                'packing': 'Export-worthy wooden crate',
                'insurance': 'Comprehensive, covered by supplier',
                'unloading': 'Customer scope'
            },
            'installation': {
                'site_requirements': 'Level floor, adequate clearance, utilities ready',
                'customer_scope': 'Civil works, utility connections up to chamber',
                'supplier_scope': 'Equipment installation, commissioning, training'
            },
            'acceptance_criteria': {
                'performance_tests': 'As per IEC 61215, IEC 61730, IEC 60068',
                'acceptance_tolerance': '±5% of specified values',
                'documentation': 'Test reports, certificates, manuals'
            },
            'force_majeure': {
                'applicability': 'Natural disasters, pandemics, government regulations',
                'liability': 'Neither party liable for delays due to force majeure'
            },
            'dispute_resolution': {
                'jurisdiction': 'Bangalore, India',
                'arbitration': 'As per Indian Arbitration & Conciliation Act',
                'language': 'English'
            }
        }

    def generate_complete_quote(self,
                               customer_name: str,
                               customer_address: str,
                               options: Dict = None,
                               payment_schedule: str = '30-40-30',
                               warranty_months: int = 24) -> Dict:
        """
        Generate complete commercial quotation
        """
        # Generate quote number
        quote_number = f"PVC-{datetime.now().strftime('%Y%m%d')}-{hash(customer_name) % 1000:03d}"
        quote_date = datetime.now().strftime('%Y-%m-%d')

        # Cost calculation
        cost_breakdown = self.calculate_system_cost(options)

        # Payment terms
        payment_terms = self.generate_payment_terms(cost_breakdown['total_inr'], payment_schedule)

        # Warranty
        warranty = self.generate_warranty_terms(warranty_months)

        # Delivery timeline
        timeline = self.generate_delivery_timeline()

        # Terms & conditions
        terms = self.generate_terms_conditions()

        return {
            'quote_header': {
                'quote_number': quote_number,
                'quote_date': quote_date,
                'valid_until': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                'prepared_by': 'Sales Engineering Team',
                'customer_name': customer_name,
                'customer_address': customer_address
            },
            'system_description': {
                'title': 'UV+TC+HF+DH Combined Environmental Chamber',
                'model': 'PV-3200-2100-2200-UVTC',
                'application': 'PV Module Testing per IEC 61215/61730',
                'capacity': '2 PV modules (3.2m x 2.1m)',
                'standards_compliance': ['IEC 61215', 'IEC 61730', 'IEC 60068', 'IEC 60904-9', 'ISO 17025']
            },
            'cost_breakdown': cost_breakdown,
            'payment_terms': payment_terms,
            'warranty_support': warranty,
            'delivery_timeline': timeline,
            'terms_conditions': terms,
            'supplier_information': {
                'company_name': 'Your Company Name',
                'address': 'Your Company Address',
                'gstin': 'XXXXXXXXXXXX',
                'contact_person': 'Sales Manager',
                'phone': '+91-XXXXXXXXXX',
                'email': 'sales@yourcompany.com'
            }
        }

    def export_quote_to_dict(self, quote: Dict) -> pd.DataFrame:
        """
        Export quote line items to pandas DataFrame for Excel export
        """
        line_items = []

        for item, cost_lakhs in quote['cost_breakdown']['line_items_lakhs'].items():
            line_items.append({
                'Item': item.replace('_', ' ').title(),
                'Cost (Lakhs)': cost_lakhs,
                'Cost (INR)': cost_lakhs * 100000
            })

        # Add subtotal
        line_items.append({
            'Item': 'SUBTOTAL',
            'Cost (Lakhs)': quote['cost_breakdown']['subtotal_lakhs'],
            'Cost (INR)': quote['cost_breakdown']['subtotal_inr']
        })

        # Add GST
        line_items.append({
            'Item': f"GST ({quote['cost_breakdown']['gst_rate_percent']}%)",
            'Cost (Lakhs)': quote['cost_breakdown']['gst_lakhs'],
            'Cost (INR)': quote['cost_breakdown']['gst_inr']
        })

        # Add total
        line_items.append({
            'Item': 'TOTAL',
            'Cost (Lakhs)': quote['cost_breakdown']['total_lakhs'],
            'Cost (INR)': quote['cost_breakdown']['total_inr']
        })

        return pd.DataFrame(line_items)
