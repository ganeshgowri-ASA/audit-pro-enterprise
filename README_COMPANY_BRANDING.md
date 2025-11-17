# 🎨 Feature: Company Branding Configuration

## Branch Information
- **Branch Name:** `claude/company-branding-01SEv5CMSXysveBjz1kGW6f8`
- **Merge Priority:** 2️⃣ (After core-calculations, before others)
- **Status:** ✅ Ready for Testing & Merge
- **Dependencies:** None (standalone configuration)

## What's in This Branch?

### 📁 Files Added:
```
config/
  ├── branding.json                    (Complete branding configuration)
  └── terms_and_conditions.txt         (Standard T&C template)

modules/
  └── branding_config.py               (Branding management module)

assets/
  ├── logos/                           (Company logos directory)
  ├── signatures/                      (Digital signatures)
  └── certifications/                  (Certification logos)
```

## 🎯 Purpose
Centralized branding configuration for:

1. **Company Identity** - Name, logo, colors, tagline
2. **Document Templates** - Quotes, invoices, technical specs
3. **Certifications** - ISO, CE, and other certifications
4. **Localization** - Currency, units, date formats
5. **UI Theming** - Streamlit theme generation
6. **Letterhead Generation** - HTML letterheads for PDFs

## 🚀 Quick Start

### Run Tests:
```bash
python modules/branding_config.py
```

### Example Usage:
```python
from modules.branding_config import BrandingConfig

# Load configuration
config = BrandingConfig("config/branding.json")

# Access company info
print(f"Company: {config.company_info.name}")
print(f"Address: {config.address.format_full()}")

# Get colors
print(f"Primary: {config.color_scheme.primary_color}")

# Generate letterhead HTML
letterhead_html = config.generate_letterhead_html()

# Get Streamlit theme
theme = config.get_theme_for_streamlit()

# Get document configuration
quote_config = config.get_document_config("quote")
```

## ✅ What's Configured

### Company Information:
```json
{
  "name": "Audit-Pro Enterprise",
  "tagline": "Precision Environmental Testing Solutions",
  "legal_name": "Audit-Pro Enterprise Systems Private Limited",
  "registration_number": "U29190KA2020PTC123456",
  "tax_id": "GST29AABCU9603R1ZN",
  "website": "www.auditpro-enterprise.com",
  "email": "info@auditpro-enterprise.com",
  "phone": "+91-80-1234-5678"
}
```

### Color Scheme:
- **Primary:** #1E3A8A (Deep Blue)
- **Secondary:** #3B82F6 (Blue)
- **Accent:** #10B981 (Green)
- **Text:** #1F2937 (Dark Gray)
- **Background:** #FFFFFF (White)

### Certifications Included:
1. **ISO 9001:2015** - Quality Management System
2. **ISO 14001:2015** - Environmental Management System
3. **CE Marking** - European Conformity

### Document Features:
- ✅ Customizable letterhead
- ✅ Header/footer templates
- ✅ Signature configuration
- ✅ Watermark support (optional)
- ✅ Page numbering
- ✅ Table of contents generation
- ✅ Certification badges on quotes

### Localization Settings:
- **Language:** English (default)
- **Currency:** INR (Indian Rupee)
- **Units:** Metric
- **Date Format:** DD/MM/YYYY
- **Time Format:** 24-hour

## 🔗 Integration Architecture

```
branding_config (This Branch)
       ↓
    Used by:
       ↓
  ┌────┼─────────────────┐
  ↓    ↓                 ↓
reports_export   quote_generator   virtual_hmi (UI)
  ↓              ↓                 ↓
PDF Gen    Branded Quotes    Themed Interface
```

### Integration Examples:

#### With Quote Generator:
```python
from modules.branding_config import BrandingConfig
from modules.quote_generator import QuoteEngine

config = BrandingConfig()
engine = QuoteEngine(branding=config)

# Quotes will automatically use company branding
quote = engine.generate_quote(...)
```

#### With Reports Export:
```python
from modules.branding_config import BrandingConfig
from utils.pdf_generator import PDFGenerator

config = BrandingConfig()
pdf = PDFGenerator(branding=config)

# PDFs will include letterhead, colors, certifications
pdf.generate_quote_pdf(quote_data, include_certifications=True)
```

