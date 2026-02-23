import pandas as pd
import re, html, os, time
from typing import List, Dict
import streamlit as st
import streamlit.components.v1 as components
import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "Files"
ACCOUNT_SUMMARY_PATH   = FILES_DIR / "account_summary.xlsx"
RECOMMENDATIONS_PATH   = FILES_DIR / "recommendations.xlsx"

# --------------------------------------------------
# CSS (Combined from both files)
# --------------------------------------------------
st.markdown(
    """
<style>
/* ===== PAGE HEADER ===== */
.page-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 4px;
}
.page-desc {
    color: #555;
    font-size: 0.95rem;
    margin-bottom: 20px;
}

/* ===== AGENT LOG BOX ===== */
.agent-log-box {
    background: #faf4ff;
    border-radius: 8px;
    border: 1px dashed #d7c6ff;
    padding: 12px 14px;
    font-size: 13px;
    color: #3b2a6f;
    margin-bottom: 16px;
}
.agent-log-line { margin-bottom: 4px; }

.agent-log-line.title {
    font-weight: 700;
    color: #6b00b8;
    margin-bottom: 6px;
}

.step-label { color: #6b00b8; font-weight: 700; }
.agent-log-line.info { color: #4a3b8f; }
.agent-log-line.success { color: #1b7f3b; }
.agent-log-line.source-tag {
    display: inline-block;
    background: #ede9fe;
    border: 1px solid #c4b5fd;
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 11px;
    color: #6b21a8;
    margin-left: 6px;
    font-weight: 600;
}
.agent-log-empty { color: #999; font-style: italic; }

/* ===== TASK CARD ===== */
.task-card {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    margin-bottom: 20px;
    background-color: #ffffff;
    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);
    padding: 15px;
}
.task-card-header { display: flex; align-items: center; margin-bottom: 10px; }
.task-name {
    font-weight: 600;
    font-size: 1.05rem;
    color: #1f2937;
    display: flex;
    align-items: center;
    gap: 6px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    border-right: 1px solid #e6e6e6;
    width: 400px !important;
    min-width: 400px !important;
}
[data-testid="stSidebar"] > div:first-child {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 1.2rem 1rem 1rem 1rem;
    background: linear-gradient(to bottom, #f7f7f9 0%, #f7f7f9 60%, #f1f1f4 60%, #f1f1f4 100%);
}
.sidebar-header { display: flex; align-items: center; gap: 10px; margin-bottom: 18px; }
.sidebar-logo-img {
    width: 44px; height: 44px; border-radius: 12px; background: #fff;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.sidebar-logo-img img { width: 32px; height: auto; }
.sidebar-title-block { display: flex; flex-direction: column; font-weight: 800; color: #18181b; }
.sidebar-title-block span { font-size: 1.5rem !important; font-weight: 800 !important; color: #18181b !important; line-height: 1.2; letter-spacing: -0.3px; }
.scope-title { color: #6b00b8; font-weight: 700; font-size: 0.9rem; }

.sidebar-user-inline { display: flex; align-items: center; gap: 8px; padding-top: 6px; }
.sidebar-user-avatar-inline {
    width: 32px; height: 32px; border-radius: 50%; background: #f3ecff;
    border: 1px solid #d3c3ff; display: flex; align-items: center; justify-content: center;
    font-size: 18px; color: #8b6cff;
}
.sidebar-user-name-inline { font-weight: 600; color: #6b00b8; font-size: 0.9rem; }
.sidebar-user-name-inline span { font-weight: 700; }
.sidebar-user-role-inline { color: #666; font-size: 0.85rem; margin-top: 2px; }

.sidebar-logout-wrapper { width: 100%; display: flex; justify-content: center; margin-top: 10px; }
.sidebar-logout-wrapper button { min-width: 120px; }
.stButton > button { white-space: nowrap !important; }

/* ===== FILE UPLOADER ===== */
div[data-testid="stFileUploader"] > label { color: #6b00b8 !important; font-weight: 600 !important; }
div[data-testid="stFileUploader"] { background: #fff; border: 1px solid #dcdcdc; border-radius: 10px; padding: 10px 12px 14px; }
div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] { border: none !important; background: transparent !important; padding: 6px !important; }
div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] span { font-size: 0.9rem !important; }
div[data-testid="stFileUploader"] button { background-color: #6b00b8 !important; color: white !important; border-radius: 8px !important; padding: 6px 14px !important; border: none !important; }
div[data-testid="stFileUploader"] button:hover { background-color: #54008f !important; }

/* Progress bar */
progress.progress-inline {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    border: none;
    background: #f3f4f6;
}
progress.progress-inline::-webkit-progress-bar {
    background: #f3f4f6;
    border-radius: 4px;
}
progress.progress-inline::-webkit-progress-value {
    background: #6b00b8;
    border-radius: 4px;
}
progress.progress-inline::-moz-progress-bar {
    background: #6b00b8;
    border-radius: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
/* Output Box Styling */
.output-box {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 12px;
    margin-top: 10px;
    border: 1px solid #eef0f2;
}
.output-box ul {
    margin-top: 5px;
    margin-bottom: 0;
    padding-left: 20px;
}
.output-box li {
    margin-bottom: 4px;
    font-size: 13px;
    color: #4b5563;
}

.kv .label {
    font-weight: 700;
    font-size: 1.05rem;
    color: #1f2937;
    display: block;
    margin-bottom: 5px;
}
.small-muted {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 10px;
}

/* ===== PRIORITIZATION TABLE ===== */
.prioritization-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    line-height: 1.4;
    color: #374151;
    min-width: 1400px;
}

.prioritization-table thead th {
    background-color: #f9fafb;
    color: #4b5563;
    font-weight: 600;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 2px solid #e5e7eb;
    position: sticky;
    top: 0;
    z-index: 10;
}

.prioritization-table tbody tr {
    border-bottom: 1px solid #f3f4f6;
    transition: background-color 0.15s ease;
}

.prioritization-table tbody tr:hover {
    background-color: #f9fafb;
}

.prioritization-table tbody td {
    padding: 12px 16px;
    vertical-align: top;
}

.prioritization-table .col-idx {
    width: 20px;
    font-size: 12px;
    color: #9ca3af;
    padding-right: 0;
}

.prioritization-table .col-priority {
    width: 80px;
}

.priority-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    line-height: 1;
}

.priority-high {
    background-color: #d1fae5;
    color: #065f46;
    border: 1px solid #34d399;
}
.priority-medium {
    background-color: #fffbeb;
    color: #92400e;
    border: 1px solid #fcd34d;
}
.priority-low {
    background-color: #fee2e2;
    color: #991b1b;
    border: 1px solid #f87171;
}

.prioritization-table .col-rationale {
    min-width: 300px;
}

.scrollable-table-wrapper {
    overflow-x: auto;
    max-height: 500px;
    overflow-y: auto;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    margin-top: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
/* ===== CAPABILITY CHIPS ===== */
.cap-chip {
    display: inline-block; padding: 4px 10px; border-radius: 999px;
    font-size: 11px; font-weight: 600;
    background: linear-gradient(135deg, #eef2ff, #e0e7ff);
    color: #4338ca; border: 1px solid #c7d2fe;
    margin: 3px 5px 3px 0; white-space: nowrap;
}

/* ===== PRODUCT CARDS ===== */
.product-card {
    border: 2px solid #e5e7eb; border-radius: 14px; padding: 16px;
    background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    height: 360px; min-height: 360px; max-height: 360px;
    display: flex; flex-direction: column;
    transition: all 0.3s ease; position: relative; overflow: hidden; margin-bottom: 18px;
}
.product-card::before {
    content:''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transform: scaleX(0); transition: transform 0.3s ease;
}
.product-card:hover::before { transform: scaleX(1); }
.product-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(102,126,234,0.15); border-color: #667eea; }

.card-header { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px; }

.card-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: #f0f0f5;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
}
.card-title-section { flex: 1; min-width: 0; }
.product-title { font-weight: 700; font-size: 0.92rem; color: #111827; line-height: 1.3; margin-bottom: 6px; }
.product-meta { display: flex; gap: 6px; flex-wrap: wrap; }
.meta-line-compact {
    font-size: 10.5px;
    color: #6b7280;
    margin-bottom: 3px;
    line-height: 1.5;
}

.meta-line-compact strong {
    font-weight: 600;
    color: #374151;
    margin-right: 4px;
}
.product-desc { font-size: 0.8rem; color: #6b7280; line-height: 1.4; margin-bottom: 10px; font-style: italic; }
.product-benefits { font-size: 0.8rem; color: #4b5563; line-height: 1.5; margin-bottom: 10px; flex: 1; overflow-y: auto; }
.product-benefits ul { margin: 0; padding-left: 16px; }
.product-benefits li { margin-bottom: 4px; }
.product-link { display: inline-flex; align-items: center; gap: 5px; font-size: 0.75rem; color: #667eea; text-decoration: none; font-weight: 600; margin-bottom: 10px; transition: all 0.2s ease; }
.product-link:hover { color: #764ba2; gap: 7px; }
.product-footer { margin-top: auto; padding-top: 10px; border-top: 1px dashed #e5e7eb; display: flex; flex-wrap: wrap; gap: 5px; }

</style>
""",
    unsafe_allow_html=True,
)

st.markdown("""
<style>
/* ===== UNIFIED TABLE SYSTEM ===== */
:root {
  --table-font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --table-bg: #ffffff;
  --table-border: #e2e8f0;
  --header-bg: #f9fafb;
  --header-text: #64748b;
  --row-alt: #f8fafc;
  --row-hover: #f5f3ff;
  --accent: #7c3aed;
  --text: #0f172a;
  --muted: #64748b;
}

/* Table Container */
.unified-table-card {
  background: var(--table-bg);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  overflow: hidden;
  border: 1px solid var(--table-border);
  font-family: var(--table-font);
}

.unified-table-wrap {
  overflow-x: auto;
  overflow-y: auto;
  max-height: 600px;
}

/* Scrollbar Styling */
.unified-table-wrap::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}
.unified-table-wrap::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}
.unified-table-wrap::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
  border: 2px solid #f1f5f9;
}
.unified-table-wrap::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Base Table */
.unified-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  background: white;
  min-width: 1200px;
}

/* Sticky Header */
.unified-table thead th {
  position: sticky;
  top: 0;
  background: var(--header-bg);
  padding: 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 800;
  color: var(--header-text);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #edf2f7;
  z-index: 10;
}

/* Table Rows */
.unified-table tbody tr {
  border-bottom: 1px solid #edf2f7;
  border-left: 4px solid transparent;
}
.unified-table tbody tr:nth-child(even) {
  background-color: var(--row-alt);
}
.unified-table tbody tr:hover {
  background-color: var(--row-hover) !important;
  border-left: 4px solid var(--accent);
}

/* Table Cells */
.unified-table td {
  padding: 18px 16px;
  vertical-align: middle;
  color: var(--text);
  font-size: 12px;
  line-height: 1.5;
}

/* Company Name - Consistent */
.company-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text);
  display: block;
  margin-bottom: 6px;
  line-height: 1.3;
}

/* Priority Pills */
.priority-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 11px;
  border: 1px solid;
  white-space: nowrap;
}
.p-high { background: #dcfce7; color: #15803d; border-color: #86efac; }
.p-medium { background: #fef3c7; color: #d97706; border-color: #fbbf24; }
.p-low { background: #fee2e2; color: #dc2626; border-color: #fca5a5; }

/* Tags & Pills */
.tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  background: #dbeafe;
  color: #1e40af;
  white-space: nowrap;
  margin: 0 4px 4px 0;
}

.pill {
  display: inline-flex;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
  border: 1px solid;
  white-space: nowrap;
  margin: 0 4px 4px 0;
}
.pill-amber { background: #fef3c7; color: #d97706; border-color: #fbbf24; }
.pill-green { background: #dcfce7; color: #15803d; border-color: #86efac; }

/* Text Styles */
.muted {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.6;
}

.cell-score strong {
  font-weight: 700;
  color: #0f172a;
}

.cell-explain {
  margin-top: 4px;
  color: #475569;
  font-size: 12px;
}

/* Expandable Details */
.trigger-details {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  margin-top: 8px;
}
.trigger-summary {
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
}
.trigger-summary::-webkit-details-marker { display: none; }
.trigger-summary::before {
  content: '→';
  margin-right: 8px;
  color: #a855f7;
  transition: 0.2s;
}
.trigger-details[open] .trigger-summary::before {
  transform: rotate(90deg);
}
.trigger-details[open] .trigger-summary {
  border-bottom: 1px solid #f1f5f9;
}
.trigger-content {
  padding: 12px;
  font-size: 12px;
  color: #334155;
  line-height: 1.5;
  background: #fafafa;
  border-radius: 0 0 8px 8px;
}
</style>
""", unsafe_allow_html=True)

GLOBAL_IFRAME_TABLE_CSS = """
<style>
/* ===== UNIFIED TABLE SYSTEM (iframe-safe) ===== */
:root {
  --table-font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --table-bg: #ffffff;
  --table-border: #e2e8f0;
  --header-bg: #f9fafb;
  --header-text: #64748b;
  --row-alt: #f8fafc;
  --row-hover: #f5f3ff;
  --accent: #7c3aed;
  --text: #0f172a;
  --muted: #64748b;
}

/* Container */
.unified-table-card {
  background: var(--table-bg);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--table-border);
  font-family: var(--table-font);
}

/* Scroll wrapper */
.unified-table-wrap {
  overflow-x: auto;
  overflow-y: auto;
  max-height: 600px;
}

/* Base table */
.unified-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  background: white;
  min-width: 1200px;
}

/* Sticky header */
.unified-table thead th {
  position: sticky;
  top: 0;
  background: var(--header-bg);
  padding: 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 800;
  color: var(--header-text);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #edf2f7;
  z-index: 10;
}

/* Rows */
.unified-table tbody tr {
  border-bottom: 1px solid #edf2f7;
  border-left: 4px solid transparent;
}
.unified-table tbody tr:nth-child(even) { background-color: var(--row-alt); }
.unified-table tbody tr:hover {
  background-color: var(--row-hover) !important;
  border-left: 4px solid var(--accent);
}

/* Cells */
.unified-table td {
  padding: 18px 16px;
  vertical-align: middle;
  color: var(--text);
  font-size: 12px;
  line-height: 1.5;
  white-space: normal;
  overflow-wrap: anywhere;
  word-break: break-word;
}

/* Text helpers */
.company-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text);
  display: block;
  margin-bottom: 6px;
  line-height: 1.3;
}
.muted {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.6;
}

/* Pills/tags used in Account Summary */
.tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  background: #dbeafe;
  color: #1e40af;
  white-space: nowrap;
  margin: 0 4px 4px 0;
}

.pill {
  display: inline-flex;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
  border: 1px solid;
  white-space: nowrap;
  margin: 0 4px 4px 0;
}
.pill-amber { background: #fef3c7; color: #d97706; border-color: #fbbf24; }
.pill-green { background: #dcfce7; color: #15803d; border-color: #86efac; }
</style>
"""

