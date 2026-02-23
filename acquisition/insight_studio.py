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
    st.session_state.company_input_insight = "A-Mark Precious Metals"

if "insight_content_type" not in st.session_state:
    st.session_state.insight_content_type = "Scouting Report"

if "insight_scope" not in st.session_state:
    st.session_state.insight_scope = "Content Generation"



# ================================================================
#  WOLFSPEED SCOUTING REPORT DATA
# ================================================================
WOLFSPEED_SCOUTING_REPORT: Dict[str, Any] = {
    "company_name": "Wolfspeed",
    "company_overview": {
        "summary": (
            "Wolfspeed is a semiconductor technology company specializing in silicon "
            "carbide (SiC). They lead the industry transition from silicon to silicon "
            "carbide through pure-play, vertically integrated operations. Their "
            "SiC-based products — including materials, power modules, MOSFETs, and "
            "reference kits — enable efficiency and sustainability across EVs, "
            "renewables, aerospace, and industrial sectors."
        ),
        "details": {
            "company_name": "Wolfspeed",
            "headquarters": "4600 Silicon Drive, Durham, North Carolina, 27703, USA",
            "year_founded": 2015,
            "public_company": "Yes",
            "region": "North America",
            "global_offices": "20+",
            "industry": "Semiconductor Manufacturing",
            "revenue_range": "$500M – $1B",
            "employee_range": "1,001 – 5,000",
            "website": "https://www.wolfspeed.com",
            "linkedin": "https://www.linkedin.com/company/wolfspeed",
            "youtube": "https://youtube.com/c/wolfspeedinc"
        }
    },
    "contacts": {
        "primary_contact": {
            "name": "Robert Feurle",
            "title": "Chief Executive Officer",
            "email": "robert.feuerle@wolfspeed.com",
            "phone": "+1 919-313-5300",
        },
        "secondary_contact": {
            "name": "Priya Almelkar",
            "title": "Senior Vice President & Chief Information Officer",
            "email": "priya.almelkar@wolfspeed.com",
            "phone": "+1 919-287-7888",
        }
    },
    "prospect_context": {
        "financial_insights": [
            "Revenue is down (~6% YoY) and net losses have widened to ~$1.6B.",
            "Shareholders’ equity is negative (~-$447M), indicating serious concerns.",
            "Significant one-time charges: ~$417M restructuring + ~$359M goodwill impairment.",
            "Liquidity pressure; relies on a ~$1.25B financing facility."
        ],
        "growth_summary": [
            "200mm SiC production ramping; Mohawk Valley fab revenue doubling.",
            "Planning $5B North Carolina wafer facility (major expansion).",
            "Consolidating older 150mm fabs → modern 200mm digital fabs.",
            "25% workforce reduction → cost optimization during scale-up."
        ],
        "why_prioritize_and_recommendations": [
            {
                "signal": "Rapid fab expansion and rising inter-fab data volumes.",
                "recommendation": "Dedicated Fiber / DIA",
                "value": "Low-latency connectivity for automation and data transport."
            },
            {
                "signal": "Shift to fully digital 200mm manufacturing.",
                "recommendation": "High-bandwidth Business Internet",
                "value": "Support analytics, digital twins, IoT, real-time systems."
            },
            {
                "signal": "Multi-site operations (NY, NC).",
                "recommendation": "SD-WAN / Unified Connectivity",
                "value": "Improve resilience, uptime, and centralized networking."
            }
        ]
    },
    "tech_landscape": {
        "tech_stack": {
            "cloud_infrastructure": ["AWS Cloud", "Azure", "Google Cloud Platform", "Oracle Cloud"],
            "identity_and_collaboration": ["Microsoft Entra ID", "Power Automate", "Microsoft Teams"],
            "network_and_security_infrastructure": ["Cisco Catalyst", "Cisco Firewalls", "Cisco ISE", "Viptela SD-WAN"],
            "enterprise_apps_and_security_saas": ["Salesforce", "SAP CRM", "SailPoint", "Saviynt", "Symantec", "Securonix"],
            "ai_simulation_and_engineering": ["PyTorch", "ReliaSoft", "FlexSim", "Trellix"]
        }
    },
    "marketing_campaign": {
        "notes": (
            "Targeted Campaign: 'Enabling 200mm Digital Fab Connectivity and Security'."
        )
    }
}


