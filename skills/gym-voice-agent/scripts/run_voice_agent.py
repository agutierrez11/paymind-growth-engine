#!/usr/bin/env python3
"""
Production Runner for Gym Voice Agent (CPS Gym)
Inspired by Shubham Saboo's Customer Support Voice Agent architecture.
Conversational reception, objection resolution, lead capture, and voice synthesis.
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime

# Base de conocimiento operativo de CPS Gym
CPS_KNOWLEDGE = {
    "plans": {
        "basico": "$599 MXN mensuales (Acceso ilimitado a pesas y cardio)",
        "total_black": "$899 MXN mensuales (Pesas, cardio, todas las clases grupales, lockers y regaderas)",
        "trimestral": "$1,999 MXN pago único por 3 meses (Ahorras 15%)",
        "day_pass": "$99 MXN por visita"
    },
    "schedules": {
        "semana": "Lunes a Viernes de 06:00 AM a 10:30 PM",
        "sabado": "Sábados de 07:00 AM a 06:00 PM",
        "domingo": "Domingos de 08:00 AM a 02:00 PM"
    },
    "classes": {
        "spinning": "07:00 AM y 07:00 PM",
        "crossfit": "08:00 AM y 06:30 PM",
        "box": "08:00 PM"
    }
}

def resolve_cps_intent(query):
    """Clasifica la intención del usuario y redacta la respuesta en lenguaje natural."""
    q = query.lower()
    
    # 1. Detección de datos de lead (registro)
    phone_match = re.search(r'\b(?:\+?52\s*)?(?:\(?\d{2,3}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}\b', query)
    name_match = re.search(r'(?:me llamo|soy|mi nombre es)\s+([A-Za-zÁÉÍÓÚáéíóúñ]+)', query, re.IGNORECASE)
    
    lead_info = {}
    if phone_match or name_match:
        lead_info["captured"] = True
        if name_match:
            lead_info["name"] = name_match.group(1).capitalize()
        if phone_match:
            lead_info["phone"] = phone_match.group(0).strip()
            
    # 2. Respuestas por intención
    if any(k in q for k in ["precio", "cuesta", "mensualidad", "costo", "plan", "cuanto"]):
        response = (
            "¡Hola! En CPS Gym tenemos dos planes principales: el Plan Básico en $599 pesos al mes con pesas y cardio, "
            "y el Plan Total Black en $899 pesos que te incluye todas las clases de spinning, cross training y box, además de lockers y regaderas. "
            "Si vienes con tu credencial de estudiante te damos un 15% de descuento adicional. ¿Te gustaría agendar una clase muestra gratis hoy?"
        )
        intent = "pricing"
        
    elif any(k in q for k in ["horario", "abren", "cierran", "hora", "domingo", "sabado"]):
        response = (
            f"Abrimos de lunes a viernes desde las 6:00 de la mañana hasta las 10:30 de la noche. "
            f"Los sábados estamos de 7:00 AM a 6:00 PM y los domingos de 8:00 AM a 2:00 PM. "
            f"¿A qué hora te acomoda entrenar para esperarte con el staff listo?"
        )
        intent = "schedule"
        
    elif any(k in q for k in ["clase", "spinning", "crossfit", "box", "funcional"]):
        response = (
            "Tenemos clases en dos turnos: Spinning a las 7:00 AM y 7:00 PM, Cross Training a las 8:00 AM y 6:30 PM, "
            "y Box recreativo a las 8:00 de la noche. Todas están incluidas en el Plan Total Black. ¿Cuál te llama más la atención para apartar tu lugar?"
        )
        intent = "classes"
        
    elif any(k in q for k in ["caro", "descuento", "mucho dinero", "rebaja", "esquina"]):
        response = (
            "Te entiendo totalmente, pero fíjate: en CPS Gym no solo pagas por las máquinas, sino por equipo de alta gama con mantenimiento continuo, "
            "entrenadores de piso certificados que sí te corrigen la técnica y cero filas para usar los aparatos. "
            "Ven hoy a probar un día por nuestra cuenta, siente la diferencia y si no te convence, no pagas nada. ¿A qué hora te esperamos?"
        )
        intent = "objection_price"
        
    elif any(k in q for k in ["cancelar", "baja", "pausar", "tiempo"]):
        response = (
            "En CPS Gym no tenemos plazos forzosos con tarjeta ni letras chiquitas. Si necesitas pausar tu membresía por trabajo o viaje, "
            "te congelamos los días restantes sin penalización alguna. Pasa con recepción o mándanos tu número de socio para apoyarte de inmediato."
        )
        intent = "cancellation"
        
    elif lead_info.get("captured"):
        nombre = lead_info.get("name", "Campeón")
        response = (
            f"¡Excelente, {nombre}! Ya registré tus datos. Nuestro equipo te va a mandar tu pase de acceso digital "
            f"por WhatsApp en unos momentos para que entrenes hoy mismo en CPS Gym. ¡Nos vemos en el piso!"
        )
        intent = "lead_registered"
        
    else:
        response = (
            "¡Bienvenido a CPS Gym! Con gusto te apoyo con precios de membresías, horarios, clases de spinning y box, "
            "o registro para tu primera clase muestra. ¿Qué información te gustaría conocer?"
        )
        intent = "general_faq"
        
    return response, intent, lead_info

def generate_voice_file(text, output_path, persona="recepcion_amable"):
    """Sintetiza la respuesta hablada usando VoiceStudio o SAPI5."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        if persona == "coach_motivacional":
            engine.setProperty('rate', int(rate * 1.15))
        else:
            engine.setProperty('rate', int(rate * 0.98))
            
        voices = engine.getProperty('voices')
        for v in voices:
            if "spanish" in v.name.lower() or "sabina" in v.name.lower() or "helena" in v.name.lower():
                engine.setProperty('voice', v.id)
                break
                
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return True
    except Exception:
        # Respaldo simple
        return False

def main():
    parser = argparse.ArgumentParser(description="Gym Voice Agent (CPS Gym) - Production Runner")
    parser.add_argument("--query", required=True, help="Mensaje o pregunta del socio / prospecto")
    parser.add_argument("--persona", choices=["recepcion_amable", "coach_motivacional", "cobranza_firme"], default="recepcion_amable", help="Tono de voz")
    parser.add_argument("--generate-audio", action="store_true", help="Generar archivo de audio WAV")
    parser.add_argument("--output-audio", default="output_gym.wav", help="Ruta de guardado del audio")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Formato de salida")
    
    args = parser.parse_args()
    
    response_text, intent, lead_info = resolve_cps_intent(args.query)
    audio_generated = False
    
    if args.generate_audio:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_audio)) if os.path.dirname(args.output_audio) else ".", exist_ok=True)
        audio_generated = generate_voice_file(response_text, args.output_audio, args.persona)
        
    result = {
        "timestamp": datetime.now().isoformat(),
        "query": args.query,
        "intent": intent,
        "persona": args.persona,
        "lead_captured": lead_info,
        "agent_response": response_text,
        "audio_file": args.output_audio if audio_generated else None
    }
    
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n" + "="*60)
        print(f"🏋️ CPS GYM VOICE AGENT | Intención: [{intent.upper()}] | Tono: [{args.persona}]")
        if lead_info.get("captured"):
            print(f"  [✓] Lead detectado: {lead_info}")
        print("\n🗣️ RESPUESTA DEL AGENTE:")
        print(f"\"{response_text}\"")
        if audio_generated:
            print(f"\n🎧 Archivo de voz generado: {args.output_audio}")
        print("="*60)

if __name__ == "__main__":
    main()
