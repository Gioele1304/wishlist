#!/usr/bin/env python3
import sys
import time
import requests

# CONFIGURAZIONE SUPABASE
SUPABASE_URL = 'https://zvohvfxmdqfsfnevqips.supabase.co';
# Incolla qui sotto la tua anon key presa da Supabase (Project Settings > API)
SUPABASE_KEY = 'sb_publishable_zjFI466Teft8rdtRNDNqOg_yMKX0UTn';

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

ENDPOINT = f"{SUPABASE_URL}/rest/v1/gifts"

def get_existing_categories():
    """Recupera l'elenco delle categorie uniche già presenti nel database."""
    res = requests.get(f"{ENDPOINT}?select=category", headers=HEADERS)
    if res.status_code == 200:
        items = res.json()
        categories = sorted(list(set(item.get("category") for item in items if item.get("category"))))
        return categories
    return []

def interactive_add():
    """Procedura guidata passo-passo per aggiungere un oggetto."""
    print("\n--- AGGIUNGI OGGETTO ALLA WISHLIST ---")
    
    # 1. Gestione Categoria
    categories = get_existing_categories()
    print("\nCategorie disponibili nel database:")
    if categories:
        for i, cat in enumerate(categories, 1):
            print(f"  [{i}] {cat}")
    else:
        print("  (Nessuna categoria trovata)")
        
    print("  [+] Aggiungi una nuova categoria")
    
    scelta = input("\nSeleziona il numero della categoria o scrivi il nome (o '+' per crearne una nuova): ").strip()
    
    category = ""
    if scelta.isdigit() and 1 <= int(scelta) <= len(categories):
        category = categories[int(scelta) - 1]
    elif scelta == "+":
        category = input("Inserisci il nome della nuova categoria: ").strip().lower()
    else:
        category = scelta.strip().lower()
        
    if not category:
        print("✖ Errore: La categoria non può essere vuota.")
        return

    # 2. Nome / Titolo
    title = input("Nome dell'oggetto: ").strip()
    if not title:
        print("✖ Errore: Il titolo non può essere vuoto.")
        return

    # 3. Descrizione / Note
    description = input("Descrizione o note (opzionale, premi Invio per saltare): ").strip()

    # 4. Link URL
    url = input("Link (opzionale, premi Invio per saltare): ").strip()

    # Generazione ID unico basato su categoria e timestamp
    safe_title = "".join(c if c.isalnum() else "_" for c in title.lower()).strip("_")
    unique_id = f"{category}_{int(time.time())}"

    data = {
        "id": unique_id,
        "title": title,
        "category": category,
        "description": description,
        "url": url,
        "border_color": "#6366f1"
    }

    res = requests.post(ENDPOINT, json=data, headers=HEADERS)
    if res.status_code in [200, 201]:
        print(f"\n✔ Oggetto aggiunto con successo nella categoria '{category}'! (ID: {unique_id})")
    else:
        print(f"\n✖ Errore [{res.status_code}]: {res.text}")

def list_items():
    """Elenca tutti gli elementi presenti nella wishlist."""
    res = requests.get(f"{ENDPOINT}?select=id,title,category,url", headers=HEADERS)
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
            print(f"ID: {item_id} -> {title}{cat}")
        print("------------------------\n")
    else:
        print(f"✖ Errore [{res.status_code}]: {res.text}")

def delete_item(item_id):
    """Rimuove un elemento tramite il suo ID."""
    url_del = f"{ENDPOINT}?id=eq.{item_id}"
    res = requests.delete(url_del, headers=HEADERS)
    if res.status_code in [200, 204]:
        print(f"✔ Oggetto con ID '{item_id}' rimosso con successo.")
    else:
        print(f"✖ Errore [{res.status_code}]: {res.text}")
        
def show_help():
    print("""
Uso:
  python3 Linux.py add     (Avvia la procedura guidata interattiva)
  python3 Linux.py list    (Mostra tutti gli oggetti)
  python3 Linux.py del <ID> (Elimina un oggetto per ID)
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "add":
        interactive_add()
    elif cmd == "list":
        list_items()
    elif cmd == "del" and len(sys.argv) >= 3:
        delete_item(sys.argv[2])
    else:
        show_help()