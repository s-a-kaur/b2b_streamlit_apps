# insight_studio.py
import streamlit as st
from typing import Dict, Any, List
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
from difflib import SequenceMatcher
import time
import textwrap



# -----------------------------
# DEFAULT SALES INTELLIGENCE STATE
# -----------------------------
if "company_input_insight" not in st.session_state:
    st.session_state.company_input_insight = "IronBuild Infrastructure"

if "insight_content_type" not in st.session_state:
    st.session_state.insight_content_type = "Scouting Report"

if "insight_scope" not in st.session_state:
    st.session_state.insight_scope = "Content Generation"




# FIXED — preserves acronyms like CRM, CDN, AI
ACRONYMS = {"Crm", "Cdn", "Ai", "Iot", "Saas", "Erp", "Api", "Sdk", "Sso", "Orm"}

def smart_title(s: str) -> str:
    words = s.replace("_", " ").split()
    result = []
    for w in words:
        titled = w.title()
        result.append(titled.upper() if titled in ACRONYMS else titled)
    return " ".join(result)



IRONBUILD_SCOUTING_REPORT: Dict[str, Any] = {

    "company_name": "IronBuild Infrastructure",

    # -------------------------------------------------
    # ACCOUNT OVERVIEW
    # -------------------------------------------------
    "company_overview": {
        "summary": (
            "IronBuild Infrastructure Pty Ltd is a high-priority construction account "
            "undergoing rapid multi-site expansion, with strong networking intent and "
            "immediate opportunities to cross-sell new site connectivity and upsell "
            "bandwidth, security, and managed network services."
        ),
        "details": {
            "company_name": "IronBuild Infrastructure Pty Ltd",
            "headquarters": "Newcastle, NSW, Australia",
            "year_founded": 2008,
            "public_company": "No",
            "region": "Australia",
            "global_offices": "8 (Au), 8 (Global)",
            "industry": "Construction",
            "revenue_range": "$100M – $250M",
            "employee_range": "500–1000",
            "website": "https://www.iron-built.com.au/",
            "linkedin": "https://www.linkedin.com/company/ironbuild-infrastructure"
        }
    },

    # -------------------------------------------------
    # PRODUCT PORTFOLIO
    # -------------------------------------------------
    "product_portfolio": {
        "internet": {
            "bandwidth": "500 Gbps",
            "utilization": "85%",
            "tcv": "200K",
            "start": "Jun 2021",
            "end": "May 2026",
            "renewal": "In 3 Months"
        },
        "sdwan": {
            "total_sites": "8",
            "sites_deployed": "6",
            "tcv": "150K",
            "start": "Feb 2023",
            "end": "Feb 2028",
            "renewal": "In 24 Months"
        },
        "mobility": {
            "active_lines": "180",
            "tcv": "100K",
            "start": "Jun 2022",
            "end": "May 2026",
            "renewal": "In 3 Months"
        }
    },

    # -------------------------------------------------
    # CONTACTS
    # -------------------------------------------------
    "contacts": {
        "primary_contact": {
            "name": "Gregory N. Roberts",
            "title": "Chief Executive Officer",
            "email": "groberts@ironbuild.com",
            "phone": "+1 310-319-0200",
        },
        "secondary_contact": {
            "name": "Ryan Anderson",
            "title": "Chief Information Officer",
            "email": "randerson@ironbuild.com",
            "phone": "+1 310-319-0215",
        }
    },

    # -------------------------------------------------
    # PROSPECT CONTEXT
    # -------------------------------------------------
    "prospect_context": {

        "financial_insights": [
            "Reported ~12% YoY revenue growth driven by sustained public infrastructure investment.",
            "Large multi-year project wins increasing active construction footprint.",
            "Strong ICT investment aligned to operational scale and modernization."
        ],

        "growth_summary": [
            "Secured multiple multi-year civil infrastructure contracts across NSW and QLD, expanding active project footprint.",
            "Formed regional delivery partnerships accelerating execution capacity and site rollout velocity.",
            "Active workforce expansion across site operations supporting increased equipment and project throughput.",
            "Enterprise-wide digital transformation initiative focused on operational visibility, automation, and site connectivity.",
            "Infrastructure investment tailwinds sustaining ~12% YoY revenue growth and predictable pipeline scale."
        ],


        "intent_signals": [
            "Network Infrastructure — Bandwidth expansion, Ethernet networking, SD-WAN optimization.",
            "IoT & Asset Management — Equipment monitoring, fleet telematics, asset tracking.",
            "AI & Automation — Construction AI, site safety automation, computer vision.",
            "Competitors Searched — Cisco, Optus."
        ],

        "spend_profile": [
            "ICT Spend: $13.3M – $57.2M",
            "Software Spend: $600K – $1.9M",
            "Hardware Spend: $800K – $1.5M",
            "Telco Spend: $1.7M – $8.2M",
            "IT Services Spend: $2.9M – $11.7M",
            "Spend Tier: Very High"
        ],

        "intent_signals": [
            {
                "name": "Network Infrastructure",
                "level": "Very High",
                "keywords": "Bandwidth expansion, Ethernet networking, SD-WAN optimization"
            },
            {
                "name": "IoT & Asset Management",
                "level": "High",
                "keywords": "Equipment monitoring systems, Heavy equipment fleet management, Construction IoT telemetry, Asset tracking systems, Fleet telematics"
            },
            {
                "name": "AI & Automation",
                "level": "Medium",
                "keywords": "Construction AI solutions, Site safety automation, AI workforce scheduling, Computer vision construction"
            }
        ],

        "competitors": ["Cisco", "Optus"],

        "why_prioritize_and_recommendations": [
            {
                "signal": "Rapid multi-site expansion across Australia.",
                "recommendation": "Adaptive Networks (Ethernet)",
                "product_fit_score": "86%",
                "value": "Ensure scalable, high-performance connectivity as operations expand from 8 to 10+ active construction sites, supporting site mobility, partnerships, and fluctuating bandwidth demands."
            },
            {
                "signal": "Partial SD-WAN deployment across distributed locations.",
                "recommendation": "SD-WAN Expansion (Managed Network Services)",
                "product_fit_score": "82%",
                "value": "Extend SD-WAN coverage to all sites to enable centralized control, consistent performance, and secure connectivity across geographically dispersed construction hubs."
            },
            {
                "signal": "Growing need for connected equipment and asset visibility.",
                "recommendation": "IoT Solutions (IoT)",
                "product_fit_score": "74%",
                "value": "Enable real-time tracking and monitoring of construction equipment through IoT and edge connectivity, improving asset utilization, safety, and operational efficiency."
            },
            {
                "signal": "Increasing regulatory and safety requirements.",
                "recommendation": "AI Site Safety (Sovereign AI – Computer Vision)",
                "product_fit_score": "72%",
                "value": "Deploy on-site, sovereign AI-powered safety monitoring to support regulatory compliance, low-latency decision-making, and scalable site safety as construction operations expand."
            }
        ],

        "engagement_triggers": [
            "Won Opportunities (Last 3 yrs): 4",
            "Lost Opportunities: 0",
            "Open Opportunities: 1",
            "Last Interaction: Q4 FY25 — Network optimization & site expansion discussions.",
            "Upcoming Trigger: Mobility renewal due in ~3 months.",
            "Expansion Trigger: Planned site growth (8 → 10+).",
            "Seller Insight: Strong marketing engagement + positive win history."
        ]
    },

    # -------------------------------------------------
    # TECHNOLOGY LANDSCAPE
    # -------------------------------------------------
    "tech_landscape": {
        "tech_stack": {
            "networking_and_connectivity": [
                "Cisco Catalyst Switches",
                "Cisco Firewalls",
                "WAN Routing",
                "SD-WAN"
            ],
            "cloud_and_infrastructure": [
                "AWS EC2",
                "Azure Virtual Machines",
                "Backup & Recovery"
            ],
            "it_security": [
                "Fortinet Firewall",
                "Rapid7 Vulnerability Management"
            ],
            "data_and_analytics": [
                "Microsoft Power BI"
            ],
            "enterprise_apps": [
                "SAP S/4HANA",
                "Salesforce CRM",
                "Project Management Tools"
            ]
        }
    },

    # -------------------------------------------------
    # CAMPAIGN
    # -------------------------------------------------
    "marketing_campaign": {
        "notes": (
            "Campaign Theme: 'Enabling Multi-Site Construction Connectivity and Sovereign AI-Driven Site Intelligence.'"
        )
    }
}