# ================================================================
#  A-MARK PRECIOUS METALS SCOUTING REPORT DATA (DEMO)
# ================================================================
A_MARK_SCOUTING_REPORT: Dict[str, Any] = {
    "company_name": "A-Mark Precious Metals",
    "company_overview": {
        "summary": (
            "A-Mark Precious Metals is a leading global precious metals trading, "
            "distribution, and financial services company serving wholesale, "
            "institutional, and retail customers. Following its acquisition of "
            "Monex and the rebrand to Gold.com, A-Mark has transitioned into a "
            "high-velocity, digitally driven global trading platform with "
            "mission-critical uptime and security requirements."
        ),
        "details": {
            "company_name": "A-Mark Precious Metals (Gold.com)",
            "headquarters": "2121 Rosecrans Avenue, El Segundo, CA 90245, USA",
            "year_founded": 1965,
            "public_company": "Yes (NYSE: GOLD)",
            "region": "North America",
            "global_offices": "7+",
            "industry": "Merchant Wholesalers, Durable Goods (423940)",
            "revenue_range": "$500M+",
            "employee_range": "300-500",
            "website": "https://www.amark.com/",
            "linkedin": "https://www.linkedin.com/company/a-mark-precious-metals"
        }
    },
    "contacts": {
        "primary_contact": {
            "name": "Gregory N. Roberts",
            "title": "Chief Executive Officer",
            "email": "groberts@amark.com",
            "phone": "+1 310-319-0200",
        },
        "secondary_contact": {
            "name": "Ryan Anderson",
            "title": "Chief Information Officer",
            "email": "randerson@amark.com",
            "phone": "+1 310-319-0215",
        }
    },
    "prospect_context": {
        "financial_insights": [
            "Revenue growth of ~13% YoY driven by acquisitions and expanded trading volume.",
            "Net income declined due to acquisition integration and restructuring costs.",
            "Operating cash flow increased significantly, signaling strong liquidity.",
            "Public market exposure increases compliance and uptime pressure."
        ],
        "growth_summary": [
            "Completed $835M Monex acquisition, expanding global trading footprint.",
            "Rebranded to Gold.com with focus on digital consumer & institutional platforms.",
            "Expanded collectibles, auctions, and online precious metals trading.",
            "Increased global transaction volume and real-time pricing workloads."
        ],
        "why_prioritize_and_recommendations": [
            {
                "signal": "High-volume real-time trading & auction platforms.",
                "recommendation": "Dedicated Fiber / Low-Latency DIA",
                "value": "Ensure real-time pricing, auctions, and transaction execution."
            },
            {
                "signal": "Multi-site global trading & fulfillment hubs.",
                "recommendation": "SD-WAN / Unified Connectivity",
                "value": "Secure and resilient global site-to-site operations."
            },
            {
                "signal": "NYSE listing & regulatory exposure.",
                "recommendation": "Managed Security / Zero Trust",
                "value": "Protect financial data and meet compliance requirements."
            }
        ]
    },
    "tech_landscape": {
        "tech_stack": {
            "cloud_infrastructure": ["AWS", "Azure"],
            "identity_and_collaboration": ["Microsoft Entra ID", "Microsoft Teams"],
            "network_and_security_infrastructure": ["Cisco Firewalls", "SD-WAN"],
            "enterprise_apps_and_security_saas": ["Salesforce", "SAP", "SailPoint"],
            "aI_and_analytics": ["Python", "Power BI"]
        }
    },
    "marketing_campaign": {
        "notes": (
            "Campaign Theme: 'Secure, Always-On Trading Infrastructure for Global "
            "Precious Metals Markets.'"
        )
    }
}



# ================================================================
#  AVEPOINT SCOUTING REPORT DATA
# ================================================================
AVEPOINT_SCOUTING_REPORT = {
    "company_name": "AvePoint",
    "company_overview": {
        "summary": (
            "AvePoint provides a unified data protection platform for enterprises, "
            "focusing on security, governance, and resilience in the AI-driven workplace. "
            "They help organizations manage their data across the full digital lifecycle. "
            "Dual-listed on Nasdaq and SGX, AvePoint is accelerating global growth through "
            "SaaS expansion, MSP partnerships, and AI-driven data protection capabilities, "
            "targeting $1B ARR by 2029."
        ),
        "details": {
            "company_name": "AvePoint",
            "headquarters": "525 Washington Blvd, Suite 1400, Jersey City, NJ 07310",
            "year_founded": 2001,
            "public_company": "Yes (Nasdaq: AVPT / SGX)",
            "region": "North America",
            "global_offices": "10+ global sites (US, EMEA, APAC)",
            "industry": "Information Technology",
            "revenue_range": "$100M – $500M",
            "employee_range": "500+",
            "website": "https://www.avepoint.com/",
            "linkedin": "https://www.linkedin.com/company/avepoint",
            "instagram": "https://www.instagram.com/avepoint/"
        }
    },
    "contacts": {
        "primary_contact": {
            "name": "TJ Jiang",
            "title": "Chief Executive Officer",
            "email": "tj.jiang@avepoint.com",
            "phone": "+1 201 793 1111",
        },
        "secondary_contact": {
            "name": "IT / Infrastructure Lead",
            "title": "Chief Information Officer",
            "email": "info@avepoint.com",
            "phone": "+1 201 793 1111",
        }
    },
    "prospect_context": {
        "financial_insights": [
            "Revenue +24% YoY (2025 vs 2024) — strong SaaS-led growth momentum.",
            "Net Income +348% YoY — dramatic profitability improvement and operating leverage.",
            "ARR reached $390M in Q3 2025; targeting $1B ARR by 2029.",
            "SaaS revenue growing at 38% — accelerating cloud-first business model.",
            "EPS -66.7% YoY — dilution from 7.37M share public offering to fund growth initiatives."
        ],


        "growth_summary": [
            "Acquired Ydentic to strengthen MSP automation and platform capabilities.",
            "Dual-listed on Nasdaq and SGX to accelerate global expansion.",
            "Launched AgentPulse — AI-driven security controls for AI agents.",
            "Expanded Azure Data Protection globally via IAMCP partnership.",
            "Priced a public offering of 7.37M shares to fund strategic growth.",
            "Multi-cloud strategy advancing across enterprise and MSP-led growth channels."
        ],
        "why_prioritize_and_recommendations": [
            {
                "signal": "Multi-site operations with heavy multi-cloud workloads and security-sensitive data governance.",
                "recommendation": "SASE",
                "value": "Unifies secure access and network policy across sites and users — reduces security gaps during scale and acquisition complexity."
            },
            {
                "signal": "Distributed global sites with bandwidth-intensive DevOps and analytics.",
                "recommendation": "Colocation / Dedicated Fiber",
                "value": "Improves reliability and throughput for cloud-adjacent workloads — supports expansion without introducing latency or resilience risk."
            },
            {
                "signal": "Cloud-first SaaS stack with growing remote workforce and collaboration needs.",
                "recommendation": "Cloud Voice with Microsoft Teams",
                "value": "Standardizes voice and collaboration across distributed teams — simplifies operations while supporting growth and mobility, reduce complexity and cost."
            }
        ]

    },
    "tech_landscape": {
        "tech_stack": {
            "cloud_infrastructure": ["AWS", "Microsoft Azure", "Google Cloud Platform", "Amazon CloudFront", "Amazon Route 53"],
            "network_and_cdn": ["CloudFlare", "Rackspace", "Verizon Wireless"],
            "security": ["Microsoft 365 Defender", "Azure Sentinel", "Sophos", "Tenable Nessus", "SentinelOne", "Barracuda Email Security"],
            "identity_and_access": ["Microsoft Active Directory", "Microsoft Entra", "OAuth", "OpenSSL"],
            "crm_and_marketing": ["Salesforce CRM", "HubSpot", "Marketo", "LinkedIn Sales Navigator"],
            "data_and_analytics": ["Google Analytics", "Tableau", "Power BI", "MongoDB", "MySQL", "Elasticsearch"],
            "devops_and_development": ["Docker", "Kubernetes", "HashiCorp Terraform", "Git", "Ansible", "React", "Angular", "Node.js"],
            "collaboration": ["Microsoft Teams", "SharePoint Online", "Outlook.com"]
        }
    },
    "marketing_campaign": {
        "notes": (
            "Targeted Campaign: 'Securing AvePoint's Multi-Cloud Growth — SASE, Connectivity & Collaboration at Enterprise Scale'."
        )
    }
}