st.markdown("""
<style>
/* ===== ENHANCED TABS - REDUCED TOP SPACING ===== */
.stTabs {
    margin-top: -20px;  /* Pull tabs up closer to sidebar */
}

.stTabs [data-baseweb="tab-list"] {
    gap: 16px;
    padding: 0;
    margin-bottom: 16px;
    border-bottom: 2px solid #e5e7eb;
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    padding: 0 20px;
    background-color: transparent;
    border-radius: 6px 6px 0 0;
    font-size: 14.5px;
    font-weight: 600;
    color: #6b7280;
    border: none;
    border-bottom: 3px solid transparent;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #374151;
    background-color: #f9fafb;
    border-bottom: 3px solid #d1d5db;
}

.stTabs [aria-selected="true"] {
    color: #1f2937 !important;
    background-color: #fafafa !important;
    border-bottom: 3px solid #6b00b8 !important;
    font-weight: 700;
}

/* ===== PAGE HEADER - TIGHTER SPACING ===== */
.page-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 8px;
    margin-top: 8px;  /* Reduced even more */
    color: #1f2937;
}
.page-desc {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 14px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ===== REMOVE TOP WHITESPACE ABOVE TABS ===== */

/* Main app container */
.block-container {
    padding-top: 0.5rem !important;
}

/* Tabs wrapper */
.stTabs {
    margin-top: -30px !important;
}

/* Extra spacer div Streamlit injects */
.stTabs > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Tab list itself */
.stTabs [data-baseweb="tab-list"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# Global CSS Injection (aligned with data_engineer style)
# -------------------------------------------------------------------
def _get_global_css() -> str:
    """Returns the custom CSS for lead prioritization + logs."""
    return """
<style>

/* Progress bar for tasks (same visual as data_engineer) */
progress.progress-inline {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    border: none;
    background: #f3f4f6;
}
progress.progress-inline::-webkit-progress-bar {
    background: #f3f4f6;
    border-radius: 4px;
}
progress.progress-inline::-webkit-progress-value {
    background: #6b00b8;
    border-radius: 4px;
}
progress.progress-inline::-moz-progress-bar {
    background: #6b00b8;
    border-radius: 4px;
}

/* =======================
    Agentic log styling
    ======================= */
.agent-log-box {
    background: #faf4ff;  /* soft lavender */
    border-radius: 8px;
    border: 1px dashed #d7c6ff;
    padding: 10px 12px;
    font-size: 13px;
    color: #3b2a6f;
    margin-bottom: 10px;
    max-height: none;
    overflow-y: visible;
}
.agent-log-line {
    margin-bottom: 4px;
}
.agent-log-line.title {
    font-weight: 700;
    color: #6b00b8;
    margin-bottom: 6px;
}
.agent-log-line.info {
    color: #4a3b8f;
}
.agent-log-line.success {
    color: #1b7f3b;
}
.agent-log-line.meta {
    color: #777;
    font-size: 12px;
}
.agent-log-empty {
    color: #999;
    font-style: italic;
}

/* Task Card Styling */
.task-card {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    margin-bottom: 20px;
    background-color: #ffffff;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.02);
    padding: 15px;
}
.task-card-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.task-name {
    font-weight: 600;
    font-size: 1.05rem;
    color: #1f2937;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Output Box Styling */
.output-box {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 12px;
    margin-top: 10px;
    border: 1px solid #eef0f2;
}
.output-box ul {
    margin-top: 5px;
    margin-bottom: 0;
    padding-left: 20px;
}
.output-box li {
    margin-bottom: 4px;
    font-size: 13px;
    color: #4b5563;
}

/* Prioritization summary header */
.kv .label {
    font-weight: 700;
    font-size: 1.05rem;
    color: #1f2937;
    display: block;
    margin-bottom: 5px;
}
.small-muted {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 10px;
}

/* Reuse same title + description classes as data_engineer */
.main-title {
    text-align: left !important;
    margin: 0 0 4px 0;
}
.panel-desc-left {
    text-align: left !important;
    margin: 0 0 14px 0;
    color: #555;
    font-size: 0.98rem;
    line-height: 1.45;
}


/* =======================
    Custom Table Styling for Lead Prioritization (NEW STYLES)
    ======================= */
.prioritization-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    line-height: 1.4;
    color: #374151; /* Dark text */
}

.prioritization-table thead th {
    background-color: #f9fafb; /* Light header background */
    color: #4b5563; /* Header text color */
    font-weight: 600;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 2px solid #e5e7eb;
    position: sticky;
    top: 0;
    z-index: 10;
}

.prioritization-table tbody tr {
    border-bottom: 1px solid #f3f4f6; /* Subtle row separator */
    transition: background-color 0.15s ease;
}

.prioritization-table tbody tr:hover {
    background-color: #f9fafb; /* Light hover effect */
}

.prioritization-table tbody td {
    padding: 12px 16px;
    vertical-align: top;
}

/* Index Column */
.prioritization-table .col-idx {
    width: 20px;
    font-size: 12px;
    color: #9ca3af;
    padding-right: 0;
}

/* Priority Column */
.prioritization-table .col-priority {
    width: 80px;
}

/* The actual badge styling */
.priority-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    line-height: 1;
}

/* Priority Color Mapping */
.priority-high {
    background-color: #d1fae5; /* Light Green */
    color: #065f46; /* Dark Green */
    border: 1px solid #34d399;
}
.priority-medium {
    background-color: #fffbeb; /* Light Yellow */
    color: #92400e; /* Dark Yellow */
    border: 1px solid #fcd34d;
}
.priority-low {
    background-color: #fee2e2; /* Light Red/Pink */
    color: #991b1b; /* Dark Red */
    border: 1px solid #f87171;
}

/* Explicit minimum width for the Rationale column to ensure it is visible */
.prioritization-table .col-rationale {
    min-width: 300px; 
}


/* Add this class to your global CSS or ensure the table is wrapped */
.scrollable-table-wrapper {
    overflow-x: auto; /* Enables horizontal scrolling if content exceeds width */
    max-height: 500px; /* Optional: Adds vertical scrolling after 500px */
    overflow-y: auto;
    border: 1px solid #e5e7eb; /* Optional: Gives the wrapper a subtle border */
    border-radius: 8px;
    margin-top: 10px;
}

/* Ensure the prioritization-table uses its full width to enable scrolling */
.prioritization-table {
    /* Set a minimum width greater than the container to force scrolling */
    min-width: 1400px; 
    border-collapse: collapse;
    font-size: 14px;
    line-height: 1.4;
    color: #374151;
}

