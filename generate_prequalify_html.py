#!/usr/bin/env python3
"""Generate prequalify.html — 4-step prequalification wizard for Pure Capital US LLC."""

from pathlib import Path

INDUSTRIES = [
    "Accounting & Bookkeeping", "Agriculture", "Automotive", "Construction",
    "Consulting", "E-commerce / Online Retail", "Education", "Entertainment & Media",
    "Financial Services", "Food & Beverage / Restaurant", "Healthcare & Medical",
    "Hospitality & Hotels", "Insurance", "Legal Services", "Manufacturing",
    "Marketing & Advertising", "Non-Profit", "Professional Services", "Real Estate",
    "Retail", "Staffing & Recruiting", "Technology", "Transportation & Logistics",
    "Wholesale & Distribution", "Other",
]

LEGAL_ENTITIES = [
    "Sole Proprietorship", "LLC", "Corporation (C-Corp)", "S-Corporation",
    "General Partnership", "Limited Partnership", "Other",
]

FICO_RANGES = [
    ("", "Select FICO range…"),
    ("720+", "720+ (Excellent)"),
    ("680-719", "680–719 (Good)"),
    ("640-679", "640–679 (Fair)"),
    ("600-639", "600–639 (Below Average)"),
    ("Below 600", "Below 600"),
    ("Unknown", "Unknown / Not Sure"),
]


def options(items):
    if isinstance(items[0], tuple):
        return "\n".join(
            f'                <option value="{v}">{label}</option>' for v, label in items
        )
    return "\n".join(f'                <option value="{item}">{item}</option>' for item in items)


def mca_rows(n=5):
    rows = []
    for i in range(1, n + 1):
        rows.append(f"""              <tr>
                <td><input type="text" name="mca_lender_{i}" placeholder="Lender name" /></td>
                <td><input type="text" name="mca_original_{i}" placeholder="$0" inputmode="decimal" /></td>
                <td><input type="text" name="mca_balance_{i}" placeholder="$0" inputmode="decimal" /></td>
                <td><input type="text" name="mca_payment_{i}" placeholder="$0/day or week" inputmode="decimal" /></td>
                <td>
                  <select name="mca_status_{i}">
                    <option value="">—</option>
                    <option value="Active">Active</option>
                    <option value="Paid Off">Paid Off</option>
                  </select>
                </td>
              </tr>""")
    return "\n".join(rows)