# ================================================================
#  AVEPOINT SCOUTING REPORT RENDER FUNCTION
# ================================================================
def render_scouting_report_avepoint():
    import time
    with st.spinner("⚙️ Generating AvePoint scouting report..."):
        time.sleep(6)
    st.success("Showing scouting report for AvePoint")
    render_sales_report(AVEPOINT_SCOUTING_REPORT)


# ================================================================
#  AVEPOINT SELLER PITCH
# ================================================================
def render_seller_pitch_avepoint():

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
Seller Pitch — AvePoint
</p>

<p style="font-weight:bold;">🏢 Company Snapshot</p>
<p>
AvePoint is a fast-scaling enterprise SaaS company delivering data protection, governance, and security across modern multi-cloud environments. 
With active expansion initiatives, partner ecosystem growth, and AI-driven product innovation, the business is operating in an acceleration phase. 

As distributed teams expand and workloads span AWS, Azure, and other cloud platforms, maintaining consistent security posture, resilient connectivity, 
and seamless collaboration becomes increasingly critical. AvePoint’s next growth stage will depend on ensuring infrastructure scales as smoothly as the platform itself.
</p>

<p style="font-weight:bold; margin-top:18px;">🎤 Call Opening (SDR-Friendly)</p>
<ul style="margin-left:18px; padding-left:18px;">
  <li>"We’ve been following AvePoint’s expansion momentum and broader global footprint."</li>
  <li>"As multi-cloud environments scale and teams become more distributed, security consistency and performance resilience typically become higher priorities."</li>
  <li>"In similar SaaS growth phases, we often see secure access standardization and connectivity optimization become strategic initiatives."</li>
  <li>"I’d love to share a few observations we’ve seen work well for enterprises operating across multiple clouds and sites."</li>
</ul>

<p style="font-weight:bold; margin-top:20px;">🚀 Where XYZ Global Networks Can Support (Top 3 Opportunities)</p>

<p><b>1. Multi-site enterprise security modernization</b><br>
→ <b>Recommendation:</b> SASE<br>
→ <b>Why:</b> With distributed offices and cloud-based workloads, SASE helps standardize secure access and policy enforcement across users, applications, and sites — reducing risk while simplifying management as complexity grows.
</p>

<p><b>2. High-performance connectivity for distributed cloud operations</b><br>
→ <b>Recommendation:</b> Colocation<br>
→ <b>Why:</b> As workloads expand across multiple environments, resilient and scalable connectivity ensures performance consistency, uptime stability, and improved throughput for data-intensive operations.
</p>

<p><b>3. Collaboration and voice standardization for a distributed workforce</b><br>
→ <b>Recommendation:</b> Cloud Voice with Microsoft Teams<br>
→ <b>Why:</b> Deep alignment with the Microsoft ecosystem allows voice and collaboration to operate within a unified environment — simplifying operations and improving business continuity across teams.
</p>

<p style="font-weight:bold; margin-top:20px;">⚡ If the Client Hesitates</p>
<ul style="margin-left:18px; padding-left:18px;">
    <li>"In high-growth SaaS environments, infrastructure gaps usually appear during expansion or integration phases."</li>
    <li>"We can benchmark AvePoint’s connectivity and secure access model against similar enterprise SaaS companies."</li>
    <li>"Even a short discovery session can highlight opportunities to improve security consistency and operational resilience."</li>
</ul>

<p style="font-weight:bold; margin-top:20px;">🟢 If the Client Shows Interest</p>
<ul style="margin-left:18px; padding-left:18px;">
    <li>"The next step would be a focused 15-minute discussion around your current multi-cloud connectivity and secure access model."</li>
    <li>"We can map where SASE, Colocation, or Cloud Voice could strengthen resilience across your distributed footprint."</li>
    <li>"Would this week or next work better for you?"</li>
</ul>

</div>
"""

    st.markdown(pitch_html, unsafe_allow_html=True)


# ================================================================
#  AVEPOINT PERSONALIZED EMAIL
# ================================================================
def render_marketing_email_avepoint():

    email_html = """
<div style="
    background:#f9f9f9;
    padding:20px;
    border-radius:10px;
    border:1px solid #e0e0e0;
    text-align:left;
">

<p style="text-align:left; font-weight:bold;">
Subject: Supporting AvePoint’s Secure Multi-Cloud Expansion
</p>

<p style="text-align:left;">Hi TJ,</p>

<p style="text-align:left;">Hope you're doing well.</p>

<p style="text-align:left;">
I'm <b>Sarah Jones</b>, and I lead enterprise initiatives at <b>XYZ Global Networks</b>.
I’m reaching out as AvePoint continues to scale its enterprise SaaS footprint through expansion activity,
partner ecosystem growth, and new AI-driven capabilities across data protection and governance.
</p>

