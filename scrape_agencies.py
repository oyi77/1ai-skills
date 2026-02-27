#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import json

# Headers to mimic browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# List of known Indonesian agencies with websites
digital_agencies_indonesia = [
    {"name": "Dentsu Indonesia", "website": "dentsu.co.id", "segment": "Enterprise Digital Agency"},
    {"name": "Ogilvy Indonesia", "website": "ogilvy.com/indonesia", "segment": "Creative Agency"},
    {"name": "Mindshare Indonesia", "website": "mindshareworld.com/id", "segment": "Media Agency"},
    {"name": "Havas Indonesia", "website": "havas.com/id", "segment": "Full-Service Agency"},
    {"name": "GroupM Indonesia", "website": "groupm.com", "segment": "Media Agency"},
    {"name": "Publicis Indonesia", "website": "publicis.com", "segment": "Full-Service Agency"},
    {"name": "Wunderman Thompson Indonesia", "website": "wundermanthompson.com", "segment": "Full-Service Agency"},
    {"name": "McCann Worldgroup Indonesia", "website": "mccannindonesia.com", "segment": "Creative Agency"},
    {"name": "M&C Saatchi Indonesia", "website": "mcsaatchi.co.id", "segment": "Creative Agency"},
    {"name": "Lowe Lintas Indonesia", "website": "lowelintas.co.id", "segment": "Creative Agency"},
    {"name": "Omnicom Media Group", "website": "omnicommediagroup.com", "segment": "Media Agency"},
    {"name": "Kantar Worldpanel Indonesia", "website": "kantarworldpanel.com", "segment": "Research Agency"},
    {"name": "Mirum Indonesia", "website": "mirumagency.com", "segment": "Digital Agency"},
    {"name": "Isobar Indonesia", "website": "isobar.com", "segment": "Digital Agency"},
    {"name": "R/GA Indonesia", "website": "rga.com", "segment": "Digital Agency"},
    {"name": "Sapient Razorfish Indonesia", "website": "sapientrazorfish.com", "segment": "Digital Agency"},
    {"name": "72andsunny Indonesia", "website": "72andsunny.com", "segment": "Creative Agency"},
    {"name": "BBDO Indonesia", "website": "bbdo.com", "segment": "Creative Agency"},
    {"name": "DDB Indonesia", "website": "ddb.com", "segment": "Creative Agency"},
    {"name": "TBWA Indonesia", "website": "tbwasoutheastasia.com", "segment": "Creative Agency"},
    {"name": "VMLY&R Indonesia", "website": "vmlyr.com", "segment": "Digital Agency"},
    {"name": "Huge Indonesia", "website": "hugeinc.com", "segment": "Digital Agency"},
    {"name": "AKQA", "website": "akqa.com", "segment": "Digital Agency"},
    {"name": "Fjord", "website": "fjordnet.com", "segment": "Design Agency"},
    {"name": "WPP Indonesia", "website": "wpp.com", "segment": "Holding Company"},
    {"name": "Interpublic Group Indonesia", "website": "interpublic.com", "segment": "Holding Company"},
    {"name": "Hakuhodo DY Holdings Indonesia", "website": "hakuhodo.co.id", "segment": "Full-Service Agency"},
    {"name": "Asatsu-DK Indonesia", "website": "adk.jp", "segment": "Full-Service Agency"},
    {"name": "Longtail Digital", "website": "longtaildigital.com", "segment": "Digital Agency"},
    {"name": "Pixelbrain", "website": "pixelbrain.com", "segment": "Digital Agency"},
    {"name": "Arfadia", "website": "arfadia.com", "segment": "Digital Agency"},
    {"name": "DigitalDistri", "website": "digitaldistri.com", "segment": "Digital Agency"},
    {"name": "eBiz Solutions", "website": "ebizsolutions.id", "segment": "E-commerce Agency"},
    {"name": "Optimatic", "website": "optimatic.co.id", "segment": "Digital Agency"},
    {"name": "Insightzz", "website": "insightzz.com", "segment": "Digital Agency"},
    {"name": "SIRCLO", "website": "sirclo.com", "segment": "E-commerce Platform"},
    {"name": "KlikEcommerce", "website": "klikecommerce.com", "segment": "E-commerce Agency"},
    {"name": "EcommerceIQ", "website": "ecommerceiq.asia", "segment": "E-commerce Agency"},
    {"name": "Bhinneka.com", "website": "bhinneka.com", "segment": "E-commerce"},
    {"name": "Blibli.com", "website": "blibli.com", "segment": "E-commerce"},
    {"name": "JD.id", "website": "jd.id", "segment": "E-commerce"},  # JD.ID
    {"name": "Shopee Indonesia", "website": "shopee.co.id", "segment": "E-commerce Platform"},
    {"name": "Tokopedia", "website": "tokopedia.com", "segment": "E-commerce Platform"},
    {"name": "Bukalapak", "website": "bukalapak.com", "segment": "E-commerce Platform"},
    {"name": "Lazada Indonesia", "website": "lazada.co.id", "segment": "E-commerce Platform"},
    {"name": "Zalora Indonesia", "website": "zalora.co.id", "segment": "Fashion E-commerce"},
    {"name": "Tiket.com", "website": "tiket.com", "segment": "Travel Platform"},
    {"name": "Traveloka", "website": "traveloka.com", "segment": "Travel Platform"},
    {"name": "OVO", "website": "ovo.id", "segment": "Fintech"},
    {"name": "GoPay", "website": "gopay.co.id", "segment": "Fintech"},
    {"name": "Dana", "website": "dana.id", "segment": "Fintech"},
    {"name": "LinkAja", "website": "linkaja.id", "segment": "Fintech"},
    {"name": "Flip", "website": "flip.id", "segment": "Fintech"},
    {"name": "Payfazz", "website": "payfazz.com", "segment": "Fintech"},
    {"name": "RupiahCepat", "website": "rupiahcepat.co.id", "segment": "Fintech"},
    {"name": "Akulaku", "website": "akulaku.com", "segment": "Fintech"},
    {"name": "HomeCredit Indonesia", "website": "homecredit.co.id", "segment": "Fintech"},
    {"name": "Adira Finance", "website": "adiraku.co.id", "segment": "Fintech"},
    {"name": "Kredit Pintar", "website": "kreditpintar.co.id", "segment": "Fintech"},
    {"name": "Digiasia Bios", "website": "digiasia.co.id", "segment": "Fintech"},
    {"name": "Qlue", "website": "qlue.co.id", "segment": "Smart City Platform"},
    {"name": "Glamo", "website": "glamo.com", "segment": "Social Commerce"},
    {"name": "Evermos", "website": "evermos.com", "segment": "Social Commerce"},
    {"name": "Super", "website": "superapp.id", "segment": "Grocery Delivery"},
    {"name": "Sayurbox", "website": "sayurbox.com", "segment": "Grocery Delivery"},
    {"name": "Tanihub", "website": "tanihub.com", "segment": "AgriTech"},
    {"name": "Kargo", "website": "kargo.tech", "segment": "Logistics"},
    {"name": "Waresix", "website": "waresix.com", "segment": "Logistics"},
    {"name": "Deliveree", "website": "deliveree.com", "segment": "Logistics"}
]

# UMKM-focused businesses
umkm_businesses = [
    {"name": "HIJUP", "website": "hijup.com", "segment": "Fashion UMKM"},
    {"name": "Jenius", "website": "jenius.co.id", "segment": "Digital Banking"},
    {"name": "Pomona", "website": "pomona.id", "segment": "Digital Marketing"},
    {"name": "Matahari Mall", "website": "mataharimall.com", "segment": "E-commerce"},
    {"name": "Berrybenka", "website": "berrybenka.com", "segment": "Fashion E-commerce"},
    {"name": "Soci