def re_rows(n=3):
    rows = []
    for i in range(1, n + 1):
        rows.append(f"""              <tr>
                <td><input type="text" name="re_address_{i}" placeholder="Street, City, State" /></td>
                <td>
                  <select name="re_type_{i}">
                    <option value="">—</option>
                    <option value="Primary Residence">Primary Residence</option>
                    <option value="Investment Property">Investment Property</option>
                    <option value="Commercial">Commercial</option>
                    <option value="Land">Land</option>
                    <option value="Other">Other</option>
                  </select>
                </td>
                <td><input type="text" name="re_value_{i}" placeholder="$0" inputmode="decimal" /></td>
                <td><input type="text" name="re_mortgage_{i}" placeholder="$0" inputmode="decimal" /></td>
                <td><input type="text" name="re_payment_{i}" placeholder="$0/mo" inputmode="decimal" /></td>
              </tr>""")
    return "\n".join(rows)


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Business Prequalification | Pure Capital US LLC</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <a href="#prequalification" class="skip-link">Skip to prequalification form</a>

  <header class="site-header">
    <div class="header-container">
      <a href="index.html" class="logo">
        <img src="assets/IMG_20260531_000449-removebg-preview.png" alt="Pure Capital US LLC — business funding" width="180" height="52" />
      </a>
      <nav class="main-nav" aria-label="Main navigation">
        <ul>
          <li><a href="index.html#solutions">Solutions</a></li>
          <li><a href="index.html#process">How It Works</a></li>
          <li><a href="index.html#about">About</a></li>
          <li><a href="index.html#contact">Contact</a></li>
        </ul>
      </nav>
      <div class="header-actions">
        <a href="index.html#apply" class="btn btn-primary">Apply Now</a>
      </div>
      <button class="menu-toggle" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <nav class="mobile-nav" aria-label="Mobile navigation">
    <ul>
      <li><a href="index.html#solutions">Solutions</a></li>
      <li><a href="index.html#process">How It Works</a></li>
      <li><a href="index.html#about">About</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
  </nav>

  <main id="main-content">
  <section class="form-page" id="prequalification">
    <div class="form-page-container form-page-container-wide">
      <div class="form-page-header">
        <h1>Business Funding Prequalification</h1>
        <p>Complete this 4-step prequalification form. Fields marked with * are required. Moving forward with funding? This form helps us evaluate your business quickly.</p>
      </div>

      <div class="form-page-card">
        <div class="form-message" role="alert"></div>

        <ol class="prequal-progress" aria-label="Form progress">
          <li class="prequal-progress-step active" data-step="1"><span class="step-num">1</span><span class="step-label">Company Info</span></li>
          <li class="prequal-progress-step" data-step="2"><span class="step-num">2</span><span class="step-label">Owner Info</span></li>
          <li class="prequal-progress-step" data-step="3"><span class="step-num">3</span><span class="step-label">Co-Owner / MCA / RE</span></li>
          <li class="prequal-progress-step" data-step="4"><span class="step-num">4</span><span class="step-label">Docs &amp; Signatures</span></li>
        </ol>

        <form class="prequal-form application-form" id="prequal-form" action="process_prequalify.php" method="POST" enctype="multipart/form-data" novalidate>
          <input type="hidden" name="source_page" value="prequalify.html" />
          <input type="hidden" name="owner_signature_data" id="owner_signature_data" value="" />
          <input type="hidden" name="co_owner_signature_data" id="co_owner_signature_data" value="" />

          <div class="prequal-step-panel active" data-step="1">
            <h2 class="form-section-title">Company Information</h2>
            <div class="form-group">
              <label for="business_legal_name">Business Legal Name <span class="required">*</span></label>
              <input type="text" id="business_legal_name" name="business_legal_name" required autocomplete="organization" />
            </div>
            <div class="form-group">
              <label for="dba">DBA (Doing Business As)</label>
              <input type="text" id="dba" name="dba" placeholder="If different from legal name" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="industry">Industry <span class="required">*</span></label>
                <select id="industry" name="industry" required>
                  <option value="" selected>Select industry…</option>
{industry_options}
                </select>
              </div>
              <div class="form-group hidden" id="industry-other-group">
                <label for="industry_other">Specify Industry <span class="required">*</span></label>
                <input type="text" id="industry_other" name="industry_other" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="legal_entity">Legal Entity Type <span class="required">*</span></label>
                <select id="legal_entity" name="legal_entity" required>
                  <option value="" selected>Select entity type…</option>
{legal_options}
                </select>
              </div>
              <div class="form-group hidden" id="legal-entity-other-group">
                <label for="legal_entity_other">Specify Entity Type <span class="required">*</span></label>
                <input type="text" id="legal_entity_other" name="legal_entity_other" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="business_start_date">Business Start Date <span class="required">*</span></label>
                <input type="date" id="business_start_date" name="business_start_date" required />
              </div>
              <div class="form-group">
                <label for="ein">EIN / Tax ID <span class="required">*</span></label>
                <input type="text" id="ein" name="ein" required placeholder="XX-XXXXXXX" maxlength="10" />
              </div>
            </div>
            <div class="form-group">
              <label for="website">Website</label>
              <input type="url" id="website" name="website" placeholder="https://" autocomplete="url" />
            </div>
            <h3 class="form-subsection-title">Company Address</h3>
            <div class="form-group">
              <label for="company_street">Street Address <span class="required">*</span></label>
              <input type="text" id="company_street" name="company_street" required autocomplete="street-address" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="company_city">City <span class="required">*</span></label>
                <input type="text" id="company_city" name="company_city" required autocomplete="address-level2" />
              </div>
              <div class="form-group">
                <label for="company_state">State <span class="required">*</span></label>
                <input type="text" id="company_state" name="company_state" required autocomplete="address-level1" maxlength="2" placeholder="NY" />
              </div>
              <div class="form-group">
                <label for="company_zip">ZIP <span class="required">*</span></label>
                <input type="text" id="company_zip" name="company_zip" required autocomplete="postal-code" maxlength="10" />
              </div>
            </div>
            <fieldset class="form-group">
              <legend>Preferred Contact Method <span class="required">*</span></legend>
              <div class="radio-group">
                <label class="radio-label"><input type="radio" name="contact_method" value="Email" required /> Email</label>
                <label class="radio-label"><input type="radio" name="contact_method" value="Phone" /> Phone</label>
                <label class="radio-label"><input type="radio" name="contact_method" value="Text" /> Text</label>
              </div>
            </fieldset>
            <div class="form-row">
              <div class="form-group">
                <label for="business_email">Business Email <span class="required">*</span></label>
                <input type="email" id="business_email" name="business_email" required autocomplete="email" />
              </div>
              <div class="form-group">
                <label for="business_phone">Business Phone <span class="required">*</span></label>
                <input type="tel" id="business_phone" name="business_phone" required autocomplete="tel" placeholder="(347) 201-2166" />
              </div>
            </div>
          </div>

          <div class="prequal-step-panel" data-step="2" hidden>
            <h2 class="form-section-title">Primary Owner Information</h2>
            <div class="form-row">
              <div class="form-group">
                <label for="owner_first_name">First Name <span class="required">*</span></label>
                <input type="text" id="owner_first_name" name="owner_first_name" required autocomplete="given-name" />
              </div>
              <div class="form-group">
                <label for="owner_last_name">Last Name <span class="required">*</span></label>
                <input type="text" id="owner_last_name" name="owner_last_name" required autocomplete="family-name" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="ownership_pct">Ownership Percentage <span class="required">*</span></label>
                <input type="number" id="ownership_pct" name="ownership_pct" required min="1" max="100" placeholder="%" />
              </div>
              <div class="form-group">
                <label for="owner_dob">Date of Birth <span class="required">*</span></label>
                <input type="date" id="owner_dob" name="owner_dob" required />
              </div>
            </div>
            <div class="form-group">
              <label for="owner_ssn">Social Security Number <span class="required">*</span></label>
              <input type="text" id="owner_ssn" name="owner_ssn" required autocomplete="off" inputmode="numeric" placeholder="XXX-XX-XXXX" maxlength="11" class="ssn-input" />
            </div>
            <h3 class="form-subsection-title">Home Address</h3>
            <div class="form-group">
              <label for="owner_street">Street Address <span class="required">*</span></label>
              <input type="text" id="owner_street" name="owner_street" required autocomplete="street-address" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="owner_city">City <span class="required">*</span></label>
                <input type="text" id="owner_city" name="owner_city" required autocomplete="address-level2" />
              </div>
              <div class="form-group">
                <label for="owner_state">State <span class="required">*</span></label>
                <input type="text" id="owner_state" name="owner_state" required autocomplete="address-level1" maxlength="2" />
              </div>
              <div class="form-group">
                <label for="owner_zip">ZIP <span class="required">*</span></label>
                <input type="text" id="owner_zip" name="owner_zip" required autocomplete="postal-code" maxlength="10" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="owner_email">Email <span class="required">*</span></label>
                <input type="email" id="owner_email" name="owner_email" required autocomplete="email" />
              </div>
              <div class="form-group">
                <label for="owner_mobile">Mobile Phone <span class="required">*</span></label>
                <input type="tel" id="owner_mobile" name="owner_mobile" required autocomplete="tel" class="phone-input" />
              </div>
            </div>
            <div class="form-group">
              <label for="owner_fico">Estimated FICO Score <span class="required">*</span></label>
              <select id="owner_fico" name="owner_fico" required>
{fico_options}
              </select>
            </div>
          </div>

          <div class="prequal-step-panel" data-step="3" hidden>
            <h2 class="form-section-title">Co-Owner Information <span class="optional-tag">(Optional)</span></h2>
            <p class="form-help-text">Complete if there is an additional owner with 20% or more ownership.</p>
            <div class="form-row">
              <div class="form-group">
                <label for="co_owner_first_name">First Name</label>
                <input type="text" id="co_owner_first_name" name="co_owner_first_name" autocomplete="given-name" />
              </div>
              <div class="form-group">
                <label for="co_owner_last_name">Last Name</label>
                <input type="text" id="co_owner_last_name" name="co_owner_last_name" autocomplete="family-name" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="co_ownership_pct">Ownership %</label>
                <input type="number" id="co_ownership_pct" name="co_ownership_pct" min="0" max="100" />
              </div>
              <div class="form-group">
                <label for="co_owner_dob">Date of Birth</label>
                <input type="date" id="co_owner_dob" name="co_owner_dob" />
              </div>
            </div>
            <div class="form-group">
              <label for="co_owner_ssn">Social Security Number</label>
              <input type="text" id="co_owner_ssn" name="co_owner_ssn" autocomplete="off" inputmode="numeric" placeholder="XXX-XX-XXXX" maxlength="11" class="ssn-input" />
            </div>
            <div class="form-group">
              <label for="co_owner_street">Home Street Address</label>
              <input type="text" id="co_owner_street" name="co_owner_street" autocomplete="street-address" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="co_owner_city">City</label>
                <input type="text" id="co_owner_city" name="co_owner_city" autocomplete="address-level2" />
              </div>
              <div class="form-group">
                <label for="co_owner_state">State</label>
                <input type="text" id="co_owner_state" name="co_owner_state" autocomplete="address-level1" maxlength="2" />
              </div>
              <div class="form-group">
                <label for="co_owner_zip">ZIP</label>
                <input type="text" id="co_owner_zip" name="co_owner_zip" autocomplete="postal-code" maxlength="10" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="co_owner_email">Email</label>
                <input type="email" id="co_owner_email" name="co_owner_email" autocomplete="email" />
              </div>
              <div class="form-group">
                <label for="co_owner_mobile">Mobile Phone</label>
                <input type="tel" id="co_owner_mobile" name="co_owner_mobile" autocomplete="tel" class="phone-input" />
              </div>
            </div>
            <div class="form-group">
              <label for="co_owner_fico">Estimated FICO Score</label>
              <select id="co_owner_fico" name="co_owner_fico">
{fico_options}
              </select>
            </div>
            <h2 class="form-section-title">Existing Merchant Cash Advances (MCA)</h2>
            <p class="form-help-text">List any active or recent MCA positions. Leave blank if none.</p>
            <div class="table-scroll">
            <table class="data-table">
              <thead><tr><th>Lender / Funder</th><th>Original Amount</th><th>Current Balance</th><th>Daily / Weekly Payment</th><th>Status</th></tr></thead>
              <tbody>{mca_rows}</tbody>
            </table>
            </div>
            <h2 class="form-section-title">Real Estate Owned</h2>
            <p class="form-help-text">List up to 3 properties. Leave blank if none.</p>
            <div class="table-scroll">
            <table class="data-table">
              <thead><tr><th>Property Address</th><th>Type</th><th>Est. Value</th><th>Mortgage Balance</th><th>Monthly Payment</th></tr></thead>
              <tbody>{re_rows}</tbody>
            </table>
            </div>
          </div>

          <div class="prequal-step-panel" data-step="4" hidden>
            <h2 class="form-section-title">Required Documents</h2>
            <p class="form-help-text">Upload PDF or image files (max 10 MB each). Bank statements should be the most recent consecutive months.</p>
            <div class="form-row">
              <div class="form-group">
                <label for="bank_statement_1">Bank Statement — Month 1 <span class="required">*</span></label>
                <input type="file" id="bank_statement_1" name="bank_statement_1" required accept=".pdf,.jpg,.jpeg,.png" class="file-input" />
              </div>
              <div class="form-group">
                <label for="bank_statement_2">Bank Statement — Month 2 <span class="required">*</span></label>
                <input type="file" id="bank_statement_2" name="bank_statement_2" required accept=".pdf,.jpg,.jpeg,.png" class="file-input" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="bank_statement_3">Bank Statement — Month 3</label>
                <input type="file" id="bank_statement_3" name="bank_statement_3" accept=".pdf,.jpg,.jpeg,.png" class="file-input" />
              </div>
              <div class="form-group">
                <label for="bank_statement_4">Bank Statement — Month 4</label>
                <input type="file" id="bank_statement_4" name="bank_statement_4" accept=".pdf,.jpg,.jpeg,.png" class="file-input" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="voided_check">Voided Check <span class="required">*</span></label>
                <input type="file" id="voided_check" name="voided_check" required accept=".pdf,.jpg,.jpeg,.png" class="file-input" />
              </div>
              <div class="form-group">
                <label for="owner_id">Owner Government ID <span class="required">*</span></label>
                <input type="file" id="owner_id" name="owner_id" required accept=".pdf,.jpg,.jpeg,.png" class="file-input" />
              </div>
            </div>
            <div class="form-group">
              <label for="co_owner_id">Co-Owner Government ID <span class="optional-tag">(if applicable)</span></label>
              <input type="file" id="co_owner_id" name="co_owner_id" accept=".pdf,.jpg,.jpeg,.png" class="file-input" />
            </div>
            <h2 class="form-section-title">Authorization &amp; Signatures</h2>
            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" id="terms_accepted" name="terms_accepted" value="1" required />
                I certify that the information provided is true and accurate. I authorize Pure Capital US LLC to obtain credit reports, verify financial information, and contact references as needed to evaluate this prequalification request. I agree to the <a href="terms.html" target="_blank" rel="noopener">Terms of Use</a> and <a href="privacy.html" target="_blank" rel="noopener">Privacy Policy</a>. <span class="required">*</span>
              </label>
            </div>
            <div class="signature-block">
              <label>Primary Owner Signature <span class="required">*</span></label>
              <p class="form-help-text">Sign below with your mouse or finger, or type your full legal name.</p>
              <div class="signature-pad-wrapper">
                <canvas id="owner-signature-pad" class="signature-pad" width="500" height="150" aria-label="Owner signature pad"></canvas>
                <button type="button" class="btn btn-outline btn-sm signature-clear" data-pad="owner">Clear Signature</button>
              </div>
              <div class="form-group">
                <label for="owner_signature_name">Or type full legal name</label>
                <input type="text" id="owner_signature_name" name="owner_signature_name" placeholder="Full legal name as signature" />
              </div>
            </div>
            <div class="signature-block">
              <label>Co-Owner Signature <span class="optional-tag">(if applicable)</span></label>
              <div class="signature-pad-wrapper">
                <canvas id="co-owner-signature-pad" class="signature-pad" width="500" height="150" aria-label="Co-owner signature pad"></canvas>
                <button type="button" class="btn btn-outline btn-sm signature-clear" data-pad="co-owner">Clear Signature</button>
              </div>
              <div class="form-group">
                <label for="co_owner_signature_name">Or type full legal name</label>
                <input type="text" id="co_owner_signature_name" name="co_owner_signature_name" placeholder="Full legal name as signature" />
              </div>
            </div>
            <p class="form-disclaimer">By submitting this form, I authorize Pure Capital US LLC (and its affiliated entities) and its referral partners to contact me at the phone number and email provided via automated dialing devices, texts, and prerecorded/artificial messages for marketing and servicing purposes. Consent is not required to obtain credit or services; to apply without providing this consent, contact Pure Capital US LLC directly at <a href="tel:+13472012166">(347) 201-2166</a>. Message and data rates may apply. I may opt out at any time.</p>
          </div>

          <div class="prequal-nav">
            <button type="button" class="btn btn-outline prequal-prev" hidden>Previous</button>
            <button type="button" class="btn btn-primary prequal-next">Next Step</button>
            <button type="submit" class="btn btn-primary btn-submit btn-lg prequal-submit" hidden>Submit Prequalification</button>
          </div>
        </form>
      </div>
    </div>
  </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <div class="footer-container">
      <div class="footer-col brand-col">
        <img src="assets/IMG_20260531_000449-removebg-preview.png" alt="Pure Capital US LLC — business funding" class="footer-logo" width="180" height="52" />
        <p class="phone-number"><a href="tel:+13472012166">(347) 201-2166</a></p>
        <p class="phone-label">Mon–Fri, 8am–6pm ET</p>
      </div>
      <div class="footer-col">
        <h4>Solutions</h4>
        <ul>
          <li><a href="business-line-of-credit.html">Business Lines of Credit</a></li>
          <li><a href="real-estate-financing.html">Real Estate Financing</a></li>
          <li><a href="sba-loans.html">SBA Loans</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="index.html#process">How It Works</a></li>
          <li><a href="prequalify.html">Prequalification</a></li>
          <li><a href="apply.html">Full Application</a></li>
          <li><a href="mailto:info@purecapital.us">info@purecapital.us</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-container">
        <p>&copy; 2026 Pure Capital. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script src="main.js"></script>
  <script src="prequalify.js"></script>
</body>
</html>
"""


def main():
    content = HTML.format(
        industry_options=options(INDUSTRIES),
        legal_options=options(LEGAL_ENTITIES),
        fico_options=options(FICO_RANGES),
        mca_rows=mca_rows(5),
        re_rows=re_rows(3),
    )
    out = Path(__file__).parent / "prequalify.html"
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