/* Remove the header styling for the 'Ix' column (it was removed in Python too, this is a guardrail) */
.prioritization-table thead th:last-child {
    /* display: none; */ 
    /* Removing this line because the last 'th' is now 'Priority Rationale' */
    /* The index 'th' is correctly the first child, so no need for this style */
}
</style>
"""

# -------------------------------------------------------------------
# Small helpers
# -------------------------------------------------------------------
def status_dot(color: str = "#ccc", size: int = 12) -> str:
    """Colored dot HTML used in headers."""
    return (
        f"<div style='width:{size}px; height:{size}px; border-radius:50%; "
        f"background:{color}; display:inline-block;'></div>"
    )

# --------------------------------------------------
# TASK DEFINITIONS
# --------------------------------------------------
ALL_TASKS = [
    {"name": "Loading Customer 360° Data", "key": "load_data", "step_num": 1, "tab": "tab1"},
    {"name": "Business Context Analyzer", "key": "business_context", "step_num": 2, "tab": "tab1"},
    {"name": "AI-Driven Category Weights", "key": "category_weights", "step_num": 3, "tab": "tab1"},
    {"name": "Prioritization Segment Classifier", "key": "prioritization_table", "step_num": 4, "tab": "tab1"},
    {"name": "Product Catalogue Analyzer", "key": "product_catalog", "step_num": 5, "tab": "tab2"},
    {"name": "AI Recommender Agent", "key": "recommender_agent", "step_num": 6, "tab": "tab2"},
]

SIMULATE_TIME_PER_STEP = 0.6 


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def status_dot(color="#ccc", size=12):
    return (f"<span style='display:inline-block;width:{size}px;height:{size}px;"
            f"border-radius:50%;background:{color};margin-right:8px;'></span>")


# --------------------------------------------------
# STATE INITIALIZATION
# --------------------------------------------------
st.session_state.setdefault("run_process", False)
st.session_state.setdefault("stop_process", False)
st.session_state.setdefault("step_done", {})
st.session_state.setdefault("log_html", {})
st.session_state.setdefault("task_running", {})

# Business context default
default_context = (
"We aim to expand our presence among mid-market technology companies in North America, focusing on SaaS and Cloud Computing sectors. "
"While our enterprise data analytics and AI-powered business intelligence offerings are strong, identifying companies with growth signals in a competitive market remains a challenge.\n\n"
"As a result, sales teams lack actionable insights to prioritize accounts and position the right telecom and AI solutions effectively.\n\n"
"Our goal is to enhance targeting, segmentation, and sales intelligence to drive adoption of advanced analytics tools, deepen market share in the mid-market technology segment, "
"and accelerate revenue growth by aligning execution with the evolving needs of digitally advanced companies."
)
if "business_context_text" not in st.session_state:
    st.session_state.business_context_text = default_context

# --------------------------------------------------
# PRODUCT CATALOG DATA
# --------------------------------------------------
PRODUCT_CATALOG = [
    # ===== CLOUD =====
    {"category": "Cloud","sub_category": "Colocation","url": "https://example.com/products/cloud/colocation","desc": "Colocation data center services to support hybrid multi-cloud environments with secure, scalable infrastructure.","benefit_1": "Enables agile hybrid multi-cloud environments","benefit_2": "Improves reliability, security, and application performance","benefit_3": "Scales with business demand across sites/regions","benefit_4": "Reduces cost/effort of on-prem data centers","segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": True,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": True,"complexity": "High","flexibility": "Standard"},
    {"category": "Cloud","sub_category": "Content Delivery Network","url": "https://example.com/products/cloud/content-delivery-network","desc": "CDN capabilities to improve end-user performance using distributed delivery and caching.","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "Mid-Market, Enterprise","industries": "Media, E-commerce, Technology, All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Standard"},
    {"category": "Cloud","sub_category": "Private Cloud Connectivity","url": "https://example.com/products/cloud/private-cloud-connectivity","desc": "Private, secure cloud connectivity for predictable performance and reduced exposure to internet-borne threats.","benefit_1": "Secure private connectivity to cloud providers","benefit_2": "Predictable, scalable bandwidth","benefit_3": "Lower latency for cloud applications","benefit_4": "Reduces exposure to DDoS and common threats","segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": False,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Flexible"},
    {"category": "Cloud","sub_category": "Managed Cloud Connect","url": "https://example.com/products/cloud/managed-cloud-connect","desc": "Managed cloud connectivity service to simplify private access to cloud providers and support hybrid cloud networking.","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Standard"},
    {"category": "Cloud","sub_category": "Cloud Connections On-Demand","url": "https://example.com/products/cloud/cloud-connections-on-demand","desc": "On-demand multi-cloud connectivity with scalable bandwidth, redundancy, and protection from public internet threats.","benefit_1": "Faster multi-cloud connectivity rollout","benefit_2": "Resilient connections with redundancy/geo-diversity","benefit_3": "Keeps traffic private to reduce breach/DDoS exposure","benefit_4": "Self-service bandwidth scaling","segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Flexible"},

    # ===== MOBILITY =====
    {"category": "Mobility Solutions","sub_category": "Mobile 5G","url": "https://example.com/products/mobility/mobile-5g","desc": "High-speed mobile connectivity to support mobile teams and advanced use cases (e.g., AR/VR) with security-focused design options.","benefit_1": "High-speed mobile connectivity for productivity","benefit_2": "Supports advanced applications (e.g., AR/VR)","benefit_3": "Designed to integrate with existing systems","benefit_4": "Security-focused service options","segments": "Small, Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": True,"cost_opt": False,"complexity": "Medium","flexibility": "Flexible"},  
    {"category": "Mobility Solutions","sub_category": "On-Premise Edge","url": "https://example.com/products/mobility/on-premise-edge","desc": "On-premise connectivity, control, and compute to enable low-latency access and integration with cloud services.","benefit_1": "Improves connectivity within campus/premises","benefit_2": "Low-latency connections for critical apps","benefit_3": "Secure access for business data","benefit_4": "Integrates with cloud providers","segments": "Mid-Market, Enterprise","industries": "Manufacturing, Logistics, Healthcare, All Industries","multi_site": True,"resilience": False,"zero_trust": True,"real_time": True,"edge_compute": True,"cost_opt": False,"complexity": "High","flexibility": "Standard"},
    {"category": "Mobility Solutions","sub_category": "On-Premises Cellular Network","url": "https://example.com/products/mobility/on-premises-cellular-network","desc": "Managed on-premises cellular coverage for reliable connectivity, capacity, and support for edge/IoT/AR/VR workloads.","benefit_1": "Improves coverage and capacity on premises","benefit_2": "Supports edge compute and local data needs","benefit_3": "Enables IoT/AI/mobile robotics use cases","benefit_4": "Supports AR/VR and bandwidth-intensive apps","segments": "Mid-Market, Enterprise","industries": "Manufacturing, Warehousing, Healthcare, All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": True,"cost_opt": False,"complexity": "High","flexibility": "Standard" },
    {"category": "Mobility Solutions","sub_category": "Private Cellular Networks","url": "https://example.com/products/mobility/private-cellular-networks","desc": "Dedicated private wireless network for greater control, security, device density, and latency-sensitive operations.","benefit_1": "Improves control and flexibility for local operations","benefit_2": "Built-in security controls for sensitive workloads","benefit_3": "Supports increased device density and lower latency","benefit_4": "Local configuration options for performance tuning","segments": "Mid-Market, Enterprise","industries": "Manufacturing, Utilities, Logistics, All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": False,"complexity": "High","flexibility": "Standard" },

    # ===== NETWORKS =====
    {"category": "Business Internet","sub_category": "Business Fiber Internet","url": "https://example.com/products/networks/business-fiber-internet","desc": "Business-grade fiber internet supporting critical operations, cloud apps, collaboration, and continuity via backup connectivity options.","benefit_1": "Fast, reliable connectivity for critical operations","benefit_2": "Supports collaboration and cloud apps","benefit_3": "Business continuity via backup connectivity","benefit_4": "Cost savings via bundles/packaging (where applicable)","segments": "SOHO, Small, Mid-Market","industries": "Professional Services, Retail, Hospitality, Education, All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": True,"complexity": "Low","flexibility": "Flexible"},
    {"category": "Business Internet","sub_category": "Dedicated Internet","url": "https://example.com/products/networks/dedicated-internet","desc": "Dedicated, symmetrical internet with strong uptime targets, low latency, and integrated security options for critical workloads.","benefit_1": "Guaranteed symmetrical performance (service dependent)","benefit_2": "High availability for business-critical usage","benefit_3": "Low latency for cloud and collaboration apps","benefit_4": "Integrated security options for threat defense","segments": "Mid-Market, Enterprise","industries": "Finance, Retail, Healthcare, Media, All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Standard"},
    {"category": "Business Internet","sub_category": "Wireless Internet for Business","url": "https://example.com/products/networks/wireless-internet-for-business","desc": "Fixed wireless internet for business sites with simplified setup and predictable usage (service dependent).","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "SOHO, Small, Mid-Market","industries": "Retail, Hospitality, Professional Services, All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": True,"edge_compute": False,"cost_opt": True,"complexity": "Low","flexibility": "Flexible",},
    {"category": "Business Internet","sub_category": "Wireless Broadband","url": "https://example.com/products/networks/wireless-broadband","desc": "Wireless broadband connectivity for sites requiring flexible access options.","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "SOHO, Small, Mid-Market","industries": "All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Low","flexibility": "Flexible" },

    # ===== SECURITY =====
    {"category": "Cybersecurity services","sub_category": "Dynamic Defense","url": "https://example.com/products/security/dynamic-defense","desc": "Network-embedded cybersecurity using threat intelligence and analytics for real-time detection and blocking before threats reach the perimeter.","benefit_1": "Real-time threat detection and response","benefit_2": "Helps prevent threats from reaching perimeter controls","benefit_3": "Uses global threat intelligence and layered security","benefit_4": "Can reduce operational security burden","segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Standard",},
    {"category": "Cybersecurity services","sub_category": "SASE","url": "https://example.com/products/security/sase","desc": "Cloud-delivered SASE combining connectivity and security controls to enable secure access for branch, remote, and cloud workloads.","benefit_1": "Simplifies management via a single cloud platform","benefit_2": "Secure access for remote/mobile users","benefit_3": "Improved performance via intelligent routing","benefit_4": "Consolidation can reduce costs","segments": "Mid-Market, Enterprise","industries": "Finance, Healthcare, Government, Technology, All Industries","multi_site": True,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": True,"complexity": "High","flexibility": "Standard",},
    {"category": "Cybersecurity services","sub_category": "SD-WAN","url": "https://example.com/products/security/sd-wan","desc": "Managed SD-WAN to improve performance, accelerate site deployment, support multi-cloud networking, and embed security capabilities.","benefit_1": "Rapid deployment across multiple sites","benefit_2": "Improves reliability with redundancy options","benefit_3": "Optimizes multi-cloud workloads and routing","benefit_4": "Built-in security and operational cost efficiencies","segments": "Mid-Market, Enterprise","industries": "Retail, Education, Finance, Healthcare, All Industries","multi_site": True,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": True,"cost_opt": True,"complexity": "High","flexibility": "Standard", },

    # ===== IoT =====
    {"category": "Internet of Things","sub_category": "IoT Platforms","url": "https://example.com/products/iot/iot-platforms","desc": "IoT connectivity and management platform to deploy, manage, and monetize connected devices with security and cost monitoring features.","benefit_1": "Global device connectivity and lifecycle management","benefit_2": "Diagnostics/analytics to improve service reliability","benefit_3": "Security features to protect device and data flows","benefit_4": "Usage monitoring to optimize costs","segments": "Mid-Market, Enterprise","industries": "Manufacturing, Logistics, Utilities, Transport, Smart Cities, All Industries","multi_site": True,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": True,"complexity": "High","flexibility": "Long-term",},
    {"category": "Internet of Things","sub_category": "Vehicle Solutions","url": "https://example.com/products/iot/vehicle-solutions","desc": "Connected vehicle solutions for fleet and automotive-related IoT use cases.","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "Mid-Market, Enterprise","industries": "Transport, Logistics, Automotive, All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Standard",},
    {"category": "Internet of Things","sub_category": "Asset Management","url": "https://example.com/products/iot/asset-management","desc": "IoT asset tracking and monitoring for powered/unpowered assets to improve visibility, utilization, and downtime reduction.","benefit_1": "Real-time visibility into asset status and location","benefit_2": "Reduces downtime via proactive monitoring","benefit_3": "Improves asset utilization and lifecycle outcomes","benefit_4": "Supports cost savings and better customer experience","segments": "Mid-Market, Enterprise","industries": "Logistics, Manufacturing, Construction, Energy, All Industries","multi_site": True,"resilience": True,"zero_trust": True,"real_time": False,"edge_compute": False,"cost_opt": True,"complexity": "Medium","flexibility": "Standard",},
    {"category": "Internet of Things","sub_category": "IoT Professional Services","url": "https://example.com/products/iot/iot-professional-services","desc": "End-to-end services to define, design, certify, and launch IoT initiatives, including prioritization and operational cost control.","benefit_1": "Defines and designs IoT programs and use cases","benefit_2": "Accelerates deployment and certification activities","benefit_3": "Supports connected environment integrations","benefit_4": "Helps control operational/service costs","segments": "Mid-Market, Enterprise","industries": "Manufacturing, Logistics, Utilities, Smart Cities, All Industries","multi_site": True,"resilience": False,"zero_trust": False,"real_time": True,"edge_compute": True,"cost_opt": True,"complexity": "High","flexibility": "Flexible",},
    {"category": "Internet of Things","sub_category": "Smart Cities and Communities","url": "https://example.com/products/iot/smart-cities-and-communities","desc": "IoT-enabled city solutions to improve sustainability and citizen services via connected infrastructure and analytics.","benefit_1": "Improves operational agility using near-real-time IoT data","benefit_2": "Enables actionable insights via analytics","benefit_3": "Supports connected infrastructure modernization","benefit_4": "Helps reduce energy, waste, and operating costs","segments": "Enterprise, Public Sector","industries": "Government, Smart Cities, Utilities","multi_site": True,"resilience": False,"zero_trust": False,"real_time": True,"edge_compute": True,"cost_opt": True,"complexity": "High","flexibility": "Long-term",},

    # ===== UNIFIED COMMUNICATIONS =====
    {"category": "Voice and collaboration","sub_category": "UC & Contact Center Platform","url": "https://example.com/products/unified-communications/uc-contact-center-platform","desc": "Unified communications platform for voice, video, messaging, and contact center capabilities with app integrations and multi-device support.","benefit_1": "Unified calling, messaging, and meetings","benefit_2": "Supports flexible/remote work patterns","benefit_3": "Integrates with common business apps","benefit_4": "Advanced call management and analytics features","segments": "Small, Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": True,"zero_trust": False,"real_time": True,"edge_compute": False,"cost_opt": True,"complexity": "Medium","flexibility": "Flexible",},
    {"category": "Voice and collaboration","sub_category": "IP Toll-Free","url": "https://example.com/products/unified-communications/ip-toll-free","desc": "Inbound VoIP toll-free service with routing, queuing, and recording options to improve customer reach and reduce operational complexity.","benefit_1": "Improves customer accessibility via toll-free reach","benefit_2": "Advanced routing/queuing for better response handling","benefit_3": "Consolidates voice and data for efficiency","benefit_4": "Can lower operating costs and complexity","segments": "Mid-Market, Enterprise","industries": "Retail, Finance, Healthcare, Utilities, All Industries","multi_site": True,"resilience": True,"zero_trust": False,"real_time": True,"edge_compute": False,"cost_opt": True,"complexity": "Medium","flexibility": "Standard",    },
    {"category": "Voice and collaboration","sub_category": "SIP Trunking","url": "https://example.com/products/unified-communications/sip-trunking","desc": "SIP trunking to consolidate voice and data over shared access with flexible call capacity and multi-site trunk sharing.","benefit_1": "Consolidates voice and data over integrated access","benefit_2": "Flexible call channel management to control costs","benefit_3": "Supports multi-site trunk sharing and virtual numbers","benefit_4": "Reliable business-grade calling experience","segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": True,"resilience": True,"zero_trust": True,"real_time": False,"edge_compute": False,"cost_opt": True,"complexity": "Medium","flexibility": "Flexible",    },
    {"category": "Voice and collaboration","sub_category": "Cloud Voice for Teams","url": "https://example.com/products/unified-communications/cloud-voice-for-teams","desc": "Cloud voice connectivity integrated with collaboration platforms to simplify global calling and reduce on-site hardware needs.","benefit_1": "Simplifies management and reduces on-site hardware","benefit_2": "Reliable calling integrated with collaboration tools","benefit_3": "Easier adds/changes for sites and numbers","benefit_4": "Supports global calling and collaboration","segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": True,"resilience": True,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": True,"complexity": "Medium","flexibility": "Standard",    },
    {"category": "Voice and collaboration","sub_category": "Teams Phone Mobile","url": "https://example.com/products/unified-communications/teams-phone-mobile","desc": "Mobile-first unified communications integrating mobile devices with collaboration calling to consolidate services and improve experience.","benefit_1": "Mobile-first unified communications experience","benefit_2": "Consolidates calling services to reduce redundancy","benefit_3": "Improves overall experience via prioritization options (service dependent)","benefit_4": "Supports meetings, calling, and collaboration in one app","segments": "Small, Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": False,"zero_trust": True,"real_time": False,"edge_compute": False,"cost_opt": True,"complexity": "Low","flexibility": "Flexible",    },
    {"category": "Voice and collaboration","sub_category": "Next Generation 9-1-1","url": "https://example.com/products/unified-communications/next-generation-9-1-1","desc": "Modernized emergency communications using secure IP-based technology to handle voice, data, and video with improved interoperability.","benefit_1": "Modernizes legacy emergency communications to IP-based","benefit_2": "Improves resiliency and reliability","benefit_3": "Supports voice, data, and video incident handling","benefit_4": "Enables better information sharing and reconstruction","segments": "Public Sector, Enterprise","industries": "Government, Public Safety","multi_site": True,"resilience": True,"zero_trust": True,"real_time": True,"edge_compute": False,"cost_opt": False,"complexity": "High","flexibility": "Standard",    },

    # ===== WIRELESS SERVICES =====
    {"category": "Wireless services","sub_category": "International Business Mobile Plans","url": "https://example.com/products/mobility/international-business-mobile-plans","desc": "International roaming and add-ons for business mobility users.","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "Small, Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Low","flexibility": "Flexible",},
    {"category": "Wireless services","sub_category": "Field Management","url": "https://example.com/products/mobility/field-management","desc": "Mobile workforce tools to support field operations.","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "Small, Mid-Market, Enterprise","industries": "Field Services, Logistics, Construction, All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Low","flexibility": "Flexible",   },
    {"category": "Wireless services","sub_category": "Mobile Business Solutions","url": "https://example.com/products/mobility/mobile-business-solutions","desc": "Subscription-based mobility services and consulting to support predictable costs and improved security for mobile/IoT estates.","benefit_1": "Predictable monthly cost model for devices/services","benefit_2": "Consulting support for mobile strategy and risk","benefit_3": "Helps reduce corporate security risks","benefit_4": "Supports bundling/standardization of device estates","segments": "Small, Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": True,"zero_trust": True,"real_time": False,"edge_compute": False,"cost_opt": True,"complexity": "Low","flexibility": "Flexible",   },
    {"category": "Wireless services","sub_category": "Mobile Remote Access","url": "https://example.com/products/mobility/mobile-remote-access","desc": "Secure remote access extending core networks to remote employees, mobile workers, and temporary locations for seamless collaboration.","benefit_1": "Extends core network access to remote/mobile users","benefit_2": "Supports remote and temporary locations","benefit_3": "Persistent secure connectivity and controls","benefit_4": "Operational intelligence to maximize uptime","segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": True,"resilience": True,"zero_trust": True,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Standard",   },
    {"category": "Wireless services","sub_category": "Mobility Professional Services","url": "https://example.com/products/mobility/mobility-professional-services","desc": "Professional services for mobility strategy, rollout, and operations.","benefit_1": None,"benefit_2": None,"benefit_3": None,"benefit_4": None,"segments": "Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": False,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Flexible",    },
    {"category": "Wireless services","sub_category": "Bring Your Own Device","url": "https://example.com/products/mobility/bring-your-own-device","desc": "BYOD onboarding to add employee-owned devices to business mobility services with streamlined provisioning.","benefit_1": "Simplifies onboarding of employee-owned devices","benefit_2": "Supports multiple device types (phones/tablets/etc.)","benefit_3": "Streamlines adding lines or porting numbers","benefit_4": None,"segments": "SOHO, Small, Mid-Market, Enterprise","industries": "All Industries","multi_site": False,"resilience": True,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Low","flexibility": "Flexible",    },
    {"category": "Wireless services","sub_category": "In-Building Wireless","url": "https://example.com/products/mobility/in-building-wireless","desc": "In-building wireless solutions to strengthen indoor mobility signals, improve coverage, and support high user density.","benefit_1": "Maintains critical connectivity across more areas","benefit_2": "Boosts indoor coverage and throughput","benefit_3": "Supports many simultaneous users","benefit_4": None,"segments": "Mid-Market, Enterprise","industries": "Manufacturing, Healthcare, Retail, Venues, All Industries","multi_site": False,"resilience": True,"zero_trust": False,"real_time": False,"edge_compute": False,"cost_opt": False,"complexity": "Medium","flexibility": "Standard", },
]

CATEGORY_ICONS = {
    "Cloud": "☁️",                    
    "Cybersecurity services": "🛡️",   
    "Business Internet": "🌐",        
    "Mobility Solutions": "📶",       
    "Internet of Things": "🔗",       
    "Voice and collaboration": "🎧",  
    "Wireless services": "📡",        
}


CAP_FLAG_MAP = {
    "multi_site": "Multi-Site",
    "resilience": "Business Resilience",
    "zero_trust": "Zero Trust",
    "real_time": "Real-Time",
    "edge_compute": "Edge Computing",
    "cost_opt": "Cost Optimized"
}

# --------------------------------------------------
# STEP LOGS
# --------------------------------------------------
STEP_LOGS = {

    "load_data": [
    "<strong>⚙️ Initializing Customer 360° Context Assembly Agent…</strong>",
    "📥 Retrieving consolidated Customer 360° profiles from the ingestion & enrichment phase.",
    "🧩 Validating presence of all core intelligence dimensions:",
    "     • 🏢 Firmographics & organizational footprint",
    "     • 💻 Technographic maturity & competitor context",
    "     • 📈 Growth indicators",
    "     • 💰 Financial and Est. Potential Spend",
    "     • 🎯 Intent signals and priority badges",
    "🗂️ Normalizing account-level attributes for downstream reasoning.",
    "📊 Preparing unified Customer 360° view for scoring and recommendation agents.",
    "✅ <span style='color:#1b7f3b;font-weight:700;'>Customer 360° context ready — handing off to Business Context Analyzer.</span>",
    ],

    
    "business_context": [
        "<strong>⚙️ Initializing Business Context Analyzer Agent…</strong>",
        "🧠 Analyzing narrative input to extract structured context dimensions…",
        "🎯 Identified business objective and strategic intent.",
        "👥 Classified target segment and customer archetype.",
        "🗺️ Recognized operational geography and market coverage.",
        "🧩 Mapped key product focus areas (Connectivity, Internet, Communication, Security).",
        "⚠️ Highlighted business challenges impacting GTM execution.",
        "📈 Derived success metrics aligned to revenue and penetration goals.",
        "🔗 Passing calibrated strategic context to Category Weight Optimizer for relevance weighting.",
        "✅ <span style='color:#1b7f3b;font-weight:700;'>Business context translated into actionable signals for downstream weighting and prioritization.</span>",
    ],
    
    "category_weights": [
    "<strong>⚙️ Initializing Category & Signal Weighting Agent…</strong>",
    "🧠 Consuming business context to understand GTM priorities, target segments, and product focus.",
    "🧩 Decomposing Customer 360° intelligence into primary signal categories:",
    "🔍 Evaluating sub-signals within each category for strategic relevance:",
    "   📈 Growth Signals: Expansion and acquisition flags, Hiring momentum, YoY revenue and TCV growth trends etc..",
    "   🎯 Intent Intelligence: Explicit vs peer-led intent classification, Domain relevance to priority products, Intent strength and recency etc..",
    "   💻 Technographics: Network, cloud, and security maturity, complexity vs solution readiness etc..",
    "   💰 Financial Indicators: Spend potential tier, Share of wallet and contract trajectory etc..",
    "⚖️ Assigning context-aware weights at category and sub-signal level",
    "📐 Producing calibrated scoring framework aligned to business objectives.",
    "🔗 Passing weighted signal model to Prioritization Segment Classifier for account-level scoring.",
    "✅ <span style='color:#1b7f3b;font-weight:700;'>Category and sub-signal weighting complete — scoring logic contextually optimized.</span>",
    ],

    "prioritization_table": [
    "<strong>⚙️ Initializing Prioritization & Segmentation Agent…</strong>",
    "🧠 Receiving calibrated category and sub-signal weights from Strategic Weighting Agent.",
    "🔗 Aggregating weighted signals for each account across Customer 360° dimensions:",
    "📊 Computing composite priority scores per account using context-aware weighting model.",
    "🧩 Normalizing scores to account for signal overlap and correlated indicators.",
    "🏷️ Translating composite scores into actionable priority segments:",
    "    • High — immediate GTM focus",
    "    • Medium — nurture and monitor",
    "    • Low — deprioritize or long-term watch",
    "🔍 Attaching explainability metadata to each account:",
    "    • Dominant contributing signal categories",
    "    • Key drivers influencing priority assignment",
    "📋 Generating ranked prioritization table with transparent rationale.",
    "✅ <span style='color:#1b7f3b;font-weight:700;'>Account prioritization complete — sales-ready priority segments generated.</span>",
    ],

    "product_catalog": [
        "<strong>⚙️ Initializing Product Catalogue Analyzer Agent…</strong>",
        "📦 Loading product catalogue source — <strong>18 Enterprise products</strong> across 6 L1 categories… <span class='source-tag'>Catalog Source</span>",
        "🔍 <strong>L1 Category Scan</strong> — Networks · Cloud · Security · Mobility Solutions · IoT · Unified Communications… <span class='source-tag'>L1 Taxonomy</span>",
        "🏷️ <strong>L2 Sub-Category Extraction</strong> — SDN, Adaptive Networks, Satellite, Broadband, Cloud Solutions, Cloud Connectivity, Cloud Advisory, SASE, Incident Response, Cyber Detection, Business Apps, Satellite Messaging, Enterprise Mobility, IoT Solutions, IoT Platform, Contact Center, UC Consulting, Calling & Collaboration… <span class='source-tag'>L2 Taxonomy</span>",
        "📝 Parsing <strong>product descriptions</strong> and mapping to enterprise use-case archetypes… <span class='source-tag'>NLP Engine</span>",
        "✨ Extracting <strong>key benefits</strong> — 3–4 value propositions per product, ranked by GTM relevance… <span class='source-tag'>Benefit Extraction</span>",
        "🏢 Tagging <strong>target segments</strong> — SOHO / Small / Mid-Market / Enterprise per product… <span class='source-tag'>Segment Classifier</span>",
        "🏭 Mapping <strong>priority industries</strong> — Construction, Mining, Energy, Healthcare, Logistics, Finance, Education, Manufacturing… <span class='source-tag'>Industry Mapper</span>",
        "🎨 Evaluating <strong>capability flags</strong> — Multi-site, Business Resilience, Zero Trust, Real-Time, Edge Computing, Cost Optimized… <span class='source-tag'>Capability Engine</span>",
        "📊 Scoring <strong>deployment complexity</strong> (Low / Medium / High) and <strong>contract flexibility</strong> per product… <span class='source-tag'>Risk Scorer</span>",
        "🔗 Building <strong>product-to-customer fit matrix</strong> — capability × industry × segment cross-reference… <span class='source-tag'>Fit Matrix</span>",
        "✅ <span style='color:#1b7f3b;font-weight:700;'>Product catalogue analysis complete — 18 products indexed, tagged, and fit-mapped.</span>",
    ],


    "recommender_agent": [
    "<strong>⚙️ Initializing AI Recommendation & Decisioning Agent…</strong>",
    "🤖 Activating multi-dimensional decision engine using enriched Customer 360° profiles and product capability intelligence.",
    "🔗 Ingesting upstream intelligence: - Account priority segments and composite scores, Growth and market momentum signals, Intent domains, Technographic maturity and existing product footprint",
    "🎯 Evaluating intent-to-capability alignment for each account, Mapping dominant intent themes to relevant product use-cases",
    "🏭 Applying industry and operating-model context.",
    "    • Construction → site connectivity, IoT, adaptive networks",
    "    • Mining → remote connectivity, satellite, IoT platforms",
    "    • Healthcare → collaboration, secure connectivity, compliance-ready solutions",
    "    • Manufacturing → cloud, security, global network resilience",
    "💻 Assessing expansion feasibility - Existing product footprint and adjacency potential, Contract posture and renewal windows, Spend tier and share-of-wallet headroom",
    "📊 Computing recommendation fit scores per product such as Capability overlap score, Intent relevance score, Industry affinity score etc.. ",
    "🧩 Ranking top 1–3 recommendations per account based on composite fit score.",
    "📝 Generating explainability layer for each recommendation:",
    "   • Primary trigger signals",
    "   • Supporting context and rationale",
    "   • Confidence indicators for sales engagement",
    "📋 Assembling final recommendation matrix with product, fit score, and rationale.",
    "✅ <span style='color:#1b7f3b;font-weight:700;'>Recommendations generated — explainable, prioritized, and ready for GTM execution.</span>",
    ]

}

# -------------------------------------------------------------------
# Format helpers for details
# -------------------------------------------------------------------
def _format_account_summary_table_html() -> str:
    """ACQ Account Summary Table - HTML for iframe with intent keywords + growth/risk signals + ICP snapshot"""
    print("ACQ Account Summary Table - Complete HTML for iframe with intent keywords")
    try:
        df = pd.read_excel(ACCOUNT_SUMMARY_PATH, sheet_name="Complete")
    except Exception as e:
        return f"<div style='padding:20px; color:#dc2626;'>Error: {e}</div>"

    if df.empty:
        return "<div style='padding:20px; color:#64748b;'>No data available.</div>"

    html_out = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f1f5f9;
    }
    .table-card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.05);
      overflow: hidden;
      border: 1px solid #e2e8f0;
    }
    .table-wrap {
      overflow-x: auto;
      overflow-y: auto;
      max-height: 580px;
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      background: white;
      min-width: 1200px;
    }
    .data-table thead th {
      position: sticky;
      top: 0;
      background: #f9fafb;
      padding: 16px;
      text-align: left;
      font-size: 11px;
      font-weight: 800;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid #edf2f7;
      z-index: 10;
    }
    .data-table tbody tr {
      border-bottom: 1px solid #edf2f7;
      border-left: 4px solid transparent;
    }
    .data-table tbody tr:nth-child(even) {
      background-color: #f8fafc;
    }
    .data-table tbody tr:hover {
      background-color: #f5f3ff !important;
      border-left: 4px solid #7c3aed;
    }
    .data-table td {
      padding: 18px 16px;
      vertical-align: top;
      color: #0f172a;
      font-size: 12px;
      line-height: 1.5;
    }
    .company-name {
      font-weight: 600;
      font-size: 14px;
      color: #0f172a;
      display: block;
      margin-bottom: 6px;
      line-height: 1.3;
    }
    .tag {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      background: #dbeafe;
      color: #1e40af;
      white-space: nowrap;
      margin: 0 4px 4px 0;
    }
    .pill {
      display: inline-flex;
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      border: 1px solid;
      white-space: nowrap;
      margin: 0 4px 4px 0;
    }
    .pill-amber { background: #fef3c7; color: #d97706; border-color: #fbbf24; }
    .pill-green { background: #dcfce7; color: #15803d; border-color: #86efac; }
    .pill-red { background: #fee2e2; color: #b91c1c; border-color: #fecaca; }
    .muted {
      font-size: 12px;
      color: #64748b;
      line-height: 1.6;
    }

    /* Intent styling */
    .intent-item {
      font-size: 12px;
      color: #334155;
      line-height: 1.5;
      padding-left: 10px;
      border-left: 2px solid #e9d5ff;
      margin-bottom: 8px;
    }
    .intent-domain {
      font-weight: 700;
      color: #0f172a;
    }
    .intent-score {
      color: #6b21a8;
      font-weight: 700;
      margin-left: 6px;
    }
    .intent-keyword {
      display: block;
      font-size: 11px;
      color: #7c3aed;
      font-style: italic;
      margin-top: 2px;
    }

    .table-wrap::-webkit-scrollbar { width: 12px; height: 12px; }
    .table-wrap::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 10px; }
    .table-wrap::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; border: 2px solid #f1f5f9; }
    .table-wrap::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    </style>
    </head>
    <body>
    <div class="table-card">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 80px;">ID</th>
              <th style="width: 220px;">Account</th>
              <th style="width: 260px;">Industry Profile</th>
              <th style="width: 260px;">Signals (Growth + Risk)</th>
              <th style="width: 380px;">Intent</th>
            </tr>
          </thead>
          <tbody>
    """

    for _, r in df.iterrows():
        acc_id = str(r.get("Account ID", "") or "").strip()
        acc_name = str(r.get("Account Name", "") or "")
        industry = str(r.get("Industry", "") or "")
        sub_industry = str(r.get("Sub-Industry", "") or "")
        fte = str(r.get("FTE Size", "") or "")
        revenue = str(r.get("Revenue Range", "") or "")
        location = str(r.get("City / State", "") or "")

        # ---------------------------
        # ICP Snapshot (Industry/Sub-industry)
        # ---------------------------

        industry_lines = []

        if industry and industry not in ["nan", "—"]:
            industry_lines.append(
                f"<div><strong>Industry:</strong> {html.escape(industry)}</div>"
            )

        if sub_industry and sub_industry not in ["nan", "—"]:
            industry_lines.append(
                f"<div><strong>Sub-Industry:</strong> {html.escape(sub_industry)}</div>"
            )

        if industry_lines:
            icp_html = "<div style='margin-top:8px;'>" + "".join(industry_lines) + "</div>"
        else:
            icp_html = "<div class='muted'>—</div>"

        # ---------------------------
        # Signals: remove TCV, keep YoY + Growth + Risk pills
        # ---------------------------
        yoy_growth = str(r.get("YoY Growth", "") or "")

        growth_tags = []
        if r.get("Acquisition") == "✓ Yes":
            growth_tags.append("<span class='pill pill-green'>✓ Acquisition</span>")
        if r.get("Expansion") == "✓ Yes":
            growth_tags.append("<span class='pill pill-green'>✓ Expansion</span>")
        if r.get("Partnership") == "✓ Yes":
            growth_tags.append("<span class='pill pill-green'>✓ Partnership</span>")
        if r.get("Hiring") == "✓ Yes":
            growth_tags.append("<span class='pill pill-green'>✓ Hiring</span>")
        if r.get("Funding") == "✓ Yes":
            growth_tags.append("<span class='pill pill-green'>✓ Funding</span>")

        risk_tags = []
        if str(r.get("Layoff", "") or "").strip() in ["Yes", "✓ Yes"]:
            risk_tags.append("<span class='pill pill-red'>⚠ Layoff</span>")
        if str(r.get("Financial Risk", "") or "").strip() in ["Yes", "✓ Yes", "High"]:
            risk_tags.append("<span class='pill pill-red'>⚠ Financial Risk</span>")

        # YoY line only if present
        yoy_line = ""
        if yoy_growth and yoy_growth not in ["nan", "—", ""]:
            yoy_line = f"<div class='muted'><strong>YoY:</strong> {html.escape(yoy_growth)}</div>"

        growth_pills = "".join(growth_tags)
        risk_pills = "".join(risk_tags)

        # If everything absent -> show dash
        if (not yoy_line) and (not growth_pills) and (not risk_pills):
            signals_html = "<div class='muted'>—</div>"
        else:
            signals_html = ""
            if yoy_line:
                signals_html += yoy_line
            if growth_pills:
                signals_html += f"<div style='margin-top:6px;'>{growth_pills}</div>"
            if risk_pills:
                signals_html += f"<div style='margin-top:6px;'>{risk_pills}</div>"

        # ---------------------------
        # Intent (UNCHANGED from your logic)
        # ---------------------------
        intent_items = []
        for i in (1, 2, 3):
            dom = r.get(f"Intent Domain {i}")
            score = r.get(f"Score {i}")
            keyword = r.get(f"Keyword {i}")

            if pd.notna(dom) and pd.notna(score) and str(dom) not in ["—", "nan", ""]:
                try:
                    score_val = int(float(score))
                except Exception:
                    continue

                kw_html = ""
                if pd.notna(keyword) and str(keyword) not in ["nan", "", "—"]:
                    kw_html = f"<span class='intent-keyword'>→ {html.escape(str(keyword))}</span>"

                intent_items.append(
                    f"""
                    <div class="intent-item">
                      <span class="intent-domain">{html.escape(str(dom))}</span>
                      <span class="intent-score">({score_val})</span>
                      {kw_html}
                    </div>
                    """
                )

        intent_html = "".join(intent_items) if intent_items else "<div class='muted'>—</div>"

        html_out += f"""
          <tr>
            <td>#{html.escape(acc_id)}</td>
            <td>
              <span class="company-name">{html.escape(acc_name)}</span>
              <div class="muted">
                📍 {html.escape(location)}<br>
                👥 {html.escape(fte)}<br>
                💰 {html.escape(revenue)}
              </div>
            </td>
            <td>{icp_html}</td>
            <td>{signals_html}</td>
            <td>{intent_html}</td>
          </tr>
        """

    html_out += """
          </tbody>
        </table>
      </div>
    </div>
    </body>
    </html>
    """
    return html_out

