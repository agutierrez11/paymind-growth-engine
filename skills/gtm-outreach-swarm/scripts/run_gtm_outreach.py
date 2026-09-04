#!/usr/bin/env python3
"""
Production Multi-Agent Runner for GTM Outreach Swarm
Inspired by Shubham Saboo's GTM Outreach Agent.
Includes Target Profiler, Copywriter, and Anti-Spam Deliverability Auditor.
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime

# Blacklisted spam trigger keywords in B2B corporate filters
SPAM_TRIGGER_WORDS = [
    "100%", "gratis", "free", "urgente", "oferta", "millones", "garantizado",
    "sin riesgo", "dinero facil", "actua ya", "haz clic aqui", "premio",
    "inversion milagrosa", "descuento exclusivo", "compre ya"
]

def generate_subject_lines(company, target_role, pain_point):
    """Genera 3 variantes de asunto con alta probabilidad de apertura."""
    clean_role = target_role.split()[0] if target_role else "Director"
    return [
        f"Operación de cobranza en {company} / {clean_role}",
        f"Mitigación de fricción operativa en {company}",
        f"Pregunta breve sobre rieles de dispersión ({company})"
    ]

def draft_email_body(company, target_role, pain_point, value_prop, style="Consultative"):
    """Redacta el cuerpo de correo B2B en 120-150 palabras según el estilo elegido."""
    greeting = f"Estimado/a {target_role}:"
    
    if style == "Consultative":
        body = (
            f"{greeting}\n\n"
            f"Le escribo con conocimiento directo de los retos en la infraestructura de {company}.\n\n"
            f"Observamos que muchas entidades del sector enfrentan fricciones críticas debido a: {pain_point}. "
            f"Cuando esto ocurre, el impacto directo se traduce en costos operativos elevados y desajustes de conciliación.\n\n"
            f"Nuestra propuesta se centra en {value_prop}, permitiendo resolver la fricción desde el riel tecnológico "
            f"sin alterar su flujo diario ni sobrecargar a sus equipos.\n\n"
            f"¿Tendría 15 minutos este jueves a las 11:00 AM para una breve llamada técnica exploratoria?\n\n"
            f"Saludos cordiales,\nAntonio Gutiérrez"
        )
    elif style == "Cold":
        body = (
            f"{greeting}\n\n"
            f"Al grano: sabemos que en {company} resolver {pain_point} es una prioridad para proteger el margen neto.\n\n"
            f"Implementamos {value_prop}, logrando un rescate de hasta el 30% en transacciones o mensualidades no recuperadas en el primer intento.\n\n"
            f"¿Tendría 10 minutos esta semana para revisar los números exactos?\n\n"
            f"Saludos cordiales,\nAntonio Gutiérrez"
        )
    else: # Professional / Casual
        body = (
            f"{greeting}\n\n"
            f"Espero que se encuentre excelente. En el marco operativo de {company}, un reto recurrente que atendemos es: {pain_point}.\n\n"
            f"A través de {value_prop}, habilitamos una arquitectura automatizada que previene caídas de servicio y optimiza la tasa de éxito.\n\n"
            f"¿Le parecería bien una llamada remota de 15 minutos este jueves o viernes para compartirle el benchmark del sector?\n\n"
            f"Atentamente,\nAntonio Gutiérrez"
        )
    return body

def audit_deliverability(subject, body):
    """Audita el correo contra filtros de spam corporativos."""
    findings = []
    score = 100
    combined_text = f"{subject} {body}".lower()
    
    # 1. Chequeo de palabras spam
    detected_spam_words = [w for w in SPAM_TRIGGER_WORDS if w in combined_text]
    if detected_spam_words:
        score -= (len(detected_spam_words) * 15)
        findings.append(f"Palabras detectadas en lista de spam: {', '.join(detected_spam_words)}")
        
    # 2. Conteo de palabras
    words = body.split()
    word_count = len(words)
    if word_count < 60:
        score -= 10
        findings.append(f"Cuerpo muy corto ({word_count} palabras). Podría parecer mensaje genérico.")
    elif word_count > 180:
        score -= 15
        findings.append(f"Cuerpo muy largo ({word_count} palabras). Los C-levels no leen más de 150 palabras.")
        
    # 3. Longitud de asunto
    if len(subject) > 55:
        score -= 10
        findings.append(f"Asunto demasiado largo ({len(subject)} caracteres). Se truncará en móviles.")
        
    # 4. Signos de exclamación excesivos
    exclamations = combined_text.count("!")
    if exclamations > 2:
        score -= 15
        findings.append(f"Exceso de signos de exclamación ({exclamations}). Activa filtros de urgencia falsa.")
        
    score = max(0, min(100, score))
    
    return {
        "deliverability_score": score,
        "word_count": word_count,
        "subject_length": len(subject),
        "status": "PASS (Excelente)" if score >= 85 else ("WARNING (Requiere Ajustes)" if score >= 65 else "FAIL (Alto Riesgo Spam)"),
        "findings": findings if findings else ["Cumple con todos los estándares de entregabilidad corporativa."]
    }

def main():
    parser = argparse.ArgumentParser(description="GTM Outreach Swarm - Multi-Agent Personalization & Deliverability Runner")
    parser.add_argument("--company", help="Nombre de la empresa objetivo")
    parser.add_argument("--target-role", default="CFO / Director de Finanzas", help="Cargo del decisor")
    parser.add_argument("--pain-point", help="Dolor operativo o regulatorio detectado")
    parser.add_argument("--value-prop", help="Propuesta de valor concreta")
    parser.add_argument("--style", choices=["Consultative", "Cold", "Professional", "Casual"], default="Consultative", help="Estilo de redacción")
    parser.add_argument("--audit-only", action="store_true", help="Solo auditar un copy provisto en --subject y --body")
    parser.add_argument("--subject", help="Asunto (usado con --audit-only)")
    parser.add_argument("--body", help="Cuerpo (usado con --audit-only)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Formato de salida")
    parser.add_argument("--output-file", help="Ruta de archivo para guardar el reporte")
    
    args = parser.parse_args()
    
    if args.audit_only:
        if not args.subject or not args.body:
            parser.error("--audit-only requiere --subject y --body")
        audit = audit_deliverability(args.subject, args.body)
        print("\n" + "="*50)
        print(f"📊 AUDITORÍA ANTI-SPAM: Puntuación {audit['deliverability_score']}/100 ({audit['status']})")
        print(f"- Conteo de palabras: {audit['word_count']}")
        print(f"- Hallazgos:")
        for f in audit["findings"]:
            print(f"  * {f}")
        print("="*50)
        return
        
    if not args.company or not args.pain-point if hasattr(args, "pain-point") else (not args.company or not args.pain_point):
        parser.error("Se requiere --company y --pain-point para generar el outreach.")
        
    p_point = getattr(args, "pain_point", "")
    v_prop = getattr(args, "value_prop", "") or "infraestructura tecnológica multi-riel automatizada"
    
    subjects = generate_subject_lines(args.company, args.target_role, p_point)
    body = draft_email_body(args.company, args.target_role, p_point, v_prop, args.style)
    audit = audit_deliverability(subjects[0], body)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "company": args.company,
        "target_role": args.target_role,
        "style": args.style,
        "recommended_subjects": subjects,
        "email_body": body,
        "audit": audit
    }
    
    if args.format == "json":
        output = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        output = f"# 🎯 GTM OUTREACH BRIEF: {args.company} ({args.target_role})\n\n"
        output += f"> **Fecha:** {report['timestamp']} | **Estilo:** {args.style} | **Entregabilidad:** {audit['deliverability_score']}/100 ({audit['status']})\n\n"
        output += "## 📩 Asuntos Recomendados (Testing A/B/C)\n"
        for i, s in enumerate(subjects, 1):
            output += f"{i}. `{s}`\n"
            
        output += "\n## 📝 Copy Quirúrgico Generado\n"
        output += f"```text\n{body}\n```\n\n"
        
        output += "## 🛡️ Auditoría Anti-Spam y Entregabilidad\n"
        output += f"- **Score:** {audit['deliverability_score']}/100\n"
        output += f"- **Extensión:** {audit['word_count']} palabras (Óptimo para C-Level: 100-150)\n"
        output += f"- **Dictamen:** {audit['status']}\n"
        for f in audit["findings"]:
            output += f"  * {f}\n"

    print("\n" + "="*60)
    print(output)
    print("="*60)
    
    if args.output_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_file)) if os.path.dirname(args.output_file) else ".", exist_ok=True)
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[✓] GTM Outreach guardado en: {args.output_file}")

if __name__ == "__main__":
    main()
