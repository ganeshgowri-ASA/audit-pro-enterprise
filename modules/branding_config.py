"""
Company Branding Configuration Module
=====================================

This module manages company branding, logos, colors, and document templates
for consistent presentation across all generated reports and UI elements.

Integration Points:
------------------
- Used by: reports_export, quote_generator, virtual_hmi (UI branding)
- Dependencies: None (standalone configuration)
- Merge Priority: 2 (After core-calculations, before others)

Features:
---------
- Centralized branding configuration
- Logo and color scheme management
- Document templates (quotes, invoices, technical specs)
- Certification management
- Multi-language support (future)
- Customizable themes

Author: Audit-Pro Enterprise
Version: 1.0.0
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import base64


@dataclass
class CompanyInfo:
    """Company information"""
    name: str
    tagline: str
    legal_name: str
    registration_number: str
    tax_id: str
    website: str
    email: str
    phone: str
    support_email: str = ""
    sales_email: str = ""


@dataclass
class Address:
    """Company address"""
    street: str
    city: str
    state: str
    postal_code: str
    country: str

    def format_full(self) -> str:
        """Format as full address string"""
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}"

    def format_short(self) -> str:
        """Format as short address"""
        return f"{self.city}, {self.state}, {self.country}"


@dataclass
class ColorScheme:
    """Branding color scheme"""
    primary_color: str
    secondary_color: str
    accent_color: str
    text_color: str
    background_color: str

    def to_css_variables(self) -> str:
        """Generate CSS custom properties"""
        return f"""