#### With Streamlit UI:
```python
import streamlit as st
from modules.branding_config import BrandingConfig

config = BrandingConfig()
theme = config.get_theme_for_streamlit()

# Apply theme to Streamlit
st.set_page_config(
    page_title=config.company_info.name,
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 📊 Configuration Structure

### JSON Schema:
```json
{
  "company": {
    "name": "string",
    "tagline": "string",
    "legal_name": "string",
    "tax_id": "string",
    ...
  },
  "address": {
    "street": "string",
    "city": "string",
    "state": "string",
    "postal_code": "string",
    "country": "string"
  },
  "branding": {
    "primary_color": "#RRGGBB",
    "logo_path": "path/to/logo.png",
    "font_family": "string"
  },
  "certifications": [
    {
      "name": "ISO 9001:2015",
      "certificate_number": "string",
      "valid_until": "YYYY-MM-DD"
    }
  ],
  "features": {
    "watermark_enabled": boolean,
    "show_certifications_on_quotes": boolean
  }
}
```

## 🎨 Customization

### Update Company Info:
```python
config.update_company_info(
    name="New Company Name",
    tagline="New Tagline",
    phone="+1-555-0100"
)
```

### Update Colors:
```python
config.update_colors(
    primary_color="#FF0000",
    accent_color="#00FF00"
)
```

### Add Certification:
```python
from modules.branding_config import Certification

new_cert = Certification(
    name="UL Certification",
    description="Safety Certification",
    certificate_number="UL-2025-001",
    issuing_authority="Underwriters Laboratories",
    valid_until="2028-12-31"
)

config.add_certification(new_cert)
```

## 🔮 Future Enhancements

### Phase 2 (Post-Merge):
```python
# Multi-language support
config.set_language("hi")  # Hindi
config.set_language("zh")  # Chinese

# Multiple branding profiles
config.load_profile("enterprise")  # Enterprise branding
config.load_profile("startup")     # Startup branding

# Dynamic logo generation
config.generate_logo_variants(
    sizes=[100, 200, 500],
    formats=["png", "svg", "ico"]
)

# Email templates
config.get_email_template("quote_sent")
config.get_email_template("invoice_reminder")

# Social media assets
config.generate_social_media_banner("linkedin")
config.generate_profile_picture(256)
```

### Planned Features:
- 🌍 Multi-language UI (Hindi, Chinese, German, Spanish)
- 🎭 Multiple branding profiles for different markets
- 📧 Email template management
- 🖼️ Automatic logo variant generation
- 📱 Social media asset generator
- 🎨 Theme preview in real-time
- 📄 Custom document template editor

## 🧪 Testing Checklist

Before merging, verify:
- [ ] Configuration file loads without errors
- [ ] Company info is displayed correctly
- [ ] Color scheme generates valid CSS
- [ ] Letterhead HTML renders properly
- [ ] Streamlit theme is applied
- [ ] Certifications are listed
- [ ] Localization settings work
- [ ] Configuration can be updated and saved
- [ ] Logo base64 encoding works (when logo file exists)

## 📖 API Reference

### Classes:

**BrandingConfig**
- `load_config()` - Load configuration from JSON
- `save_config()` - Save configuration to JSON
- `get_logo_base64(logo_type)` - Get logo as base64
- `get_document_config(doc_type)` - Get document settings
- `get_theme_for_streamlit()` - Generate Streamlit theme
- `generate_letterhead_html()` - Generate HTML letterhead
- `update_company_info(**kwargs)` - Update company details
- `update_colors(**kwargs)` - Update color scheme
- `add_certification(cert)` - Add certification
- `remove_certification(cert_number)` - Remove certification

**ColorScheme**
- `to_css_variables()` - Generate CSS custom properties

**Address**
- `format_full()` - Full address string
- `format_short()` - Short address string

## 🛡️ Code Quality
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings
- ✅ JSON schema validation
- ✅ Error handling
- ✅ Production-ready code

## 🔄 Merge Process

### Step 1: Test the Module
```bash
git checkout claude/company-branding-01SEv5CMSXysveBjz1kGW6f8
python modules/branding_config.py
```

### Step 2: Customize (Optional)
Edit `config/branding.json` with your company details

### Step 3: Merge to Main (After core-calculations)
```bash
git checkout main
git merge claude/company-branding-01SEv5CMSXysveBjz1kGW6f8
git push origin main
```

### Step 4: Add Your Logos
```bash
# Place your company logos
cp your_logo.png assets/logos/company_logo.png
cp your_logo_small.png assets/logos/company_logo_small.png
cp favicon.ico assets/logos/favicon.ico

# Place certifications
cp iso9001.png assets/certifications/iso9001.png
```

## 📞 Support
- **Module Author:** Audit-Pro Enterprise Team
- **Version:** 1.0.0
- **Python Requirement:** 3.7+
- **External Dependencies:** None (core functionality)

---

## ⚡ Why This Matters

1. **Professional Appearance** - Consistent branding across all documents
2. **Easy Customization** - Change colors/logos in one place
3. **Multi-tenant Ready** - Support multiple branding profiles
4. **PDF Generation** - Branded letterheads and certificates
5. **UI Consistency** - Streamlit apps use same branding

## 🎉 Next Steps

After this branch is merged:
1. ✅ All reports will use company branding
2. ✅ Quotes will include company logo and certifications
3. ✅ UI will have consistent colors and theme
4. ✅ PDFs will have professional letterheads

**Make it yours! Customize the branding and stand out! 🎨✨**