def render_marketing_email_ironbuild():

    email_html = """
<div style="
    background:#f9f9f9;
    padding:20px;
    border-radius:10px;
    border:1px solid #e0e0e0;
    text-align:left;
">

<p style="text-align:left; font-weight:bold;">
Subject: Supporting IronBuild’s Multi-Site Expansion with Scalable Connectivity
</p>

<p style="text-align:left;">Hi Gregory N. Roberts,</p>

<p style="text-align:left;">
Hope you're doing well.
</p>

<p style="text-align:left;">
I'm <b>Sarah Jones</b>, Sales Manager at <b>XYZ Corporation</b>. 
I’m reaching out as IronBuild continues expanding operations across NSW and QLD, 
with active site growth and increasing reliance on resilient connectivity, 
real-time visibility, and secure operational infrastructure.
</p>

<p style="text-align:left;">
With IronBuild moving from <b>8 toward 10+ active construction sites</b>, alongside your existing use of 
<b>Business Internet, SD-WAN, and Mobility services</b>, this is a strong moment to ensure 
your network architecture scales seamlessly with operational demand.
</p>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
📌 Where We Can Support IronBuild’s Next Phase
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">

<li>
<b>Adaptive Networks (Ethernet)</b><br>
→ Provide scalable, high-performance connectivity across expanding construction sites to maintain performance consistency and operational continuity.
</li>

<li style="margin-top:8px;">
<b>SD-WAN Expansion</b><br>
→ Extend SD-WAN coverage across all locations to deliver centralized visibility, optimized bandwidth utilization, and consistent network performance.
</li>

<li style="margin-top:8px;">
<b>IoT Solutions</b><br>
→ Enable real-time equipment tracking, telemetry, and operational visibility across distributed construction assets.
</li>

<li style="margin-top:8px;">
<b>AI Site Safety (Sovereign AI – Computer Vision)</b><br>
→ Deploy on-site sovereign AI safety monitoring to support regulatory compliance, low-latency insights, and scalable safety oversight across infrastructure projects.
</li>

</ul>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
⭐ Why XYZ Corporation
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">
<li>Deep experience supporting multi-site infrastructure and construction environments</li>
<li>Proven delivery of resilient connectivity across distributed operational sites</li>
<li>Scalable architecture aligned to expansion-driven growth</li>
<li>Integrated networking, IoT, and sovereign AI enablement</li>
<li>24/7 enterprise-grade operational support</li>
</ul>

<p style="text-align:left; margin-top:16px;">
Would you be open to a brief conversation this week to explore how we can support IronBuild’s upcoming site expansion and infrastructure priorities?
</p>

<p style="text-align:left;">
Happy to tailor a short walkthrough aligned to your current footprint and near-term roadmap.
</p>

<p style="text-align:left; margin-top:20px;">
Best regards,<br>
<b>Sarah Jones</b><br>
Sales Manager<br>
XYZ Corporation<br>
+1 111-234-7631
</p>

</div>
"""

    st.markdown(email_html, unsafe_allow_html=True)

# ================================================================
#  Global CSS
# ================================================================
CSS = """
<style>

.tight-list {
    margin-top: 0px !important;
    padding-top: 0px !important;
}

.context-list {
    margin-top: 2px !important;
}

.main-panel {
    max-width: 1100px;
    margin: auto;
    padding: 10px 30px;
}

.report-header {
    color: #4a0070;
    text-align: center;
    margin-top: 0;
    font-size: 2em;
    font-weight: 800;
}

h4.section-title {
    text-align: left;
    margin-top: 0 !important;
    margin-bottom: 8px !important;
    color: #444;
    font-size: 1.05rem;
    font-weight: 600;
}

.context-list {
    padding-left: 18px !important;
}

.context-list li {
    font-size: 0.875rem;
    margin: 6px 0;
    line-height: 1.35;
}

.section-spacer {
    height: 16px;
}

/* ===============================
   CHAT WRAPPER + GLOBAL CHAT FONT
   =============================== */
.chat-wrapper {
    max-width: 700px;
    margin: auto;
    background: #faf9ff;
    padding: 22px 26px;
    border-radius: 14px;
    border: 1px solid #ebe7ff;
    text-align: left !important;
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 0.9rem;
}

/* Everything inside chat uses same font + left alignment */
.chat-wrapper * {
    font-family: inherit;
    text-align: left;
}

/* ===============================
   CHAT HISTORY + BUBBLES
   =============================== */
.chat-history {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 12px;
}

.chat-message-user {
    background: #e5e7eb;
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    max-width: 90%;
    align-self: flex-end;
}

.chat-message-bot {
    background: #ffffff;
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    max-width: 90%;
    border-left: 4px solid #6b00b8;
}

/* Unify font size + line-height for both sides */
.chat-message-user-inner,
.chat-message-bot-inner {
    font-size: 0.9rem;
    line-height: 1.5;
}
/* Force left alignment for all chat answer content */
.chat-message-bot-inner,
.chat-message-bot-inner * {
    text-align: left !important;
}

/* Tidy headings inside bot messages (for STATIC_QA content) */
.chat-message-bot-inner h3,
.chat-message-bot-inner h4 {
    margin-top: 0;
    margin-bottom: 6px;
}

/* Static QA container (used in your HTML) */
.static-answer {
    font-size: 0.9rem;
    line-height: 1.55;
}

/* ===============================
   LOG / ANSWER BOXES (PIPELINE STYLE)
   =============================== */

.log-box {
    margin-top: 10px;
    font-size: 0.85rem;
    background: #f4f1ff;
    padding: 8px 12px;
    border-radius: 8px;
    border-left: 3px solid #6b00b8;
}

.answer-box {
    margin-top: 18px;
    background: #ffffff;
    padding: 16px;
    border-radius: 10px;
    border-left: 4px solid #6b00b8;
    font-size: 0.9rem;
    text-align: left !important;
}

/* (Optional legacy class, safe to keep) */
.chat-answer {
    margin-top: 18px;
    background: #ffffff;
    padding: 16px;
    border-radius: 10px;
    border-left: 4px solid #6b00b8;
}


.email-card * {
    text-align: left !important;
}
.email-card {
    text-align: left !important;
}

</style>
"""