def _format_account_summary_table_html_old() -> str:
    """Account Summary Table - Complete HTML for iframe with top alignment and intent keywords"""
    print("Account Summary Table - Complete HTML for iframe with top alignment and intent keywords")
    try:
        df = pd.read_excel(ACCOUNT_SUMMARY_PATH, sheet_name="Complete")
    except Exception as e:
        return f"<div style='padding:20px; color:#dc2626;'>Error: {e}</div>"
    
    if df.empty:
        return "<div style='padding:20px; color:#64748b;'>No data available.</div>"
    
    html_out = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f1f5f9;
    }
    .table-card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.05);
      overflow: hidden;
      border: 1px solid #e2e8f0;
    }
    .table-wrap {
      overflow-x: auto;
      overflow-y: auto;
      max-height: 580px;
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      background: white;
      min-width: 1200px;
    }
    .data-table thead th {
      position: sticky;
      top: 0;
      background: #f9fafb;
      padding: 16px;
      text-align: left;
      font-size: 11px;
      font-weight: 800;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid #edf2f7;
      z-index: 10;
    }
    .data-table tbody tr {
      border-bottom: 1px solid #edf2f7;
      border-left: 4px solid transparent;
    }
    .data-table tbody tr:nth-child(even) {
      background-color: #f8fafc;
    }
    .data-table tbody tr:hover {
      background-color: #f5f3ff !important;
      border-left: 4px solid #7c3aed;
    }
    .data-table td {
      padding: 18px 16px;
      vertical-align: top;  /* TOP ALIGNED */
      color: #0f172a;
      font-size: 12px;
      line-height: 1.5;
    }
    .company-name {
      font-weight: 600;
      font-size: 14px;
      color: #0f172a;
      display: block;
      margin-bottom: 6px;
      line-height: 1.3;
    }
    .tag {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      background: #dbeafe;
      color: #1e40af;
      white-space: nowrap;
      margin: 0 4px 4px 0;
    }
    .pill {
      display: inline-flex;
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      border: 1px solid;
      white-space: nowrap;
      margin: 0 4px 4px 0;
    }
    .pill-amber { background: #fef3c7; color: #d97706; border-color: #fbbf24; }
    .pill-green { background: #dcfce7; color: #15803d; border-color: #86efac; }
    .muted {
      font-size: 12px;
      color: #64748b;
      line-height: 1.6;
    }
    /* Intent styling */
    .intent-item {
      font-size: 12px;
      color: #334155;
      line-height: 1.5;
      padding-left: 10px;
      border-left: 2px solid #e9d5ff;
      margin-bottom: 8px;
    }
    .intent-domain {
      font-weight: 700;
      color: #0f172a;
    }
    .intent-score {
      color: #6b21a8;
      font-weight: 700;
      margin-left: 6px;
    }
    .intent-keyword {
      display: block;
      font-size: 11px;
      color: #7c3aed;
      font-style: italic;
      margin-top: 2px;
    }
    .table-wrap::-webkit-scrollbar {
      width: 12px;
      height: 12px;
    }
    .table-wrap::-webkit-scrollbar-track {
      background: #f1f5f9;
      border-radius: 10px;
    }
    .table-wrap::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 10px;
      border: 2px solid #f1f5f9;
    }
    .table-wrap::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }
    </style>
    </head>
    <body>
    <div class="table-card">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 80px;">ID</th>
              <th style="width: 220px;">Account</th>
              <th style="width: 200px;">Active Products</th>
              <th style="width: 200px;">Growth & Signals</th>
              <th style="width: 380px;">Intent</th>
            </tr>
          </thead>
          <tbody>
    """
    
    for idx, r in df.iterrows():
        acc_id = str(r.get("Account ID", "") or "").strip()
        acc_name = str(r.get("Account Name", "") or "")
        industry = str(r.get("Industry", "") or "")
        fte = str(r.get("FTE Size", "") or "")
        revenue = str(r.get("Revenue Range", "") or "")
        location = str(r.get("City / State", "") or "")
        
        # Products
        renewal = r.get("Renewal_Due_Next_180Days")
        renewal_products = []
        if pd.notna(renewal) and str(renewal).strip() not in ["—", "nan", ""]:
            renewal_products = [p.strip() for p in str(renewal).split(",") if p.strip()]
        
        products = str(r.get("Active Products", "") or "")
        products_html = ""
        if products and products not in ["nan", "—"]:
            tags = []
            for p in products.split(","):
                p_clean = p.strip()
                if not p_clean:
                    continue
                if p_clean in renewal_products:
                    tags.append(f"<span class='pill pill-amber'>* {html.escape(p_clean)}</span>")
                else:
                    tags.append(f"<span class='tag'>{html.escape(p_clean)}</span>")
            products_html = "<div>" + "".join(tags) + "</div>"
        else:
            products_html = "<div class='muted'>—</div>"
        
        # Growth
        tcv_growth = str(r.get("TCV Growth (3Yr)", "") or "")
        yoy_growth = str(r.get("YoY Growth", "") or "")
        signal_tags = []
        if r.get("Acquisition") == "✓ Yes":
            signal_tags.append("<span class='pill pill-green'>✓ Acquisition</span>")
        if r.get("Expansion") == "✓ Yes":
            signal_tags.append("<span class='pill pill-green'>✓ Expansion</span>")
        if r.get("Partnership") == "✓ Yes":
            signal_tags.append("<span class='pill pill-green'>✓ Partnership</span>")
        if r.get("Hiring") == "✓ Yes":
            signal_tags.append("<span class='pill pill-green'>✓ Hiring</span>")
        
        growth_lines = []
        if tcv_growth and tcv_growth not in ["nan", "—", "0%"]:
            growth_lines.append(f"<div class='muted'><strong>TCV:</strong> {html.escape(tcv_growth)}</div>")
        if yoy_growth and yoy_growth not in ["nan", "—", ""]:
            growth_lines.append(f"<div class='muted'><strong>YoY:</strong> {html.escape(yoy_growth)}</div>")
        
        growth_text = "".join(growth_lines) if growth_lines else "<div class='muted'>—</div>"
        signal_text = "".join(signal_tags) if signal_tags else "<span class='muted'>—</span>"
        growth_html = f"{growth_text}<div style='margin-top:6px;'>{signal_text}</div>"
        
        # Intent WITH KEYWORDS
        intent_items = []
        for i in (1, 2, 3):
            dom = r.get(f"Intent Domain {i}")
            score = r.get(f"Score {i}")
            keyword = r.get(f"Keyword {i}")
            
            if pd.notna(dom) and pd.notna(score) and str(dom) not in ["—", "nan", ""]:
                try:
                    score_val = int(float(score))
                except Exception:
                    continue
                
                # Add keyword if available
                kw_html = ""
                if pd.notna(keyword) and str(keyword) not in ["nan", "", "—"]:
                    kw_html = f"<span class='intent-keyword'>→ {html.escape(str(keyword))}</span>"
                
                intent_items.append(
                    f"""
                    <div class="intent-item">
                      <span class="intent-domain">{html.escape(str(dom))}</span>
                      <span class="intent-score">({score_val})</span>
                      {kw_html}
                    </div>
                    """
                )
        
        intent_html = "".join(intent_items) if intent_items else "<div class='muted'>—</div>"
        
        html_out += f"""
          <tr>
            <td>#{html.escape(acc_id)}</td>
            <td>
              <span class="company-name">{html.escape(acc_name)}</span>
              <div class="muted">
                📍 {html.escape(location)}<br>
                👥 {html.escape(fte)}<br>
                🏢 {html.escape(industry)}
              </div>
            </td>
            <td>{products_html}</td>
            <td>{growth_html}</td>
            <td>{intent_html}</td>
          </tr>
        """
    
    html_out += """
          </tbody>
        </table>
      </div>
    </div>
    </body>
    </html>
    """
    return html_out

def _business_context_html_from_text(ctx_text: str) -> str:
    import re, html

    if not ctx_text or str(ctx_text).strip() == "":
        ctx_text = ""

    paragraphs = [p.strip() for p in re.split(r"\n{1,2}", str(ctx_text)) if p.strip()]
    objective = html.escape(paragraphs[0]) if paragraphs else "(no objective provided)"

    # Acquisition Use Case (Updated)
    target_segment = "Mid-Market Businesses"
    geography = "United States"
    primary_goal = "Acquisition (New Customer Growth)"

    key_products = [
        "Connectivity services (Fixed, Broadband, Ethernet)",
        "Unified Communications & Collaboration",
        "Network & Cloud Security solutions",
        "IoT / Edge Solutions",
    ]

    key_challenges = [
        "Limited visibility into which prospects are actively in-market and ready to buy",
        "Difficulty identifying and prioritizing the highest-fit accounts across large prospect pools",
        "Lack of actionable signals to time outreach effectively and improve engagement rates",
    ]

    success_metrics = [
        "Increased new customer acquisition (logos won)",
        "Higher lead-to-opportunity conversion rates",
        "Improved win rate and faster sales cycle (time-to-close)",
        "Higher pipeline velocity and revenue growth from new customers",
    ]

    html_out = f"""
