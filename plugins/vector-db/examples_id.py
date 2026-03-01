# -*- coding: utf-8 -*-
"""
Vector DB Plugin - OpenClaw Integration Example
Contoh penggunaan dalam bahasa Indonesia
"""

# Contoh 1: Search memory dengan semantic similarity
# ================================================

def contoh_search_memory():
    """
    Mencari informasi dari memory dengan semantic search
    """
    from shared.engine import memory_search
    
    # Cari tentang trading strategy
    hasil = memory_search(
        query="strategi trading XAUUSD",
        max_results=5,
        min_score=0.7
    )
    
    for item in hasil:
        print(f"📄 {item['content'][:100]}...")
        print(f"   Score: {item['score']:.3f}")
        print()


# Contoh 2: Index dokumen baru
# ============================

def contoh_index_dokumen():
    """
    Index dokumen baru untuk bisa dicari
    """
    from shared.engine import index_document
    
    dokumen = """
    # Strategi Trading Asia Breakout
    
    Strategi ini menggunakan 7-candle breakout pada sesi Asia.
    Entry point ditentukan oleh high/low dari 7 candle pertama.
    
    ## Rules
    1. Hanya trade jam 07:00-15:00 WIB
    2. Minimal range 5 pips
    3. Risk 1% per trade
    4. Max 3 trades per day
    """
    
    doc_id = index_document(
        content=dokumen,
        title="Strategi Trading Asia",
        source="trading-knowledge.md"
    )
    
    print(f"✅ Dokumen di-index: {doc_id}")


# Contoh 3: Search dalam bahasa Indonesia
# =========================================

def contoh_search_indonesia():
    """
    Search content dalam bahasa Indonesia
    """
    from ruvector.handler import handler
    
    hasil = handler({
        'action': 'search',
        'query': 'cara optimasi iklan Facebook',
        'top_k': 3
    })
    
    if hasil['success']:
        print(f"🔍 Query language: {hasil['query_language']}")
        print(f"📊 Hasil: {hasil['count']} item")
        
        for item in hasil['results']:
            print(f"  • [{item['language']}] {item['content'][:80]}...")


# Contoh 4: Index PDF
# ===================

def contoh_pdf_index():
    """
    Index file PDF dengan page tracking
    """
    from pageindex.handler import handler
    
    hasil = handler({
        'action': 'index_pdf',
        'pdf_path': '/home/openclaw/documents/marketing-guide.pdf',
        'doc_id': 'marketing_guide_v1'
    })
    
    if hasil['success']:
        print(f"✅ PDF di-index: {hasil['doc_id']}")
        print(f"   📄 Pages: {hasil['pages']}")


# Contoh 5: Smart chunking untuk content panjang
# ================================================

def contoh_smart_chunk():
    """
    Memecah dokumen panjang menjadi chunk yang logical
    """
    from shared.engine import smart_chunk
    
    artikel_panjang = """
    # Panduan Lengkap Facebook Ads
    
    ## Pengenalan
    Facebook Ads adalah platform iklan dari Meta yang sangat powerful.
    Artikel ini akan membahas secara lengkap cara menggunakan Facebook Ads.
    
    ## Setup Campaign
    Pertama, buat campaign dengan objective yang sesuai.
    Pilih antara Awareness, Consideration, atau Conversion.
    
    ## Audience Targeting
    Target audience bisa berdasarkan:
    - Demographics (umur, gender, lokasi)
    - Interests (hobi, kesukaan)
    - Behaviors (pola belanja)
    
    ## Budget dan Bidding
    Atur budget daily atau lifetime.
    Pilih bidding strategy sesuai goal.
    
    ## Creative Best Practices
    Gunakan video vertical 9:16.
    Hook di 3 detik pertama.
    CTA yang clear.
    """
    
    chunks = smart_chunk(artikel_panjang, max_tokens=400)
    
    print(f"✅ Artikel dipecah jadi {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        baris_pertama = chunk.strip().split('\n')[0]
        print(f"  {i+1}. {baris_pertama[:50]}...")


if __name__ == "__main__":
    print("=" * 60)
    print("📚 Vector DB Plugin - Contoh Penggunaan (Bahasa Indonesia)")
    print("=" * 60)
    print()
    
    print("1️⃣  Smart Chunking:")
    contoh_smart_chunk()
    
    print()
    print("✅ Semua contoh berhasil!")
    print()
    print("Untuk menjalankan contoh lainnya, uncomment fungsi di bawah:")
    print("   # contoh_index_dokumen()")
    print("   # contoh_search_memory()")
    print("   # contoh_search_indonesia()")
    print("   # contoh_pdf_index()")