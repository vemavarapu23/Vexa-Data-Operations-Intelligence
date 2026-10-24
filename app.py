
import io
import os
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

from database import DB_PATH, initialize_database, save_audit_action
from ai_assistant import analyze_finding


# ============================================================
# VEXA — DATA OPERATIONS INTELLIGENCE
# Local SQLite + Public Demo + Groq AI + Readable UI
# ============================================================

st.set_page_config(
    page_title="Vexa | Data Operations Intelligence",
    page_icon="✅",
    layout="wide",
)


# ============================================================
# APPLICATION MODE
# ============================================================

def get_setting(name, default=""):
    value = os.getenv(name)
    if value is not None:
        return value
    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, KeyError):
        return default


PUBLIC_DEMO = (
    str(get_setting("VEXA_PUBLIC_DEMO", "false"))
    .strip()
    .lower() == "true"
)

if not PUBLIC_DEMO:
    initialize_database()


# ============================================================
# VEXA PINK AND WHITE THEME — CONTRAST FIXED
# ============================================================

st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: #fbf9fb !important;
    color: #24212b !important;
}

.block-container {
    max-width: 1320px;
    padding-top: 1.8rem;
}

/* Main text */
h1, h2, h3, h4 {
    color: #26212c !important;
    letter-spacing: -0.5px;
}

[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] .stMarkdown {
    color: #24212b;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #f0e0e9;
}

[data-testid="stSidebar"] p {
    color: #625b67;
}

/* Branding */
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 22px;
}

.brandmark {
    width: 47px;
    height: 47px;
    background-color: #bc4074;
    color: #ffffff;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    font-weight: 800;
}

.brandname {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #25212b;
}

.brandsub {
    font-size: 10px;
    letter-spacing: 1px;
    color: #777777;
    font-weight: 700;
    margin-top: 5px;
}

.overline {
    font-size: 12px;
    color: #bc4074;
    font-weight: 800;
    letter-spacing: 1.3px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #efdfe8;
    border-top: 3px solid #bc4074;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #625b67 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #24212b !important;
    font-weight: 800;
}

/* General buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* Primary pink buttons */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background-color: #bc4074 !important;
    border-color: #bc4074 !important;
    color: #ffffff !important;
}

.stButton > button[kind="primary"] *,
.stButton > button[data-testid="stBaseButton-primary"] * {
    color: #ffffff !important;
}

/* Secondary and download buttons */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"],
.stDownloadButton > button {
    background-color: #ffffff !important;
    border: 1px solid #d8bac9 !important;
    color: #24212b !important;
}

.stButton > button[kind="secondary"] *,
.stButton > button[data-testid="stBaseButton-secondary"] *,
.stDownloadButton > button * {
    color: #24212b !important;
}

.stDownloadButton > button:hover,
.stButton > button[kind="secondary"]:hover {
    background-color: #fff0f6 !important;
    border-color: #bc4074 !important;
}

/* Text boxes */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background-color: #ffffff !important;
    color: #24212b !important;
    -webkit-text-fill-color: #24212b !important;
    caret-color: #bc4074 !important;
}

/* Text box containers */
[data-baseweb="input"],
[data-baseweb="textarea"] {
    background-color: #ffffff !important;
    color: #24212b !important;
    border-color: #d8bac9 !important;
}

/* Placeholder text */
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: #817783 !important;
    -webkit-text-fill-color: #817783 !important;
    opacity: 1 !important;
}

/* Form labels */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stCheckbox"] label,
[data-testid="stRadio"] label {
    color: #24212b !important;
}

/* Dropdowns */
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #24212b !important;
    border-color: #d8bac9 !important;
}

[data-baseweb="select"] input,
[data-baseweb="select"] span {
    color: #24212b !important;
    -webkit-text-fill-color: #24212b !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #ffffff !important;
    color: #24212b !important;
}

[role="option"] {
    color: #24212b !important;
}

[role="option"]:hover {
    background-color: #fff0f6 !important;
}

/* Sidebar privacy text */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #625b67 !important;
    opacity: 1 !important;
}

/* General captions */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: #625b67 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
    color: #24212b !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border: 1px dashed #e3aac5;
    border-radius: 12px;
    padding: 10px;
}

[data-testid="stFileUploader"] button,
[data-testid="stFileUploader"] button * {
    color: #24212b !important;
}

/* Progress */
[data-testid="stProgress"] [role="progressbar"] {
    accent-color: #bc4074;
}

/* Table text readability */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Expander */
[data-testid="stExpander"] {
    background-color: #ffffff;
    border-radius: 10px;
}

/* Sidebar navigation buttons */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background-color: #ffffff !important;
    color: #24212b !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background-color: #bc4074 !important;
    color: #ffffff !important;
}

