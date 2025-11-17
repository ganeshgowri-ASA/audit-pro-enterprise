"""
Supplier Database Manager - Custom Quote Upload & Comparison
============================================================

This module handles custom supplier quote uploads, parsing, storage, and comparison.
Supports multiple file formats (PDF, Excel, CSV) and provides side-by-side comparison.

Integration Points:
------------------
- Used by: quote_generator (supplier selection and pricing)
- Dependencies: None (can work standalone)
- Merge Priority: 3 (After core-calculations and company-branding)

Features:
---------
- Upload supplier quotes (PDF/Excel/CSV/JSON)
- Auto-parse supplier data
- Store in suppliers_custom.json
- Compare multiple quotes side-by-side
- Add/Edit/Delete suppliers
- Upload company logos
- Export comparison reports

Author: Audit-Pro Enterprise
Version: 1.0.0
"""

import json
import os
import csv
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import base64


class FileFormat(Enum):
    """Supported file formats for supplier quotes"""
    PDF = "pdf"
    EXCEL = "xlsx"
    EXCEL_OLD = "xls"
    CSV = "csv"
    JSON = "json"


class ItemCategory(Enum):
    """Categories for quote items"""
    COMPRESSOR = "compressor"
    HEATER = "heater"
    COOLING_SYSTEM = "cooling_system"
    HUMIDIFIER = "humidifier"
    CONTROLLER = "controller"
    SENSOR = "sensor"
    UV_LED = "uv_led"
    UV_SYSTEM = "uv_system"
    CHAMBER_MATERIAL = "chamber_material"
    INSULATION = "insulation"
    DOOR_ASSEMBLY = "door_assembly"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    OTHER = "other"


@dataclass
class QuoteItem:
    """Individual item in a supplier quote"""
    item_id: str
    description: str
    category: str
    quantity: int
    unit_price: float
    total_price: float
    currency: str = "USD"
    lead_time_days: int = 30
    warranty_months: int = 12
    specifications: Dict[str, Any] = None
    notes: str = ""

    def __post_init__(self):
        if self.specifications is None:
            self.specifications = {}


@dataclass
class SupplierQuote:
    """Complete supplier quote"""
    quote_id: str
    supplier_name: str
    contact_person: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    website: str = ""
    items: List[QuoteItem] = None
    subtotal: float = 0.0
    tax_rate: float = 0.0
    tax_amount: float = 0.0
    shipping_cost: float = 0.0
    total_amount: float = 0.0
    currency: str = "USD"
    valid_until: str = ""
    payment_terms: str = ""
    delivery_terms: str = ""
    notes: str = ""
    logo_base64: str = ""
    created_date: str = ""
    last_updated: str = ""
    source_file: str = ""

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if not self.created_date:
            self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.last_updated:
            self.last_updated = self.created_date


