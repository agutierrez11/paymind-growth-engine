import smtplib
import socket
import dns.resolver
import pandas as pd

def check_email_exists(email):
    """
    Verifica si un correo electrónico existe mediante:
    1. Sintaxis
    2. Registros DNS MX
    3. Handshake SMTP (RCPT TO) sin enviar correo real.
    """
    if "@" not in email:
        return False, "Sintaxis inválida"
    
    domain = email.split("@")[1]
    
    # 1. Obtenemos los servidores MX del dominio
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange).rstrip('.')
    except Exception as e:
        return False, f"Sin MX DNS: {str(e)}"
    
    # 2. Handshake SMTP ficticio
    try:
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('check@paymind.mx')
        code, message = server.rcpt(str(email))
        server.quit()
        
        if code == 250:
            return True, "Email Válido y Entregable"
        else:
            return False, f"Bounced (SMTP Code: {code})"
    except Exception as e:
        return False, f"Falla SMTP: {str(e)}"

if __name__ == '__main__':
    test_email = "antoniogtzjimenez@gmail.com"
    print(f"Probando verificación gratuita de: {test_email}")
    valid, reason = check_email_exists(test_email)
    print(f"Resultado: Valid={valid} | Motivo={reason}")
