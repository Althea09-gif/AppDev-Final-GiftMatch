from urllib.parse import quote_plus
import requests
from django.conf import settings

MARKETPLACE_SEARCH_BASES = {
    'Shopee': 'https://shopee.ph/search?keyword=',
    'Lazada': 'https://www.lazada.com.ph/catalog/?q=',
    'TikTok Shop': 'https://www.tiktok.com/shop/search?q=',
    'Temu': 'https://www.temu.com/search_result.html?search_key=',
}

FALLBACK_PRODUCTS = [
    {
        'title': 'Premium Gift Box Set',
        'price': 899,
        'store': 'Shopee',
        'url': 'https://shopee.ph/search?keyword=premium%20gift%20box',
        'image': 'https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&w=900&q=80',
    },
    {
        'title': 'Minimalist Smart Watch',
        'price': 1299,
        'store': 'Lazada',
        'url': 'https://www.lazada.com.ph/catalog/?q=smart%20watch',
        'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80',
    },
    {
        'title': 'Self-Care Wellness Kit',
        'price': 650,
        'store': 'TikTok Shop',
        'url': 'https://www.tiktok.com/shop/search?q=self%20care%20kit',
        'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=900&q=80',
    },
    {
        'title': 'Wireless Headphones',
        'price': 1499,
        'store': 'Shopee',
        'url': 'https://shopee.ph/search?keyword=wireless%20headphones',
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80',
    },
    {
        'title': 'Travel Organizer Set',
        'price': 540,
        'store': 'Temu',
        'url': 'https://www.temu.com/search_result.html?search_key=travel%20organizer',
        'image': 'https://images.unsplash.com/photo-1517404215738-15263e9f9178?auto=format&fit=crop&w=900&q=80',
    },
    {
        'title': 'Coffee Gift Sampler',
        'price': 720,
        'store': 'Lazada',
        'url': 'https://www.lazada.com.ph/catalog/?q=coffee%20gift%20sampler',
        'image': 'https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=900&q=80',
    },
]


def marketplace_url(store, query):
    base = MARKETPLACE_SEARCH_BASES.get(store, MARKETPLACE_SEARCH_BASES['Shopee'])
    return base + quote_plus(query)


def marketplace_urls_for_gift(gift_name):
    return {store: marketplace_url(store, gift_name) for store in MARKETPLACE_SEARCH_BASES}


def fetch_external_products(query='gift', min_price=0, max_price=999999, limit=4, marketplace='any'):
    """External product search with graceful fallback for classroom demos."""
    url = getattr(settings, 'EXTERNAL_PRODUCT_API_URL', '')
    products = []
    chosen_store = None if marketplace in (None, '', 'any') else marketplace
    if url:
        try:
            response = requests.get(url, params={'q': query, 'limit': limit}, timeout=3)
            response.raise_for_status()
            data = response.json()
            for item in data.get('products', [])[:limit]:
                price = float(item.get('price', 0)) * 58
                if min_price <= price <= max_price:
                    store = chosen_store or 'Lazada'
                    products.append({
                        'title': item.get('title', 'External Product'),
                        'price': round(price, 2),
                        'store': store,
                        'url': marketplace_url(store, item.get('title', query)),
                        'image': item.get('thumbnail') or 'https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&w=900&q=80',
                    })
        except Exception:
            products = []
    if not products:
        fallback = [p for p in FALLBACK_PRODUCTS if min_price <= p['price'] <= max_price]
        if chosen_store:
            fallback = [p for p in fallback if p['store'] == chosen_store]
        products = fallback
    return products[:limit]