<div style="font-family: Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#f6f7fb; padding:16px;">
  <div style="max-width:1050px; margin:0 auto;">

    <!-- Card -->
    <div style="background:#ffffff; border:1px solid #e5e7eb; border-radius:16px; box-shadow:0 10px 30px rgba(15,23,42,.08); overflow:hidden;">

      <!-- Body -->
      <div style="padding:18px 20px; background:#ffffff;">

        <!-- Objective -->
        <div style="border:1px solid #e2e8f0; background:#f8fafc; border-radius:14px; padding:14px 14px 12px; margin-bottom:14px;">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <div style="width:26px; height:26px; border-radius:10px; background:#ede9fe; border:1px solid #ddd6fe; display:grid; place-items:center; color:#6b21a8;">🎯</div>
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; font-weight:900; color:#64748b;">Business Objective</div>
          </div>

          <div style="font-size:13px; line-height:1.6; color:#0f172a; font-weight:650;">
            {objective}
          </div>

          <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
            <span style="display:inline-flex; padding:6px 10px; border-radius:999px; background:#ffffff; border:1px solid #e2e8f0; font-size:11px; font-weight:800; color:#334155;">
              Primary Goal: Acquire new customers
            </span>
            <span style="display:inline-flex; padding:6px 10px; border-radius:999px; background:#ffffff; border:1px solid #e2e8f0; font-size:11px; font-weight:800; color:#334155;">
              Discovery: Identify in-market prospects
            </span>
            <span style="display:inline-flex; padding:6px 10px; border-radius:999px; background:#ffffff; border:1px solid #e2e8f0; font-size:11px; font-weight:800; color:#334155;">
              Execution: Prioritize high-fit accounts
            </span>
          </div>
        </div>

        <!-- Highlights row -->
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:14px;">
          <div style="border:1px solid #e2e8f0; border-radius:14px; padding:12px; background:#ffffff;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <div style="width:24px; height:24px; border-radius:10px; background:#dcfce7; border:1px solid #bbf7d0; display:grid; place-items:center;">👥</div>
              <div style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; font-weight:900; color:#64748b;">Target Segment</div>
            </div>
            <div style="font-weight:900; color:#0f172a; font-size:13px;">{html.escape(target_segment)}</div>
            <div style="font-size:12px; color:#64748b; margin-top:4px; line-height:1.5;">Prospective mid-market accounts with high-fit characteristics.</div>
          </div>

          <div style="border:1px solid #e2e8f0; border-radius:14px; padding:12px; background:#ffffff;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <div style="width:24px; height:24px; border-radius:10px; background:#dbeafe; border:1px solid #bfdbfe; display:grid; place-items:center;">📍</div>
              <div style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; font-weight:900; color:#64748b;">Geography</div>
            </div>
            <div style="font-weight:900; color:#0f172a; font-size:13px;">{html.escape(geography)}</div>
            <div style="font-size:12px; color:#64748b; margin-top:4px; line-height:1.5;">Prioritize high-growth regions and whitespace opportunities.</div>
          </div>

          <div style="border:1px solid #e2e8f0; border-radius:14px; padding:12px; background:#ffffff;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <div style="width:24px; height:24px; border-radius:10px; background:#fef3c7; border:1px solid #fde68a; display:grid; place-items:center;">⚡</div>
              <div style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; font-weight:900; color:#64748b;">Primary Goal</div>
            </div>
            <div style="font-weight:900; color:#0f172a; font-size:13px;">{html.escape(primary_goal)}</div>
            <div style="font-size:12px; color:#64748b; margin-top:4px; line-height:1.5;">Drive net-new revenue through targeted acquisition.</div>
          </div>
        </div>

        <!-- Two panels -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">

          <!-- Key Products -->
          <div style="border:1px solid #e2e8f0; border-radius:14px; padding:14px; background:#ffffff;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
              <div style="width:26px; height:26px; border-radius:10px; background:#ede9fe; border:1px solid #ddd6fe; display:grid; place-items:center;">🧩</div>
              <div style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; font-weight:900; color:#64748b;">Key Products</div>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:8px;">
              <span style="display:inline-flex; padding:7px 10px; border-radius:999px; background:#f8fafc; border:1px solid #e2e8f0; font-size:11px; font-weight:900; color:#0f172a;">🌐 Connectivity (Fixed/Broadband/Ethernet)</span>
              <span style="display:inline-flex; padding:7px 10px; border-radius:999px; background:#f8fafc; border:1px solid #e2e8f0; font-size:11px; font-weight:900; color:#0f172a;">💬 UC & Collaboration</span>
              <span style="display:inline-flex; padding:7px 10px; border-radius:999px; background:#f8fafc; border:1px solid #e2e8f0; font-size:11px; font-weight:900; color:#0f172a;">🔒 Network & Cloud Security</span>
              <span style="display:inline-flex; padding:7px 10px; border-radius:999px; background:#f8fafc; border:1px solid #e2e8f0; font-size:11px; font-weight:900; color:#0f172a;">🔗 IoT / Edge</span>
            </div>

            <div style="margin-top:10px; font-size:12px; color:#64748b; line-height:1.6;">
              Focus areas mapped to intent + technographics for prospect-level fit scoring.
            </div>
          </div>

          <!-- Key Challenges -->
          <div style="border:1px solid #e2e8f0; border-radius:14px; padding:14px; background:#ffffff;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
              <div style="width:26px; height:26px; border-radius:10px; background:#fee2e2; border:1px solid #fecaca; display:grid; place-items:center;">⚠️</div>
              <div style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; font-weight:900; color:#64748b;">Key Challenges</div>
            </div>

            <ul style="margin:0; padding-left:18px; color:#0f172a; font-size:12.5px; line-height:1.7;">
              <li style="margin-bottom:8px;">{html.escape(key_challenges[0])}</li>
              <li style="margin-bottom:8px;">{html.escape(key_challenges[1])}</li>
              <li style="margin-bottom:0;">{html.escape(key_challenges[2])}</li>
            </ul>

            <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
              <span style="display:inline-flex; padding:6px 10px; border-radius:999px; background:#fff7ed; border:1px solid #fed7aa; font-size:11px; font-weight:900; color:#9a3412;">Need: intent signals</span>
              <span style="display:inline-flex; padding:6px 10px; border-radius:999px; background:#fff7ed; border:1px solid #fed7aa; font-size:11px; font-weight:900; color:#9a3412;">Need: prioritization</span>
              <span style="display:inline-flex; padding:6px 10px; border-radius:999px; background:#fff7ed; border:1px solid #fed7aa; font-size:11px; font-weight:900; color:#9a3412;">Need: timing precision</span>
            </div>
          </div>
        </div>

        <!-- Success metrics -->
        <div style="border:1px solid #e2e8f0; border-radius:14px; padding:14px; background:#ffffff;">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <div style="width:26px; height:26px; border-radius:10px; background:#dcfce7; border:1px solid #bbf7d0; display:grid; place-items:center;">✅</div>
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; font-weight:900; color:#64748b;">Success Metrics</div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div style="border:1px solid #e2e8f0; border-radius:12px; padding:10px 12px; background:#f8fafc;">
              <div style="font-weight:900; color:#0f172a; font-size:12.5px;">🚀 Increased new logos acquired</div>
              <div style="font-size:12px; color:#64748b; margin-top:4px; line-height:1.5;">Growth in net-new customer acquisition.</div>
            </div>

            <div style="border:1px solid #e2e8f0; border-radius:12px; padding:10px 12px; background:#f8fafc;">
              <div style="font-weight:900; color:#0f172a; font-size:12.5px;">📊 Higher lead-to-opportunity conversion</div>
              <div style="font-size:12px; color:#64748b; margin-top:4px; line-height:1.5;">Improved qualification and engagement rates.</div>
            </div>

            <div style="border:1px solid #e2e8f0; border-radius:12px; padding:10px 12px; background:#f8fafc;">
              <div style="font-weight:900; color:#0f172a; font-size:12.5px;">🎯 Improved win rate & faster sales cycle</div>
              <div style="font-size:12px; color:#64748b; margin-top:4px; line-height:1.5;">Reduced time-to-close through better targeting.</div>
            </div>

            <div style="border:1px solid #e2e8f0; border-radius:12px; padding:10px 12px; background:#f8fafc;">
              <div style="font-weight:900; color:#0f172a; font-size:12.5px;">⚡ Higher pipeline velocity</div>
              <div style="font-size:12px; color:#64748b; margin-top:4px; line-height:1.5;">Faster progression and increased new revenue growth.</div>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