/* Focus outlines */
input:focus,
textarea:focus,
button:focus-visible {
    outline-color: #bc4074 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

S = st.session_state

if "initialized" not in S:
    S.initialized = True
    S.a = None
    S.b = None
    S.original_a = None
    S.original_b = None
    S.row_ids_a = []
    S.row_ids_b = []
    S.na = "Report A"
    S.nb = "Report B"
    S.ka = None
    S.kb = None
    S.company = "My Workspace"
    S.findings = pd.DataFrame()
    S.reviews = {}
    S.history = []
    S.deletions = 0
    S.load_number = 0
    S.audit_counter = 0
    S.page = "Dashboard"
    S.ai_response = None
    S.ai_context = None


# ============================================================
# BASIC HELPERS
# ============================================================

def safe_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize(df):
    result = df.copy()
    result.columns = [
        str(column).strip()
        for column in result.columns
    ]

    if result.columns.duplicated().any():
        raise ValueError("Duplicate column names found.")

    return (
        result.fillna("")
        .astype(str)
        .apply(lambda column: column.str.strip())
        .reset_index(drop=True)
    )


def read_upload(file):
    if len(file.getvalue()) > 8 * 1024 * 1024:
        raise ValueError("Maximum file size is 8 MB.")

    stream = io.BytesIO(file.getvalue())

    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(
            stream,
            dtype=str,
            keep_default_na=False,
        )
    elif file.name.lower().endswith(".xlsx"):
        df = pd.read_excel(
            stream,
            dtype=str,
            keep_default_na=False,
        )
    else:
        raise ValueError("Only CSV and XLSX files are supported.")

    if len(df) > 25000:
        raise ValueError("Maximum 25,000 rows per report.")

    return normalize(df)


def csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def xlsx_bytes(df):
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            sheet_name="Report",
            index=False,
        )

    return buffer.getvalue()


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def public_view(df):
    return df[
        [
            "Finding ID",
            "Record",
            "Issue",
            "What Vexa found",
            "Suggested check",
        ]
    ]


# ============================================================
# AUDIT HISTORY
# ============================================================

AUDIT_COLUMNS = [
    "Audit ID",
    "When",
    "Action",
    "Finding ID",
    "Record",
    "Reviewer",
    "Details",
]


def load_audit_history():
    if PUBLIC_DEMO:
        return pd.DataFrame(
            list(reversed(S.history)),
            columns=AUDIT_COLUMNS,
        )

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            """
            SELECT
                id AS "Audit ID",
                timestamp AS "When",
                action AS "Action",
                finding_id AS "Finding ID",
                record_id AS "Record",
                reviewer AS "Reviewer",
                details AS "Details"
            FROM audit_history
            ORDER BY id DESC
            """,
            conn,
        )


def log_history(
    action,
    finding_id,
    record,
    reviewer,
    details,
):
    event_time = timestamp()

    if not PUBLIC_DEMO:
        save_audit_action(
            event_time,
            str(action),
            str(finding_id),
            str(record),
            str(reviewer),
            str(details),
        )

    S.audit_counter += 1

    S.history.append({
        "Audit ID": S.audit_counter,
        "When": event_time,
        "Action": action,
        "Finding ID": finding_id,
        "Record": record,
        "Reviewer": reviewer,
        "Details": details,
    })


# ============================================================
# FICTIONAL SAMPLE DATA
# ============================================================

def sample_files():
    a = []
    b = []

    for n in range(1, 120):
        row = {
            "ID": f"REQ-{n:04d}",
            "Category": [
                "Visit",
                "Outreach",
                "Document",
            ][n % 3],
            "Status": (
                "Pending"
                if n % 5 == 0
                else "Completed"
            ),
            "Owner": [
                "Team A",
                "Team B",
                "Team C",
            ][n % 3],
        }

        a.append(row.copy())

        if n not in {
            12, 24, 36, 48,
            60, 72, 84, 96,
        }:
            other = row.copy()

            if n in {7, 14, 21, 28}:
                other["Status"] = "Changed"

            b.append(other)

    a.append(a[11].copy())

    for n in range(120, 124):
        b.append({
            "ID": f"REQ-{n:04d}",
            "Category": "Outreach",
            "Status": "Pending",
            "Owner": "Team B",
        })

    return pd.DataFrame(a), pd.DataFrame(b)


# ============================================================
# COMPARISON ENGINE
# ============================================================

