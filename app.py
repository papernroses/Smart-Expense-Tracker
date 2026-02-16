import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data, save_expense, category_summary, monthly_summary

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# ================= DARK MODE =================
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    BG = "#0e1117"
    CARD = "#1c1f26"
    TEXT = "#ffffff"
else:
    BG = "#f6f7fb"
    CARD = "#ffffff"
    TEXT = "#000000"

# ================= COLORS =================
PRIMARY = "#6A5AF9"
SECONDARY = "#4CC9F0"
ACCENT = "#F72585"
GRADIENT = ["#6A5AF9", "#4CC9F0", "#F72585", "#FFD166", "#06D6A0", "#EF476F"]

# ================= CSS =================
st.markdown(f"""
<style>
body {{
    background-color: {BG};
    color: {TEXT};
}}
.card {{
    background-color: {CARD};
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
}}
.balance {{
    background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
    color: white;
    padding: 25px;
    border-radius: 22px;
}}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
df = load_data()
total_expense = df["amount"].sum() if not df.empty else 0

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>💸 Smart Expense Tracker</h1>", unsafe_allow_html=True)

# ================= ANIMATED TOTAL =================
counter = st.empty()
for val in np.linspace(0, total_expense, 25):
    counter.markdown(
        f"<div class='balance'><h3>Total Spent</h3><h1>₹ {val:.0f}</h1></div>",
        unsafe_allow_html=True
    )

# ================= ADD EXPENSE =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("➕ Add Expense")

c1, c2 = st.columns(2)
with c1:
    date = st.date_input("Date")
    amount = st.number_input("Amount (₹)", min_value=1)
with c2:
    category = st.selectbox(
        "Category",
        ["🍔 Food", "🚕 Travel", "🛍 Shopping", "🏠 Rent", "📺 Bills", "🎮 Entertainment", "📦 Other"]
    )
    description = st.text_input("Description")

if st.button("Add Expense"):
    save_expense(date, amount, category, description)
    st.success("Expense added ✅")
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ================= LAYOUT =================
left, right = st.columns([1.3, 1])

# ================= TRANSACTIONS =================
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Recent Transactions")
    if df.empty:
        st.info("No expenses yet")
    else:
        st.dataframe(
            df.sort_values("date", ascending=False),
            use_container_width=True,
            height=350
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ================= ANALYTICS =================
if not df.empty:
    with right:
        # ---------- CATEGORY DONUT ----------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🍩 Category-wise Spending")

        cat_data = category_summary(df)

        fig1, ax1 = plt.subplots()
        ax1.pie(
            cat_data,
            labels=cat_data.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=GRADIENT[:len(cat_data)],
            wedgeprops={"width": 0.45, "edgecolor": BG}
        )
        ax1.axis("equal")
        st.pyplot(fig1)
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- MONTHLY BAR ----------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Monthly Overview")

        month_data = monthly_summary(df)

        fig2, ax2 = plt.subplots()
        bars = ax2.bar(month_data.index.astype(str), month_data.values)

        for bar, color in zip(bars, GRADIENT):
            bar.set_color(color)

        ax2.set_ylabel("₹ Amount")
        ax2.grid(axis="y", linestyle="--", alpha=0.3)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)

        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

# ================= DOWNLOAD =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.download_button(
    "⬇️ Download Expense CSV",
    df.to_csv(index=False),
    file_name="expenses.csv",
    mime="text/csv"
)
st.markdown("</div>", unsafe_allow_html=True)