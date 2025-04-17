import os
import re
import email
import imaplib
from datetime import datetime, timedelta

from app.utils import strip_accents


def fetch_emails():
    imap_server = os.getenv("IMAP_SERVER")
    imap_port = int(os.getenv("IMAP_PORT"))
    
    acc_addr = os.getenv("IMAP_USER")
    acc_pwd = os.getenv("IMAP_PASSWORD")
    
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail.login(acc_addr, acc_pwd)
    mail.select("INBOX")

    fourteen_days_ago = (datetime.now() - timedelta(days=14)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(SINCE {fourteen_days_ago})')

    if status != "OK": return []
        
    results = []
    mail_ids = messages[0].split()[::-1]
    
    pattern = re.compile(r'^correcao\s*:\s*remessa\s*(\d{1,4})\b', re.IGNORECASE)

    for mail_id in mail_ids:
        _, msg_data = mail.fetch(mail_id, '(RFC822)')
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                email_message = email.message_from_bytes(response_part[1])
                subject_header = email_message["Subject"]

                if subject_header:
                    decoded_header = email.header.decode_header(subject_header)
                    subject_parts = []
                    for text, charset in decoded_header:
                        try:
                            if isinstance(text, bytes):
                                charset = charset or 'utf-8'
                                subject_parts.append(text.decode(charset, errors='replace'))
                            else:
                                subject_parts.append(text)
                        except (LookupError, UnicodeDecodeError):
                            # Fallback se o charset for inválido
                            subject_parts.append(text.decode('utf-8', errors='replace') if isinstance(text, bytes) else str(text))
                            
                    subject = ''.join(subject_parts) 
                    subject_sem_acentos = strip_accents(subject.lower())
                    match = pattern.match(subject_sem_acentos)

                    if match:
                        lote = match.group(1)
                        email_date_raw = email_message["Date"].split(' (')[0]
                        data_obj = datetime.strptime(email_date_raw, "%a, %d %b %Y %H:%M:%S %z")
                        email_date = data_obj.strftime("%Y-%m-%d %H:%M:%S")

                        results.append({
                            "code": lote,
                            "received_at": email_date
                        })

    return sorted(results, key=lambda x: x['received_at'])
