import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def wyslij_powiadomienie(nowe_oferty):
    # Wybieramy tylko te oferty, które mają ocenę 75 lub więcej
    hity = [o for o in nowe_oferty if o.priorytet >= 75]
    
    if not hity:
        print("Brak hitów, nie wysyłam e-maila.")
        return

    # TWOJE DANE (Uzupełnij to!)
    EMAIL_NADAWCY = "your_email"
    HASLO_APLIKACJI = "password"
    EMAIL_ODBIORCY = "your_email" # Możesz wysyłać sam do siebie

    temat = f"⭐ Job Aggregator: Znalazłem {len(hity)} świetnych ofert!"
    
    # Tworzymy ładną treść w HTML
    tresc_html = "<h2>Oto najnowsze oferty dopasowane do Ciebie:</h2><hr><ul style='list-style:none; padding:0;'>"
    
    for o in hity:
        tresc_html += f"<li style='margin-bottom: 20px; padding: 10px; border-left: 5px solid #4ade80; background: #f0fdf4;'>"
        tresc_html += f"<h3 style='margin: 0;'>{o.stanowisko} <span style='color: #16a34a;'>(⭐ {o.priorytet}/100)</span></h3>"
        tresc_html += f"<b>Firma:</b> {o.firma}<br>"
        tresc_html += f"<b>Kasa:</b> 💰 {o.wynagrodzenie or 'Brak danych'} <br>"
        tresc_html += f"<b>Info:</b> 📍 {o.dodatkowe_info} <br>"
        tresc_html += f"<a href='{o.link}' style='display: inline-block; margin-top: 10px; background: #2563eb; color: white; padding: 5px 10px; text-decoration: none; border-radius: 5px;'>ZOBACZ OFERTĘ</a>"
        tresc_html += f"</li>"
        
    tresc_html += "</ul>"

    # Składamy maila w całość
    msg = MIMEMultipart()
    msg['From'] = EMAIL_NADAWCY
    msg['To'] = EMAIL_ODBIORCY
    msg['Subject'] = temat
    msg.attach(MIMEText(tresc_html, 'html'))

    # Wysyłanie przez serwer Gmail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_NADAWCY, HASLO_APLIKACJI)
        server.send_message(msg)
        server.quit()
        print(f"Pomyślnie wysłano e-mail z {len(hity)} ofertami!")
    except Exception as e:
        print(f"Błąd podczas wysyłania e-maila: {e}")
