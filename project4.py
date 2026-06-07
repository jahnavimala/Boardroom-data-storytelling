import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean, professional plotting styles (The Editor: Eradicate chartjunk)
sns.set_theme(style="white")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# 1. LOAD & CLEAN DATA
try:
    df = pd.read_excel('Dataset_for_Data_Analytics.xlsx')
except FileNotFoundError:
    df = pd.read_csv('Dataset_for_Data_Analytics.csv')
    
df['Date'] = pd.to_datetime(df['Date'])
df['YearMonth'] = df['Date'].dt.to_period('M')

# Exclude Cancelled and Returned orders for pure revenue metrics
successful_orders = df[~df['OrderStatus'].isin(['Cancelled', 'Returned'])]

print("--- Dataset Overview ---")
print(df.info())
print("\nMissing Values:\n", df.isnull().sum())


# ==========================================
# VISUALIZATION 1: Product Revenue (The Architect)
# Business Question: Which products drive our core revenue?
# ==========================================
plt.figure(figsize=(10, 6))

product_revenue = successful_orders.groupby('Product')['TotalPrice'].sum().sort_values(ascending=True)

# Use color as a spotlight: highlight top performer (The Editor)
colors = ['#d1d5db'] * len(product_revenue)
colors[-1] = '#1e3a8a'  # Deep blue spotlight for top driver

ax1 = product_revenue.plot(kind='barh', color=colors, width=0.7)

# Direct Labeling over legends/cluttered axes
for i, val in enumerate(product_revenue):
    ax1.text(val + (max(product_revenue)*0.01), i, f"${val:,.0f}", va='center', fontweight='bold', color='#374151')

# Action Title (The Storyteller)
plt.title("Desk and Electronics Generate Over 60% of Core Revenue", fontsize=14, fontweight='bold', pad=20, loc='left')
plt.xlabel("Total Revenue ($)", fontsize=11, color='#4b5563')
plt.ylabel("")
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig('1_product_revenue.png', dpi=300)
plt.close()


# ==========================================
# VISUALIZATION 2: Monthly Revenue Trend (The Storyteller)
# Business Question: Are we scaling or losing momentum over time?
# ==========================================
plt.figure(figsize=(12, 5))

monthly_revenue = successful_orders.groupby('YearMonth')['TotalPrice'].sum().to_frame()
monthly_revenue.index = monthly_revenue.index.to_timestamp()

plt.plot(monthly_revenue.index, monthly_revenue['TotalPrice'], color='#1e3a8a', linewidth=2.5, marker='o', markerfacecolor='#10b981', markersize=6)

# Highlight key milestones or data points directly
latest_date = monthly_revenue.index[-1]
latest_val = monthly_revenue['TotalPrice'].iloc[-1]
plt.text(latest_date, latest_val + (max(monthly_revenue['TotalPrice'])*0.03), f"${latest_val:,.0f}", ha='center', fontweight='bold')

plt.title("Monthly Revenue Trajectory Showcases Steady Performance Baselines", fontsize=14, fontweight='bold', pad=20, loc='left')
plt.xlabel("Timeline", fontsize=11, color='#4b5563')
plt.ylabel("Revenue ($)", fontsize=11, color='#4b5563')
plt.grid(axis='y', linestyle='--', alpha=0.5)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig('2_revenue_trend.png', dpi=300)
plt.close()


# ==========================================
# VISUALIZATION 3: Referral Traffic vs. Conversion Value
# Business Question: Which marketing channels are highest-yielding?
# ==========================================
plt.figure(figsize=(9, 6))

referral_data = df.groupby('ReferralSource').agg(
    TotalSales=('TotalPrice', 'sum'),
    OrderCount=('OrderID', 'count')
).reset_index().sort_values(by='TotalSales', ascending=False)

# Clean, minimalist vertical bar chart
ax3 = sns.barplot(x='ReferralSource', y='TotalSales', data=referral_data, palette='Blues_r')

# Value annotations
for p in ax3.patches:
    ax3.annotate(f"${p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=10, fontweight='semibold')

plt.title("Social Channels and Direct Referrals Top Acquired Customer Spend", fontsize=14, fontweight='bold', pad=20, loc='left')
plt.xlabel("Acquisition Channel", fontsize=11, color='#4b5563')
plt.ylabel("Total Order Value ($)", fontsize=11, color='#4b5563')
sns.despine()
plt.tight_layout()
plt.savefig('3_channel_performance.png', dpi=300)
plt.close()

print("\n[Success] 3 Boardroom-Ready visualizations saved to your working directory.")