STATIC_QA: Dict[str, str] = {}

# ----------------------------------------------------------------
# Q1 — High Priority Accounts (AvePoint replaces A-Mark)
# ----------------------------------------------------------------
STATIC_QA["give me key insights on high priority accounts which i should target today"] = (

    "<h3 style='margin-bottom:4px;'>🎯 Top Priority Accounts to Target Today</h3>"
    "<p style='margin-top:0;'>These accounts stand out due to strong growth signals, digital maturity, and major transformation movements. "
    "Below is a refined, executive-ready intelligence summary with SDR talking points.</p>"

    "<hr style='border: none; border-top: 1px solid #ccc; margin: 12px 0;'>"

    "<h4>🏗 IronBuild Infrastructure — <i>National Expansion + Sovereign AI-Ready Construction Modernisation</i></h4>"
    "<p>"
    "IronBuild Infrastructure Pty Ltd is a high-priority construction account experiencing sustained national expansion, "
    "strong technology adoption, and clear intent to modernize network capacity, security posture, and managed services — "
    "with increasing readiness for sovereign AI-driven operational capabilities across regulated infrastructure projects."
    "</p>"

    "<b>Why IronBuild is High Priority:</b>"
    "<ul>"
    "<li>📈 ~12% YoY revenue growth driven by major civil infrastructure wins</li>"
    "<li>🏗 Active site expansion (8→10 sites) across NSW & QLD</li>"
    "<li>🌐 Very High networking intent (Score: 85) — bandwidth + Ethernet + SD-WAN optimisation</li>"
    "<li>🚜 Strong IoT & asset monitoring interest </li>"
    "<li>🤖 Emerging sovereign AI readiness for site safety & regulated workloads</li>"
    "<li>💰 Very High spend tier — Enterprise ICT &amp; services opportunity</li>"
    "</ul>"

    "<b>SDR Talk Tracks:</b>"
    "<ul>"
    "<li>\"As your site footprint expands, resilient connectivity becomes mission-critical.\"</li>"
    "<li>\"We can help standardize performance and security across all active sites.\"</li>"
    "<li>\"Let’s align your digital transformation with scalable edge-ready infrastructure.\"</li>"
    "</ul>"

    "<hr style='border: none; border-top: 1px solid #ccc; margin: 18px 0;'>"

    "<h4>🌐 VeriSign — <i>Mission-Critical Infrastructure, Zero Room for Error</i></h4>"
    "<p>"
    "VeriSign runs global DNS and identity workloads — systems where milliseconds matter and uptime is mission-critical. Their advanced "
    "multi-cloud and IAM architecture makes them an ideal match for XYZ Global Networks enterprise-grade reliability offerings."
    "</p>"

    "<b>Why VeriSign is High Priority:</b>"
    "<ul>"
    "<li>🛡 Mission-critical DNS + security infrastructure</li>"
    "<li>☁️ Advanced multi-cloud &amp; IAM stack</li>"
    "<li>💵 Strong financial strength</li>"
    "<li>⚠️ Zero tolerance for latency or outages</li>"
    "<li>🏆 High maturity → perfect for premium XYZ Global Networks solutions</li>"
    "</ul>"

    "<b>SDR Talk Tracks:</b>"
    "<ul>"
    "<li>\"We support companies where milliseconds matter — like yours.\"</li>"
    "<li>\"Let's optimize global network paths for DNS &amp; identity.\"</li>"
    "<li>\"We can harden resilience across your multi-cloud backbone.\"</li>"
    "</ul>"

    "<hr style='border: none; border-top: 1px solid #ccc; margin: 18px 0;'>"

    "<h4>🏬 VF Corporation — <i>Global Transformation = Perfect Timing</i></h4>"
    "<p>"
    "VF Corporation is undergoing major transformation — portfolio optimization, retail modernization, and supply-chain refresh. "
    "This creates a unique window for XYZ Global Networks to lead with connectivity, SD-WAN upgrades, and managed security."
    "</p>"

    "<b>Why VF Corporation is High Priority:</b>"
    "<ul>"
    "<li>🌍 Large global enterprise with complex retail footprint</li>"
    "<li>🔄 Active divestiture + optimization initiatives</li>"
    "<li>🤖 High maturity across cloud, AI, security, ERP/CRM</li>"
    "<li>🚚 Modernizing supply chain &amp; store operations</li>"
    "<li>📊 Strong intent signals during restructuring</li>"
    "</ul>"

    "<b>SDR Talk Tracks:</b>"
    "<ul>"
    "<li>\"This transformation window is the perfect time to modernize connectivity.\"</li>"
    "<li>\"Let's simplify and secure SD-WAN across your global retail environment.\"</li>"
    "<li>\"We help unify store connectivity, supply-chain visibility, and managed security.\"</li>"
    "</ul>"

    "<hr style='border: none; border-top: 1px solid #ccc; margin: 18px 0;'>"

    "<p style='font-size:16px; font-weight:600; color:#111; margin-top: 2px;'>"
    "⭐ These three accounts should be your top focus today — each is in a strategic, high-impact transformation phase where XYZ Global Networks can deliver immediate enterprise value."
    "</p>"
)


# ----------------------------------------------------------------
# Q2 — Deep Dive on AvePoint (replaces old A-Mark deep dive key)
# ----------------------------------------------------------------


