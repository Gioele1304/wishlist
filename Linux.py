#!/usr/bin/env python3
import sys
import requests

// CONFIGURAZIONE SUPABASE
const SUPABASE_URL = 'https://zvohvfxmdqfsfnevqips.supabase.co';
// Incolla qui sotto la tua anon key presa da Supabase (Project Settings > API)
const SUPABASE_KEY = 'sb_publishable_zjFI466Teft8rdtRNDNqOg_yMKX0UTn';

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

ENDPOINT = f"{SUPABASE_URL}/rest/v1/gifts"

def add_item(title, category="", description="", url=""):
    """Aggiunge un nuovo elemento."""
    data = {
        "title": title,
        "category": category,
        "description": description,
        "url": url
    }
    res = requests.post(ENDPOINT, json=data, headers=HEADERS)
    if res.status_code in [200, 201]:
        print(f"✔ Oggetto aggiunto: '{title}'")
    else:
        print(f"✖ Errore [{res.status_code}]: {res.text}")

def list_items():
    """Elenca tutti gli elementi presenti nella wishlist."""
    # Ordina per ID decrescente (ultimi aggiunti prima)
    res = requests.get(f"{ENDPOINT}?select=*&order=id.desc", headers=HEADERS)
    if res.status_code == 200:
        items = res.json()
        if not items:
            print("La wishlist è vuota.")
            return
        
        print("\n--- LA TUA WISHLIST ---")
        for item in items:
            item_id = item.get("id")
            title = item.get("title", "")
            cat = f" [{item.get('category')}]" if item.get("category") else ""
            desc = f"\n    Note: {item.get('description')}" if item.get("description") else ""
            url = f"\n    Link: {item.get('url')}" if item.get("url") else ""
            
            print(f"[{item_id}] {title}{cat}{desc}{url}")
        print("------------------------\n")
    else:
        print(f"✖ Errore [{res.status_code}]: {res.text}")

def delete_item(item_id):
    """Rimuove un elemento tramite il suo ID."""
    url_del = f"{ENDPOINT}?id=eq.{item_id}"
    res = requests.delete(url_del, headers=HEADERS)
    if res.status_code in [200, 204]:
        print(f"✔ Oggetto con ID [{item_id}] rimosso con successo.")
    else:
        print(f"✖ Errore [{res.status_code}]: {res.text}")

def show_help():
    print("""
Uso:
  python3 wishlist.py add "Titolo" [categoria] [note/descrizione] [url]
  python3 wishlist.py list
  python3 wishlist.py del <ID_oggetto>

Esempi:
  python3 wishlist.py add "Arduino Uno R4" "Elettronica" "Per test IoT" "https://..."
  python3 wishlist.py list
  python3 wishlist.py del 5
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "add" and len(sys.argv) >= 3:
        title = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else ""
        description = sys.argv[4] if len(sys.argv) > 4 else ""
        url = sys.argv[5] if len(sys.argv) > 5 else ""
        add_item(title, category, description, url)

    elif cmd == "list":
        list_items()

    elif cmd == "del" and len(sys.argv) >= 3:
        delete_item(sys.argv[2])

    else:
        show_help()