<p style="text-align:left;">
As organizations grow across multiple clouds and distributed teams, infrastructure pressure typically shows up in three places:
<b>secure access consistency</b>, <b>reliable high-performance connectivity</b>, and <b>collaboration standardization</b>.
This is where we support high-growth SaaS companies operating at enterprise scale.
</p>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
📌 Where We Can Support AvePoint’s Next Stage of Growth
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">
  <li>
    <b>SASE (Cybersecurity Services) — Secure access and policy consistency across sites and users</b><br>
    → Strengthen security posture as environments expand, teams become more distributed, and operational complexity increases.
  </li>

  <li style="margin-top:8px;">
    <b>Colocation (Cloud Connectivity) — Reliable performance for cloud-adjacent workloads and distributed operations</b><br>
    → Improve resilience and throughput for the infrastructure supporting SaaS delivery and enterprise operations.
  </li>

  <li style="margin-top:8px;">
    <b>Cloud Voice with Microsoft Teams (Voice &amp; Collaboration) — Standardized collaboration and voice for a distributed workforce</b><br>
    → Simplify operations while improving employee experience and business continuity.
  </li>
</ul>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
🤝 Would you be open to a brief discussion?
</p>

<p style="text-align:left;">
If you're open to it, I’d love to share a short perspective on how similar SaaS organizations simplify
security and connectivity as they scale across multi-cloud and distributed teams.
</p>

<p style="text-align:left;">
We can also tailor a quick architecture conversation around AvePoint’s current footprint and priorities,
and identify a few practical areas to improve <b>security consistency</b>, <b>network resilience</b>, and <b>operational simplicity</b>.
</p>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
⭐ Why XYZ Global Networks
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">
<li>Enterprise-grade reliability and resilient connectivity for distributed operations</li>
<li>Deep experience supporting multi-cloud environments and cloud-adjacent workloads</li>
<li>Proven approach to secure access standardization and policy consistency</li>
<li>Strong delivery model for multi-site enterprises and remote workforce enablement</li>
</ul>

<p style="text-align:left; margin-top:20px;">
Best regards,<br>
<b>Sarah Jones</b><br>
Enterprise Solutions Manager<br>
XYZ Global Networks<br>
📞 (555) 123-4567<br>
🌐 <a href="https://www.xyzglobalnetworks.com" target="_blank">xyzglobalnetworks.com</a>
</p>