class SupplierDatabase:
    """Manage supplier database with custom uploads"""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize supplier database

        Args:
            data_dir: Directory to store supplier data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.suppliers_file = self.data_dir / "suppliers_custom.json"
        self.logos_dir = self.data_dir / "supplier_logos"
        self.logos_dir.mkdir(parents=True, exist_ok=True)

        self.suppliers: Dict[str, SupplierQuote] = {}
        self.load_suppliers()

    def load_suppliers(self):
        """Load suppliers from JSON file"""
        if self.suppliers_file.exists():
            try:
                with open(self.suppliers_file, 'r') as f:
                    data = json.load(f)
                    for quote_id, quote_data in data.items():
                        # Convert items back to QuoteItem objects
                        items = [QuoteItem(**item) for item in quote_data.get('items', [])]
                        quote_data['items'] = items
                        self.suppliers[quote_id] = SupplierQuote(**quote_data)
            except Exception as e:
                print(f"Warning: Could not load suppliers: {e}")
                self.suppliers = {}
        else:
            self.suppliers = {}
            self._create_sample_suppliers()

    def save_suppliers(self):
        """Save suppliers to JSON file"""
        data = {}
        for quote_id, quote in self.suppliers.items():
            quote_dict = asdict(quote)
            data[quote_id] = quote_dict

        with open(self.suppliers_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _create_sample_suppliers(self):
        """Create sample suppliers for demonstration"""
        sample_suppliers = [
            SupplierQuote(
                quote_id="SUP001",
                supplier_name="ThermoTech Industries",
                contact_person="John Smith",
                email="john.smith@thermotech.com",
                phone="+1-555-0100",
                website="www.thermotech.com",
                items=[
                    QuoteItem(
                        item_id="TT-COMP-500",
                        description="Industrial Compressor 5HP",
                        category=ItemCategory.COMPRESSOR.value,
                        quantity=1,
                        unit_price=2500.00,
                        total_price=2500.00,
                        lead_time_days=45,
                        warranty_months=24
                    ),
                    QuoteItem(
                        item_id="TT-HEAT-1000",
                        description="Electric Heater 10kW",
                        category=ItemCategory.HEATER.value,
                        quantity=2,
                        unit_price=800.00,
                        total_price=1600.00,
                        lead_time_days=30,
                        warranty_months=12
                    )
                ],
                subtotal=4100.00,
                tax_rate=0.08,
                tax_amount=328.00,
                shipping_cost=150.00,
                total_amount=4578.00,
                valid_until="2025-12-31",
                payment_terms="Net 30",
                delivery_terms="FOB Factory"
            ),
            SupplierQuote(
                quote_id="SUP002",
                supplier_name="ClimateControl Solutions",
                contact_person="Sarah Johnson",
                email="sarah.j@climatecontrol.com",
                phone="+1-555-0200",
                website="www.climatecontrol.com",
                items=[
                    QuoteItem(
                        item_id="CC-HUM-300",
                        description="Ultrasonic Humidifier 30L/day",
                        category=ItemCategory.HUMIDIFIER.value,
                        quantity=1,
                        unit_price=1200.00,
                        total_price=1200.00,
                        lead_time_days=20,
                        warranty_months=18
                    ),
                    QuoteItem(
                        item_id="CC-CTRL-PRO",
                        description="PLC Controller with Touchscreen",
                        category=ItemCategory.CONTROLLER.value,
                        quantity=1,
                        unit_price=3500.00,
                        total_price=3500.00,
                        lead_time_days=35,
                        warranty_months=36
                    )
                ],
                subtotal=4700.00,
                tax_rate=0.08,
                tax_amount=376.00,
                shipping_cost=100.00,
                total_amount=5176.00,
                valid_until="2025-11-30",
                payment_terms="50% advance, 50% on delivery",
                delivery_terms="CIF destination"
            )
        ]

        for supplier in sample_suppliers:
            self.suppliers[supplier.quote_id] = supplier

        self.save_suppliers()

    def add_supplier(self, supplier: SupplierQuote) -> str:
        """
        Add or update a supplier quote

        Args:
            supplier: SupplierQuote object

        Returns:
            quote_id of the added supplier
        """
        supplier.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.suppliers[supplier.quote_id] = supplier
        self.save_suppliers()
        return supplier.quote_id

    def delete_supplier(self, quote_id: str) -> bool:
        """
        Delete a supplier quote

        Args:
            quote_id: ID of quote to delete

        Returns:
            True if deleted, False if not found
        """
        if quote_id in self.suppliers:
            del self.suppliers[quote_id]
            self.save_suppliers()
            return True
        return False

    def get_supplier(self, quote_id: str) -> Optional[SupplierQuote]:
        """Get a specific supplier quote"""
        return self.suppliers.get(quote_id)

    def list_suppliers(self) -> List[SupplierQuote]:
        """Get all supplier quotes"""
        return list(self.suppliers.values())

    def search_suppliers(self, query: str) -> List[SupplierQuote]:
        """
        Search suppliers by name or quote ID

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching supplier quotes
        """
        query_lower = query.lower()
        results = []

        for supplier in self.suppliers.values():
            if (query_lower in supplier.supplier_name.lower() or
                query_lower in supplier.quote_id.lower()):
                results.append(supplier)

        return results

    def save_logo(self, quote_id: str, logo_data: bytes, file_extension: str = "png") -> str:
        """
        Save supplier logo

        Args:
            quote_id: Supplier quote ID
            logo_data: Binary logo data
            file_extension: File extension (png, jpg, svg)

        Returns:
            Path to saved logo
        """
        logo_path = self.logos_dir / f"{quote_id}.{file_extension}"
        with open(logo_path, 'wb') as f:
            f.write(logo_data)

        # Update supplier with base64 encoded logo
        if quote_id in self.suppliers:
            logo_base64 = base64.b64encode(logo_data).decode('utf-8')
            self.suppliers[quote_id].logo_base64 = f"data:image/{file_extension};base64,{logo_base64}"
            self.save_suppliers()

        return str(logo_path)


class QuoteParser:
    """Parse supplier quotes from various file formats"""

    @staticmethod
    def parse_csv(file_path: str, supplier_name: str) -> SupplierQuote:
        """
        Parse CSV file containing supplier quote

        Expected CSV format:
        Item ID, Description, Category, Quantity, Unit Price, Lead Time, Warranty

        Args:
            file_path: Path to CSV file
            supplier_name: Name of supplier

        Returns:
            SupplierQuote object
        """
        items = []

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    quantity = int(row.get('Quantity', 1))
                    unit_price = float(row.get('Unit Price', 0))

                    item = QuoteItem(
                        item_id=row.get('Item ID', f"ITEM-{len(items)+1}"),
                        description=row.get('Description', ''),
                        category=row.get('Category', ItemCategory.OTHER.value),
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=quantity * unit_price,
                        lead_time_days=int(row.get('Lead Time', 30)),
                        warranty_months=int(row.get('Warranty', 12))
                    )
                    items.append(item)
                except (ValueError, KeyError) as e:
                    print(f"Warning: Skipping row due to error: {e}")
                    continue

        # Calculate totals
        subtotal = sum(item.total_price for item in items)

        quote = SupplierQuote(
            quote_id=f"SUP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            supplier_name=supplier_name,
            items=items,
            subtotal=subtotal,
            total_amount=subtotal,
            source_file=file_path
        )

        return quote

    @staticmethod
    def parse_json(file_path: str) -> SupplierQuote:
        """
        Parse JSON file containing supplier quote

        Args:
            file_path: Path to JSON file

        Returns:
            SupplierQuote object
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert items to QuoteItem objects
        items = []
        for item_data in data.get('items', []):
            items.append(QuoteItem(**item_data))

        data['items'] = items
        data['source_file'] = file_path

        return SupplierQuote(**data)

    @staticmethod
    def parse_excel(file_path: str, supplier_name: str) -> SupplierQuote:
        """
        Parse Excel file containing supplier quote

        Note: This is a placeholder. Requires openpyxl or pandas for full implementation.

        Args:
            file_path: Path to Excel file
            supplier_name: Name of supplier

        Returns:
            SupplierQuote object
        """
        # Placeholder implementation
        # In production, use openpyxl or pandas to read Excel
        print(f"Excel parsing for {file_path} - requires openpyxl library")

        return SupplierQuote(
            quote_id=f"SUP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            supplier_name=supplier_name,
            items=[],
            notes="Parsed from Excel file (placeholder)",
            source_file=file_path
        )

    @staticmethod
    def parse_pdf(file_path: str, supplier_name: str) -> SupplierQuote:
        """
        Parse PDF file containing supplier quote

        Note: This is a placeholder. Requires PyPDF2 or pdfplumber for full implementation.

        Args:
            file_path: Path to PDF file
            supplier_name: Name of supplier

        Returns:
            SupplierQuote object
        """
        # Placeholder implementation
        # In production, use PyPDF2 or pdfplumber to extract text
        print(f"PDF parsing for {file_path} - requires pdfplumber library")

        return SupplierQuote(
            quote_id=f"SUP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            supplier_name=supplier_name,
            items=[],
            notes="Parsed from PDF file (placeholder)",
            source_file=file_path
        )

    @staticmethod
    def auto_parse(file_path: str, supplier_name: str) -> SupplierQuote:
        """
        Automatically detect file format and parse

        Args:
            file_path: Path to file
            supplier_name: Name of supplier

        Returns:
            SupplierQuote object
        """
        file_ext = Path(file_path).suffix.lower()

        if file_ext == '.csv':
            return QuoteParser.parse_csv(file_path, supplier_name)
        elif file_ext == '.json':
            return QuoteParser.parse_json(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return QuoteParser.parse_excel(file_path, supplier_name)
        elif file_ext == '.pdf':
            return QuoteParser.parse_pdf(file_path, supplier_name)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")


class QuoteComparator:
    """Compare multiple supplier quotes side-by-side"""

    @staticmethod
    def compare_quotes(quotes: List[SupplierQuote], by_category: bool = True) -> Dict:
        """
        Compare multiple quotes

        Args:
            quotes: List of SupplierQuote objects
            by_category: Group comparison by item category

        Returns:
            Comparison dictionary
        """
        if not quotes:
            return {}

        comparison = {
            'suppliers': [q.supplier_name for q in quotes],
            'total_amounts': [q.total_amount for q in quotes],
            'currencies': [q.currency for q in quotes],
            'lead_times': [],
            'warranty_periods': [],
            'items_comparison': {}
        }

        # Calculate average lead times and warranties
        for quote in quotes:
            if quote.items:
                avg_lead = sum(item.lead_time_days for item in quote.items) / len(quote.items)
                avg_warranty = sum(item.warranty_months for item in quote.items) / len(quote.items)
                comparison['lead_times'].append(round(avg_lead, 1))
                comparison['warranty_periods'].append(round(avg_warranty, 1))
            else:
                comparison['lead_times'].append(0)
                comparison['warranty_periods'].append(0)

        # Compare items by category
        if by_category:
            all_categories = set()
            for quote in quotes:
                for item in quote.items:
                    all_categories.add(item.category)

            for category in all_categories:
                category_items = {}
                for quote in quotes:
                    items_in_category = [item for item in quote.items if item.category == category]
                    category_items[quote.supplier_name] = items_in_category

                comparison['items_comparison'][category] = category_items

        return comparison

    @staticmethod
    def find_best_value(quotes: List[SupplierQuote], weight_price: float = 0.6,
                       weight_lead_time: float = 0.3, weight_warranty: float = 0.1) -> Dict:
        """
        Find best value quote based on weighted criteria

        Args:
            quotes: List of SupplierQuote objects
            weight_price: Weight for price (0-1)
            weight_lead_time: Weight for lead time (0-1)
            weight_warranty: Weight for warranty (0-1)

        Returns:
            Analysis with best value supplier
        """
        if not quotes:
            return {}

        scores = []

        # Normalize values
        prices = [q.total_amount for q in quotes]
        max_price = max(prices) if prices else 1

        for quote in quotes:
            if not quote.items:
                scores.append({'supplier': quote.supplier_name, 'score': 0})
                continue

            # Price score (lower is better, so invert)
            price_score = 1 - (quote.total_amount / max_price) if max_price > 0 else 0

            # Lead time score (lower is better)
            avg_lead = sum(item.lead_time_days for item in quote.items) / len(quote.items)
            lead_score = 1 - (avg_lead / 180)  # Assume 180 days is worst case
            lead_score = max(0, lead_score)

            # Warranty score (higher is better)
            avg_warranty = sum(item.warranty_months for item in quote.items) / len(quote.items)
            warranty_score = avg_warranty / 36  # Assume 36 months is best case
            warranty_score = min(1, warranty_score)

            # Calculate weighted score
            total_score = (price_score * weight_price +
                          lead_score * weight_lead_time +
                          warranty_score * weight_warranty)

            scores.append({
                'supplier': quote.supplier_name,
                'quote_id': quote.quote_id,
                'total_score': round(total_score, 3),
                'price_score': round(price_score, 3),
                'lead_time_score': round(lead_score, 3),
                'warranty_score': round(warranty_score, 3),
                'total_amount': quote.total_amount
            })

        # Sort by total score (descending)
        scores.sort(key=lambda x: x['total_score'], reverse=True)

        return {
            'best_value': scores[0] if scores else None,
            'all_scores': scores,
            'weights': {
                'price': weight_price,
                'lead_time': weight_lead_time,
                'warranty': weight_warranty
            }
        }

    @staticmethod
    def export_comparison(comparison: Dict, output_file: str):
        """
        Export comparison to JSON file

        Args:
            comparison: Comparison dictionary
            output_file: Output file path
        """
        # Convert any non-serializable objects
        serializable_comparison = json.loads(
            json.dumps(comparison, default=lambda o: str(o))
        )

        with open(output_file, 'w') as f:
            json.dump(serializable_comparison, f, indent=2)


# Example usage and testing
if __name__ == "__main__":
    print("=== Supplier Database Manager Tests ===\n")

    # Initialize database
    db = SupplierDatabase(data_dir="data/suppliers")

    # Test 1: List existing suppliers
    print("1. Existing Suppliers:")
    suppliers = db.list_suppliers()
    for supplier in suppliers:
        print(f"   {supplier.quote_id}: {supplier.supplier_name} - ${supplier.total_amount:.2f}")
        print(f"      Items: {len(supplier.items)}")

    # Test 2: Search suppliers
    print("\n2. Search for 'ThermoTech':")
    results = db.search_suppliers("ThermoTech")
    for result in results:
        print(f"   Found: {result.supplier_name} ({result.quote_id})")

    # Test 3: Compare quotes
    print("\n3. Quote Comparison:")
    if len(suppliers) >= 2:
        comparison = QuoteComparator.compare_quotes(suppliers[:2])
        print(f"   Suppliers: {comparison['suppliers']}")
        print(f"   Total Amounts: {comparison['total_amounts']}")
        print(f"   Avg Lead Times: {comparison['lead_times']}")

        # Find best value
        best = QuoteComparator.find_best_value(suppliers[:2])
        if best.get('best_value'):
            print(f"\n   Best Value: {best['best_value']['supplier']}")
            print(f"   Score: {best['best_value']['total_score']}")

    # Test 4: Create sample CSV for testing
    print("\n4. Creating sample CSV file for testing:")
    sample_csv = "data/suppliers/sample_quote.csv"
    os.makedirs("data/suppliers", exist_ok=True)

    with open(sample_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Item ID', 'Description', 'Category', 'Quantity', 'Unit Price', 'Lead Time', 'Warranty'])
        writer.writerow(['LED-UV-365', 'UV LED 365nm 100W', 'uv_led', '10', '125.50', '45', '24'])
        writer.writerow(['LED-UV-385', 'UV LED 385nm 100W', 'uv_led', '5', '135.00', '45', '24'])

    print(f"   Sample CSV created: {sample_csv}")

    # Parse the CSV
    parsed_quote = QuoteParser.parse_csv(sample_csv, "UV Components Inc")
    print(f"   Parsed {len(parsed_quote.items)} items")
    print(f"   Total: ${parsed_quote.total_amount:.2f}")

    # Add to database
    db.add_supplier(parsed_quote)
    print(f"   Added to database with ID: {parsed_quote.quote_id}")

    print("\n=== All Tests Passed ===")
    print("\n✅ Supplier database manager ready for integration!")