</div>
"""
    return html_out

def _format_weights_to_html() -> str:
    """MWC-ready Category Weights with icons + High/Medium/Low Impact pill + circular weight ring"""

    categories = [
        {
            "title": "Technographics",
            "icon": "💻",
            "priority": "High",
            "weight": 25,
            "value": "Maps current technology footprint to solution readiness and expansion paths.",
            "chips": ["Triggers: cloud, security stack", "Best for: solution fit"],
            "rationale": [
                "Complex stacks correlate with higher adoption",
                "Reveals logical adjacency opportunities",
                "Improves recommendation relevance",
            ],
            "breakdown": [
                {"name": "Network", "pct": "35%"},
                {"name": "Cloud", "pct": "25%"},
                {"name": "Collaboration", "pct": "20%"},
                {"name": "Security & IoT", "pct": "15%"},
                {"name": "Other", "pct": "5%"},
            ],
        },
        {
            "title": "Growth Signals",
            "icon": "📈",
            "priority": "High",
            "weight": 20,
            "value": "Identifies account entry points by detecting business changes that increase openness to evaluating new telecom and connectivity vendors.",
            "chips": ["Triggers: New sites, M&A, partnerships", "Best for: “why now?”"],
            "rationale": [
                "Prioritizes accounts with near-term change (expansion / acquisition)",
                "Signals demand for SD-WAN expansion, bandwidth uplift, multi-site rollout",
                "Improves conversion by aligning outreach to “moment of need”",
            ],
            "breakdown": [
                {"name": "Business Expansion", "pct": "30%"},
                {"name": "Acquisition / Merger", "pct": "25%"},
                {"name": "Partnerships", "pct": "20%"},
                {"name": "Hiring Trends", "pct": "10%"},
                {"name": "Risk / Disruption Flags", "pct": "15%"},
            ],
        },
        {
            "title": "Estimated Spend Potential",
            "icon": "💰",
            "priority": "Medium",
            "weight": 15,
            "value": "Focuses sales effort on accounts with meaningful wallet size.",
            "chips": ["Triggers: spend tier, headroom", "Best for: wallet expansion"],
            "rationale": [
                "Defines commercial headroom",
                "Guides AE capacity allocation",
                "Avoids low-value pursuits",
            ],
            "breakdown": [
                {"name": "ICT Spend", "pct": "30%"},
                {"name": "Telco Spend", "pct": "30%"},
                {"name": "Hardware & Software", "pct": "20%"},
                {"name": "IT Services", "pct": "20%"},
            ],
        },
        {
            "title": "Intent Signals",
            "icon": "🎯",
            "priority": "Medium",
            "weight": 15,
            "value": "Captures in-market behavior before CRM opportunity creation.",
            "chips": ["Triggers: search + content signals", "Best for: early pipeline"],
            "rationale": [
                "Flags active research behavior",
                "Improves outreach timing",
            ],
            "breakdown": [
                {"name": "Active Research", "pct": "70%"},
                {"name": "Baseline Interest", "pct": "30%"},
            ],
        },
        {
            "title": "Firmographics",
            "icon": "🏢",
            "priority": "Medium",
            "weight": 15,
            "value": "Baseline segmentation filter, not a near-term trigger.",
            "chips": ["Triggers: ICP match", "Best for: segmentation"],
            "rationale": [
                "Ensures ICP alignment",
                "Supports benchmarking",
                # "Not a “why now” signal",
            ],
            "breakdown": [
                {"name": "Employee Size", "pct": "20%"},
                {"name": "Revenue", "pct": "20%"},
                {"name": "Footprint", "pct": "15%"},
                {"name": "Industry", "pct": "15%"},
                {"name": "Other", "pct": "30%"},
            ],
        },
        {
            "title": "Financial Data",
            "icon": "📦",
            "priority": "Low",
            "weight": 10,
            "value": "Supports risk-aware targeting by filtering for accounts with sufficient budget capacity and financial stability for new vendor adoption.",
            "chips": ["Signals: revenue scale, spend bands", "Best for: qualification & deal sizing"],
            "rationale": [
                "Revenue scale indicates ability to onboard new vendors",
                "Spend bands help qualify deal size and sales motion",
                "Financial stability reduces acquisition risk, but does not signal intent"
            ],
            "breakdown": [
                {"name": "Revenue Growth", "pct": "70%"},
                {"name": "Others", "pct": "30%"},
            ],
        },
    ]

    COLOR = {"High": "#16a34a", "Medium": "#f59e0b", "Low": "#94a3b8"}
    BG = {"High": "#dcfce7", "Medium": "#fef3c7", "Low": "#f1f5f9"}

    html_out = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body{
  font-family: Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  background:#f6f7fb;
  padding:16px;
}
.wrap{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:14px;}
.card{
  background:#fff;border:1px solid #e5e7eb;border-radius:16px;
  box-shadow:0 10px 30px rgba(15,23,42,.08);overflow:hidden;
}
summary{list-style:none;cursor:pointer;padding:18px 18px 14px;display:flex;gap:16px;align-items:flex-start;}
summary::-webkit-details-marker{display:none;}
.hdr-left{flex:1;min-width:0;}
.hdr-top{display:flex;align-items:center;gap:10px;justify-content:space-between;}
.title-row{display:flex;align-items:center;gap:10px;min-width:0;}
.icon{
  width:28px;height:28px;border-radius:10px;background:#f3f4f6;
  display:grid;place-items:center;font-size:16px;flex:0 0 auto;
}
.title{font-weight:900;font-size:14px;color:#0f172a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pill{
  display:inline-flex;align-items:center;gap:8px;
  padding:6px 10px;border-radius:999px;font-weight:900;font-size:11px;
  border:1px solid; white-space:nowrap;
}
.dot{width:8px;height:8px;border-radius:50%;}
.desc{margin-top:8px;font-size:12.5px;color:#64748b;line-height:1.5;}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;}
.chip{
  display:inline-flex;align-items:center;
  padding:6px 10px;border-radius:999px;
  background:#f8fafc;border:1px solid #e2e8f0;
  font-size:11px;font-weight:700;color:#334155;
}
.hdr-right{width:98px;display:flex;justify-content:flex-end;}
.circle{
  width:64px;height:64px;border-radius:50%;
  display:grid;place-items:center;font-weight:900;font-size:13px;color:#0f172a;
  background:conic-gradient(var(--clr) calc(var(--pct)*1%), #e5e7eb 0);
}
.circle span{
  width:48px;height:48px;background:#fff;border-radius:50%;
  display:grid;place-items:center;border:1px solid #e5e7eb;
}
.content{
  padding:14px 18px 18px;border-top:1px solid #f1f5f9;
  display:grid;grid-template-columns:1fr 1fr;gap:16px;
}
.panel{background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:14px;}
.panel h4{font-size:11px;text-transform:uppercase;color:#64748b;margin:0 0 10px;letter-spacing:.4px;}
.panel ul{padding-left:18px;margin:0;font-size:12.5px;line-height:1.6;color:#334155;}
.panel li{margin:0 0 8px;}
.row{
  display:flex;justify-content:space-between;gap:10px;
  font-size:12.5px;padding:10px 12px;border:1px solid #e2e8f0;border-radius:12px;
  background:#fff;margin-bottom:8px;
}
.row strong{color:#0f172a;}
</style>
</head>
<body>
<div class="wrap">
"""

    for c in categories:
        clr = COLOR[c["priority"]]
        bg = BG[c["priority"]]
        icon = c.get("icon", "✨")
        chips = c.get("chips", [])
        chip_html = "".join([f"<span class='chip'>{html.escape(ch)}</span>" for ch in chips])

        html_out += f"""
<details class="card" {"open" if c["title"] == "Technographics" else ""}>
  <summary>
    <div class="hdr-left">
      <div class="hdr-top">
        <div class="title-row">
          <div class="icon">{html.escape(icon)}</div>
          <div class="title">{html.escape(c["title"])}</div>
          <span class="pill" style="background:{bg};border-color:{clr};color:{clr};">
            <span class="dot" style="background:{clr};"></span>
            {c["priority"]} Impact
          </span>
        </div>
      </div>

      <div class="desc">{html.escape(c["value"])}</div>

      <div class="chips">{chip_html}</div>
    </div>

    <div class="hdr-right">
      <div class="circle" style="--pct:{c['weight']}; --clr:{clr};">
        <span>{c['weight']}%</span>
      </div>
    </div>
  </summary>

  <div class="content">
    <div class="panel">
      <h4>What it drives</h4>
      <ul>
"""
        for r in c["rationale"]:
            html_out += f"<li>{html.escape(r)}</li>"
        html_out += """
      </ul>
    </div>

    <div class="panel">
      <h4>Signals used</h4>
"""
        for b in c["breakdown"]:
            html_out += f"""
      <div class="row">
        <span>{html.escape(b['name'])}</span>
        <strong>{b['pct']}</strong>
      </div>
"""
        html_out += """
    </div>
  </div>
</details>
"""

    html_out += """
</div>
</body>
</html>
"""
    return html_out

