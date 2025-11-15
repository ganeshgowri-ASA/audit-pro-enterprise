"""
Table Components
AuditPro Enterprise - Reusable data table displays
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any


def display_dataframe(df: pd.DataFrame, title: str = None, height: int = 400, use_container_width: bool = True):
    """
    Display formatted dataframe

    Args:
        df: DataFrame to display
        title: Optional title
        height: Table height
        use_container_width: Use full container width
    """
    if title:
        st.subheader(title)

    if df.empty:
        st.info("No data available")
        return

    st.dataframe(df, height=height, use_container_width=use_container_width)


def paginated_table(df: pd.DataFrame, rows_per_page: int = 10, key: str = "table"):
    """
    Display paginated table

    Args:
        df: DataFrame to display
        rows_per_page: Number of rows per page
        key: Unique key for pagination
    """
    if df.empty:
        st.info("No data available")
        return

    total_rows = len(df)
    total_pages = (total_rows - 1) // rows_per_page + 1

    # Initialize page number in session state
    page_key = f"{key}_page"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1

    # Page selector
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.button("← Previous", key=f"{key}_prev", disabled=st.session_state[page_key] == 1):
            st.session_state[page_key] -= 1
            st.rerun()

    with col2:
        st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>Page {st.session_state[page_key]} of {total_pages} ({total_rows} total rows)</div>", unsafe_allow_html=True)

    with col3:
        if st.button("Next →", key=f"{key}_next", disabled=st.session_state[page_key] == total_pages):
            st.session_state[page_key] += 1
            st.rerun()

    # Display current page
    start_idx = (st.session_state[page_key] - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)

    st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)


def searchable_table(df: pd.DataFrame, search_columns: List[str], key: str = "search"):
    """
    Display searchable table

    Args:
        df: DataFrame to display
        search_columns: Columns to search in
        key: Unique key for search
    """
    if df.empty:
        st.info("No data available")
        return

    # Search box
    search_term = st.text_input("🔍 Search", key=f"{key}_input", placeholder="Type to search...")

    # Filter dataframe
    if search_term:
        mask = df[search_columns].astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_df = df[mask]
        st.info(f"Found {len(filtered_df)} results")
    else:
        filtered_df = df

    # Display
    st.dataframe(filtered_df, use_container_width=True)


def sortable_table(df: pd.DataFrame, default_sort_col: str = None, ascending: bool = True, key: str = "sort"):
    """
    Display sortable table

    Args:
        df: DataFrame to display
        default_sort_col: Default column to sort by
        ascending: Sort order
        key: Unique key
    """
    if df.empty:
        st.info("No data available")
        return

    # Sort selector
    col1, col2 = st.columns([3, 1])

    with col1:
        sort_column = st.selectbox(
            "Sort by",
            options=df.columns.tolist(),
            index=df.columns.tolist().index(default_sort_col) if default_sort_col in df.columns else 0,
            key=f"{key}_col"
        )

    with col2:
        sort_order = st.selectbox(
            "Order",
            options=["Ascending", "Descending"],
            index=0 if ascending else 1,
            key=f"{key}_order"
        )

    # Sort and display
    sorted_df = df.sort_values(
        by=sort_column,
        ascending=(sort_order == "Ascending")
    )

    st.dataframe(sorted_df, use_container_width=True)


def clickable_table(df: pd.DataFrame, id_column: str, display_columns: List[str] = None, key: str = "clickable"):
    """
    Display table with clickable rows (using radio buttons)

    Args:
        df: DataFrame to display
        id_column: Column containing unique IDs
        display_columns: Columns to display (None for all)
        key: Unique key

    Returns:
        Selected row ID or None
    """
    if df.empty:
        st.info("No data available")
        return None

    display_df = df[display_columns] if display_columns else df

    # Create selection column
    selection = st.radio(
        "Select a row",
        options=range(len(df)),
        format_func=lambda i: " | ".join(str(display_df.iloc[i][col]) for col in display_df.columns[:3]),
        key=key,
        label_visibility="collapsed"
    )

    if selection is not None:
        return df.iloc[selection][id_column]

    return None


def summary_table(data: Dict[str, Any], title: str = "Summary"):
    """
    Display summary table (key-value pairs)

    Args:
        data: Dictionary of key-value pairs
        title: Table title
    """
    st.subheader(title)

    df = pd.DataFrame(list(data.items()), columns=['Field', 'Value'])
    st.table(df)


def comparison_table(data: List[Dict[str, Any]], compare_columns: List[str], title: str = "Comparison"):
    """
    Display comparison table

    Args:
        data: List of dictionaries to compare
        compare_columns: Columns to compare
        title: Table title
    """
    st.subheader(title)

    if not data:
        st.info("No data to compare")
        return

    df = pd.DataFrame(data)
    if compare_columns:
        df = df[compare_columns]

    st.table(df)


def export_to_csv(df: pd.DataFrame, filename: str = "export.csv"):
    """
    Create download button for CSV export

    Args:
        df: DataFrame to export
        filename: Export filename
    """
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )


def export_to_excel(df: pd.DataFrame, filename: str = "export.xlsx"):
    """
    Create download button for Excel export

    Args:
        df: DataFrame to export
        filename: Export filename
    """
    from io import BytesIO

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

    st.download_button(
        label="📥 Download Excel",
        data=output.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