def compare(a, b, ka, kb, na, nb):
    ids_a = a[ka].map(safe_text)
    ids_b = b[kb].map(safe_text)
    findings = []

    def add(
        record,
        issue,
        description,
        suggestion,
        kind="",
        ia=None,
        ib=None,
        column="",
        va="",
        vb="",
        target="",
    ):
        findings.append({
            "Finding ID": f"F-{len(findings) + 1:03d}",
            "Record": str(record),
            "Issue": issue,
            "What Vexa found": description,
            "Suggested check": suggestion,
            "_kind": kind,
            "_ia": ia,
            "_ib": ib,
            "_column": column,
            "_va": va,
            "_vb": vb,
            "_target": target,
        })

    # Missing and duplicate IDs
    for name, ids, side in [
        (na, ids_a, "A"),
        (nb, ids_b, "B"),
    ]:
        for idx, key in ids.items():
            if not key:
                add(
                    f"{name}, row {idx + 2}",
                    "Missing ID",
                    f"No matching ID in {name}, row {idx + 2}.",
                    "Confirm the original ID. Do not invent an identifier.",
                    kind="missing_id",
                    target=side,
                )

        counts = ids[ids != ""].value_counts()

        for key, count in counts[counts > 1].items():
            add(
                key,
                "Possible duplicate",
                f"{key} occurs {count} times in {name}.",
                "Check whether these rows are true duplicates "
                "or valid separate entries.",
                kind="duplicate",
                target=side,
            )

    loc_a = {
        key: list(ids_a[ids_a == key].index)
        for key in ids_a.unique()
        if key
    }

    loc_b = {
        key: list(ids_b[ids_b == key].index)
        for key in ids_b.unique()
        if key
    }

    for key in sorted(set(loc_a) - set(loc_b)):
        add(
            key,
            "Only in first report",
            f"{key} appears in {na}, but not in {nb}.",
            "Check whether this record should appear in both reports.",
            kind="only_a",
        )

    for key in sorted(set(loc_b) - set(loc_a)):
        add(
            key,
            "Only in second report",
            f"{key} appears in {nb}, but not in {na}.",
            "Check whether this difference is expected.",
            kind="only_b",
        )

    common_cols = [
        col for col in a.columns
        if col in b.columns and col not in {ka, kb}
    ]

    for key in sorted(set(loc_a) & set(loc_b)):
        if len(loc_a[key]) != 1 or len(loc_b[key]) != 1:
            continue

        ia = loc_a[key][0]
        ib = loc_b[key][0]

        for col in common_cols:
            va = safe_text(a.at[ia, col])
            vb = safe_text(b.at[ib, col])

            if va != vb:
                add(
                    key,
                    "Different values",
                    f'{col}: {na} = "{va}"; {nb} = "{vb}".',
                    "Verify the correct value using a trusted "
                    "source before changing either report.",
                    kind="value",
                    ia=ia,
                    ib=ib,
                    column=col,
                    va=va,
                    vb=vb,
                )

    return pd.DataFrame(
        findings,
        columns=[
            "Finding ID",
            "Record",
            "Issue",
            "What Vexa found",
            "Suggested check",
            "_kind",
            "_ia",
            "_ib",
            "_column",
            "_va",
            "_vb",
            "_target",
        ],
    )


def refresh():
    if S.a is None or S.b is None:
        return

    S.findings = compare(
        S.a,
        S.b,
        S.ka,
        S.kb,
        S.na,
        S.nb,
    )

    S.ai_response = None
    S.ai_context = None


def load_reports(a, b, na, nb, ka, kb, company):
    S.original_a = normalize(a)
    S.original_b = normalize(b)

    S.a = S.original_a.copy(deep=True)
    S.b = S.original_b.copy(deep=True)

    S.row_ids_a = list(range(len(S.a)))
    S.row_ids_b = list(range(len(S.b)))

    S.na = na
    S.nb = nb
    S.ka = ka
    S.kb = kb
    S.company = company

    S.reviews = {}
    S.history = []
    S.audit_counter = 0
    S.deletions = 0
    S.load_number += 1

    refresh()
    S.page = "Dashboard"


# ============================================================
# CHANGE REPORT
# ============================================================

def build_change_report(original, corrected, row_ids, key_col):
    changes = []

    current_map = {
        original_id: current_idx
        for current_idx, original_id in enumerate(row_ids)
    }

    for orig_idx in range(len(original)):
        record = safe_text(original.at[orig_idx, key_col])
        excel_row = orig_idx + 2

        if orig_idx not in current_map:
            changes.append({
                "Change Type": "Deleted row",
                "Record ID": record,
                "Original Excel Row": excel_row,
                "Column": "Entire row",
                "Original Value": str(
                    original.loc[orig_idx].to_dict()
                ),
                "Corrected Value": "(Row removed)",
            })
            continue

        curr_idx = current_map[orig_idx]

        for col in original.columns:
            old = safe_text(original.at[orig_idx, col])
            new = safe_text(corrected.at[curr_idx, col])

            if old != new:
                changes.append({
                    "Change Type": "Value corrected",
                    "Record ID": record,
                    "Original Excel Row": excel_row,
                    "Column": col,
                    "Original Value": old,
                    "Corrected Value": new,
                })

    return pd.DataFrame(
        changes,
        columns=[
            "Change Type",
            "Record ID",
            "Original Excel Row",
            "Column",
            "Original Value",
            "Corrected Value",
        ],
    )


def filtered_preview(frame, key_col, search_text):
    if not search_text.strip():
        return frame

    return frame[
        frame[key_col]
        .map(safe_text)
        .str.contains(
            search_text.strip(),
            case=False,
            regex=False,
            na=False,
        )
    ]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brandmark">✓</div>
            <div>
                <div class="brandname">vexa.</div>
                <div class="brandsub">
                    DATA OPERATIONS INTELLIGENCE
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = [
        "Dashboard",
        "Upload & Compare",
        "Investigations",
        "AI Assistant",
        "Review History",
        "Export Results",
    ]

    for page in pages:
        if st.button(
            page,
            use_container_width=True,
            type="primary" if S.page == page else "secondary",
            key=f"nav_{page}",
        ):
            S.page = page
            st.rerun()

    st.divider()

    st.caption(
        "Fictional / non-sensitive files only. "
        "Never upload patient information."
    )

    if PUBLIC_DEMO:
        st.caption(
            "Public demo · Session-only audit history"
        )