STATIC_QA["give me a deep dive on ironbuild infrastructure"] = (

    "<h3 style='margin-bottom:6px;'>Deep-Dive on IronBuild Infrastructure</h3>"
    "<p style='margin-top:0;'>IronBuild Infrastructure is classified as a <b>High-Priority Account (ACC001)</b> "
    "due to multi-site expansion, strong network modernization intent, rising IoT interest, "
    "and an enterprise-wide digital transformation initiative across regulated infrastructure projects.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🏢 Company Overview</h4>"
    "<p>IronBuild Infrastructure Pty Ltd delivers complex civil, commercial, and industrial infrastructure projects across Australia. "
    "Its distributed, site-heavy operating model requires resilient connectivity, secure collaboration, mobility, and scalable edge infrastructure.</p>"
    "<ul>"
    "<li><b>Founded:</b> 2008</li>"
    "<li><b>Headquarters:</b> Newcastle, NSW</li>"
    "<li><b>Employees:</b> 500–1000</li>"
    "<li><b>Revenue:</b> $100M – $250M</li>"
    "<li><b>Active Sites:</b> 8 (Australia)</li>"
    "<li><b>YoY Revenue Growth:</b> ~12.4%</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🚀 Growth Signals & Recent Activity</h4>"
    "<ul>"
    "<li>Secured multi-year infrastructure projects across NSW & QLD</li>"
    "<li>Formed regional delivery partnerships to accelerate execution</li>"
    "<li>Active hiring across site operations</li>"
    "<li>Enterprise-wide digital transformation initiative underway</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🎯 Intent Signals</h4>"
    "<ul>"
    "<li><b>Network Infrastructure:</b> Very High (Score: 85)</li>"
    "<li><b>IoT & Asset Management:</b> High (Score: 72)</li>"
    "<li><b>AI & Automation:</b> Emerging (Score: 68)</li>"
    "<li><b>Competitors Present:</b> Cisco, Optus</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>💡 Top Recommendations</h4>"
    "<ul>"
    "<li><b>1. Adaptive Networks</b> <i>(Networks — Cross-Sell)</i> — Support rapid site expansion with scalable Ethernet and resilient backbone connectivity.</li>"
    "<li><b>2. SD-WAN Expansion</b> <i>(Networks — Up-Sell)</i> — Extend centralized control and performance optimisation across all active sites.</li>"
    "<li><b>3. IoT Solutions</b> <i>(Internet of Things — Cross-Sell)</i> — Enable connected equipment, fleet telemetry, and construction asset tracking.</li>"
    "<li><b>4. AI Site Safety (Computer Vision)</b> <i>(Sovereign AI Products — Cross-Sell)</i> — Deploy in-country, edge-based AI to enhance site safety and regulatory compliance.</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:14px 0;'>"

    "<h4>🏅 Lead Priority Conclusion</h4>"
    "<p style='font-size:16px;'>"
    "<b>IronBuild Infrastructure is a high-impact construction modernization opportunity.</b> "
    "Expansion-driven site growth, strong networking intent, and sovereign AI readiness create immediate strategic alignment "
    "for scalable connectivity, edge intelligence, and regulated infrastructure support."
    "</p>"
)


STATIC_QA["give me a deep dive on ironbuild infrastructure"] = (

    "<h3 style='margin-bottom:6px;'>Deep-Dive on IronBuild Infrastructure</h3>"
    "<p style='margin-top:0;'>IronBuild Infrastructure is classified as a <b>High-Priority Account (ACC001)</b> due to sustained national expansion, "
    "strong digital transformation momentum, expanding site footprint, and increasing intent to modernize network capacity, operational visibility, "
    "and sovereign AI-enabled site intelligence across regulated infrastructure projects.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🏢 Company Overview</h4>"
    "<p>IronBuild Infrastructure Pty Ltd is a large-scale Australian construction and infrastructure services company delivering "
    "complex civil, commercial, and industrial projects across NSW and QLD. The company operates a distributed, site-heavy model "
    "requiring resilient connectivity, mobility, secure collaboration, and real-time operational visibility to support ongoing project execution.</p>"
    "<ul>"
    "<li><b>Founded:</b> 2008</li>"
    "<li><b>Headquarters:</b> Newcastle, NSW, Australia</li>"
    "<li><b>Employees:</b> 500–1000</li>"
    "<li><b>Revenue Range:</b> $100M – $250M</li>"
    "<li><b>Industry:</b> Construction — Infrastructure & Civil Projects</li>"
    "<li><b>Active Sites:</b> 8 (Australia)</li>"
    "<li><b>Website:</b> https://www.iron-built.com.au/</li>"
    "<li><b>Corporate Line:</b> 02 8358 4170</li>"
    "<li><b>LinkedIn:</b> https://www.linkedin.com/company/ironbuild-infrastructure</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🌍 Operating Footprint</h4>"
    "<p>IronBuild operates across multiple active infrastructure sites in Australia, with expansion across NSW and QLD. "
    "Its distributed project model requires consistent, high-performance connectivity between headquarters, regional offices, "
    "and temporary construction sites.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🛠️ Services & Capabilities</h4>"
    "<p>IronBuild delivers large-scale civil and infrastructure solutions across transportation, utilities, and commercial developments. "
    "Core capabilities include:</p>"
    "<ul>"
    "<li>Major civil infrastructure delivery</li>"
    "<li>Industrial and commercial construction projects</li>"
    "<li>Equipment-intensive project operations</li>"
    "<li>Multi-site project coordination and subcontractor ecosystems</li>"
    "<li>Digitally enabled site operations and workforce management</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>📊 Financial Interpretation</h4>"
    "<p>IronBuild is in a strong growth phase supported by sustained public infrastructure investment and successful project wins. "
    "<b>Revenue grew approximately 12% YoY</b>, driven by multi-year civil infrastructure contracts and expanding site operations. "
    "Technology investment is aligned to operational scale, with continued focus on digital modernization and infrastructure resilience.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🚀 Growth Signals &amp; Recent Activity</h4>"
    "<p>IronBuild is experiencing operational acceleration across multiple dimensions:</p>"
    "<ul>"
    "<li><b>Business Expansion:</b> Secured multiple multi-year civil infrastructure projects across NSW and QLD, increasing active construction sites and equipment deployment.</li>"
    "<li><b>Partnerships:</b> Formed regional delivery partnerships to accelerate large-scale project execution.</li>"
    "<li><b>Hiring:</b> Actively expanding site-based workforce to support growing project pipeline.</li>"
    "<li><b>Financial Performance:</b> Reported ~12% YoY revenue growth driven by sustained infrastructure investment.</li>"
    "<li><b>Digital Transformation:</b> Announced enterprise-wide modernization initiative to enhance operational efficiency and site intelligence.</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🎯 Intent Signals</h4>"
    "<ul>"
    "<li><b>Network Modernization:</b> Active exploration of bandwidth expansion, Ethernet networking, and SD-WAN optimisation to support site scalability.</li>"
    "<li><b>IoT & Asset Monitoring:</b> Growing focus on connected equipment, fleet telemetry, and asset tracking across distributed construction environments.</li>"
    "<li><b>AI & Site Automation:</b> Emerging interest in computer vision, workforce automation, and AI-powered safety systems.</li>"
    "<li><b>Competitive Environment:</b> Existing networking relationships indicate openness to alternative architectures and carrier optimisation.</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>💡 Top Recommendations</h4>"
    "<ul>"
    "<li><b>1. Adaptive Networks</b> <i>(Networks — Cross-Sell)</i>"
    " — Support rapid site expansion with scalable Ethernet backbone and resilient connectivity across active and upcoming construction sites.</li>"
    "<li><b>2. SD-WAN Expansion</b> <i>(Networks — Up-Sell)</i>"
    " — Extend centralized visibility and performance optimization across all distributed locations to support operational scale.</li>"
    "<li><b>3. IoT Solutions</b> <i>(Internet of Things — Cross-Sell)</i>"
    " — Enable real-time equipment tracking, telemetry, and asset visibility across heavy construction fleets.</li>"
    "<li><b>4. AI Site Safety (Computer Vision)</b> <i>(Sovereign AI Products — Cross-Sell)</i>"
    " — Deploy in-country, edge-based AI for site safety monitoring and regulatory compliance across critical infrastructure projects.</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:14px 0;'>"

    "<h4>🏅 Lead Priority Conclusion</h4>"
    "<p style='font-size:16px;'>"
    "<b>IronBuild Infrastructure is a High-Priority account (ACC001)</b> — expansion-driven, digitally modernizing construction enterprise "
    "with growing demand for resilient connectivity, edge intelligence, and sovereign AI-ready infrastructure to support regulated, "
    "multi-site project environments."
    "</p>"
)

