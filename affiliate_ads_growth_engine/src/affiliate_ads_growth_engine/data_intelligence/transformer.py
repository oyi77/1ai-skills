import pandas as pd

class FunnelBuilder:
 def __init__(self, fb_df: pd.DataFrame, click_df: pd.DataFrame, conv_df: pd.DataFrame):
 self.fb = fb_df
 self.clicks = click_df
 self.conv = conv_df

 def build(self):
 fb = self.fb.copy()
 click = self.clicks.copy()
 conv = self.conv.copy()

 click_grouped = click.groupby("date").agg({"clicks": "sum"}).rename(columns={"clicks": "shopee_clicks"})
 conv_grouped = conv.groupby("date").agg({
 "orders": "sum",
 "revenue": "sum",
 "commission": "sum"
 })

 fb_grouped = fb.groupby("date").agg({
 "spend": "sum",
 "impressions": "sum",
 "clicks": "sum",
 "ctr": "mean",
 "cpc": "mean",
 "cpm": "mean"
 })

 funnel = fb_grouped.join(click_grouped, how="left").join(conv_grouped, how="left").fillna(0)
 funnel["conversion_rate"] = funnel["orders"] / funnel["shopee_clicks"].replace(0, pd.NA)
 funnel["roas"] = funnel["revenue"] / funnel["spend"].replace(0, pd.NA)
 funnel["profit"] = funnel["revenue"] - funnel["spend"]
 return funnel.reset_index()