st.markdown(
    '<div class="overline">'
    'DATA OPERATIONS INTELLIGENCE'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if S.page == "Dashboard":
    st.title("Data Quality Overview")

    if S.a is None:
        st.info(
            "Welcome to Vexa. Upload two reports "
            "to begin your data quality analysis."
        )

        st.write(
            "Vexa compares records, identifies differences, "
            "supports investigations, and allows "
            "employee-approved corrections."
        )

        if st.button("Upload Your Reports", type="primary"):
            S.page = "Upload & Compare"
            st.rerun()

    else:
        f = S.findings

        st.caption(f"{S.company} · {S.na} vs {S.nb}")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Rows in Report A", len(S.a))
        c2.metric("Rows in Report B", len(S.b))
        c3.metric("Current differences", len(f))
        c4.metric("Reviews saved", len(S.reviews))
        c5.metric(
            "Corrections applied",
            sum(
                item["Action"] == "Correction applied"
                for item in S.history
            ),
        )

        st.caption(
            "Current differences come from the latest comparison. "
            "Corrections applied counts approved value changes "
            "in this session."
        )

        if S.deletions:
            st.caption(
                f"Verified duplicate rows removed: {S.deletions}"
            )

        left, right = st.columns([1.5, 1])

        with left:
            st.subheader("Differences by Category")

            if not f.empty:
                st.bar_chart(
                    f["Issue"].value_counts(),
                    color="#bc4074",
                    height=320,
                )
            else:
                st.success(
                    "No differences found with these comparison rules."
                )

        with right:
            st.subheader("Review Activity")

            st.metric(
                "Findings reviewed this comparison",
                len(S.reviews),
            )

            st.progress(
                min(len(S.reviews) / max(len(f), 1), 1.0)
            )

            st.write(
                "A reviewed finding is not necessarily resolved."
            )

            if st.button(
                "Open Investigations",
                type="primary",
            ):
                S.page = "Investigations"
                st.rerun()

        st.subheader("Recent Findings")

        if not f.empty:
            st.dataframe(
                public_view(f).head(10),
                hide_index=True,
                use_container_width=True,
            )


# ============================================================
# PAGE 2 — UPLOAD & COMPARE
# ============================================================

elif S.page == "Upload & Compare":
    st.title("Upload & Compare")

    st.write(
        "Upload two CSV or Excel files. "
        "Choose the matching identifier column in both files."
    )

    if PUBLIC_DEMO:
        st.warning(
            "Public demo: use only fictional, non-sensitive reports."
        )

    company = st.text_input(
        "Company or workspace name",
        value=S.company,
    )

    col1, col2 = st.columns(2)

    with col1:
        na = st.text_input(
            "First report name",
            value=S.na,
        )

        ua = st.file_uploader(
            "First report",
            type=["csv", "xlsx"],
            key="upload_a",
        )

    with col2:
        nb = st.text_input(
            "Second report name",
            value=S.nb,
        )

        ub = st.file_uploader(
            "Second report",
            type=["csv", "xlsx"],
            key="upload_b",
        )

    if ua is not None and ub is not None:
        try:
            aa = read_upload(ua)
            bb = read_upload(ub)

            if aa.empty or bb.empty:
                st.error(
                    "Both reports need at least one data row."
                )

            else:
                key1, key2 = st.columns(2)

                with key1:
                    ka = st.selectbox(
                        "Matching column in first report",
                        list(aa.columns),
                    )

                with key2:
                    kb = st.selectbox(
                        "Matching column in second report",
                        list(bb.columns),
                    )

                st.caption(
                    f"{len(aa)} first-report rows · "
                    f"{len(bb)} second-report rows"
                )

                if st.button(
                    "Compare Reports",
                    type="primary",
                ):
                    if not na.strip() or not nb.strip():
                        st.error(
                            "Give each report a name."
                        )
                    elif na.strip() == nb.strip():
                        st.error(
                            "Report names must be different."
                        )
                    else:
                        load_reports(
                            aa,
                            bb,
                            na.strip(),
                            nb.strip(),
                            ka,
                            kb,
                            company.strip() or "My Workspace",
                        )
                        st.rerun()

        except Exception as ex:
            st.error(f"Cannot read file: {ex}")

    st.divider()

    with st.expander("Optional: fictional sample data"):
        st.caption(
            "Sample reports are loaded only "
            "when you click the button."
        )

        if st.button("Load fictional sample reports"):
            aa, bb = sample_files()

            load_reports(
                aa,
                bb,
                "Report A",
                "Report B",
                "ID",
                "ID",
                "Example Company",
            )
            st.rerun()

    st.info(
        "Reports may have different purposes. "
        "Missing records or mismatched values "
        "are not automatically errors."
    )


# ============================================================
# PAGE 3 — INVESTIGATIONS
# ============================================================

elif S.page == "Investigations":
    st.title("Investigations")

    st.caption(
        "Inspect evidence, save your decision, "
        "and apply only verified changes."
    )

    if S.a is None:
        st.info("Upload and compare two reports first.")

    elif S.findings.empty:
        st.success("No differences to investigate.")

    else:
        f = S.findings

        categories = [
            "All"
        ] + sorted(f["Issue"].unique().tolist())

        category = st.selectbox(
            "Filter findings",
            categories,
        )

        filtered = (
            f if category == "All"
            else f[f["Issue"] == category]
        )

        st.dataframe(
            public_view(filtered)[
                ["Finding ID", "Record", "Issue"]
            ],
            hide_index=True,
            use_container_width=True,
        )

        chosen = st.selectbox(
            "Select finding",
            filtered["Finding ID"].tolist(),
        )

        issue = f[
            f["Finding ID"] == chosen
        ].iloc[0]

        record = issue["Record"]
        suffix = f"{S.load_number}_{chosen}"

        with st.container(border=True):
            st.subheader(
                f"{record} · {issue['Issue']}"
            )

            st.write("**What Vexa found**")
            st.write(issue["What Vexa found"])

            st.write("**What to investigate**")
            st.write(issue["Suggested check"])

            previous = S.reviews.get(chosen, {})

            reviewer = st.text_input(
                "Reviewed by",
                value=previous.get("Reviewer", "Analyst"),
                key="reviewer_" + suffix,
            )

            decisions = [
                "Needs follow-up",
                "Confirmed issue",
                "Expected difference",
                "Resolved",
            ]

            decision = st.selectbox(
                "Decision",
                decisions,
                index=(
                    decisions.index(previous["Decision"])
                    if previous.get("Decision") in decisions
                    else 0
                ),
                key="decision_" + suffix,
            )

            notes = st.text_area(
                "What did you verify?",
                value=previous.get("Notes", ""),
                key="notes_" + suffix,
            )

            if st.button(
                "Save Review",
                type="primary",
                key="save_" + suffix,
            ):
                if not reviewer.strip():
                    st.error("Enter the reviewer name.")

                else:
                    try:
                        log_history(
                            "Review saved",
                            chosen,
                            record,
                            reviewer.strip(),
                            f"{decision}: {notes}",
                        )

                    except sqlite3.Error as ex:
                        st.error(
                            f"Unable to save review: {ex}"
                        )

                    else:
                        S.reviews[chosen] = {
                            "Reviewer": reviewer.strip(),
                            "Decision": decision,
                            "Notes": notes,
                            "Reviewed at": timestamp(),
                        }

                        if PUBLIC_DEMO:
                            st.success(
                                "Review saved for this demo session."
                            )
                        else:
                            st.success(
                                "Review saved permanently in SQLite."
                            )

        # ----------------------------------------------------
        # VERIFIED VALUE CORRECTION
        # ----------------------------------------------------

        if issue["_kind"] == "value":
            with st.container(border=True):
                st.subheader(
                    "Apply a verified correction"
                )

                st.write(
                    "Changes are applied to a working copy. "
                    "Original uploads remain unchanged."
                )

                target = st.radio(
                    "Which report contains the wrong value?",
                    [S.na, S.nb],
                    horizontal=True,
                    key="target_" + suffix,
                )

                if target == S.na:
                    frame = S.a
                    idx = int(issue["_ia"])
                    original = issue["_va"]
                else:
                    frame = S.b
                    idx = int(issue["_ib"])
                    original = issue["_vb"]

                column = issue["_column"]

                st.write(f"**Column:** {column}")
                st.write(f"**Current value:** `{original}`")

                verified = st.text_input(
                    "Correct value (verified by employee)",
                    key="value_" + suffix,
                )

                proof = st.text_area(
                    "How did you verify this value?",
                    placeholder=(
                        "Example: Checked the approved source report."
                    ),
                    key="proof_" + suffix,
                )

                confirm = st.checkbox(
                    "I verified this correction and approve "
                    "applying it to a copy.",
                    key="confirm_" + suffix,
                )

                if st.button(
                    "Apply Approved Correction",
                    type="primary",
                    key="apply_" + suffix,
                ):
                    if (
                        not reviewer.strip()
                        or not verified.strip()
                        or not proof.strip()
                        or not confirm
                    ):
                        st.error(
                            "Enter reviewer, correct value, "
                            "evidence, and approval."
                        )

                    elif idx not in frame.index:
                        st.error(
                            "Selected row no longer exists."
                        )

                    elif safe_text(frame.at[idx, column]) != original:
                        st.error(
                            "The value has changed. "
                            "Compare again before correcting."
                        )

                    elif verified.strip() == original:
                        st.warning(
                            "New value matches current value."
                        )

                    else:
                        detail = (
                            f"{target}, {column}: "
                            f"{original!r} → "
                            f"{verified.strip()!r}. "
                            f"Evidence: {proof}"
                        )

                        try:
                            log_history(
                                "Correction applied",
                                chosen,
                                record,
                                reviewer.strip(),
                                detail,
                            )

                        except sqlite3.Error as ex:
                            st.error(
                                "Audit save failed; "
                                f"correction not applied: {ex}"
                            )

                        else:
                            frame.at[
                                idx, column
                            ] = verified.strip()

                            refresh()
                            st.rerun()

        # ----------------------------------------------------
        # VERIFIED DUPLICATE DELETION
        # ----------------------------------------------------

        elif issue["_kind"] == "duplicate":
            st.info(
                "Possible duplicates must be verified "
                "before deleting any row."
            )

            with st.container(border=True):
                st.subheader(
                    "Verified Duplicate Row Deletion"
                )

                side = issue["_target"]

                if side == "A":
                    frame = S.a
                    key_col = S.ka
                    report_name = S.na
                    row_ids = S.row_ids_a
                else:
                    frame = S.b
                    key_col = S.kb
                    report_name = S.nb
                    row_ids = S.row_ids_b

                candidates = frame[
                    frame[key_col].map(safe_text) == record
                ]

                st.write(
                    f"**Duplicate rows in {report_name}**"
                )

                preview = candidates.copy()

                preview.insert(
                    0,
                    "Original Excel Row",
                    [
                        row_ids[int(i)] + 2
                        for i in candidates.index
                    ],
                )

                st.dataframe(
                    preview,
                    hide_index=True,
                    use_container_width=True,
                )

                st.caption(
                    "Select the exact row verified "
                    "as unnecessary."
                )

                selected_row = st.selectbox(
                    "Exact duplicate row to remove",
                    candidates.index.tolist(),
                    format_func=lambda i: (
                        "Original Excel row "
                        f"{row_ids[int(i)] + 2}"
                    ),
                    key="delete_row_" + suffix,
                )

                st.write("**Selected row preview**")

                st.dataframe(
                    frame.loc[[selected_row]],
                    hide_index=True,
                    use_container_width=True,
                )

                deletion_reason = st.text_area(
                    "Why is this exact row safe to delete?",
                    placeholder=(
                        "Example: Verified against source records; "
                        "accidental duplicate."
                    ),
                    key="delete_reason_" + suffix,
                )

                deletion_approved = st.checkbox(
                    "I verified this exact duplicate and "
                    "approve removing it from the "
                    "corrected working copy.",
                    key="delete_approval_" + suffix,
                )

                if st.button(
                    "Delete Selected Duplicate Row",
                    type="primary",
                    key="delete_button_" + suffix,
                ):
                    saved_review = S.reviews.get(chosen, {})

                    if (
                        saved_review.get("Decision")
                        != "Confirmed issue"
                    ):
                        st.error(
                            "First select Confirmed issue "
                            "and click Save Review."
                        )

                    elif not reviewer.strip():
                        st.error(
                            "Enter reviewer name."
                        )

                    elif not deletion_reason.strip():
                        st.error(
                            "Enter deletion reason."
                        )

                    elif not deletion_approved:
                        st.error(
                            "Employee approval is required."
                        )

                    elif selected_row not in frame.index:
                        st.error(
                            "Selected row no longer exists."
                        )

                    elif (
                        safe_text(
                            frame.at[selected_row, key_col]
                        ) != record
                    ):
                        st.error(
                            "Selected row no longer matches."
                        )

                    elif (
                        frame[key_col]
                        .map(safe_text)
                        .eq(record)
                        .sum() < 2
                    ):
                        st.error(
                            "This ID is no longer duplicated."
                        )

                    else:
                        original_row_id = row_ids[
                            int(selected_row)
                        ]

                        removed = (
                            frame.loc[selected_row]
                            .to_dict()
                        )

                        updated = (
                            frame.drop(index=selected_row)
                            .reset_index(drop=True)
                        )

                        updated_row_ids = [
                            rid
                            for i, rid in enumerate(row_ids)
                            if i != int(selected_row)
                        ]

                        detail = (
                            f"{report_name}, original Excel "
                            f"row {original_row_id + 2}. "
                            f"Deleted: {removed}. "
                            f"Evidence: {deletion_reason}"
                        )

                        try:
                            log_history(
                                "Duplicate row deleted",
                                chosen,
                                record,
                                reviewer.strip(),
                                detail,
                            )

                        except sqlite3.Error as ex:
                            st.error(
                                "Audit save failed; "
                                f"row not deleted: {ex}"
                            )

                        else:
                            if side == "A":
                                S.a = updated
                                S.row_ids_a = updated_row_ids
                            else:
                                S.b = updated
                                S.row_ids_b = updated_row_ids

                            S.deletions += 1

                            refresh()
                            st.rerun()

        else:
            st.info(
                "This finding requires investigation. "
                "Missing records are not added automatically."
            )


# ============================================================
# PAGE 4 — GROQ AI ASSISTANT
# ============================================================

elif S.page == "AI Assistant":
    st.title("AI Investigation Assistant")

    st.write(
        "Understand data differences, explore possible "
        "business causes, and get investigation guidance "
        "using a real Large Language Model."
    )

    st.caption(
        "Powered by Groq LLM · Employee verification "
        "required · No automatic data changes"
    )

    if S.a is None:
        st.info(
            "Upload and compare two fictional reports "
            "before using the AI Assistant."
        )

    elif S.findings.empty:
        st.success(
            "No current differences found."
        )

    else:
        st.subheader("Select a Finding")

        chosen = st.selectbox(
            "Finding ID",
            S.findings["Finding ID"].tolist(),
            key="ai_finding_select",
        )

        issue = S.findings[
            S.findings["Finding ID"] == chosen
        ].iloc[0]

        with st.container(border=True):
            st.write(
                f"**Record:** {issue['Record']}"
            )

            st.write(
                f"**Issue:** {issue['Issue']}"
            )

            st.write("**What Vexa detected**")
            st.write(issue["What Vexa found"])

            st.write("**Existing suggested check**")
            st.write(issue["Suggested check"])

        st.divider()
        st.subheader("Ask Vexa AI")

        st.write(
            "Get possible business causes, impact, "
            "investigation steps, and recommendations."
        )

        question = st.text_area(
            "Optional question for AI",
            placeholder=(
                "Example: Why might this record "
                "be missing from another report?"
            ),
            max_chars=500,
            key="ai_question",
        )

        fictional_confirm = st.checkbox(
            "I confirm this finding and my question "
            "contain only fictional, non-sensitive "
            "information suitable for an external AI service.",
            key="ai_fictional_confirm",
        )

        st.caption(
            "Only the selected finding description, "
            "issue type, suggested check, and optional question "
            "are sent to Groq. Full Excel reports are not sent."
        )

        ai_context = (
            S.load_number,
            chosen,
            str(issue["Record"]),
            str(issue["Issue"]),
            str(issue["What Vexa found"]),
            str(issue["Suggested check"]),
            question,
        )

        if st.button(
            "Analyze Finding with AI ✨",
            type="primary",
            use_container_width=True,
        ):
            if not fictional_confirm:
                st.warning(
                    "Confirm fictional, non-sensitive "
                    "information before calling AI."
                )

            else:
                try:
                    api_key = get_setting("GROQ_API_KEY", "")

                    if not api_key:
                        st.error(
                            "Groq API key not found. "
                            "Check .streamlit/secrets.toml "
                            "or Streamlit Cloud secrets."
                        )

                    else:
                        safe_finding = {
                            "Issue": str(issue["Issue"]),
                            "What Vexa found": str(
                                issue["What Vexa found"]
                            ),
                            "Suggested check": str(
                                issue["Suggested check"]
                            ),
                        }

                        with st.spinner(
                            "Vexa AI is analyzing..."
                        ):
                            response = analyze_finding(
                                api_key=api_key,
                                finding=safe_finding,
                                question=question,
                            )

                        S.ai_response = response
                        S.ai_context = ai_context

                except Exception as ex:
                    S.ai_response = None
                    S.ai_context = None

                    error_name = type(ex).__name__

                    if error_name == "RateLimitError":
                        st.warning(
                            "Groq free-tier limit reached. "
                            "Try again when quota resets."
                        )

                    elif error_name == "AuthenticationError":
                        st.error(
                            "Groq authentication failed. "
                            "Check your API key."
                        )

                    elif error_name == "NotFoundError":
                        st.error(
                            "Groq model unavailable. "
                            "Check ai_assistant.py."
                        )

                    elif error_name == "APIConnectionError":
                        st.error(
                            "Cannot connect to Groq. "
                            "Check internet connection."
                        )

                    else:
                        st.error(
                            "AI request could not be completed. "
                            f"Error type: {error_name}"
                        )

        if (
            S.ai_response
            and S.ai_context == ai_context
        ):
            st.divider()
            st.subheader("Vexa AI Analysis")

            with st.container(border=True):
                st.markdown(S.ai_response)

            st.caption(
                "AI-generated guidance may be inaccurate. "
                "Validate against trusted records."
            )

            st.warning(
                "AI has not modified either report. "
                "An employee must verify evidence "
                "and approve data changes."
            )

            if st.button(
                "Open Investigations",
                type="primary",
                key="ai_open_investigations",
            ):
                S.page = "Investigations"
                st.rerun()


# ============================================================
# PAGE 5 — REVIEW HISTORY
# ============================================================

elif S.page == "Review History":
    st.title("Review History")

    if PUBLIC_DEMO:
        st.caption(
            "Public demo: audit actions belong only "
            "to your current session. They are not "
            "saved to a shared database."
        )
    else:
        st.caption(
            "Audit history is saved in the local SQLite "
            "database. Saved actions remain available "
            "after restarting Vexa."
        )

    try:
        history = load_audit_history()

    except sqlite3.Error as ex:
        st.error(
            f"Unable to load audit history: {ex}"
        )

    else:
        if not history.empty:
            if PUBLIC_DEMO:
                st.success(
                    f"{len(history)} audit actions "
                    "in your demo session."
                )
            else:
                st.success(
                    f"{len(history)} saved audit "
                    "actions found in SQLite."
                )

            st.dataframe(
                history,
                hide_index=True,
                use_container_width=True,
            )

            st.download_button(
                "Download Review History",
                csv_bytes(history),
                file_name="vexa_review_history.csv",
                mime="text/csv",
            )

        else:
            st.info(
                "No review actions have been saved yet."
            )

    if PUBLIC_DEMO:
        st.caption(
            "Demo history is not permanent. "
            "Download it before your session ends."
        )
    else:
        st.caption(
            "Audit actions are permanent locally. "
            "Uploaded reports and corrected working "
            "copies remain session-based."
        )


# ============================================================
# PAGE 6 — EXPORT RESULTS
# ============================================================

elif S.page == "Export Results":
    st.title("Export Results")

    st.write(
        "Preview original and corrected reports, "
        "verify changes, and download only when ready."
    )

    if S.a is None:
        st.info(
            "Upload and compare two reports "
            "before viewing exports."
        )

    else:
        selected_report = st.radio(
            "Select report",
            ["Report A", "Report B"],
            horizontal=True,
            key="export_report_choice",
        )

        if selected_report == "Report A":
            original_df = S.original_a
            corrected_df = S.a
            row_ids = S.row_ids_a
            key_col = S.ka
            report_name = S.na
            prefix = "vexa_report_a"

        else:
            original_df = S.original_b
            corrected_df = S.b
            row_ids = S.row_ids_b
            key_col = S.kb
            report_name = S.nb
            prefix = "vexa_report_b"

        st.subheader(report_name)

        changes = build_change_report(
            original_df,
            corrected_df,
            row_ids,
            key_col,
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Original rows",
            len(original_df),
        )

        c2.metric(
            "Current rows",
            len(corrected_df),
        )

        c3.metric(
            "Changes made",
            len(changes),
        )

        st.caption(
            "Changes made counts corrected cells "
            "and deleted rows. It does not count "
            "unresolved differences between reports."
        )

        st.divider()

        preview_mode = st.radio(
            "Preview mode",
            [
                "Original Preview",
                "Corrected Preview",
                "Compare Changes",
            ],
            horizontal=True,
            key="export_preview_mode",
        )

        search_text = st.text_input(
            "Search by Request ID",
            placeholder="Example: R-107",
            key="export_search",
        )

        if preview_mode == "Original Preview":
            st.subheader("Original Uploaded Report")

            result = filtered_preview(
                original_df,
                key_col,
                search_text,
            )

            st.caption(
                f"Showing {len(result)} matching original rows."
            )

            st.dataframe(
                result,
                hide_index=True,
                use_container_width=True,
            )

            st.info(
                "This is the original uploaded data. "
                "Vexa has not modified this snapshot."
            )

        elif preview_mode == "Corrected Preview":
            st.subheader("Current Corrected Report")

            result = filtered_preview(
                corrected_df,
                key_col,
                search_text,
            )

            st.caption(
                f"Showing {len(result)} matching corrected rows."
            )

            st.dataframe(
                result,
                hide_index=True,
                use_container_width=True,
            )

            st.success(
                "This working copy includes approved "
                "corrections and verified deletions."
            )

        else:
            st.subheader("Original vs Corrected Changes")

            if search_text.strip():
                visible_changes = changes[
                    changes["Record ID"]
                    .astype(str)
                    .str.contains(
                        search_text.strip(),
                        case=False,
                        regex=False,
                        na=False,
                    )
                ]
            else:
                visible_changes = changes

            if visible_changes.empty:
                st.info(
                    "No changes found for this search. "
                    "Try another Request ID."
                )
            else:
                st.dataframe(
                    visible_changes,
                    hide_index=True,
                    use_container_width=True,
                )

                st.caption(
                    "Deleted rows show original contents. "
                    "Value corrections show old and new values."
                )

        st.divider()
        st.subheader("Download Reports")

        original_col, corrected_col = st.columns(2)

        excel_mime = (
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        )

        with original_col:
            st.write("**Original Report**")

            st.download_button(
                "Download Original — CSV",
                csv_bytes(original_df),
                file_name=f"{prefix}_original.csv",
                mime="text/csv",
                use_container_width=True,
                key="export_original_csv",
            )

            try:
                st.download_button(
                    "Download Original — Excel",
                    xlsx_bytes(original_df),
                    file_name=f"{prefix}_original.xlsx",
                    mime=excel_mime,
                    use_container_width=True,
                    key="export_original_excel",
                )
            except ImportError:
                st.caption(
                    "Install openpyxl for Excel download."
                )

        with corrected_col:
            st.write("**Corrected Report**")

            st.download_button(
                "Download Corrected — CSV",
                csv_bytes(corrected_df),
                file_name=f"{prefix}_corrected.csv",
                mime="text/csv",
                use_container_width=True,
                key="export_corrected_csv",
            )

            try:
                st.download_button(
                    "Download Corrected — Excel",
                    xlsx_bytes(corrected_df),
                    file_name=f"{prefix}_corrected.xlsx",
                    mime=excel_mime,
                    use_container_width=True,
                    key="export_corrected_excel",
                )
            except ImportError:
                st.caption(
                    "Install openpyxl for Excel download."
                )

        st.divider()
        st.subheader("Additional Reports")

        st.download_button(
            "Download difference report",
            csv_bytes(public_view(S.findings)),
            file_name="vexa_differences.csv",
            mime="text/csv",
        )

        st.download_button(
            "Download changes made",
            csv_bytes(changes),
            file_name=f"{prefix}_changes.csv",
            mime="text/csv",
        )

        try:
            saved_history = load_audit_history()

            if not saved_history.empty:
                st.download_button(
                    "Download review & correction history",
                    csv_bytes(saved_history),
                    file_name="vexa_review_history.csv",
                    mime="text/csv",
                )

        except sqlite3.Error as ex:
            st.warning(
                f"Could not load audit history: {ex}"
            )

        if st.button(
            "Compare current corrected copies again",
            type="primary",
        ):
            refresh()
            S.page = "Dashboard"
            st.rerun()

        st.caption(
            "Original files are never overwritten. "
            "Download corrected reports before ending "
            "your session."
        )