# ----------------------------------------------------------------
# Q3 — Financially Growing Companies 
# ----------------------------------------------------------------
STATIC_QA["show companies that are financially growing"] = (

    "<h3 style='margin-bottom:6px;'>📈 Companies That Are Financially Growing</h3>"
    "<p>These companies demonstrate strong YoY or QoQ improvement across revenue, profitability, cash flow, or "
    "operational efficiency. Below is a structured, executive-ready summary of the top growth performers.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🏗 Terex Corporation — Strong Short-Term Growth Momentum</h4>"
    "<ul>"
    "<li><b>Quarterly revenue more than doubled</b>, signaling high demand and strong operational execution.</li>"
    "<li>Annual revenue stable with mild softening — short-term acceleration remains strong.</li>"
    "</ul>"
    "<p><i>Interpretation:</i> Terex shows <b>robust near-term recovery</b> fueled by construction and industrial demand.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🧬 Incyte Pharmaceuticals — High Revenue Expansion</h4>"
    "<ul>"
    "<li><b>YoY revenue increased sharply</b>, showing strong product adoption.</li>"
    "<li><b>Quarter-over-quarter revenue more than doubled</b>, likely driven by new oncology/immunology growth.</li>"
    "</ul>"
    "<p><i>Interpretation:</i> Incyte is on a <b>high-growth trajectory</b> from pipeline expansion and strong sales momentum.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🚜 Caterpillar Inc. — Strong Quarterly Sales Performance</h4>"
    "<ul>"
    "<li><b>Quarterly revenue +16.27%</b>, reflecting strong demand and backlog conversion.</li>"
    "<li>Annual revenue dipped slightly — long-term trend requires monitoring.</li>"
    "</ul>"
    "<p><i>Interpretation:</i> Caterpillar is in a <b>short-term upswing</b> driven by industrial demand cycles.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🏭 Air Products — Exceptional Profitability &amp; Efficiency Gains</h4>"
    "<ul>"
    "<li><b>Net income +66% YoY</b> — large profitability boost.</li>"
    "<li><b>EPS +66.19%</b> — strong earnings leverage.</li>"
    "<li><b>Operating income +79%</b> — major cost efficiency improvements.</li>"
    "<li><b>Operating cash flow +75%</b> — excellent operational strength.</li>"
    "</ul>"
    "<p><i>Interpretation:</i> Air Products displays <b>top-tier financial performance</b> with strong operational discipline.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🌐 VeriSign — Stable Long-Term Growth + Sharp Quarterly Spike</h4>"
    "<ul>"
    "<li><b>Annual revenue +4.31% YoY</b> — consistent long-term growth.</li>"
    "<li><b>Quarterly revenue doubled</b> from Q1 → Q2 2025.</li>"
    "<li><b>Gross profit +5.41%</b> — healthy recurring revenue structure.</li>"
    "</ul>"
    "<p><i>Interpretation:</i> VeriSign remains a <b>stable compounder</b> with subscription-based recurring revenue growth.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:14px 0;'>"

    "<h4>⭐ Summary</h4>"
    "<p>The companies demonstrating the strongest financial growth are:</p>"
    "<ul>"
    "<li><b>Terex Corporation</b> — short-term acceleration</li>"
    "<li><b>Incyte Pharmaceuticals</b> — powerful YoY + QoQ expansion</li>"
    "<li><b>Caterpillar Inc.</b> — strong quarterly performance</li>"
    "<li><b>Air Products</b> — leading profitability growth</li>"
    "<li><b>VeriSign</b> — steady long-term growth + recent spike</li>"
    "</ul>"
)




def fuzzy_match(query: str, choices: Dict[str, str], threshold: float = 0.55):
    query = query.lower().strip()
    best_key = None
    best_score = 0
    for key in choices.keys():
        score = SequenceMatcher(None, query, key).ratio()
        if score > best_score:
            best_score = score
            best_key = key
    return best_key if best_score >= threshold else None


# ================================================================
#  EXPORT HELPERS
# ================================================================
def build_text_sections(report):
    lines = []
    company = report["company_name"].upper()
    lines.append(f"AI-Generated Scouting Report: {company}")
    lines.append("")

    lines.append("Company Overview")
    lines.append(report["company_overview"]["summary"])
    lines.append("")

    lines.append("Financial Insights")
    for x in report["prospect_context"]["financial_insights"]:
        lines.append(f"• {x}")
    lines.append("")

    lines.append("Growth Summary")
    for x in report["prospect_context"]["growth_summary"]:
        lines.append(f"• {x}")
    lines.append("")

    lines.append("Why Prioritize")
    for r in report["prospect_context"]["why_prioritize_and_recommendations"]:
        lines.append(f"- {r['signal']}")
        lines.append(f"  Recommendation: {r['recommendation']}")
        lines.append(f"  Value: {r['value']}")
    lines.append("")

    lines.append("Tech Stack")
    for k, v in report["tech_landscape"]["tech_stack"].items():
        lines.append(f"{k}: {', '.join(v)}")
    lines.append("")

    lines.append("Campaign Strategy")
    lines.append(report["marketing_campaign"]["notes"])

    return lines


def generate_pdf(report):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    lines = build_text_sections(report)
    for line in lines:
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_docx(report):
    buffer = BytesIO()
    doc = Document()
    lines = build_text_sections(report)

    for line in lines:
        doc.add_paragraph(line)

    doc.save(buffer)
    buffer.seek(0)
    return buffer


