#!/usr/bin/env python3
"""
WEBHOOK SERVER HYBRID: LYNX.ID + SCALEV
Author: Vilona AI Architect
Date: 2026-02-28
"""

from flask import Flask, request, jsonify
import requests
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('/home/openclaw/.openclaw/workspace/output/webhook_hybrid.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# === CONFIGURASI PRODUK BUNDLE ===
PRODUCT_DATA = {
    "lynx": {
        "nama": "BerkahKarya All-Access Pass",
        "harga": 499000,
        "kategori": "Digital",
        "deskripsi": "Akses seumur hidup ke 14+ Tools AI BerkahKarya. Satu harga untuk menguasai pasar. Termasuk Blueprint Master Veris.",
        "foto_url": "https://berkahkarya.org/assets/bundle_master_infographic.jpg"
    },
    "scalev": {
        "nama": "BerkahKarya All-Access Pass",
        "harga": 499000,
        "kategori": "Digital Product",
        "deskripsi": "Full Access Pass ke seluruh ekosistem AI BerkahKarya. 14+ Tools, Blueprint Scaling, Support Grup.",
        "slug": "berkah-karya-all-access",
        "checkout_form_id": "#main-form-0twHs0chfL"
    }
}

# === LYNX.ID API ENDPOINTS ===
# NOTE: Ganti URL sesung API dokumentasi Lynx.id yang asli
# Ini adalah placeholder struktur umum marketplace
LYNX_BASE_URL = "https://api.lynx.id/v1"  # PLACEHOLDER - Ganti dengan URL asli
LYNX_HEADERS = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_LYNX_API_KEY"  # Aktifkan kalau pakai API key
}

# === SCALEV API ENDPOINTS ===
SCALEV_BASE_URL = "https://api.scalev.io/v1"  # PLACEHOLDER - Ganti dengan URL asli
SCALEV_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_SCALEV_API_KEY"  # Aktifkan kalau pakai API key
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "lynx_endpoint": "/lynx/create-product",
        "scalev_endpoint": "/scalev/create-product"
    }), 200

@app.route('/lynx/create-product', methods=['POST'])
def lynx_create_product():
    """
    Endpoint: Create & Publish Product di Lynx.id
    
    Request Payload (Optional):
    {
        "override_nama": "Nama Produk Kustom (opsional)",
        "override_harga": 450000,
        "override_kategori": "Fashion"
    }
    """
    try:
        data = request.json if request.is_json else {}
        
        # Override data jika ada di payload
        nama = data.get('override_nama', PRODUCT_DATA['lynx']['nama'])
        harga = data.get('override_harga', PRODUCT_DATA['lynx']['harga'])
        kategori = data.get('override_kategori', PRODUCT_DATA['lynx']['kategori'])
        deskripsi = PRODUCT_DATA['lynx']['deskripsi']
        
        logging.info(f"[LYNX] Creating product: {nama}")
        logging.info(f"[LYNX] Price: Rp {harga}")
        logging.info(f"[LYNX] Category: {kategori}")
        
        # === STEP 1: CREATE PRODUCT ===
        # NOTE: Ganti dengan endpoint sebenarnya dari dokumentasi Lynx.id
        product_payload = {
            "name": nama,
            "price": harga,
            "category": kategori,
            "description": deskripsi,
            "image_url": PRODUCT_DATA['lynx']['foto_url']
        }
        
        # response = requests.post(f"{LYNX_BASE_URL}/products", json=product_payload, headers=LYNX_HEADERS)
        # Simulasi response (Hapus bawah ini kalau pakai API asli)
        response = {
            "status": "success",
            "data": product_payload,
            "message": "Product created via API"
        }
        
        if response.get('status') == 'success':
            product_id = response.get('data', {}).get('id', 'PROD-001')
            logging.info(f"[LYNX] Product created: ID {product_id}")
            
            # === STEP 2: CREATE LISTING (JUALAN) ===
            # NOTE: Ganti dengan endpoint sebenarnya
            listing_payload = {
                "product_id": product_id,
                "title": nama,
                "description": deskripsi,
                "stock": 9999,  # Unlimited stock
                "is_active": True
            }
            
            # listing_response = requests.post(f"{LYNX_BASE_URL}/listings", json=listing_payload, headers=LYNX_HEADERS)
            # Simulasi response
            listing_response = {
                "status": "success",
                "data": listing_payload,
                "message": "Listing created via API"
            }
            
            logging.info(f"[LYNX] Listing created for product {product_id}")
            
            return jsonify({
                "status": "success",
                "lynx": {
                    "product": response,
                    "listing": listing_response,
                    "product_url": f"https://lynx.id/product/{product_id}",
                    "listing_url": f"https://lynx.id/listing/{product_id}"
                },
                "message": "✅ Produk & Listing berhasil dibuat di Lynx.id!"
            }), 200
        else:
            logging.error(f"[LYNX] Failed to create product: {response}")
            return jsonify({
                "status": "error",
                "message": f"Gagal buat produk di Lynx.id: {response.get('message', 'Unknown error')}"
            }), 500
    
    except Exception as e:
        logging.error(f"[LYNX] Exception: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error di server: {str(e)}"
        }), 500

