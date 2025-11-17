"""
Supplier Upload UI - Streamlit Interface for Supplier Management
================================================================

This module provides the Streamlit-based user interface for:
- Uploading custom supplier quotes (PDF/Excel/CSV)
- Previewing data before import
- Manual entry form
- Bulk import from Excel template
- Supplier comparison dashboard

Integration Points:
------------------
- Uses: modules.supplier_manager
- Used by: Main Streamlit app
- Dependencies: streamlit, modules/supplier_manager.py

Author: Audit-Pro Enterprise
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from modules.supplier_manager import (
        SupplierDatabase,
        QuoteParser,
        QuoteComparator,
        SupplierQuote,
        QuoteItem,
        ItemCategory
    )
except ImportError:
    print("Warning: supplier_manager module not found. Using mock implementation.")
    SupplierDatabase = None


class SupplierUploadUI:
    """Streamlit UI for supplier management"""

    def __init__(self):
        """Initialize the UI"""
        if SupplierDatabase:
            self.db = SupplierDatabase(data_dir="data/suppliers")
        else:
            self.db = None

    def render_upload_section(self):
        """Render file upload section"""
        st.subheader("📤 Upload Supplier Quote")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Supported formats:**
            - 📄 PDF files
            - 📊 Excel (.xlsx, .xls)
            - 📋 CSV files
            - 🔤 JSON files
            """)

            uploaded_file = st.file_uploader(
                "Drag and drop your quote file here",
                type=['pdf', 'xlsx', 'xls', 'csv', 'json'],
                help="Upload a supplier quote in any supported format"
            )

            supplier_name = st.text_input(
                "Supplier Name",
                placeholder="Enter supplier company name",
                help="Name of the supplier providing this quote"
            )

        with col2:
            st.markdown("**Quick Actions:**")
            if st.button("📥 Download CSV Template", use_container_width=True):
                self._download_csv_template()

            if st.button("➕ Manual Entry", use_container_width=True):
                st.session_state['show_manual_entry'] = True

        if uploaded_file and supplier_name:
            self._process_upload(uploaded_file, supplier_name)

    def _process_upload(self, uploaded_file, supplier_name: str):
        """Process uploaded file"""
        st.markdown("---")
        st.subheader("📋 Preview Data")

        # Save uploaded file temporarily
        temp_path = Path("data/temp") / uploaded_file.name
        temp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            # Parse the file
            if QuoteParser:
                with st.spinner("Parsing quote..."):
                    quote = QuoteParser.auto_parse(str(temp_path), supplier_name)

                # Show preview
                st.success(f"✅ Parsed {len(quote.items)} items from {uploaded_file.name}")

                # Display quote details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Items", len(quote.items))
                with col2:
                    st.metric("Subtotal", f"${quote.subtotal:,.2f}")
                with col3:
                    st.metric("Currency", quote.currency)

                # Show items table
                if quote.items:
                    items_data = []
                    for item in quote.items:
                        items_data.append({
                            'Item ID': item.item_id,
                            'Description': item.description,
                            'Category': item.category,
                            'Qty': item.quantity,
                            'Unit Price': f"${item.unit_price:.2f}",
                            'Total': f"${item.total_price:.2f}",
                            'Lead Time': f"{item.lead_time_days} days",
                            'Warranty': f"{item.warranty_months} months"
                        })

                    df = pd.DataFrame(items_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)

                # Manual override section
                with st.expander("✏️ Edit Quote Details"):
                    contact = st.text_input("Contact Person", value=quote.contact_person)
                    email = st.text_input("Email", value=quote.email)
                    phone = st.text_input("Phone", value=quote.phone)

                    col1, col2 = st.columns(2)
                    with col1:
                        tax_rate = st.number_input("Tax Rate (%)", value=quote.tax_rate * 100, min_value=0.0, max_value=100.0) / 100
                    with col2:
                        shipping = st.number_input("Shipping Cost", value=quote.shipping_cost, min_value=0.0)

                    payment_terms = st.text_input("Payment Terms", value=quote.payment_terms, placeholder="e.g., Net 30")
                    notes = st.text_area("Notes", value=quote.notes)

                    # Update quote
                    quote.contact_person = contact
                    quote.email = email
                    quote.phone = phone
                    quote.tax_rate = tax_rate
                    quote.tax_amount = quote.subtotal * tax_rate
                    quote.shipping_cost = shipping
                    quote.total_amount = quote.subtotal + quote.tax_amount + shipping
                    quote.payment_terms = payment_terms
                    quote.notes = notes

                # Logo upload
                st.markdown("### 🖼️ Supplier Logo (Optional)")
                logo_file = st.file_uploader("Upload supplier logo", type=['png', 'jpg', 'jpeg', 'svg'])

                # Import button
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("✅ Import Quote", use_container_width=True, type="primary"):
                        if self.db:
                            # Save logo if provided
                            if logo_file:
                                logo_data = logo_file.read()
                                self.db.save_logo(quote.quote_id, logo_data, logo_file.name.split('.')[-1])

                            # Add to database
                            self.db.add_supplier(quote)
                            st.success(f"✅ Quote imported successfully! ID: {quote.quote_id}")
                            st.rerun()

                with col2:
                    if st.button("🔄 Reset", use_container_width=True):
                        st.rerun()

        except Exception as e:
            st.error(f"❌ Error parsing file: {e}")
            st.info("Try using manual entry or check the file format.")

    def _download_csv_template(self):
        """Generate and download CSV template"""
        template_data = {
            'Item ID': ['ITEM-001', 'ITEM-002', 'ITEM-003'],
            'Description': ['Example Compressor 5HP', 'Example Heater 10kW', 'Example Controller PLC'],
            'Category': ['compressor', 'heater', 'controller'],
            'Quantity': [1, 2, 1],
            'Unit Price': [2500.00, 800.00, 3500.00],
            'Lead Time': [45, 30, 35],
            'Warranty': [24, 12, 36]
        }

        df = pd.DataFrame(template_data)
        csv = df.to_csv(index=False)

        st.download_button(
            label="📥 Download CSV Template",
            data=csv,
            file_name="supplier_quote_template.csv",
            mime="text/csv"
        )

    def render_manual_entry(self):
        """Render manual entry form"""
        st.subheader("➕ Manual Quote Entry")

        with st.form("manual_quote_entry"):
            st.markdown("### Supplier Information")
            col1, col2 = st.columns(2)

            with col1:
                supplier_name = st.text_input("Supplier Name *", placeholder="Company name")
                contact = st.text_input("Contact Person", placeholder="John Doe")
                email = st.text_input("Email", placeholder="contact@supplier.com")

            with col2:
                phone = st.text_input("Phone", placeholder="+1-555-0100")
                website = st.text_input("Website", placeholder="www.supplier.com")
                valid_until = st.date_input("Quote Valid Until")

            st.markdown("### Quote Items")

            # Dynamic item entry
            num_items = st.number_input("Number of items", min_value=1, max_value=20, value=3)

            items_data = []
            for i in range(int(num_items)):
                st.markdown(f"**Item {i+1}**")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    item_id = st.text_input(f"Item ID", key=f"id_{i}", placeholder=f"ITEM-{i+1}")
                    quantity = st.number_input(f"Quantity", key=f"qty_{i}", min_value=1, value=1)

                with col2:
                    description = st.text_input(f"Description", key=f"desc_{i}", placeholder="Item description")
                    unit_price = st.number_input(f"Unit Price", key=f"price_{i}", min_value=0.0, value=0.0, step=0.01)

                with col3:
                    category = st.selectbox(
                        f"Category",
                        options=[cat.value for cat in ItemCategory],
                        key=f"cat_{i}"
                    )
                    lead_time = st.number_input(f"Lead Time (days)", key=f"lead_{i}", min_value=0, value=30)

                with col4:
                    warranty = st.number_input(f"Warranty (months)", key=f"warranty_{i}", min_value=0, value=12)

                if description and unit_price > 0:
                    items_data.append({
                        'item_id': item_id or f"ITEM-{i+1}",
                        'description': description,
                        'category': category,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'lead_time': lead_time,
                        'warranty': warranty
                    })

            st.markdown("### Additional Details")
            col1, col2, col3 = st.columns(3)

            with col1:
                tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=8.0) / 100
            with col2:
                shipping = st.number_input("Shipping Cost", min_value=0.0, value=0.0, step=0.01)
            with col3:
                currency = st.selectbox("Currency", options=['USD', 'EUR', 'GBP', 'INR', 'CNY'])

            payment_terms = st.text_input("Payment Terms", placeholder="Net 30")
            notes = st.text_area("Notes")

            submitted = st.form_submit_button("✅ Save Quote", type="primary", use_container_width=True)

            if submitted:
                if not supplier_name:
                    st.error("Supplier name is required!")
                elif not items_data:
                    st.error("Please add at least one item!")
                else:
                    self._save_manual_quote(
                        supplier_name, contact, email, phone, website, str(valid_until),
                        items_data, tax_rate, shipping, currency, payment_terms, notes
                    )

    def _save_manual_quote(self, supplier_name, contact, email, phone, website, valid_until,
                          items_data, tax_rate, shipping, currency, payment_terms, notes):
        """Save manually entered quote"""
        if not self.db or not SupplierQuote or not QuoteItem:
            st.error("Database not initialized")
            return

        from datetime import datetime

        # Create quote items
        items = []
        for item_data in items_data:
            total = item_data['quantity'] * item_data['unit_price']
            items.append(QuoteItem(
                item_id=item_data['item_id'],
                description=item_data['description'],
                category=item_data['category'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total_price=total,
                currency=currency,
                lead_time_days=item_data['lead_time'],
                warranty_months=item_data['warranty']
            ))

        subtotal = sum(item.total_price for item in items)
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount + shipping

        # Create quote
        quote = SupplierQuote(
            quote_id=f"SUP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            supplier_name=supplier_name,
            contact_person=contact,
            email=email,
            phone=phone,
            website=website,
            items=items,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            shipping_cost=shipping,
            total_amount=total,
            currency=currency,
            valid_until=valid_until,
            payment_terms=payment_terms,
            notes=notes
        )

        self.db.add_supplier(quote)
        st.success(f"✅ Quote saved successfully! ID: {quote.quote_id}")
        st.session_state['show_manual_entry'] = False
        st.rerun()

    def render_supplier_list(self):
        """Render list of all suppliers"""
        st.subheader("📋 All Suppliers")

        if not self.db:
            st.warning("Database not initialized")
            return

        suppliers = self.db.list_suppliers()

        if not suppliers:
            st.info("No suppliers found. Upload your first quote!")
            return

        # Search bar
        search = st.text_input("🔍 Search suppliers", placeholder="Search by name or ID")

        if search:
            suppliers = self.db.search_suppliers(search)

        # Display suppliers
        for supplier in suppliers:
            with st.expander(f"**{supplier.supplier_name}** ({supplier.quote_id}) - ${supplier.total_amount:,.2f}"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"**Contact:** {supplier.contact_person or 'N/A'}")
                    st.markdown(f"**Email:** {supplier.email or 'N/A'}")
                    st.markdown(f"**Phone:** {supplier.phone or 'N/A'}")

                with col2:
                    st.markdown(f"**Items:** {len(supplier.items)}")
                    st.markdown(f"**Subtotal:** ${supplier.subtotal:,.2f}")
                    st.markdown(f"**Tax:** ${supplier.tax_amount:,.2f}")

                with col3:
                    st.markdown(f"**Shipping:** ${supplier.shipping_cost:,.2f}")
                    st.markdown(f"**Total:** ${supplier.total_amount:,.2f}")
                    st.markdown(f"**Valid Until:** {supplier.valid_until or 'N/A'}")

                if supplier.items:
                    st.markdown("**Items:**")
                    items_df = pd.DataFrame([{
                        'ID': item.item_id,
                        'Description': item.description,
                        'Qty': item.quantity,
                        'Price': f"${item.unit_price:.2f}",
                        'Total': f"${item.total_price:.2f}"
                    } for item in supplier.items])
                    st.dataframe(items_df, hide_index=True)

                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🗑️ Delete", key=f"del_{supplier.quote_id}"):
                        self.db.delete_supplier(supplier.quote_id)
                        st.rerun()

    def render_comparison(self):
        """Render quote comparison"""
        st.subheader("📊 Compare Quotes")

        if not self.db or not QuoteComparator:
            st.warning("Comparison not available")
            return

        suppliers = self.db.list_suppliers()

        if len(suppliers) < 2:
            st.info("You need at least 2 quotes to compare. Upload more quotes!")
            return

        # Select quotes to compare
        selected = st.multiselect(
            "Select quotes to compare",
            options=[f"{s.supplier_name} ({s.quote_id})" for s in suppliers],
            default=[f"{s.supplier_name} ({s.quote_id})" for s in suppliers[:min(3, len(suppliers))]]
        )

        if len(selected) < 2:
            st.warning("Please select at least 2 quotes")
            return

        # Get selected quote objects
        selected_ids = [s.split('(')[1].rstrip(')') for s in selected]
        selected_quotes = [self.db.get_supplier(qid) for qid in selected_ids]

        # Comparison
        comparison = QuoteComparator.compare_quotes(selected_quotes)

        # Display comparison
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Suppliers Compared", len(selected_quotes))
        with col2:
            st.metric("Lowest Total", f"${min(comparison['total_amounts']):,.2f}")
        with col3:
            st.metric("Highest Total", f"${max(comparison['total_amounts']):,.2f}")

        # Detailed comparison table
        comp_df = pd.DataFrame({
            'Supplier': comparison['suppliers'],
            'Total Amount': [f"${amt:,.2f}" for amt in comparison['total_amounts']],
            'Avg Lead Time': [f"{lt} days" for lt in comparison['lead_times']],
            'Avg Warranty': [f"{w} months" for w in comparison['warranty_periods']]
        })
        st.dataframe(comp_df, hide_index=True, use_container_width=True)

        # Best value analysis
        st.markdown("### 🏆 Best Value Analysis")
        best = QuoteComparator.find_best_value(selected_quotes)

        if best.get('best_value'):
            st.success(f"**Recommended:** {best['best_value']['supplier']} (Score: {best['best_value']['total_score']})")

            scores_df = pd.DataFrame(best['all_scores'])
            st.dataframe(scores_df, hide_index=True, use_container_width=True)


def render_supplier_management():
    """Main function to render supplier management UI"""
    st.title("📦 Supplier Database Manager")

    ui = SupplierUploadUI()

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload", "➕ Manual Entry", "📋 All Suppliers", "📊 Compare"])

    with tab1:
        ui.render_upload_section()

    with tab2:
        ui.render_manual_entry()

    with tab3:
        ui.render_supplier_list()

    with tab4:
        ui.render_comparison()


# For standalone testing
if __name__ == "__main__":
    render_supplier_management()