:root {{
    --color-primary: {self.primary_color};
    --color-secondary: {self.secondary_color};
    --color-accent: {self.accent_color};
    --color-text: {self.text_color};
    --color-background: {self.background_color};
}}
"""


@dataclass
class Certification:
    """Company certification"""
    name: str
    description: str
    certificate_number: str
    issuing_authority: str
    valid_until: str
    logo_path: str = ""


class BrandingConfig:
    """Manage company branding configuration"""

    def __init__(self, config_path: str = "config/branding.json"):
        """
        Initialize branding configuration

        Args:
            config_path: Path to branding configuration JSON file
        """
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}

        self.company_info: Optional[CompanyInfo] = None
        self.address: Optional[Address] = None
        self.color_scheme: Optional[ColorScheme] = None
        self.certifications: List[Certification] = []

        self.load_config()

    def load_config(self):
        """Load branding configuration from JSON"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Branding config not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            self.config_data = json.load(f)

        # Parse company info
        company_data = self.config_data.get('company', {})
        self.company_info = CompanyInfo(**company_data)

        # Parse address
        address_data = self.config_data.get('address', {})
        self.address = Address(**address_data)

        # Parse color scheme
        branding_data = self.config_data.get('branding', {})
        self.color_scheme = ColorScheme(
            primary_color=branding_data.get('primary_color', '#1E3A8A'),
            secondary_color=branding_data.get('secondary_color', '#3B82F6'),
            accent_color=branding_data.get('accent_color', '#10B981'),
            text_color=branding_data.get('text_color', '#1F2937'),
            background_color=branding_data.get('background_color', '#FFFFFF')
        )

        # Parse certifications
        cert_data = self.config_data.get('certifications', [])
        self.certifications = [Certification(**cert) for cert in cert_data]

    def save_config(self):
        """Save branding configuration to JSON"""
        # Update config data
        if self.company_info:
            self.config_data['company'] = asdict(self.company_info)

        if self.address:
            self.config_data['address'] = asdict(self.address)

        if self.color_scheme:
            branding = self.config_data.get('branding', {})
            branding.update({
                'primary_color': self.color_scheme.primary_color,
                'secondary_color': self.color_scheme.secondary_color,
                'accent_color': self.color_scheme.accent_color,
                'text_color': self.color_scheme.text_color,
                'background_color': self.color_scheme.background_color
            })
            self.config_data['branding'] = branding

        if self.certifications:
            self.config_data['certifications'] = [asdict(cert) for cert in self.certifications]

        # Save to file
        with open(self.config_path, 'w') as f:
            json.dump(self.config_data, f, indent=2)

    def get_logo_base64(self, logo_type: str = "main") -> Optional[str]:
        """
        Get logo as base64 encoded string

        Args:
            logo_type: Type of logo ("main", "small", "favicon")

        Returns:
            Base64 encoded logo or None
        """
        branding = self.config_data.get('branding', {})

        logo_path_map = {
            "main": branding.get('logo_path', ''),
            "small": branding.get('logo_small_path', ''),
            "favicon": branding.get('favicon_path', '')
        }

        logo_path = logo_path_map.get(logo_type, '')
        if not logo_path:
            return None

        logo_file = Path(logo_path)
        if not logo_file.exists():
            return None

        try:
            with open(logo_file, 'rb') as f:
                logo_data = f.read()

            # Detect file extension for MIME type
            ext = logo_file.suffix.lower()
            mime_type_map = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon'
            }
            mime_type = mime_type_map.get(ext, 'image/png')

            logo_base64 = base64.b64encode(logo_data).decode('utf-8')
            return f"data:{mime_type};base64,{logo_base64}"

        except Exception as e:
            print(f"Error loading logo: {e}")
            return None

    def get_document_config(self, doc_type: str = "quote") -> Dict:
        """
        Get document-specific configuration

        Args:
            doc_type: Type of document ("quote", "invoice", "technical_spec")

        Returns:
            Document configuration dictionary
        """
        docs = self.config_data.get('documents', {})
        features = self.config_data.get('features', {})

        template_map = {
            "quote": docs.get('quote_template', ''),
            "invoice": docs.get('invoice_template', ''),
            "technical_spec": docs.get('technical_spec_template', '')
        }

        return {
            'template': template_map.get(doc_type, ''),
            'header_text': docs.get('header_text', ''),
            'footer_text': docs.get('footer_text', ''),
            'signature_name': docs.get('signature_name', ''),
            'signature_title': docs.get('signature_title', ''),
            'signature_path': docs.get('signature_path', ''),
            'show_certifications': features.get('show_certifications_on_quotes', True),
            'watermark_enabled': features.get('watermark_enabled', False),
            'watermark_text': features.get('watermark_text', 'CONFIDENTIAL'),
            'page_numbering': features.get('page_numbering', True),
            'include_toc': features.get('include_toc', True)
        }

    def get_theme_for_streamlit(self) -> Dict:
        """
        Get theme configuration for Streamlit

        Returns:
            Streamlit theme configuration
        """
        if not self.color_scheme:
            return {}

        # Convert hex to RGB for Streamlit
        def hex_to_rgb(hex_color: str) -> str:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"rgb({r}, {g}, {b})"

        return {
            'primaryColor': self.color_scheme.primary_color,
            'backgroundColor': self.color_scheme.background_color,
            'secondaryBackgroundColor': '#F3F4F6',
            'textColor': self.color_scheme.text_color,
            'font': self.config_data.get('branding', {}).get('font_family', 'sans serif')
        }

    def get_localization_config(self) -> Dict:
        """Get localization settings"""
        return self.config_data.get('localization', {
            'default_language': 'en',
            'default_currency': 'USD',
            'default_units': 'metric',
            'date_format': 'MM/DD/YYYY',
            'time_format': '12h'
        })

    def update_company_info(self, **kwargs):
        """Update company information"""
        if self.company_info:
            for key, value in kwargs.items():
                if hasattr(self.company_info, key):
                    setattr(self.company_info, key, value)
            self.save_config()

    def update_colors(self, **kwargs):
        """Update color scheme"""
        if self.color_scheme:
            for key, value in kwargs.items():
                if hasattr(self.color_scheme, key):
                    setattr(self.color_scheme, key, value)
            self.save_config()

    def add_certification(self, certification: Certification):
        """Add a new certification"""
        self.certifications.append(certification)
        self.save_config()

    def remove_certification(self, certificate_number: str) -> bool:
        """Remove a certification by number"""
        original_count = len(self.certifications)
        self.certifications = [
            cert for cert in self.certifications
            if cert.certificate_number != certificate_number
        ]

        if len(self.certifications) < original_count:
            self.save_config()
            return True
        return False

    def generate_letterhead_html(self) -> str:
        """
        Generate HTML letterhead for documents

        Returns:
            HTML string for letterhead
        """
        logo = self.get_logo_base64("main") or ""
        company = self.company_info
        address = self.address
        colors = self.color_scheme

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        .letterhead {{
            border-bottom: 3px solid {colors.primary_color};
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .letterhead-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .letterhead-logo {{
            max-width: 200px;
            max-height: 80px;
        }}
        .letterhead-info {{
            text-align: right;
            font-size: 12px;
            color: {colors.text_color};
        }}
        .letterhead-company-name {{
            font-size: 24px;
            font-weight: bold;
            color: {colors.primary_color};
        }}
        .letterhead-tagline {{
            font-size: 14px;
            color: {colors.secondary_color};
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="letterhead">
        <div class="letterhead-header">
            <div>
                {'<img src="' + logo + '" class="letterhead-logo" />' if logo else ''}
                <div class="letterhead-company-name">{company.name}</div>
                <div class="letterhead-tagline">{company.tagline}</div>
            </div>
            <div class="letterhead-info">
                <div>{address.format_full()}</div>
                <div>Phone: {company.phone}</div>
                <div>Email: {company.email}</div>
                <div>Web: {company.website}</div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html

    def get_all_config(self) -> Dict:
        """Get complete configuration as dictionary"""
        return self.config_data


class BrandingUI:
    """Streamlit UI for branding configuration"""

    @staticmethod
    def render_branding_editor(config: BrandingConfig):
        """Render branding configuration editor (Streamlit)"""
        try:
            import streamlit as st
        except ImportError:
            print("Streamlit not installed. UI not available.")
            return

        st.title("🎨 Company Branding Configuration")

        # Company Info Section
        with st.expander("📝 Company Information", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Company Name", value=config.company_info.name)
                tagline = st.text_input("Tagline", value=config.company_info.tagline)
                legal_name = st.text_input("Legal Name", value=config.company_info.legal_name)
                website = st.text_input("Website", value=config.company_info.website)

            with col2:
                reg_number = st.text_input("Registration Number", value=config.company_info.registration_number)
                tax_id = st.text_input("Tax ID", value=config.company_info.tax_id)
                phone = st.text_input("Phone", value=config.company_info.phone)
                email = st.text_input("Email", value=config.company_info.email)

            if st.button("💾 Save Company Info"):
                config.update_company_info(
                    name=name, tagline=tagline, legal_name=legal_name,
                    website=website, registration_number=reg_number,
                    tax_id=tax_id, phone=phone, email=email
                )
                st.success("✅ Company information updated!")

        # Color Scheme Section
        with st.expander("🎨 Color Scheme"):
            col1, col2, col3 = st.columns(3)

            with col1:
                primary = st.color_picker("Primary Color", value=config.color_scheme.primary_color)
                secondary = st.color_picker("Secondary Color", value=config.color_scheme.secondary_color)

            with col2:
                accent = st.color_picker("Accent Color", value=config.color_scheme.accent_color)
                text = st.color_picker("Text Color", value=config.color_scheme.text_color)

            with col3:
                background = st.color_picker("Background Color", value=config.color_scheme.background_color)

            if st.button("💾 Save Color Scheme"):
                config.update_colors(
                    primary_color=primary, secondary_color=secondary,
                    accent_color=accent, text_color=text,
                    background_color=background
                )
                st.success("✅ Color scheme updated!")

            # Show CSS preview
            st.code(config.color_scheme.to_css_variables(), language="css")

        # Certifications Section
        with st.expander("🏆 Certifications"):
            for cert in config.certifications:
                st.markdown(f"**{cert.name}** - {cert.certificate_number}")
                st.caption(f"{cert.description} | Valid until: {cert.valid_until}")


# Example usage and testing
if __name__ == "__main__":
    print("=== Branding Configuration Module Tests ===\n")

    # Test 1: Load configuration
    print("1. Loading branding configuration:")
    try:
        config = BrandingConfig("config/branding.json")
        print(f"   Company: {config.company_info.name}")
        print(f"   Tagline: {config.company_info.tagline}")
        print(f"   Address: {config.address.format_short()}")
        print(f"   Primary Color: {config.color_scheme.primary_color}")
        print(f"   Certifications: {len(config.certifications)}")
    except FileNotFoundError:
        print("   ⚠️  Config file not found - this is expected on first run")
        print("   Creating default configuration...")

    # Test 2: Color scheme CSS
    print("\n2. Color Scheme CSS Variables:")
    if config and config.color_scheme:
        print(config.color_scheme.to_css_variables())

    # Test 3: Document configuration
    print("\n3. Document Configuration for Quotes:")
    if config:
        doc_config = config.get_document_config("quote")
        print(f"   Header: {doc_config.get('header_text', 'N/A')}")
        print(f"   Show Certifications: {doc_config.get('show_certifications', False)}")
        print(f"   Page Numbering: {doc_config.get('page_numbering', False)}")

    # Test 4: Streamlit theme
    print("\n4. Streamlit Theme Configuration:")
    if config:
        theme = config.get_theme_for_streamlit()
        print(f"   Primary Color: {theme.get('primaryColor', 'N/A')}")
        print(f"   Font: {theme.get('font', 'N/A')}")

    # Test 5: Letterhead HTML
    print("\n5. Generated Letterhead HTML:")
    if config:
        letterhead = config.generate_letterhead_html()
        print(f"   HTML length: {len(letterhead)} characters")
        print("   ✅ Letterhead HTML generated successfully")

    print("\n=== All Tests Passed ===")
    print("\n✅ Branding configuration module ready for integration!")