# ================================================================
#  REUSABLE UI HELPERS
# ================================================================
def section_header(icon: str, title: str):
    st.markdown(
        f"<div style='font-weight:700;margin-top:6px;margin-bottom:2px;font-size:0.95rem;'>"
        f"{icon} {title}</div>",
        unsafe_allow_html=True
    )


def render_kv(label: str, value: Any):
    st.markdown(
        f"<div style='font-size:0.875rem; padding:3px 0;'><b>{label}:</b> {value}</div>",
        unsafe_allow_html=True
    )


# ================================================================
#  MAIN REPORT RENDERER
# ================================================================
def render_sales_report(report: Dict[str, Any]):
    company = report["company_name"]
    
    # Header
    st.markdown(
    f"""
    <h3 style="
        color:#4a0070;
        text-align:left;
        margin-top:10px;
        margin-bottom:6px;
        font-size:1.4rem;
        font-weight:700;
    ">
        💡 AI-Generated Scouting Report: {company.upper()}
    </h3>
    """,
    unsafe_allow_html=True,)

    # --- DOWNLOAD BUTTONS (Side-by-Side) ---
    colA, colB = st.columns([0.25, 0.25])
    with colA:
        st.download_button(
            "📄 Download PDF",
            data=generate_pdf(report),
            file_name=f"{company}_scouting_report.pdf",
            mime="application/pdf",
            use_container_width=False
        )
    with colB:
        st.download_button(
            "📝 Download Word",
            data=generate_docx(report),
            file_name=f"{company}_scouting_report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=False
        )

    

    st.markdown("---")

    # Company Overview
    with st.expander("Company Overview 🏢", expanded=True):
        summary = report["company_overview"]["summary"]
        details = report["company_overview"]["details"]

        st.markdown(f"<div style='font-size:0.875rem; margin-bottom:10px;'>{summary}</div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            section_header("🎯", "Firmographics")
            for k in ["company_name", "headquarters", "region", "year_founded"]:
                render_kv(k.replace("_"," ").title(), details[k])

        with c2:
            section_header("📊", "Size & Market")
            for k in ["industry", "revenue_range", "employee_range", "global_offices"]:
                render_kv(k.replace("_"," ").title(), details[k])

        with c3:
            section_header("🌐", "Web Presence")
            for k in ["website", "linkedin", "youtube"]:
                if k in details and details[k]:
                    render_kv(k.title(), details[k])


    # Company Overview
    with st.expander("Product Portfolio 📦", expanded=True):

        st.markdown("""
        <style>
        .product-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-top: 6px;
        }

        .product-card {
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            padding: 16px 18px;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .product-title {
            color: #6b00b8;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .product-label {
            font-weight: 600;
        }

        .renewal-red {
            color: #dc2626;
            font-weight: 700;
        }

        .renewal-green {
            color: #16a34a;
            font-weight: 700;
        }
        </style>
        """, unsafe_allow_html=True)


        internet = report["product_portfolio"]["internet"]
        sdwan = report["product_portfolio"]["sdwan"]
        mobility = report["product_portfolio"]["mobility"]

        st.markdown(f"""
        <div class="product-grid">

        <div class="product-card">
        <div class="product-title">Internet</div>
        <div><span class="product-label">Vendor:</span> XYZ Corporation</div>
        <div><span class="product-label">Bandwidth:</span> {internet["bandwidth"]}</div>
        <div><span class="product-label">Utilization:</span> {internet["utilization"]}</div>
        <div><span class="product-label">Product TCV:</span> {internet["tcv"]}</div>
        <div><span class="product-label">Product Start Date:</span> {internet["start"]}</div>
        <div><span class="product-label">Product End Date:</span> {internet["end"]}</div>
        <div><span class="product-label">Renewal:</span> <span class="renewal-red">{internet["renewal"]}</span></div>
        </div>

        <div class="product-card">
        <div class="product-title">SD-WAN</div>
        <div><span class="product-label">Vendor:</span> XYZ Corporation</div>
        <div><span class="product-label">Sites Deployed:</span> {sdwan["sites_deployed"]}</div>
        <div><span class="product-label">Product TCV:</span> {sdwan["tcv"]}</div>
        <div><span class="product-label">Product Start Date:</span> {sdwan["start"]}</div>
        <div><span class="product-label">Product End Date:</span> {sdwan["end"]}</div>
        <div><span class="product-label">Renewal:</span> <span class="renewal-green">{sdwan["renewal"]}</span></div>
        </div>

        <div class="product-card">
        <div class="product-title">Mobility</div>
        <div><span class="product-label">Vendor:</span> XYZ Corporation</div>
        <div><span class="product-label">Active Lines:</span> {mobility["active_lines"]}</div>
        <div><span class="product-label">Product TCV:</span> {mobility["tcv"]}</div>
        <div><span class="product-label">Product Start Date:</span> {mobility["start"]}</div>
        <div><span class="product-label">Product End Date:</span> {mobility["end"]}</div>
        <div><span class="product-label">Renewal:</span> <span class="renewal-red">{mobility["renewal"]}</span></div>
        </div>

        </div>
        """, unsafe_allow_html=True)



    # Contacts
    with st.expander("Key Contact Information 📞", expanded=True):
        contacts = report["contacts"]
        c1, c2 = st.columns(2)

        with c1:
            section_header("📞", "Primary Contact")
            for k, v in contacts["primary_contact"].items():
                render_kv(k.title(), v)

        with c2:
            section_header("📞", "Secondary Contact")
            for k, v in contacts["secondary_contact"].items():
                render_kv(k.title(), v)

    # Prospect Context
    with st.expander("Account Context: Signals & Priorities 🚨", expanded=True):

        section_header("📉", "Financial Insights")
        for x in report["prospect_context"]["financial_insights"]:
            st.markdown(f"<li>{x}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        section_header("📈", "Growth & Operational Summary")
        for x in report["prospect_context"]["growth_summary"]:
            st.markdown(f"<li>{x}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        section_header("💻", "Technology Landscape")
        tech = report["tech_landscape"]["tech_stack"]
        for category, tools in tech.items():
            tools_str = ", ".join(tools)
            st.markdown(
                f"<li><b>{smart_title(category)}:</b> {tools_str}</li>",
                unsafe_allow_html=True
            )
        st.markdown("</ul>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        section_header("💰", "Est Spend Potential: <span style='color:#16a34a;'>Very High</span>")
        spend_items = report["prospect_context"]["spend_profile"]
        for item in spend_items:
            label, value = item.split(":", 1)
            st.markdown(
                f"<li><b>{label}:</b>{value}</li>",
                unsafe_allow_html=True
            )

        st.markdown("</ul>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        section_header(
            "🎯",
            "Active Buyer Intent Signals: <span style='color:#16a34a;'>Very High</span>"
        )

        intent_data = report["prospect_context"]["intent_signals"]
        for intent in intent_data:
            name = intent["name"]
            level = intent["level"]
            keywords = intent["keywords"]

            color = {
                "Very High": "#16a34a",
                "High": "#16a34a",
                "Medium": "#f97316"
            }.get(level, "#333")

            st.markdown(
                f"""
        <li>
        <b>{name}:</b> <span style="color:{color}; font-weight:600;">{level}</span><br>
        <i>Keywords Searched:</i> {keywords}
        </li>
        """,
                unsafe_allow_html=True
            )

        # Competitors
        competitors = report["prospect_context"]["competitors"]
        st.markdown(
            f"<li><b>Competitors Searched:</b> {', '.join(competitors)}</li>",
            unsafe_allow_html=True
        )

        st.markdown("</ul>", unsafe_allow_html=True)
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        section_header("🎯", "Why Prioritize & What to Recommend")
        for r in report["prospect_context"]["why_prioritize_and_recommendations"]:
            st.markdown(
                f"<li><b>{r['signal']}</b><br>"
                f"<b>Recommendation:</b> {r['recommendation']}<br>"
                f"<b>Product Fit Score:</b> {r['product_fit_score']}<br>"
                f"<i>{r['value']}</i></li>",
                unsafe_allow_html=True
            )
        st.markdown("</ul>", unsafe_allow_html=True)


    # Campaign
    with st.expander("Campaign Strategy 📧", expanded=True):
        section_header("🎯", "Targeted Campaign")
        render_kv("Focus", report["marketing_campaign"]["notes"])
        if "engagement_triggers" in report["prospect_context"]:
            section_header("📞", "Engagement & Near-Term Triggers")
            # st.markdown("<ul class='context-list'>", unsafe_allow_html=True)
            for x in report["prospect_context"]["engagement_triggers"]:
                st.markdown(f"<li>{x}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)


def render_seller_pitch_ironbuild():

    pitch_html = """
<div style="
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    padding: 18px 20px;
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.95rem;
    line-height: 1.55;
    text-align: left;
">

<p style="font-size:1.1rem; font-weight:700; margin-top:0;">
Seller Pitch — IronBuild Infrastructure
</p>

<p style="font-weight:bold;">🏢 Company Snapshot</p>
<p>
IronBuild Infrastructure is a rapidly expanding construction and infrastructure services organization operating across distributed project sites in Australia. 
With active expansion across NSW and QLD and increasing reliance on connected equipment, workforce mobility, and real-time operational visibility, 
IronBuild is entering a phase where connectivity, reliability, and secure edge intelligence become foundational to execution speed and safety compliance.
</p>

<p>
As construction environments scale from <b>8 toward 10+ active sites</b>, infrastructure must support consistent performance, centralized control, 
and low-latency operational insights across geographically dispersed environments.
</p>

<p style="font-weight:bold; margin-top:18px;">🎤 Call Opening (SDR-Friendly)</p>
<ul style="margin-left:18px; padding-left:18px;">
  <li>"We’ve been following IronBuild’s expansion across NSW and QLD."</li>
  <li>"As construction operations scale across more distributed sites, connectivity consistency and operational visibility typically become critical priorities."</li>
  <li>"Companies at this stage often look to standardize connectivity and improve visibility across assets and teams."</li>
  <li>"I’d love to share a few observations we’ve seen work well for infrastructure organizations expanding multi-site operations."</li>
</ul>

<p style="font-weight:bold; margin-top:20px;">🚀 Where XYZ Global Networks Can Support (Top Opportunities)</p>

<p><b>1. Scalable multi-site connectivity backbone</b><br>
→ <b>Recommendation:</b> Adaptive Networks (Ethernet)<br>
→ <b>Why:</b> Provides consistent, high-performance connectivity across expanding construction sites while supporting fluctuating bandwidth demands and centralized oversight.
</p>

<p><b>2. Centralized visibility and performance across distributed locations</b><br>
→ <b>Recommendation:</b> SD-WAN Expansion<br>
→ <b>Why:</b> Extends centralized orchestration, improves resilience, and ensures predictable performance across all operational sites.
</p>

<p><b>3. Connected equipment and operational telemetry</b><br>
→ <b>Recommendation:</b> IoT Solutions<br>
→ <b>Why:</b> Enables real-time monitoring of equipment, workforce coordination, and operational efficiency improvements across job sites.
</p>

<p><b>4. Site safety and compliance intelligence</b><br>
→ <b>Recommendation:</b> AI Site Safety (Sovereign AI — Computer Vision)<br>
→ <b>Why:</b> Delivers on-site AI-driven safety monitoring with local data residency and low-latency decision support across critical infrastructure environments.
</p>

<p style="font-weight:bold; margin-top:20px;">⚡ If the Client Hesitates</p>
<ul style="margin-left:18px; padding-left:18px;">
    <li>"Many infrastructure firms underestimate how quickly connectivity requirements grow as new sites come online."</li>
    <li>"We can benchmark IronBuild’s connectivity posture against similar construction leaders."</li>
    <li>"Even a short discovery session often highlights quick wins around performance and operational visibility."</li>
</ul>

<p style="font-weight:bold; margin-top:20px;">🟢 If the Client Shows Interest</p>
<ul style="margin-left:18px; padding-left:18px;">
    <li>"The next step would be a short conversation around your current site connectivity and expansion roadmap."</li>
    <li>"We can map where Ethernet, SD-WAN, IoT, and AI safety capabilities create immediate value."</li>
    <li>"Would this week or next work better for you?"</li>
</ul>

</div>
"""

    st.markdown(pitch_html, unsafe_allow_html=True)


# ================================================================
#  MAIN PAGE
# ================================================================

def insight_studio_page():

    # Load global CSS
    st.markdown(CSS, unsafe_allow_html=True)

    # Wrapper container
    st.markdown("<div class='main-panel'>", unsafe_allow_html=True)

    # Defaults if sidebar hasn't set them yet
    if "insight_scope" not in st.session_state:
        st.session_state.insight_scope = "Content Generation"
    if "insight_content_type" not in st.session_state:
        st.session_state.insight_content_type = "Scouting Report"
    if "run_insight_generation" not in st.session_state:
        st.session_state.run_insight_generation = False

    st.session_state.setdefault("company_input_insight", "IronBuild Infrastructure")

    scope = st.session_state.insight_scope
    company_name = st.session_state.get("company_input_insight") or "IronBuild Infrastructure"
    content_type = st.session_state.insight_content_type

    # =====================================================================
    # CHAT MODE
    # =====================================================================
    if scope == "Chat":

        if "chat_history" not in st.session_state or not isinstance(st.session_state.chat_history, list):
            st.session_state.chat_history = []  # list of {"role": "user"/"assistant", "content": "..."}


        st.markdown(
            "<h3 style='color:#6b00b8; text-align:center;'>🤖 AI Insight Chatbot</h3>"
            "<p style='text-align:center;'>Ask about companies, technologies, trends, or insights.</p>",
            unsafe_allow_html=True,
        )

        # Chat UI container
        st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

        # --- RENDER HISTORY ---
        st.markdown("<div class='chat-history'>", unsafe_allow_html=True)
        if not st.session_state.chat_history:
            st.markdown(
                "<div class='log-box'>No messages yet. Ask your first question to start the conversation.</div>",
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-message-user">
                            <div class="chat-message-user-inner"><b>You:</b> {msg['content']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-message-bot">
                            <div class="chat-message-bot-inner">{msg['content']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        st.markdown("</div>", unsafe_allow_html=True)  # close chat-history

        # --- INPUT AT BOTTOM ---
        with st.form("insight_chat_form", clear_on_submit=True):
            user_query = st.text_input(
                "Type your question",
                placeholder="companies with 500+ employees",
            )
            send = st.form_submit_button("Send")

        # --- QUICK QUESTION CHIPS ---
        chip_questions = [
        ("🎯 Top Priority Accounts", "Give me key insights on high priority accounts which I should target today"),
        ("🏢 IronBuild Deep Dive",    "Give me a deep dive on ironbuild infrastructure"),
        ("📈 Financial Growing Companies", "Show companies that are financially growing")
        ]

        st.markdown("<div class='chip-row'>", unsafe_allow_html=True)
        # chip_cols = st.columns(len(chip_questions))
        chip_cols = st.columns([2,2,2,5])  # last col is empty spacer
        for ci, (label, full_query) in enumerate(chip_questions):
            with chip_cols[ci]:
                if st.button(label, key=f"chip_{ci}"):
                    st.session_state.chat_history.append({"role": "user", "content": full_query})
                    st.session_state["pending_chip_query"] = full_query
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


        # --- HANDLE CHIP QUERY WITH SPINNER ---
        if st.session_state.get("pending_chip_query"):
            pending = st.session_state.pop("pending_chip_query")
            log_placeholder = st.empty()

            def show_log(msg):
                log_placeholder.markdown(f"<div class='log-box'>{msg}</div>", unsafe_allow_html=True)

            show_log("📦 Routing query...")
            time.sleep(0.4)
            show_log("🔍 Running semantic search...")
            time.sleep(0.4)
            show_log("🧠 Processing...")
            time.sleep(0.4)
            show_log("📄 Preparing final answer...")
            time.sleep(0.4)
            log_placeholder.empty()

            matched_key = fuzzy_match(pending.lower(), STATIC_QA)
            answer_html = STATIC_QA[matched_key] if matched_key else "<b>Answer:</b><br>No static answer found."
            st.session_state.chat_history.append({"role": "assistant", "content": answer_html})
            st.rerun()

        if send and user_query.strip():
            # 1) append user message
            st.session_state.chat_history.append(
                {"role": "user", "content": user_query.strip()}
            )

            # 2) simulate agent logs (optional, like your other pipelines)
            log_placeholder = st.empty()

            def show_log(msg: str):
                log_placeholder.markdown(
                    f"<div class='log-box'>{msg}</div>",
                    unsafe_allow_html=True,
                )

            show_log("📦 Routing query...")
            time.sleep(0.4)
            show_log("🔍 Running semantic search...")
            time.sleep(0.4)
            show_log("🧠 Processing...")
            time.sleep(0.4)
            show_log("📄 Preparing final answer...")
            time.sleep(0.4)
            log_placeholder.empty()

            # 3) build assistant answer (using your static QA for now)
            key = fuzzy_match(user_query, STATIC_QA)

            if key:
                answer_html = STATIC_QA[key]
            else:
                answer_html = (
                    "<b>Answer:</b><br>"
                    "I don't have a static answer for this query yet. Try rephrasing or asking about high-priority accounts."
                )

            # 4) append assistant message
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer_html}
            )

            # trigger re-render with new history
            st.rerun()

        # Close chat container + main panel
        st.markdown("</div>", unsafe_allow_html=True)  # close chat-wrapper
        st.markdown("</div>", unsafe_allow_html=True)  # close main-panel
        return  # IMPORTANT: stop here in Chat mode

    # =====================================================================
    # 📝 CONTENT GENERATION MODE (SCOUTING REPORT / PITCH / CAMPAIGN)
    # =====================================================================

    # Clear any chat state 
    st.session_state.chat_history = []

    st.markdown(
        "<h3 style='color:#6b00b8;'>📝 Content Generation & Deliverables</h3>",
        unsafe_allow_html=True,
    )

    # If no company selected yet, don't show Wolfspeed by default
    if not company_name:
        st.info("Please select a company and content type in the sidebar to generate an output.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # --- Scouting Report ---
    
    if content_type == "Scouting Report":
        if not st.session_state.get("run_insight_generation", False):
            st.info("Select your options and click **Generate** to produce the report.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        company = company_name.lower().strip()
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(company)

        if company.lower() in ["ironbuild", "ironbuild infrastructure"]:
            with st.spinner("⚙️ Generating IronBuild Infrastructure scouting report..."):
                time.sleep(6)
            st.success("Showing scouting report for IronBuild Infrastructure")
            render_sales_report(IRONBUILD_SCOUTING_REPORT)
        else:
            st.warning("Scouting Report pitch is not available for this company.")

        st.markdown("</div>", unsafe_allow_html=True)
        return


    # --- Seller Pitch ---
    if content_type == "Seller Pitch":
        if not st.session_state.get("run_insight_generation", False):
            st.info("Select your options and click **Generate** to produce the pitch.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        
        company = company_name.lower().strip()

        if company.lower() in ["ironbuild", "ironbuild infrastructure"]:
            with st.spinner("⚙️ Building seller pitch for IronBuild Infrastructure..."):
                time.sleep(6)
            st.success("Showing Seller Pitch for IronBuild Infrastructure")
            render_seller_pitch_ironbuild()
        else:
            st.warning("Seller pitch is not available for this company.")

        st.markdown("</div>", unsafe_allow_html=True)
        return


    # --- Personalized Email ---
    if content_type == "Personalized Email":
        if not st.session_state.get("run_insight_generation", False):
            st.info("Select your options and click **Generate** to produce the email.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        
        company = company_name.lower().strip()
        
        if company.lower() in ["ironbuild", "ironbuild infrastructure"]:
            with st.spinner("⚙️ Generating personalized email for IronBuild Infrastructure..."):
                time.sleep(6)
            st.success("Showing marketing email for IronBuild Infrastructure")
            render_marketing_email_ironbuild()

        else:
            st.warning("No marketing email available for this company.")

        st.markdown("</div>", unsafe_allow_html=True)
        return
