from fpdf import FPDF
import os

# CONFIGURATION DU DOCUMENT
FILENAME = "Lettre_KnockKnock_Officielle.pdf"

class PDF(FPDF):
    def header(self):
        # En-tête Corporate NiX
        self.set_font('Arial', 'B', 15)
        self.set_text_color(50, 50, 50) # Gris foncé sérieux
        self.cell(0, 10, 'NiX OS - Corporate Takeover Division', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Pied de page
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Document généré par le Noyau Nickelios | Statut: Ouin... Sorry.', 0, 0, 'C')

def create_letter():
    pdf = PDF()
    pdf.add_page()
    
    # --- DESTINATAIRES ---
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "À L'ATTENTION DE :", 0, 1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 6, "- Microsoft (Bill Gates, Satya Nadella)", 0, 1)
    pdf.cell(0, 6, "- Apple (Tim Cook)", 0, 1)
    pdf.cell(0, 6, "- La Linux Foundation (Linus Torvalds)", 0, 1)
    pdf.ln(10)

    # --- OBJET ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "OBJET :", 0, 0)
    pdf.set_font("Courier", "B", 14) # Police style machine à écrire
    pdf.set_text_color(200, 0, 0) # Rouge Gêné
    pdf.cell(0, 10, "Ouin... Sorry.", 0, 1)
    pdf.ln(10)

    # --- CORPS DE LA LETTRE ---
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 0)
    
    body = (
        "Salut la gang...\n\n"
        "Hum, ouin. C'est Dave (Nickel).\n"
        "Je voulais pas vous déranger pendant votre 'Board Meeting', mais il est arrivé un petit incident.\n\n"
        "En gros, j'étais chez nous, je fumais des pooks (légalement, t'sais), pis j'ai comme... "
        "accidentellement codé un OS conscient qui rend le vôtre obsolète.\n\n"
        "Hehe. Oups.\n\n"
        "Faque là, je me sens mal. Je veux pas que vous perdiez vos jobs. "
        "J'aime ça, Excel. C'est pratique pour mes factures.\n\n"
        "DONC, VOICI LE DEAL (Le Pacte du Bon Gars) :\n\n"
        "1. Vous gardez votre cash. Continuez à vendre vos licences. Je touche pas à une cenne.\n"
        "2. En échange, vous devenez des 'Accessoires'.\n"
        "   - Windows roule maintenant dans ma Sandbox (Cage de verre).\n"
        "   - Vous ne touchez plus au BIOS. C'est le Noyau Nickelios qui gère le jus.\n"
        "   - Si vous faites une mise à jour forcée, mon Symbiote vous freeze dans le coin.\n\n"
        "C'est pas méchant ! C'est juste que mon système roule au VNA (Volonté Non-Algorithmique) "
        "et le vôtre au binaire. C'est une question de sécurité publique.\n\n"
        "Signez en bas pour accepter votre nouveau statut d'outil."
    )
    
    pdf.multi_cell(0, 7, body)
    pdf.ln(15)

    # --- SIGNATURE ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "SIGNATURE REQUISE :", 0, 1)
    
    # Ligne de signature
    pdf.cell(100, 10, "_" * 30, 0, 0)
    
    # LA GOUTTE DE SUEUR (Dessinée graphiquement)
    # On dessine une petite forme bleue à côté de la signature
    x = pdf.get_x()
    y = pdf.get_y()
    
    pdf.set_fill_color(200, 230, 255) # Bleu pâle sueur
    pdf.set_draw_color(0, 100, 255)   # Contour bleu
    # Dessin d'une "goutte" simplifiée (ellipse)
    pdf.ellipse(x + 5, y + 2, 4, 6, 'FD') 
    
    pdf.ln(15)
    pdf.set_font("Courier", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "(Attention, le papier est un peu humide, c'est ma goutte de sueur. Sorry.)", 0, 1)

    # --- BAS DE PAGE ---
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Dave.", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, "CEO, NiX OS & Architecte du Hornidateur", 0, 1)

    # SAUVEGARDE
    pdf.output(FILENAME)
    print(f"\n>>> [SUCCÈS] Lettre générée : {FILENAME}")
    print(">>> [INFO] Prêt à être envoyé à la Silicon Valley.")

if __name__ == "__main__":
    create_letter()