</div>
"""

    st.markdown(email_html, unsafe_allow_html=True)



# ================================================================
#  Global CSS
# ================================================================
CSS = """
<style>

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

    "<h4>🚀 AvePoint — <i>Security-Led Enterprise + Acquisition-Driven Momentum</i></h4>"
    "<p>"
    "AvePoint is scaling aggressively. 24% revenue growth, ARR at $390M, a dual Nasdaq/SGX listing, and the Ydentic acquisition "
    "signal a company in full expansion mode. Their multi-cloud, multi-site infrastructure creates an immediate opening for SASE, "
    "Colocation, and Cloud Voice — all high-fit, high-urgency plays."
    "</p>"

    "<b>Why AvePoint is High Priority:</b>"
    "<ul>"
    "<li>📈 +24% YoY revenue growth, ARR at $390M</li>"
    "<li>🏢 Acquisition of Ydentic → rising network and MSP complexity</li>"
    "<li>☁️ Heavy multi-cloud footprint (AWS, Azure, GCP) → SASE adjacency</li>"
    "<li>🔐 Very High intent signals in Security Network + Cloud Services</li>"
    "<li>💰 Very High spend tier — Enterprise ICT &amp; services opportunity</li>"
    "</ul>"

    "<b>SDR Talk Tracks:</b>"
    "<ul>"
    "<li>\"You're scaling faster than your infrastructure — let's secure and modernize it.\"</li>"
    "<li>\"Your multi-cloud footprint and acquisition pace are ideal for SASE consolidation.\"</li>"
    "<li>\"Let's protect your $390M ARR base with enterprise-grade connectivity and security.\"</li>"
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
STATIC_QA["give me a deep dive on avepoint"] = (

    "<h3 style='margin-bottom:6px;'>Deep-Dive on AvePoint</h3>"
    "<p style='margin-top:0;'>AvePoint is classified as a <b>High-Priority Account (ACC001)</b> due to aggressive SaaS growth, "
    "acquisition-driven expansion, very high intent signals in security and cloud, and a large enterprise multi-cloud footprint "
    "that maps directly to XYZ Global Networks' SASE, Colocation, and Cloud Voice offerings.</p>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🏢 Company Overview</h4>"
    "<p>AvePoint provides a unified data protection platform for enterprises, focusing on security, governance, and resilience "
    "in the AI-driven workplace. They help organizations manage data across the full digital lifecycle, with a growing MSP "
    "channel and AI-native product portfolio.</p>"
    "<ul>"
    "<li><b>Founded:</b> 2001</li>"
    "<li><b>Headquarters:</b> 525 Washington Blvd, Suite 1400, Jersey City, NJ 07310</li>"
    "<li><b>Employees:</b> 500+</li>"
    "<li><b>Revenue:</b> $100M – $500M</li>"
    "<li><b>Industry:</b> Information Technology</li>"
    "<li><b>Listed:</b> Nasdaq (AVPT) + SGX (dual-listed)</li>"
    "<li><b>Website:</b> https://www.avepoint.com/</li>"
    "<li><b>Corporate Line:</b> +1 201 793 1111</li>"
    "<li><b>LinkedIn:</b> https://www.linkedin.com/company/avepoint</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🌍 Operating Footprint</h4>"
    "<p>AvePoint operates across multiple US locations supporting enterprise SaaS delivery and MSP channels:</p>"
    "<ul>"
    "<li>Jersey City, NJ (HQ)</li>"
    "<li>Chicago, IL</li>"
    "<li>Richmond, VA</li>"
    "<li>Arlington, VA</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>📊 Financial Interpretation</h4>"
    "<p>AvePoint is in a high-growth SaaS expansion phase — accelerating revenue, improving profitability, "
    "and building toward $1B ARR by 2029.</p>"
    "<ul>"
    "<li><b>Revenue Growth:</b> +24% YoY (2025 vs 2024) — strong SaaS-led momentum</li>"
    "<li><b>Net Income Change:</b> +348% YoY — significant profitability improvement</li>"
    "<li><b>ARR:</b> $390M in Q3 2025, targeting $1B by 2029</li>"
    "<li><b>SaaS Growth:</b> +38% — accelerating cloud-first model</li>"
    "<li><b>EPS:</b> -66.7% — dilution from 7.37M share offering to fund strategic growth</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🚀 Growth Signals &amp; Recent Activity</h4>"
    "<p>AvePoint is in a full acceleration phase driven by acquisitions, AI product launches, and global market expansion.</p>"
    "<ul>"
    "<li><b>Acquisition:</b> Acquired Ydentic to strengthen MSP automation and platform capabilities.</li>"
    "<li><b>Dual Listing:</b> Listed on SGX alongside Nasdaq to accelerate global expansion.</li>"
    "<li><b>New Product:</b> Launched AgentPulse — AI-driven security controls for AI agents.</li>"
    "<li><b>Partnership:</b> Expanded Azure Data Protection globally via IAMCP partnership.</li>"
    "<li><b>Capital Raise:</b> Priced a public offering of 7.37M shares to support strategic growth.</li>"
    "<li><b>Market Focus:</b> Advancing multi-cloud strategy across enterprise and MSP-led channels.</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>🎯 Intent Signals</h4>"
    "<ul>"
    "<li><b>Security Network (Score: 85):</b> zero trust architecture, SIEM platforms, endpoint detection, cloud security posture, threat analytics</li>"
    "<li><b>Cloud Services (Score: 80):</b> multi-cloud optimisation, cloud scalability, CDN performance, workload distribution</li>"
    "<li><b>Digital Infrastructure (Score: 78):</b> SD-WAN optimisation, global backbone connectivity, carrier benchmarking, network resilience</li>"
    "<li><b>Competitor Products Researched:</b> AWS, Microsoft Azure, Cloudflare, Salesforce</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:12px 0;'>"

    "<h4>💡 Top Recommendations</h4>"
    "<ul>"
    "<li><b>1. SASE (Fit: 0.9)</b> — Enterprise security modernization aligned to strong network intent and multi-site footprint.</li>"
    "<li><b>2. Colocation (Fit: 0.85)</b> — Infrastructure scaling requires centralized high-performance connectivity.</li>"
    "<li><b>3. Cloud Voice with Microsoft Teams (Fit: 0.80)</b> — Cloud-native collaboration consolidation across Microsoft ecosystem.</li>"
    "</ul>"

    "<hr style='border:none; border-top:1px solid #ccc; margin:14px 0;'>"

    "<h4>🏅 Lead Priority Conclusion</h4>"
    "<p style='font-size:16px;'>"
    "<b>AvePoint is a High-Priority account (ACC001)</b> — security-led enterprise with acquisition-driven momentum. "
    "Engage immediately for SASE + security displacement, Colocation for infrastructure scaling, and Cloud Voice for collaboration consolidation."
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

    "<h4>💻 AvePoint — Strong SaaS Revenue Growth &amp; Profitability Surge</h4>"
    "<ul>"
    "<li><b>Revenue +24% YoY</b> — accelerating SaaS-led expansion.</li>"
    "<li><b>Net Income +348% YoY</b> — dramatic profitability improvement.</li>"
    "<li><b>ARR at $390M</b> — targeting $1B ARR by 2029.</li>"
    "<li><b>SaaS Growth +38%</b> — cloud-first model accelerating strongly.</li>"
    "</ul>"
    "<p><i>Interpretation:</i> AvePoint shows <b>exceptional SaaS growth momentum</b> with improving profitability and a clear path to $1B ARR.</p>"

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
    "<li><b>AvePoint</b> — exceptional SaaS growth &amp; profitability surge</li>"
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
    st.markdown(f"<h4 class='section-title'>{icon} {title}</h4>", unsafe_allow_html=True)


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
            for k in ["company_name", "headquarters", "region", "year_founded", "public_company"]:
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
    with st.expander("Prospect Context: Signals & Priorities 🚨", expanded=True):

        section_header("📉", "Financial Insights")
        st.markdown("<ul class='context-list'>", unsafe_allow_html=True)
        for x in report["prospect_context"]["financial_insights"]:
            st.markdown(f"<li>{x}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        section_header("📈", "Growth & Operational Summary")
        st.markdown("<ul class='context-list'>", unsafe_allow_html=True)
        for x in report["prospect_context"]["growth_summary"]:
            st.markdown(f"<li>{x}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        section_header("🎯", "Why Prioritize & What to Recommend")
        st.markdown("<ul class='context-list'>", unsafe_allow_html=True)
        for r in report["prospect_context"]["why_prioritize_and_recommendations"]:
            st.markdown(
                f"<li><b>{r['signal']}</b><br>"
                f"<b>Recommendation:</b> {r['recommendation']}<br>"
                f"<i>{r['value']}</i></li>",
                unsafe_allow_html=True
            )
        st.markdown("</ul>", unsafe_allow_html=True)

    # Tech Landscape
    with st.expander("Technology Landscape 💻", expanded=True):
        tech = report["tech_landscape"]["tech_stack"]
        for k, v in tech.items():
            render_kv(k.replace("_", " ").title(), ", ".join(v))

    # Campaign
    with st.expander("Campaign Strategy 📧", expanded=True):
        section_header("🎯", "Targeted Campaign")
        render_kv("Focus", report["marketing_campaign"]["notes"])


def render_marketing_email_wolfspeed():

    email_html = """
<div style="
    background:#f9f9f9;
    padding:20px;
    border-radius:10px;
    border:1px solid #e0e0e0;
    text-align:left;
">

<p style="text-align:left; font-weight:bold;">
Subject: Supporting Wolfspeed’s 200mm Digital Fab Expansion
</p>

<p style="text-align:left;">Hi John,</p>

<p style="text-align:left;">Hope you're doing well.</p>

<p style="text-align:left;">
I’m <b>Sarah Jones</b>, and I lead enterprise initiatives at <b>XYZ Global Networks</b>. 
I’m reaching out after reviewing Wolfspeed’s ongoing transformation — especially the scale-up of your 
<b>200mm silicon carbide operations</b> and the expansion across <b>Durham</b>, 
<b>Mohawk Valley</b>, and the new <b>North Carolina facility</b>.
</p>

<p style="text-align:left;">
Your continued investment in next-generation manufacturing makes this the perfect time to strengthen the 
<b>connectivity foundation</b> supporting your digital fabs.
</p>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
📌 Where We Can Support Your Next Stage of Growth
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">
<li><b>High-volume inter-fab data transport</b><br>
→ Dedicated Fiber / DIA ensures low-latency MES, telemetry &amp; analytics movement.
</li>
<li><b>Multi-site coordination across fab locations</b><br>
→ SD-WAN / Unified Connectivity enables secure, synchronized operations across Durham, Mohawk Valley &amp; NC.
</li>
<li><b>Growing robotics, automation, and AI workloads</b><br>
→ High-Bandwidth Business Internet powering digital twins, computer vision &amp; real-time analytics.
</li>
<li><b>Operational uptime pressure</b><br>
→ Managed Security &amp; Resilience protecting high-volume SiC production environments.
</li>
</ul>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
🤝 Would you be open to a brief discussion?
</p>

<p style="text-align:left;">
I can walk you through a quick <b>10-minute overview</b> of how we support semiconductor and advanced manufacturing 
environments undergoing digital expansion.
</p>

<p style="text-align:left;">
If helpful, we can also schedule a short <b>demo tailored to Wolfspeed’s connectivity flow &amp; inter-fab data needs</b>.
</p>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
⭐ Why XYZ Global Networks
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">
<li>99% uptime guarantees for critical industrial networks</li>
<li>Deep experience in OT/IT security for manufacturing</li>
<li>Proven support for high-volume automation &amp; data workloads</li>
<li>Industry-leading fiber footprint and multi-site orchestration</li>
</ul>

<p style="text-align:left; margin-top:20px;">
Best regards,<br>
<b>Sarah Jones</b><br>
Enterprise Solutions Manager<br>
XYZ Global Networks<br>
📞 (555) 123-4567<br>
🌐 <a href="https://www.xyzglobalnetworks.com" target="_blank">xyzglobalnetworks.com</a>
</p>

</div>
"""

    st.markdown(email_html, unsafe_allow_html=True)

def render_marketing_email_amark():

    email_html = """
<div style="
    background:#f9f9f9;
    padding:20px;
    border-radius:10px;
    border:1px solid #e0e0e0;
    text-align:left;
">

<p style="text-align:left; font-weight:bold;">
Subject: Supporting Gold.com’s Post-Monex Integration & NYSE Scale
</p>

<p style="text-align:left;">Hi John,</p>

<p style="text-align:left;">Hope you're doing well.</p>

<p style="text-align:left;">
I’m <b>Sarah Jones</b>, and I lead enterprise initiatives at <b>XYZ Global Networks</b>. 
I’m reaching out following A-Mark’s transformation into <b>Gold.com (NYSE: GOLD)</b> 
and the official closing of the <b>$835M Monex acquisition</b> on January 5th.
</p>

<p style="text-align:left;">
As you integrate these massive global trading and fulfillment assets, this is the critical 
window to ensure your <b>digital infrastructure</b> is prepared for the next level of 
public-market scale and consumer demand.
</p>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
📌 Where We Can Support Your Next Stage of Growth
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">
<li><b>Unified connectivity across acquired platforms</b><br>
→ SD-WAN ensures seamless integration between legacy A-Mark, Monex, and new collectibles hubs.
</li>
<li><b>Ultra-low-latency trading &amp; auction environments</b><br>
→ Dedicated Fiber / DIA supports real-time pricing, live auctions, and 24/7 transaction execution.
</li>
<li><b>NYSE-grade security &amp; compliance requirements</b><br>
→ Zero-Trust security aligned to the high standards of institutional financial services and public markets.
</li>
<li><b>Growing consumer &amp; digital platform traffic</b><br>
→ High-bandwidth, resilient connectivity for Gold.com’s expanding DTC and fractional collectibles marketplace.
</li>
</ul>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
🤝 Would you be open to a brief discussion?
</p>

<p style="text-align:left;">
I can walk you through a quick <b>10-minute overview</b> of how we help financial and 
precious-metals platforms manage post-acquisition infrastructure risk while scaling securely.
</p>

<p style="text-align:left;">
If helpful, we can also map <b>Day-1 vs Day-90 integration needs</b> across your 
expanded global trading and fulfillment footprint.
</p>

<p style="text-align:left; font-weight:bold; margin-top:20px;">
⭐ Why XYZ Global Networks
</p>

<ul style="text-align:left; margin-left:18px; padding-left:18px; font-size:0.95rem;">
<li>99% uptime guarantees for revenue-critical trading networks</li>
<li>Deep experience in fintech and regulated financial services security</li>
<li>Proven support for high-stakes M&amp;A infrastructure consolidation</li>
<li>Industry-leading fiber footprint and secure multi-site orchestration</li>
</ul>

<p style="text-align:left; margin-top:20px;">
Best regards,<br>
<b>Sarah Jones</b><br>
Enterprise Solutions Manager<br>
XYZ Global Networks<br>
📞 (555) 123-4567<br>
🌐 <a href="https://www.xyzglobalnetworks.com" target="_blank">xyzglobalnetworks.com</a>
</p>

</div>
"""

    st.markdown(email_html, unsafe_allow_html=True)

def render_seller_pitch_wolfspeed():

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

<p style="font-size:1.1rem; font-weight:700; margin-top:0; text-align:left;">
Seller Pitch — Wolfspeed
</p>

<p style="font-weight:bold; text-align:left;">🏢 Company Snapshot</p>
<p style="text-align:left;">
Wolfspeed is a global leader in silicon carbide semiconductor manufacturing, currently undergoing one of the most 
ambitious transformations in advanced manufacturing. With the ramp-up of 200mm digital fabs, expansion across 
Mohawk Valley and North Carolina, and increasing automation and data volumes, Wolfspeed is entering a phase where 
network reliability, bandwidth, and security are mission-critical.
</p>

<p style="font-weight:bold; margin-top:18px; text-align:left;">🎤 Call Opening (SDR-Friendly)</p>
<ul style="margin-left:18px; padding-left:18px; text-align:left;">
    <li>“We’ve been following Wolfspeed’s expansion of 200mm SiC manufacturing and the scale-up of your digital fabs.”</li>
    <li>“Your inter-fab data volumes and automation footprint are growing rapidly across NY and NC.”</li>
    <li>“Companies at this stage typically see connectivity and resilience become a bottleneck.”</li>
    <li>“That’s where AT&amp;T supports advanced manufacturing leaders.”</li>
</ul>

<p style="font-weight:bold; margin-top:20px; text-align:left;">🚀 Where XYZ Global Networks Can Support (Top 5 Opportunities)</p>

<p style="text-align:left;"><b>1. High-volume inter-fab data movement</b><br>
→ <b>Recommendation:</b> Dedicated Fiber / DIA<br>
→ <b>Why:</b> Enables low-latency transport for MES, telemetry, AI analytics, and real-time fab automation.</p>

<p style="text-align:left;"><b>2. Fully digital 200mm manufacturing operations</b><br>
→ <b>Recommendation:</b> High-bandwidth Business Internet<br>
→ <b>Why:</b> Supports digital twins, computer vision, IoT sensors, and AI-driven yield optimization.</p>

<p style="text-align:left;"><b>3. Multi-site fab coordination (NY, NC, future sites)</b><br>
→ <b>Recommendation:</b> SD-WAN / Unified Connectivity<br>
→ <b>Why:</b> Centralized visibility, consistent policy enforcement, and resilient site-to-site communication.</p>

<p style="text-align:left;"><b>4. Operational uptime and manufacturing resilience</b><br>
→ <b>Recommendation:</b> Managed Network &amp; Security Services<br>
→ <b>Why:</b> Prevents production downtime in capital-intensive semiconductor environments.</p>

<p style="text-align:left;"><b>5. Growing cybersecurity exposure in OT + IT environments</b><br>
→ <b>Recommendation:</b> Managed Security &amp; Zero Trust Networking<br>
→ <b>Why:</b> Protects IP, fab automation systems, and high-value manufacturing data.</p>

<p style="font-weight:bold; margin-top:20px; text-align:left;">⚡ If the Client Hesitates</p>
<ul style="margin-left:18px; padding-left:18px; text-align:left;">
    <li>“Many semiconductor manufacturers underestimate how fast network demands grow during 200mm transitions.”</li>
    <li>“We can benchmark Wolfspeed’s connectivity model against other advanced manufacturing leaders.”</li>
    <li>“Even a short discovery can help identify future capacity or resilience gaps.”</li>
</ul>

<p style="font-weight:bold; margin-top:20px; text-align:left;">🟢 If the Client Shows Interest</p>
<ul style="margin-left:18px; padding-left:18px; text-align:left;">
    <li>“The next step would be a 15-minute discovery focused on your inter-fab data flows.”</li>
    <li>“We can map where latency, redundancy, or security improvements could deliver immediate value.”</li>
    <li>“Would this week or next work better for you?”</li>
</ul>

</div>
    """

    st.markdown(pitch_html, unsafe_allow_html=True)


def render_seller_pitch_amark():

    pitch_html = """
<div style="
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    padding: 18px 20px;
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.95rem;
    line-height: 1.55;
    text-align: left !important;
">

<p style="font-size:1.1rem; font-weight:700; margin-top:0; text-align:left;">
Seller Pitch — A-Mark (Rebranded to Gold.com)
</p>

<p style="font-weight:bold; text-align:left;">🏢 Company Snapshot</p>
<p style="text-align:left;">
A-Mark has officially transitioned to its new corporate identity, <b>Gold.com (NYSE: GOLD)</b>. Following the massive <b>$835M Monex acquisition</b> in January 2026, the company is now a high-velocity global platform for alternative assets. With 7+ global hubs and a focus on digital consumer platforms, Gold.com is scaling faster than its legacy infrastructure can adapt. This creates a strong opening for <b>XYZ Global Networks</b> to support "Day 1" integration and secure global operations.
</p>

<p style="font-weight:bold; margin-top:18px; text-align:left;">🎤 Call Opening (SDR-Friendly)</p>
<ul style="margin-left:18px; padding-left:18px; text-align:left;">
    <li style="text-align:left;">“Congratulations on the official rebrand to <b>Gold.com</b> and the closing of the Monex acquisition this week.”</li>
    <li style="text-align:left;">“With your transition to the <b>NYSE</b> and the integration of these new global assets, your trading ecosystem has become significantly more complex.”</li>
    <li style="text-align:left;">“Teams scaling at this pace typically see pressure on connectivity, security, and multi-site coordination — that’s where we help.”</li>
    <li style="text-align:left;">“I’d love to highlight a few areas where companies in a similar model see meaningful impact during post-acquisition integration.”</li>
</ul>

<p style="font-weight:bold; margin-top:20px; text-align:left;">🚀 Where XYZ Global Networks Can Support (Top 5 Opportunities)</p>

<p style="text-align:left ;"><b>1. Post-Acquisition Integration (Monex & A-Mark)</b><br>
→ <b>Recommendation:</b> SD-WAN + Managed Fabric<br>
→ <b>Why:</b> Ensures consistent performance, unified security policies, and rapid connectivity across newly acquired global sites.</p>

<p style="text-align:left;"><b>2. High-volume digital auctions & real-time trading</b><br>
→ <b>Recommendation:</b> High-bandwidth DIA / Low-latency Dedicated Fiber<br>
→ <b>Why:</b> Supports live bidding for Stack’s Bowers, pricing engines, and the surge in marketplace traffic at Gold.com.</p>

<p style="text-align:left;"><b>3. Heavy movement of trading, logistics, and inventory data</b><br>
→ <b>Recommendation:</b> Dedicated inter-facility transport<br>
→ <b>Why:</b> Guarantees fast, secure data transfer between your 7+ global trading, storage, and fulfillment operations.</p>

<p style="text-align:left;"><b>4. NYSE-Grade Cybersecurity & Compliance</b><br>
→ <b>Recommendation:</b> Managed Zero-Trust Security<br>
→ <b>Why:</b> Protects transaction data, marketplace operations, and distributed employees while meeting public-market security standards.</p>

<p style="text-align:left;"><b>5. Need for predictable uptime in revenue-critical operations</b><br>
→ <b>Recommendation:</b> Managed redundant connectivity with 99.99% SLAs<br>
→ <b>Why:</b> Gold.com’s live auctions and trading ops rely on always-on availability — any downtime equals immediate revenue loss.</p>

<p style="font-weight:bold; margin-top:20px; text-align:left;">⚡ If the Client Hesitates</p>
<ul style="margin-left:18px; padding-left:18px; text-align:left ;">
    <li style="text-align:left ;">“Integration windows like the one Gold.com is in right now are when network blind spots and security risks typically surface.”</li>
    <li style="text-align:left ;">“We can benchmark your environment against similar high-growth fintech companies to ensure your infrastructure is NYSE-ready.”</li>
    <li style="text-align:left ;">“Even if now isn’t the right time, we can map out pressure points across your trading & fulfillment network for your 2026 roadmap.”</li>
</ul>

<p style="font-weight:bold; margin-top:20px; text-align:left;">🟢 If the Client Shows Interest</p>
<ul style="margin-left:18px; padding-left:18px; text-align:left ;">
    <li style="text-align:left ;">“Great — the next step is a 15-minute discovery to map your post-acquisition trading, auction, and fulfillment paths.”</li>
    <li style="text-align:left ;">“We’ll show how <b>XYZ Global Networks</b> can support scale, uptime, and secure multi-site operations tailored for Gold.com.”</li>
    <li style="text-align:left ;">“How does your calendar look later this week?”</li>
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

    st.session_state.setdefault("company_input_insight", "AvePoint")

    scope = st.session_state.insight_scope
    company_name = st.session_state.get("company_input_insight") or "AvePoint"
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
        ("🏢 AvePoint Deep Dive",    "Give me a deep dive on avepoint"),
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
        company = company_name.lower().strip()

        if company == "wolfspeed":
            with st.spinner("⚙️ Generating Wolfspeed scouting report..."):
                time.sleep(6)
            st.success("Showing scouting report for Wolfspeed")
            render_sales_report(WOLFSPEED_SCOUTING_REPORT)

        # elif company in ["a-mark", "amark", "a-mark precious metals", "a mark", "a mark precious metals"]:
        #     with st.spinner("⚙️ Generating A-Mark Precious Metals scouting report..."):
        #         time.sleep(6)
        #     st.success("Showing scouting report for A-Mark Precious Metals")
        #     render_sales_report(A_MARK_SCOUTING_REPORT)

        elif company in ["avepoint"]:
            with st.spinner("⚙️ Generating AvePoint scouting report..."):
                time.sleep(6)
            st.success("Showing scouting report for AvePoint")
            render_sales_report(AVEPOINT_SCOUTING_REPORT)

        else:
            with st.spinner("⚙️ Generating AvePoint scouting report..."):
                time.sleep(6)
            st.success("Showing scouting report for AvePoint")
            render_sales_report(AVEPOINT_SCOUTING_REPORT)

        st.markdown("</div>", unsafe_allow_html=True)
        return



   
    # --- Seller Pitch  ---
    if content_type == "Seller Pitch":
        company = company_name.lower().strip()

        if company in ["a-mark", "amark", "a-mark precious metals", "a mark", "a mark precious metals"]:
            with st.spinner("⚙️ Building seller pitch for A-Mark Precious Metals..."):
                time.sleep(6)
            st.success("Showing Seller Pitch for A-Mark Precious Metals")
            render_seller_pitch_amark()

        elif company in ["wolfspeed"]:
            with st.spinner("⚙️ Building seller pitch for Wolfspeed..."):
                time.sleep(6)
            st.success("Showing Seller Pitch for Wolfspeed")
            render_seller_pitch_wolfspeed()

        elif company in ["avepoint"]:
            with st.spinner("⚙️ Building seller pitch for AvePoint..."):
                time.sleep(6)
            st.success("Showing Seller Pitch for AvePoint")
            render_seller_pitch_avepoint()

        else:
            st.warning("Seller pitch is not available for this company.")

        st.markdown("</div>", unsafe_allow_html=True)
        return


    # --- Marketing Campaign / Marketing Email ---
    if content_type == "Personalized Email":
        
        if company_name.lower() == "wolfspeed":
            with st.spinner("⚙️ Generating personalized email for Wolfspeed..."):
                time.sleep(6)
            st.success(f"Showing marketing email for Wolfspeed")
            render_marketing_email_wolfspeed()
        
        elif company_name.lower() in ["a-mark", "amark", "a-mark precious metals", "a mark", "a mark precious metals"]:  
            with st.spinner("⚙️ Generating personalized email for A-Mark Precious Metals..."):
                time.sleep(6)
            st.success("Showing marketing email for A-Mark Precious Metals")
            render_marketing_email_amark()

        elif company_name.lower() in ["avepoint"]:  
            with st.spinner("⚙️ Generating personalized email for AvePoint..."):
                time.sleep(6)
            st.success("Showing marketing email for AvePoint")
            render_marketing_email_avepoint()
        
        else:
            st.warning("No marketing email available for this company.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown("</div>", unsafe_allow_html=True)


