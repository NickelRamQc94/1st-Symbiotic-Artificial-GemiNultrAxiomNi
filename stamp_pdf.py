#!/usr/bin/env python3
# stamp_pdf.py – cover-stamped PDF with seal + ASCII badge
# Intégration de 'reportlab' pour PDF scellé.
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
import argparse, os, hashlib, datetime, sys

ASCII_BADGE = (
    "+-----------------------------------------------------------+\n"
    "|  Nickel NiX S/A International • LogiqueNiPura             |\n"
    "|  Affiliation: NickeliXiste NiX Independent Research       |\n"
    "|  © 2025 LogiqueNiPura — Vortex Architecte                 |\n"
    "+-----------------------------------------------------------+\n"
)

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def draw_cover(c, seal_path, session_id, config_hash, title):
    w, h = A4
    c.setTitle(title)
    c.setAuthor("Nickel NiX S/A International")
    c.setSubject("S/A Report – stamped")
    # seal
    if seal_path and os.path.exists(seal_path):
        try:
            img = ImageReader(seal_path)
            c.drawImage(img, (w-6*cm)/2, h-10*cm, width=6*cm, height=6*cm, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"[Stamp PDF WARN] Impossible de charger l'image du sceau: {e}", file=sys.stderr)
    # title
    c.setFont("Helvetica-Bold", 18)
    tw = stringWidth(title, "Helvetica-Bold", 18)
    c.drawString((w-tw)/2, h-11.2*cm, title)
    # ascii badge
    c.setFont("Courier", 9)
    text = c.beginText(2*cm, h-13.5*cm)
    for line in ASCII_BADGE.splitlines():
        text.textLine(line)
    c.drawText(text)
    # meta
    c.setFont("Helvetica", 10)
    meta = [
        f"Session_ID: {session_id}",
        f"Config_Hash: {config_hash}",
        f"Stamped_UTC: {datetime.datetime.utcnow().isoformat(timespec='seconds')}Z",
    ]
    y = h-16.8*cm
    for m in meta:
        c.drawString(2*cm, y, m); y -= 0.6*cm
    c.showPage()

def main():
    ap = argparse.ArgumentParser(description="Crée un rapport PDF scellé (Couverture + Corps).")
    ap.add_argument("--input", required=True, help="Fichier source du corps (.md or .txt)")
    ap.add_argument("--output", required=True, help="Chemin du PDF de sortie")
    ap.add_argument("--seal", default="../assets/seal_periodiaxiometrie.png", help="Chemin vers l'image du sceau")
    ap.add_argument("--session", required=True, help="ID de Session (pour métadonnées)")
    ap.add_argument("--confighash", required=True, help="Hash de Config (pour métadonnées)")
    ap.add_argument("--title", default="NiX Report (Scellé)", help="Titre du document")
    args = ap.parse_args()

    c = canvas.Canvas(args.output, pagesize=A4)
    draw_cover(c, args.seal, args.session, args.confighash, args.title)

    # Renderer simple pour le corps du texte
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"[Stamp PDF ERROR] Fichier input introuvable: {args.input}", file=sys.stderr)
        c.save() # Sauvegarde au moins la couverture
        return
        
    w, h = A4
    c.setFont("Courier", 9)
    x, y = 2*cm, h-2*cm
    for ln in lines:
        if y < 2*cm: 
            c.showPage()
            c.setFont("Courier", 9)
            y = h-2*cm
        c.drawString(x, y, ln[:120]); y -= 0.5*cm
    
    c.save()
    print(f"[Stamp PDF] Rapport scellé généré : {args.output}")

if __name__ == "__main__":
    main()