@app.route('/scalev/create-product', methods=['POST'])
def scalev_create_product():
    """
    Endpoint: Create Product & Landing Page di Scalev
    
    Request Payload (Optional):
    {
        "override_nama": "Nama Produk Kustom",
        "override_slug": "berkah-karya-all-access",
        "override_form_id": "#main-form-0twHs0chfL"
    }
    """
    try:
        data = request.json if request.is_json else {}
        
        # Override data jika ada di payload
        nama = data.get('override_nama', PRODUCT_DATA['scalev']['nama'])
        slug = data.get('override_slug', PRODUCT_DATA['scalev']['slug'])
        deskripsi = PRODUCT_DATA['scalev']['deskripsi']
        kategori = PRODUCT_DATA['scalev']['kategori']
        form_id = data.get('override_form_id', PRODUCT_DATA['scalev']['checkout_form_id'])
        
        logging.info(f"[SCALEV] Creating product: {nama}")
        logging.info(f"[SCALEV] Slug: {slug}")
        
        # === STEP 1: CREATE PRODUCT ===
        # NOTE: Ganti dengan endpoint sebenarnya dari dokumentasi Scalev
        product_payload = {
            "name": nama,
            "price": PRODUCT_DATA['scalev']['harga'],
            "description": deskripsi,
            "category": kategori
        }
        
        # response = requests.post(f"{SCALEV_BASE_URL}/products", json=product_payload, headers=SCALEV_HEADERS)
        # Simulasi response (Hapus bawah ini kalau pakai API asli)
        product_response = {
            "status": "success",
            "data": product_payload,
            "message": "Product created via API"
        }
        
        if product_response.get('status') == 'success':
            product_id = product_response.get('data', {}).get('id', 'SCALEV-PROD-001')
            logging.info(f"[SCALEV] Product created: ID {product_id}")
            
            # === STEP 2: CREATE LANDING PAGE ===
            # NOTE: Ganti dengan endpoint sebenarnya
            lp_payload = {
                "product_id": product_id,
                "title": PRODUCT_DATA['scalev']['nama'],
                "slug": slug,
                "content": f"<div style='text-align:center'><h1>{nama}</h1></div>",  # PLACEHOLDER
                "checkout_form_id": form_id
            }
            
            # lp_response = requests.post(f"{SCALEV_BASE_URL}/landing-pages", json=lp_payload, headers=SCALEV_HEADERS)
            # Simulasi response
            lp_response = {
                "status": "success",
                "data": lp_payload,
                "message": "Landing page created via API"
            }
            
            logging.info(f"[SCALEV] Landing page created for product {product_id}")
            
            # === STEP 3: CONNECT PRODUCT TO LP ===
            # NOTE: Ganti dengan endpoint sebenarnya
            connect_payload = {
                "product_id": product_id,
                "landing_page_id": lp_response.get('data', {}).get('id', 'LP-001')
            }
            
            # connect_response = requests.post(f"{SCALEV_BASE_URL}/products/{product_id}/connect-lp", json=connect_payload, headers=SCALEV_HEADERS)
            # Simulasi response
            connect_response = {
                "status": "success",
                "data": connect_payload,
                "message": "Product connected to LP via API"
            }
            
            logging.info(f"[SCALEV] Product {product_id} connected to LP")
            
            return jsonify({
                "status": "success",
                "scalev": {
                    "product": product_response,
                    "landing_page": lp_response,
                    "connection": connect_response,
                    "product_url": f"https://scalev.io/product/{product_id}",
                    "lp_url": f"https://scalev.io/lp/{slug}"
                },
                "message": "✅ Produk & Landing Page berhasil dibuat di Scalev!"
            }), 200
        else:
            logging.error(f"[SCALEV] Failed to create product: {product_response}")
            return jsonify({
                "status": "error",
                "message": f"Gagal buat produk di Scalev: {product_response.get('message', 'Unknown error')}"
            }), 500
    
    except Exception as e:
        logging.error(f"[SCALEV] Exception: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error di server: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🦾 WEBHOOK SERVER HYBRID STARTED")
    print("🚀 Server berjalan di port 5000")
    print("📡 Endpoints:")
    print("   → POST http://localhost:5000/lynx/create-product")
    print("   → POST http://localhost:5000/scalev/create-product")
    print("📊 Log file: output/webhook_hybrid.log")
    print("\n🎯 Cara Pakai:")
    print("   1. LYNX.ID: curl -X POST http://localhost:5000/lynx/create-product")
    print("   2. SCALEV: curl -X POST http://localhost:5000/scalev/create-product")
    print("\n⚠️  NOTE: Ganti LYNX_BASE_URL dan SCALEV_BASE_URL dengan URL API asli!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
