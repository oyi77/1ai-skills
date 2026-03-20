import pandas as pd
from pathlib import Path

class DataIngestor:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)

    def load_facebook_ads(self, file_path):
        df = pd.read_csv(file_path)
        df.columns = [c.strip().lower() for c in df.columns]
        return df[[
            "campaign_name", "adset_name", "ad_name", "spend",
            "impressions", "clicks", "ctr", "cpc", "cpm", "date"
        ]]

    def load_shopee_clicks(self, file_path):
        df = pd.read_csv(file_path)
        df.columns = [c.strip().lower() for c in df.columns]
        return df[["product_name", "affiliate_link", "clicks", "date"]]

    def load_shopee_conversions(self, file_path):
        df = pd.read_csv(file_path)
        df.columns = [c.strip().lower() for c in df.columns]
        return df[["product_name", "orders", "revenue", "commission", "date"]]
