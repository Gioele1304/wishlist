import os
import re
import sys
import subprocess

# Forza l'output UTF-8 per le emoji e i caratteri speciali
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

HTML_FILE = "index.html"

def load_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()

def save_html(content):
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def git_commit_push(message):
    try:
        subprocess.run(["git", "add", HTML_FILE], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Fatto! Modifiche inviate a GitHub con successo.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore Git: {e}")

def add_item():
    print("\n--- AGGIUNGI OGGETTO ---")
    category = input("Categoria (chitarra, ape, costosi, musica, vinili, pesca, progetti, altro): ").strip().lower()
    title = input("Nome oggetto: ").strip()
    desc = input("Descrizione: ").strip()
    link = input("Link (URL): ").strip()

    if not category or not title or not link:
        print("❌ Errore: Categoria, Nome e Link sono obbligatori.")
        return

    colors = {"chitarra": "#3b82f6", "musica": "#3b82f6", "ape": "#a855f7", "vinili": "#a855f7"}
    border_color = colors.get(category, "#6366f1")

    snippet = f"""            <div class=\"wish-card\" style=\"border-left-color: {border_color};\">
                <div class=\"info\"><span class=\"title\">{title}</span><span class=\"desc\">{desc}</span></div>
                <a href=\"{link}\" target=\"_blank\" class=\"btn\">Vedi ➜</a>
            </div>"""

    html = load_html()
    marker = f"<!-- ADD: {category} -->"

    if marker not in html:
        print(f"❌ Categoria '{category}' non trovata nell'HTML.")
        return

    html = html.replace(marker, f"{snippet}\n            {marker}")
    save_html(html)
    print(f"✔ Oggetto '{title}' aggiunto a '{category}'.")
    git_commit_push(f"Wishlist: aggiunto {title} in {category}")

def remove_item():
    print("\n--- RIMUOVI OGGETTO ---")
    category = input("Categoria da cui rimuovere (chitarra, ape, costosi, musica, vinili, pesca, progetti, altro): ").strip().lower()
    
    html = load_html()
    marker = f"<!-- ADD: {category} -->"
    if marker not in html:
        print(f"❌ Categoria '{category}' non trovata.")
        return

    page_pattern = rf'(<div id="{category}" class="page">.*?)(<!-- ADD: {category} -->)'
    match = re.search(page_pattern, html, re.DOTALL)
    if not match:
        print(f"❌ Impossibile trovare la sezione per '{category}'.")
        return

    page_content = match.group(1)
    
    # Regex corretta per catturare l'intera wish-card senza bloccarsi sui div interni
    cards = list(re.finditer(r'(<div class="wish-card"[^>]*>.*?</a\s*>\s*</div>)', page_content, re.DOTALL))

    if not cards:
        print(f"⚠️ Nessun oggetto trovato nella categoria '{category}'.")
        return

    print(f"\nOggetti attuali in '{category}':")
    card_data = []
    for i, card in enumerate(cards, 1):
        card_html = card.group(1)
        title_match = re.search(r'<span class="title">(.*?)</span>', card_html)
        desc_match = re.search(r'<span class="desc">(.*?)</span>', card_html)
        title = title_match.group(1) if title_match else "Senza nome"
        desc = desc_match.group(1) if desc_match else ""
        card_data.append((card_html, title))
        print(f"  {i}) {title} - {desc}")

    choice = input("\nInserisci il numero dell'oggetto da rimuovere (o premi Invio per annullare): ").strip()
    if not choice:
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(card_data):
            target_card_html, title = card_data[idx]
            updated_page = page_content.replace(target_card_html, "")
            html = html.replace(page_content, updated_page)
            save_html(html)
            print(f"✔ Oggetto '{title}' rimosso con successo.")
            git_commit_push(f"Wishlist: rimosso {title} da {category}")
        else:
            print("❌ Numero non valido.")
    except ValueError:
        print("❌ Input non valido.")

def main():
    print("=== GESTIONE WISHLIST ===")
    print("1) Aggiungi oggetto")
    print("2) Rimuovi oggetto")
    choice = input("Scegli un'opzione (1 o 2): ").strip()
    if choice == '1':
        add_item()
    elif choice == '2':
        remove_item()
    else:
        print("❌ Scelta non valida.")

if __name__ == "__main__":
    main()
