#!/bin/bash

# Spostati nella cartella dello script/repository
cd "$(dirname "$0")" || exit 1

# Nome del tuo file HTML principale
HTML_FILE="index.html"

echo "=== AGGIUNGI OGGETTO ALLA WISHLIST ==="
read -p "Categoria (es. chitarra, ape, costosi, musica, vinili, pesca, altro): " CATEGORY
read -p "Nome oggetto (es. Corde Ernie Ball): " ITEM
read -p "Descrizione (es. Super Slinky 9-42): " DESC
read -p "Link (URL Amazon/eBay): " LINK

# Controllo campi vuoti
if [ -z "$CATEGORY" ] || [ -z "$ITEM" ] || [ -z "$LINK" ]; then
    echo "Errore: Categoria, Nome e Link sono obbligatori!"
    exit 1
fi

# Assegna un colore di bordo in base alla categoria (opzionale, riprende il tuo stile)
case "$CATEGORY" in
    chitarra|musica) BORDER_COLOR="#3b82f6" ;;
    ape|vinili) BORDER_COLOR="#a855f7" ;;
    *) BORDER_COLOR="#6366f1" ;;
esac

# Genera il blocco HTML identico al tuo stile
HTML_SNIPPET="            <div class=\"wish-card\" style=\"border-left-color: $BORDER_COLOR;\">
                <div class=\"info\"><span class=\"title\">$ITEM</span><span class=\"desc\">$DESC</span></div>
                <a href=\"$LINK\" target=\"_blank\" class=\"btn\">Vedi ➜</a>
            </div>"

# Marcatore da cercare nel file HTML
MARKER="<!-- ADD: $CATEGORY -->"

# Verifica che il marker esista nel file HTML
if grep -q "$MARKER" "$HTML_FILE"; then
    # Inserisce il blocco HTML subito sopra il marcatore della categoria
    sed -i "/$MARKER/i\\
$HTML_SNIPPET" "$HTML_FILE"
    echo "✔ Oggetto inserito con successo nel codice HTML!"
else
    echo "❌ Errore: Marker '<!-- ADD: $CATEGORY -->' non trovato in $HTML_FILE."
    echo "Assicurati di aver inserito il commento di controllo nella sezione corretta dell'HTML."
    exit 1
fi

# Automazione Git
git add "$HTML_FILE"
git commit -m "Wishlist: aggiunto $ITEM in $CATEGORY"
git push

echo "🚀 Fatto! Sito aggiornato e modifiche inviate a GitHub."
