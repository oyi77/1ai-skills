import pandas as pd
import json
from pathlib import Path

click_csv = '/home/openclaw/.openclaw/media/inbound/WebsiteClickReport202603161654---b7c3b2a4-8b97-4543-99bf-54108669aa29.csv'
conv_csv = '/home/openclaw/.openclaw/media/inbound/AffiliateCommissionReport202603161655---dac17ac5-808b-4a19-800d-04ba291b7d72.csv'
fb_csv = '/home/openclaw/.openclaw/media/inbound/Mahir-ID-1484-Set-Iklan-12-Mar-2026-14-Mar-2026---cc120e88-d68e-4f0e-8eda-9e26fdb74014.csv'

# 1. Process Shopee Clicks
clicks = pd.read_csv(click_csv)
clicks['date'] = pd.to_datetime(clicks['Waktu Klik']).dt.date
click_daily = clicks.groupby('date').size()

# 2. Process Shopee Conversions
conv = pd.read_csv(conv_csv)
conv['date'] = pd.to_datetime(conv['Waktu Pemesanan']).dt.date
conv_daily = conv.groupby('date').agg({
    'Nilai Pembelian(Rp)': 'sum',
    'Total Komisi per Produk(Rp)': 'sum',
    'ID Pemesanan': 'nunique'
}).rename(columns={'Nilai Pembelian(Rp)': 'revenue', 'Total Komisi per Produk(Rp)': 'commission', 'ID Pemesanan': 'orders'})

# 3. Process FB Ads
fb = pd.read_csv(fb_csv)
# FB report format: "Awal pelaporan" is the date
fb['date'] = pd.to_datetime(fb['Awal pelaporan']).dt.date
fb_daily = fb.groupby('date').agg({
    'Jumlah yang dibelanjakan (IDR)': 'sum',
    'Impresi': 'sum',
    'Klik Tautan': 'sum'
}).rename(columns={'Jumlah yang dibelanjakan (IDR)': 'spend', 'Impresi': 'impressions', 'Klik Tautan': 'fb_clicks'})

# 4. Merge
report = fb_daily.join(click_daily.to_frame('shopee_clicks'), how='outer').join(conv_daily, how='outer').fillna(0)

# 5. Calculations
report['ctr'] = report['fb_clicks'] / report['impressions']
report['cpc'] = report['spend'] / report['fb_clicks']
report['cr'] = report['orders'] / report['shopee_clicks']
report['roas'] = report['revenue'] / report['spend']
report['profit'] = report['revenue'] - report['spend']

# Print results
print(report.to_markdown())