def _format_prioritization_table_html(df: pd.DataFrame) -> str:
    """Prioritization Table - Self-contained HTML for iframe"""
    if df is None or df.empty:
        return "<!DOCTYPE html><html><body style='padding:20px; color:#64748b; font-family:sans-serif;'>No data available.</body></html>"
    
    DISPLAY_COLS = ["Growth Signals", "Tech Maturity", "Tech Relevancy", 
                    "Est. Potential Spend", "Intent Signals", 
                    "GTM Fit", "Priority Rationale"]
    
    ICON_CHARS = "⭐🟡⚪🟢🔴"
    
   
    def format_cell(content, allow_html=False):
        if not content or str(content).strip() in ["", "nan", "—"]:
            return "<span style='color:#64748b;'>—</span>"

        s = str(content).strip()

        # If this column is allowed to render HTML, return as-is
        if allow_html:
            return s

        ICON_CHARS = "⭐🟡⚪🟢🔴"
        parts = s.split("—", 1)
        if len(parts) == 2:
            score = parts[0].strip().lstrip(ICON_CHARS).strip()
            explain = html.escape(parts[1].strip())
            return (
                f"<div><strong>{html.escape(score)}</strong></div>"
                f"<div style='margin-top:4px; color:#475569; font-size:12px;'>{explain}</div>"
            )

        return f"<strong>{html.escape(s)}</strong>"

    
    html_out = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #f1f5f9;
  padding: 20px;
}
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}
.table-scroll {
  overflow-x: auto;
  overflow-y: auto;
  max-height: 580px;
}
.prio-table {
  width: 100%;
  min-width: 1700px;
  border-collapse: collapse;
  background: white;
}
.prio-table thead th {
  position: sticky;
  top: 0;
  background: #f9fafb;
  padding: 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #edf2f7;
  z-index: 10;
}
.prio-table tbody tr {
  border-bottom: 1px solid #edf2f7;
  border-left: 4px solid transparent;
  transition: all 0.15s;
}
.prio-table tbody tr:nth-child(even) { background-color: #f8fafc; }
.prio-table tbody tr:hover {
  background-color: #f5f3ff !important;
  border-left-color: #7c3aed;
}
.prio-table td {
  padding: 18px 16px;
  vertical-align: top;
  font-size: 12px;
  line-height: 1.55;
  color: #0f172a;
  word-wrap: break-word;
}
.company-name {
  font-weight: 600;
  font-size: 14px;
  color: #0f172a;
  line-height: 1.3;
}
.priority-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 11px;
  border: 1px solid;
  white-space: nowrap;
}
.p-high { background: #dcfce7; color: #15803d; border-color: #86efac; }
.p-medium { background: #fef3c7; color: #d97706; border-color: #fbbf24; }
.p-low { background: #fee2e2; color: #dc2626; border-color: #fca5a5; }
.table-scroll::-webkit-scrollbar { width: 12px; height: 12px; }
.table-scroll::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 10px; }
.table-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; border: 2px solid #f1f5f9; }
.table-scroll::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
</head>
<body>
<div class="table-container">
  <div class="table-scroll">
    <table class="prio-table">
      <thead>
        <tr>
          <th style="width: 70px;">ID</th>
          <th style="width: 200px;">Account Name</th>
          <th style="width: 100px; text-align: center;">Priority</th>
"""
    
    for name in DISPLAY_COLS:
        width = "400px" if name == "Priority Rationale" else "200px"
        html_out += f"          <th style='width: {width};'>{html.escape(name)}</th>\n"
    
    html_out += "        </tr>\n      </thead>\n      <tbody>\n"
    
    for idx, row in df.iterrows():
        pri_raw = str(row.get("Priority", "")).strip()
        pri_text = pri_raw.split()[-1].capitalize() if pri_raw else "Low"
        pill_cls = f"p-{pri_text.lower()}"
        
        acc_id = html.escape(str(row.get("Account ID", "") or "").strip())
        company = html.escape(str(row.get("Company Name", "") or "").strip())
        
        html_out += f"""        <tr>
          <td>{acc_id}</td>
          <td><span class="company-name">{company}</span></td>
          <td style="text-align: center;"><span class="priority-pill {pill_cls}">{pri_text}</span></td>
"""
        for col in DISPLAY_COLS:
            allow_html = (col == "Priority Rationale")

            cell_content = format_cell(row.get(col, ''), allow_html=allow_html)

            if col == "Priority Rationale":
                cell_content = f"<strong>{cell_content}</strong>"

            html_out += f"          <td>{cell_content}</td>\n"

        
        html_out += "        </tr>\n"
    
    html_out += """      </tbody>
    </table>
  </div>
</div>
</body>
</html>
"""
    return html_out

def _format_product_catalog_html() -> str:
    """Format high-density, collapsible product catalog with horizontal metadata"""
    
    # 1. Group products by category (L1)
    catalog_by_cat = {}
    for p in PRODUCT_CATALOG:
        cat = p.get("category", "Uncategorized")
        if cat not in catalog_by_cat:
            catalog_by_cat[cat] = []
        catalog_by_cat[cat].append(p)
    
    styles = """
    <style>
        .cat-container { 
        font-family: 'Inter',-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
        padding: 0px; background: #f8fafc; 
        }

        .shelf { margin-bottom: 8px; }
        
        /* Collapsible Shelf */
        .shelf { 
            margin-bottom: 8px; border: 1px solid #e2e8f0; 
            border-radius: 8px; background: white; overflow: hidden; 
        }
        .shelf-summary { 
            list-style: none; padding: 8px 16px; background: #f8fafc; 
            cursor: pointer; display: flex; justify-content: space-between; 
            align-items: center; border-bottom: 1px solid transparent;
        }
        .shelf[open] .shelf-summary { border-bottom: 1px solid #e2e8f0; }
        .shelf-summary::-webkit-details-marker { display: none; }
        
        .shelf-title { 
            font-size: 11px; font-weight: 800; color: #6b00b8; 
            text-transform: uppercase; letter-spacing: 0.05em; 
            display: flex; align-items: center; gap: 8px;
        }
        
        /* Product Grid */
        .prod-grid { 
            display: grid; grid-template-columns: repeat(4, 1fr); 
            gap: 10px; padding: 12px; background: #fff; 
        }
        
        /* Compact Card Design */
        .prod-card { 
            border: 1px solid #f1f5f9; border-radius: 6px; padding: 10px; 
            display: flex; flex-direction: column; background: #fff; 
            min-height: 140px; transition: border-color 0.2s;
            overflow: hidden; /* Prevent wide content from breaking grid */
        }
        .prod-card:hover { border-color: #6b00b8; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        
        .prod-name { font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 3px; }
        
        .prod-desc { 
            font-size: 10px; color: #64748b; line-height: 1.3; 
            margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; 
            -webkit-box-orient: vertical; overflow: hidden; height: 26px;
        }
        .card-link-row{
        margin-top: 6px;
        }
        .p-link{
        color:#0d00ff;
        font-weight:700;
        text-decoration: none;
        }
        .p-link:hover{
        text-decoration: underline;
        }

        
        /* Metadata Horizontal Layout */
        .meta-stack { display: flex; flex-direction: column; gap: 4px; margin-bottom: 8px; }
        .meta-item { font-size: 9px; display: flex; align-items: flex-start; }
        .meta-label { 
            font-weight: 700; color: #94a3b8; text-transform: uppercase; 
            width: 50px; flex-shrink: 0; font-size: 8px; margin-top: 1px;
        }
        .meta-val { 
            color: #475569; 
            text-transform: capitalize; 
            line-height: 1.2; 
            display: inline-block; /* Allow wrapping for long industry lists */
        }
        
        /* Footer row */
        .card-ft { 
            display: flex; justify-content: space-between; align-items: center; 
            margin-top: auto; padding-top: 6px; border-top: 1px solid #f8fafc; 
        }
        .tag-wrap { display: flex; gap: 4px; flex-wrap: wrap; }
        .p-tag { 
            font-size: 8px; background: #f5f3ff; color: #6b00b8; 
            padding: 1px 5px; border-radius: 3px; font-weight: 700; border: 1px solid #ddd6fe;
        }
        .p-link { font-size: 9px; color: #0d00ff; text-decoration: none; font-weight: 700; }
        
        .empty-box { 
            display: flex; align-items: center; justify-content: center; 
            border: 1px dashed #e2e8f0; border-radius: 6px; color: #cbd5e1; 
        }
    </style>
    """

    html_out = f"{styles}<div class='cat-container'>"

    for cat_name, products in catalog_by_cat.items():
        icon = CATEGORY_ICONS.get(cat_name, "📦")
        # Keep first category open by default
        is_open = "open" if cat_name == list(catalog_by_cat.keys())[0] else ""
        
        html_out += f"""
        <details class="shelf" {is_open}>
            <summary class="shelf-summary">
                <div class="shelf-title">{icon} {html.escape(cat_name)}</div>
                <span style="font-size: 10px; color: #94a3b8;">{len(products)} Products</span>
            </summary>
            <div class="prod-grid">
        """

        for i in range(len(products)):
            if i < len(products):
                p = products[i]
                chips = "".join([
                    f"<span class='p-tag'>{label}</span>"
                    # for flag, label in CAP_FLAG_MAP.items() if p["flags"].get(flag)
                    for flag, label in CAP_FLAG_MAP.items() if p.get(flag)
                ])
                
                # Use .title() for proper casing of industries/segments
                html_out += f"""
                <div class="prod-card">
                    <div class="prod-name">{html.escape(p['sub_category'])}</div>
                    <div class="prod-desc">{html.escape(p.get('desc', ''))}</div>
                    
                    <div class="meta-stack">
                        <div class="meta-item">
                            <span class="meta-label">Segment:</span>
                            <span class="meta-val">{html.escape(p['segments'].title())}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Industry:</span>
                            <span class="meta-val">{html.escape(p['industries'].title())}</span>
                        </div>
                    </div>

                    <div class="card-ft">
                        <div class="tag-wrap">{chips}</div>
                        </div>
                        <div class="card-link-row">
                        <a href="{p['url']}" target="_blank" class="p-link">Details →</a>
                    </div>

                </div>
                """

        
        html_out += "</div></details>"

    html_out += "</div>"
    return html_out

def _format_recommendations_table_html() -> str:
    """Recommendations Table - Complete HTML for iframe with proper HTML rendering"""
    try:
        reco_df = pd.read_excel(RECOMMENDATIONS_PATH, sheet_name="Recommendations", header=3)
    except Exception as e:
        return f"<div style='padding:20px; color:#dc2626;'>Error: {e}</div>"
    
    if reco_df.empty:
        return "<div style='padding:20px; color:#64748b;'>No data available.</div>"
    
    account_ids = reco_df["Account ID"].unique()
    
    html_out = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f1f5f9;
    }
    .table-card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.05);
      overflow: hidden;
      border: 1px solid #e2e8f0;
    }
    .table-wrap {
      overflow-x: auto;
      overflow-y: auto;
      max-height: 580px;
    }
    .reco-table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      background: white;
      min-width: 1400px;
    }
    .reco-table thead th {
      position: sticky;
      top: 0;
      background: #f9fafb;
      padding: 16px;
      text-align: left;
      font-size: 11px;
      font-weight: 800;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid #edf2f7;
      z-index: 10;
    }
    .reco-table tbody tr {
      border-bottom: 1px solid #edf2f7;
      border-left: 4px solid transparent;
    }
    .reco-table tbody tr:nth-child(even) {
      background-color: #f8fafc;
    }
    .reco-table tbody tr:hover {
      background-color: #f5f3ff !important;
      border-left: 4px solid #7c3aed;
    }
    .reco-table td {
      padding: 20px 16px;
      vertical-align: top;
      color: #0f172a;
      font-size: 12px;
      line-height: 1.5;
    }
    .company-name {
      font-weight: 600;
      color: #0f172a;
      font-size: 14px;
      display: block;
      margin-bottom: 6px;
      line-height: 1.3;
    }
    .priority-pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 6px 12px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 11px;
      border: 1px solid;
      white-space: nowrap;
    }
    .p-high { background: #dcfce7; color: #15803d; border-color: #86efac; }
    .p-medium { background: #fef3c7; color: #d97706; border-color: #fbbf24; }
    .p-low { background: #fee2e2; color: #dc2626; border-color: #fca5a5; }
    .muted {
      font-size: 12px;
      color: #64748b;
      line-height: 1.6;
    }
    .trigger-details {
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      background: white;
      margin-top: 8px;
    }
    .trigger-summary {
      padding: 8px 12px;
      font-size: 12px;
      font-weight: 600;
      color: #475569;
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
    }
    .trigger-summary::-webkit-details-marker { display: none; }
    .trigger-summary::before {
      content: '→';
      margin-right: 8px;
      color: #a855f7;
      transition: 0.2s;
    }
    .trigger-details[open] .trigger-summary::before {
      transform: rotate(90deg);
    }
    .trigger-details[open] .trigger-summary {
      border-bottom: 1px solid #f1f5f9;
    }
    .trigger-content {
      padding: 12px;
      font-size: 11px;
      color: #334155;
      line-height: 1.6;
      background: #fafafa;
      border-radius: 0 0 8px 8px;
    }
    /* Render HTML lists properly */
    .trigger-content ul {
      margin: 8px 0;
      padding-left: 20px;
    }
    .trigger-content li {
      margin-bottom: 6px;
      line-height: 1.5;
    }
    .table-wrap::-webkit-scrollbar {
      width: 12px;
      height: 12px;
    }
    .table-wrap::-webkit-scrollbar-track {
      background: #f1f5f9;
      border-radius: 10px;
    }
    .table-wrap::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 10px;
      border: 2px solid #f1f5f9;
    }
    .table-wrap::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }
    </style>
    </head>
    <body>
    <div class="table-card">
      <div class="table-wrap">
        <table class="reco-table">
          <thead>
            <tr>
              <th style="width: 70px;">ID</th>
              <th style="width: 180px;">Account</th>
              <th style="width: 90px; text-align: center;">Priority</th>
              <th style="min-width: 280px;">Recommendation 1</th>
              <th style="min-width: 280px;">Recommendation 2</th>
              <th style="min-width: 280px;">Recommendation 3</th>
            </tr>
          </thead>
          <tbody>
    """
    
    for acc_id in account_ids:
        rows = reco_df[reco_df["Account ID"] == acc_id].reset_index(drop=True)
        main = rows.iloc[0]
        
        pri_raw = str(main.get("Priority", "")).strip()
        pri_text = pri_raw.split()[-1].capitalize() if pri_raw else "Low"
        pill_cls = f"p-{pri_text.lower()}"
        
        html_out += f"""
        <tr>
          <td>#{acc_id}</td>
          <td>
            <span class="company-name">{html.escape(str(main.get('Account Name', '')))}</span>
            <div class="muted">
              📍 {html.escape(str(main.get('City / State', '')))}<br>
              👥 {html.escape(str(main.get('FTE Size', '')))}<br>
              🏢 {html.escape(str(main.get('Industry', '')))}
            </div>
          </td>
          <td style="text-align: center;">
            <span class="priority-pill {pill_cls}">{pri_text}</span>
          </td>
        """
        
        for i in range(3):
            if i < len(rows):
                r = rows.iloc[i]
                # DON'T escape the rationale - it contains HTML that should render
                rationale_raw = str(r.get('Insight & Rationale', ''))
                
                html_out += f"""
                <td>
                  <div style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px;">
                    {html.escape(str(r.get('Category', '')))}
                  </div>
                  <div style="font-weight: 700; color: #6b21a8; font-size: 14px; margin-bottom: 6px;">
                    {html.escape(str(r.get('Product', '')))}
                  </div>
                  <div style="font-size: 11px; background: #f3e8ff; color: #6b21a8; padding: 3px 8px; border-radius: 50px; display: inline-block; margin-bottom: 8px; font-weight: 700;">
                    {html.escape(str(r.get('Fit Score', '')))} Fit
                  </div>
                  <details class="trigger-details">
                    <summary class="trigger-summary">Why this reco?</summary>
                    <div class="trigger-content">{rationale_raw}</div>
                  </details>
                </td>
                """
            else:
                html_out += "<td style='color: #cbd5e1; text-align: center;'>—</td>"
        
        html_out += "</tr>"
    
    html_out += """
          </tbody>
        </table>
      </div>
    </div>
    </body>
    </html>
    """
    return html_out





# --------------------------------------------------
# STATE INITIALIZATION
# --------------------------------------------------
st.session_state.setdefault("run_process", False)
st.session_state.setdefault("stop_process", False)
st.session_state.setdefault("step_done", {})
st.session_state.setdefault("log_html", {})
st.session_state.setdefault("current_step", 0)
if "task_running" not in st.session_state:
    st.session_state.task_running = {}

# -------------------------------------------------------------------
# Main page
# -------------------------------------------------------------------
def lead_scoring_page(df=None):
    # --- CSS ---
    st.markdown(_get_global_css(), unsafe_allow_html=True)

    mock_data = {

    "Account ID": ['ACC001','ACC002','ACC003','ACC004','ACC005','ACC006','ACC007','ACC008','ACC009','ACC010'],

    "Company Name": [
        "AvePoint",
        "Moderna",
        "Suncoast Credit Union",
        "SolomonEdwards",
        "BAYSTAR",
        "CookUnity",
        "BCI Brands",
        "Bisig Impact Group",
        "Flynn Construction Inc.",
        "Vuteq USA, Inc.",
    ],

    "Priority": [
        "🟢 High",
        "🟡 Medium",
        "🟢 High",
        "🟢 High",
        "🟢 High",
        "🟡 Medium",
        "🟢 High",
        "⚪ Low",
        "⚪ Low",
        "⚪ Low",
    ],

    "Growth Signals": [
        "🟢 High — Active acquisition strategy, global expansion, and sustained SaaS growth momentum",
        "🟡 Medium — $1.5B funding and expansion; recent layoffs introduce execution risk",
        "🟢 High — Expansion and partnership activity with strong enterprise positioning",
        "🟢 High — Multiple acquisitions and expansion within last 6M",
        "🟢 High — Hiring + partnerships + expansion; industrial scale opportunity",
        "🟡 Medium — Funding and expansion; financial risk tempers confidence",
        "🟢 High — Acquisition + partnership; retail digital transformation momentum",
        "⚪ Low — No growth signals detected",
        "⚪ Low — No growth signals detected",
        "⚪ Low — No growth signals detected",
    ],

    "Tech Maturity": [
        "⭐ Very High — Advanced multi-cloud, DevOps, and enterprise security ecosystem",
        "⭐ Medium — Core SaaS/CRM with limited cloud depth",
        "⭐ High — Enterprise-grade cloud, security & analytics",
        "⭐ High — Mature ERP, analytics and security footprint",
        "⭐ HIgh — Strong ERP & core enterprise systems",
        "⭐ High — Modern cloud, AI/analytics and IoT capabilities",
        "⭐ Medium — Cloud + e-commerce + retail systems",
        "⭐ Medium — Basic cloud & marketing stack",
        "⭐ Medium — Cloud + project management focus",
        "⭐ Medium — Cloud + security + analytics present",
    ],

    "Tech Relevancy": [
        "⭐ High — Security & cloud are direct GTM adjacencies",
        "🟡 Medium — Infrastructure opportunity inferred from scale; limited active telecom signals",
        "⭐ High — Strong SASE + hybrid cloud alignment",
        "🟡 Medium — ERP/finance focus; selective cloud/security opportunity",
        "⭐ High — Wireless & industrial connectivity direct fit",
        "🟡 Medium — Cloud and IoT selective adjacency",
        "⭐ High — Cloud, fiber & wireless strong retail consolidation play",
        "🟡 Medium — Entry-level cloud & connectivity opportunity",
        "🟡 Medium — Project-driven connectivity opportunity",
        "🟡 Medium — Cloud & wireless baseline modernization opportunity",
    ],

    "Est. Potential Spend": [
        "🟢 Very High — Enterprise-scale technology and connectivity investment capacity",
        "🟢 High — Strategic infrastructure investments likely",
        "🟢 High — Enterprise-level engagement expected",
        "🟢 High — Significant ICT and services potential",
        "🟢 Very High — Enterprise-scale strategic spend",
        "🟡 Medium — Mid-market expansion spend",
        "🟡 Medium — Retail consolidation opportunity",
        "⚪ Low — Minimal confirmed spend",
        "⚪ Low — Low project-driven spend only",
        "⚪ Low — Limited spend due to rural constraints",
    ],

    "Intent Signals": [
        "⭐ Very High — Explicit multi-domain research across security, cloud, and infrastructure topics",
        "⚪ No intent — No meaningful intent activity; capital-driven but not in-market",
        "⭐ High — Cloud + security intent active",
        "⚪ Low — Light cloud/security interest only",
        "⭐ High — Strong wireless/connectivity intent",
        "⚪ Low — Weak IoT interest with minimal breadth",
        "⭐ High — Strong cloud intent with multiple connectivity themes",
        "⚪ Low — Weak cloud intent and minimal security interest",
        "⚪ Low — Very light cloud-only activity; minimal urgency",
        "⚪ Low — Cloud interest present with marginal wireless signals",
    ],

    "GTM Fit": [
        "⭐ Very High — Multi-site SaaS enterprise with modernization-driven buying posture",
        "🟡 Medium — Large biotech scale but not actively in-market",
        "⭐ High — Financial enterprise buyer with strong security posture",
        "⭐ High — Professional services multi-site expansion fit",
        "⭐ High — Industrial enterprise with wireless-heavy use case",
        "🟡 Medium — Growth account with risk-adjusted selectivity",
        "⭐ High — Retail transformation & consolidation opportunity",
        "⚪ Low — Small agency; nurture only",
        "⚪ Low — Small construction; project-triggered engagement",
        "⚪ Low — Rural manufacturing; opportunistic outreach only",
    ],

    "Priority Rationale": [
        "Acquisition-driven growth, explicit modernization signals, and enterprise scale position this account for near-term strategic engagement.",
        "Capital-rich biotech with major funding, but layoffs and no active intent reduce urgency.",
        "High intent + enterprise profile → immediate upsell/renewal urgency.",
        "Multiple recent M&A and expansion → strong renewal + expansion opportunity.",
        "Enterprise industrial account with strategic ICT needs → pursue wireless + infrastructure plays.",
        "Funding and growth present, but financial risk suggests selective engagement.",
        "Multi-brand retail consolidation opportunity → focus on cloud & network modernisation.",
        "Small agency with low spend — nurture only on inbound interest.",
        "Small construction firm — engage only for project-triggered connectivity needs.",
        "Rural manufacturer with limited spend — opportunistic outreach only.",
    ]
    }

    st.session_state["lead_prioritization_df"] = pd.DataFrame(mock_data)
    df_for_status = st.session_state["lead_prioritization_df"].copy()

    # -------------------- header --------------------
    lead_list_name = st.session_state.get(
        "lead_list_name",
        "November Lead List — Expansion Accounts",
    )

    st.markdown(
        """<h3 class='main-title'><span style='font-size: 1.1em;'>🎯</span>
        Lead Scoring &amp; Prioritization Console</h3>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p class='panel-desc-left'>
        This console converts Customer 360° signals into explainable lead scores and
        priority segments, aligned to your GTM objective.</p>""",
        unsafe_allow_html=True,
    )

    # -------------------- business context text area --------------------
    default_context = (
        "We aim to strengthen our mid-market presence across the U.S. for Dedicated Fiber, Internet, "
        "Communication, and Security offerings. While coverage is strong, identifying accounts with the highest "
        "growth potential or urgent connectivity needs remains a challenge.\n\n"
        "As a result, sales teams lack actionable insights to prioritize and position the right products.\n\n"
        "Our goal is to enhance targeting, segmentation, and sales intelligence to deepen market penetration, "
        "accelerate revenue growth, and align execution with rising digital and connectivity demands."
    )
    if "lead_ctx_text" not in st.session_state:
        st.session_state.lead_ctx_text = default_context

    # session defaults
    if "lead_placeholders" not in st.session_state: st.session_state.lead_placeholders = {}
    if "lead_cached" not in st.session_state: st.session_state.lead_cached = {}
    if "lead_run_id" not in st.session_state: st.session_state.lead_run_id = 0
    if "lead_stop_requested" not in st.session_state: st.session_state.lead_stop_requested = False

    cols = st.columns([1, 1, 8])
    with cols[0]:
        run_clicked = st.button("Run Process", key="lead_run", type="primary", use_container_width=True)
    with cols[1]:
        stop_clicked = st.button("Stop Process", key="lead_stop", type="secondary", use_container_width=True)

    if stop_clicked:
        st.session_state.lead_stop_requested = True
        run_clicked = False

    # global STEP 1 log placeholder
    step1_log_ph = st.empty()
    if "lead_step1_log_html" in st.session_state:
        step1_log_ph.markdown(st.session_state["lead_step1_log_html"], unsafe_allow_html=True)

    # -------------------- task scaffolding --------------------
    st.markdown("<hr>", unsafe_allow_html=True)
    # Expander
    EXPANDER_LABELS = {
        "load_data":           "📊 View Customer 360° Data",
        "business_context":    "🎯 View Business Context Analysis",
        "category_weights":    "⚖️ View Category & Signal Weights",
        "prioritization_table":"🏆 View Lead Prioritization Results",
        "product_catalog":     "📦 View Product Catalogue",
        "recommender_agent":   "💡 View AI Recommendations",
    }
    task_container = st.container()
    with task_container:
        for t in ALL_TASKS:
            print(t)
            key = t["key"]
            st.markdown(f"<div class='task-card' id='lead-task-{key}'>", unsafe_allow_html=True)
            header_ph = st.empty()
            progress_ph = st.empty()

            # default header: pending
            header_ph.markdown(
                f"<div class='task-card-header'><div class='task-name'>{html.escape(t['name'])} "
                f"{status_dot('#999999', 12)}<span style='color:#888;'>— Pending</span></div></div>",
                unsafe_allow_html=True,
            )

            # agent log placeholder
            log_ph = st.empty()
            if f"lead_log_html_{key}" in st.session_state:
                log_ph.markdown(st.session_state[f"lead_log_html_{key}"], unsafe_allow_html=True)
            else:
                log_ph.markdown(
                    "<div class='agent-log-box agent-log-empty'>Background agent pipeline will appear here once the run starts.</div>",
                    unsafe_allow_html=True,
                )


            # expander with details
            exp = st.expander(EXPANDER_LABELS.get(key, "Expand AI Enrichment Details"), expanded=False)

            with exp:
                results_ph = st.empty()
                cached_html = st.session_state.lead_cached.get(key)
                if cached_html:
                    with results_ph.container():
                        # The summary HTML is cached first
                        if key == "prioritization_table" and "lead_prioritization_df" in st.session_state:
                            # Split the cached HTML back into header and table/download part
                            header_html = _format_prioritization_table_html()
                            st.markdown(header_html, unsafe_allow_html=True)
                            
                            display_df = st.session_state["lead_prioritization_df"]
                            # REPLACEMENT A: Use custom HTML table instead of st.dataframe
                            st.markdown(_format_prioritization_table_html(display_df), unsafe_allow_html=True) 
                            
                            csv = display_df.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                "Download Prioritization CSV",
                                data=csv,
                                file_name=f"prioritization_cached_{st.session_state.lead_run_id}.csv",
                                mime="text/csv",
                                key=f"lead_download_cached_{key}_{st.session_state.lead_run_id}",
                            )
                        else: # For Business Context and Weights
                            st.markdown(cached_html, unsafe_allow_html=True)
                else:
                    results_ph.markdown("<div class='output-box'>(no results yet)</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.session_state.lead_placeholders[key] = {
                "header_ph": header_ph,
                "log_ph": log_ph,
                "results_ph": results_ph,
                "progress_ph": progress_ph,
            }

    overall_progress_ph = st.empty()


    # --------------------------------------------------
    # MAIN EXECUTION LOGIC
    # --------------------------------------------------

    if run_clicked:
        st.session_state.lead_stop_requested = False
        st.session_state.lead_run_id += 1
        run_id = st.session_state.lead_run_id

        # reset cache
        st.session_state.lead_cached = {}
        
        # Run ALL tasks (steps 1-6)
        tasks_to_run = ALL_TASKS
        total_tasks = len(tasks_to_run)
        
        # Update overall progress
        overall_progress_ph.progress(0, text="Overall Pipeline Progress")
        
        # Execute each task
        for idx, task in enumerate(tasks_to_run):
            if st.session_state.get("stop_process"):
                st.warning("Pipeline stopped by user.")
                st.session_state.task_running[task["key"]] = False
                break
            
            key = task["key"]
            step_num = task["step_num"]
            done_key = f"step_{step_num}_done"
            st.session_state.current_step = step_num
            st.session_state.task_running[key] = True


            # Skip if already done
            if st.session_state.step_done.get(done_key, False):
                continue
            
            # Check if previous step is done
            if step_num > 1:
                prev_done_key = f"step_{step_num - 1}_done"
                if not st.session_state.step_done.get(prev_done_key, False):
                    continue
            
            # Get placeholders
            # ph = st.session_state.placeholders.get(key, {})
            ph = st.session_state.lead_placeholders.get(key, {})
            header_ph = ph.get("header_ph")
            log_ph = ph.get("log_ph")
            results_ph = ph.get("results_ph")
            progress_ph = ph.get("progress_ph")
            
            # Update header to "Running"
            if header_ph is not None:
                step_prefix = f"<span class='step-label'>STEP {step_num} — </span>"
                # Update header to "Running" (yellow)
                header_ph.markdown(
                    f"<div class='task-card-header'><div class='task-name'>{step_prefix}{html.escape(task['name'])} "
                    f"{status_dot('#f0c040', 12)}<span style='color:#f0c040;'>— Running</span></div></div>",
                    unsafe_allow_html=True,
                )


            # Animate logs
            agent_steps = STEP_LOGS.get(key, [])

            # STEP header line
            ts0 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_html = (
                f"<div class='agent-log-line title'>"
                f"{ts0} — STEP {step_num} — {html.escape(task['name'])}"
                f"</div>"
            )

            total_lines = len(agent_steps)

            for s_idx, step_text in enumerate(agent_steps, start=1):
                if st.session_state.get("stop_process"):
                    break

                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_html += (
                    f"<div class='agent-log-line info'>"
                    f"<span class='source-tag'>{ts}</span> {step_text}"
                    f"</div>"
                )

                box_html = f"<div class='agent-log-box'>{log_html}</div>"

                if log_ph is not None:
                    log_ph.markdown(box_html, unsafe_allow_html=True)

                st.session_state.log_html[f"log_{key}"] = box_html

                # progress update stays same...
                pct = int((s_idx / max(total_lines, 1)) * 100)
                if progress_ph is not None:
                    progress_ph.markdown(
                        f"<div style='width:100%'>"
                        f"<div style='margin-bottom:6px; font-weight:600; font-size: 13px; color: #333;'>"
                        f"Executing... {pct}%"
                        f"</div>"
                        f"<progress value='{pct}' max='100' class='progress-inline'></progress>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                time.sleep(SIMULATE_TIME_PER_STEP)


            
            if st.session_state.get("stop_process"):
                if progress_ph is not None:
                    progress_ph.markdown(
                        "<div style='padding:8px;'><strong>Task interrupted by user.</strong></div>",
                        unsafe_allow_html=True,
                    )
                if header_ph is not None:
                    step_prefix = f"<span class='step-label'>STEP {step_num} — </span>"
                    header_ph.markdown(
                        f"<div class='task-card-header'><div class='task-name'>{step_prefix}{html.escape(task['name'])} "
                        f"{status_dot('#999999', 12)}<span style='color:#999;'>— Interrupted</span></div></div>",
                        unsafe_allow_html=True,
                    )
                break
            
            # Generate outputs based on task key
            if key == "load_data":
                out_html = _format_account_summary_table_html()
                
            elif key == "business_context":
                # out_html = _business_context_html_from_text(st.session_state.business_context_text)
                out_html = _business_context_html_from_text(st.session_state.lead_ctx_text)
                
            elif key == "category_weights":
                out_html = _format_weights_to_html()
                
            elif key == "prioritization_table":
                header_html = """
    <div class="output-box">
        <div class="kv">
            <span class="label">Lead Prioritization — Explanatory Data</span>
            <div class="small-muted">
                The weighted scoring framework has generated final priority segments and scores.
            </div>
        </div>
    </div>
    """
                table_html = _format_prioritization_table_html(st.session_state["lead_prioritization_df"])
                out_html = header_html + table_html
                
            elif key == "product_catalog":
                out_html = _format_product_catalog_html()
                
            elif key == "recommender_agent":
                out_html = _format_recommendations_table_html()
                
            else:
                out_html = "<div class='output-box'>(no output)</div>"
            
            # Cache output
            st.session_state[f"output_{key}"] = out_html
            
            # Mark as done
            st.session_state.step_done[done_key] = True
            st.session_state.task_running[key] = False
            st.session_state.current_step = step_num + 1
            # Update header to "Done"
            if header_ph is not None:
                step_prefix = f"<span class='step-label'>STEP {step_num} — </span>"
                header_ph.markdown(
                    f"<div class='task-card-header'><div class='task-name'>{step_prefix}{html.escape(task['name'])} "
                    f"{status_dot('#2db24a', 12)}<span style='color:#2db24a;'>— Complete</span></div></div>",
                    unsafe_allow_html=True,
                )
            
            # Clear progress bar
            if progress_ph is not None:
                progress_ph.empty()
            
            # Render results in expander
            if results_ph is not None:
                with results_ph.container():
                    if key == "load_data":
                        components.html(_format_account_summary_table_html(), height=700, scrolling=True)
                        
                    elif key == "business_context":
                        components.html(out_html, height=600, scrolling=True)
                        
                    elif key == "category_weights":
                        # st.markdown(out_html, unsafe_allow_html=True)
                        components.html(out_html, height=900, scrolling=True)
                        
                    elif key == "prioritization_table":
                        components.html(_format_prioritization_table_html(st.session_state["lead_prioritization_df"]), height=700, scrolling=True)

                        
                        csv = st.session_state["lead_prioritization_df"].to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "Download Prioritization CSV",
                            data=csv,
                            file_name="prioritization_results.csv",
                            mime="text/csv",
                            key=f"download_{key}_exec",
                        )
                        
                    elif key == "product_catalog":
                        out_html = _format_product_catalog_html()
                        components.html(out_html, height=800, scrolling=True)
                        
                    elif key == "recommender_agent":
                        st.markdown("""<div style="
                                margin-bottom:12px;
                                padding:10px 14px;
                                border-radius:10px;
                                background:#eef2ff;
                                border:1px solid #c7d2fe;
                                font-size:12.5px;
                                color:#1e3a8a;
                                font-weight:600;
                            ">
                                🔎 <strong>Recommendation Confidence:</strong>
                                All recommended products meet a minimum <strong>LLM confidence threshold</strong> to ensure relevance and actionability.
                            </div>""", unsafe_allow_html=True)
                        components.html(_format_recommendations_table_html(), height=700, scrolling=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        with open(RECOMMENDATIONS_PATH, "rb") as f:
                            rec_bytes = f.read()
                        st.download_button(
                            label="⬇️  Download Recommendations (Excel)",
                            data=rec_bytes,
                            file_name="recommendations.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"dl_recommendations_exec",
                        )
            
            # Update overall progress
            progress_value = int(((idx + 1) / total_tasks) * 100)
            overall_progress_ph.progress(progress_value, text="Overall Pipeline Progress")
        
        # Clear overall progress when done
        overall_progress_ph.empty()
        
        # Show success message if not stopped
        if not st.session_state.get("stop_process"):
            st.success("✅ Lead prioritization and product recommendation pipeline completed successfully!")

