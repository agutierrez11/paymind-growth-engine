import csv
import os

path = r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\paymind-growth-engine\data\TOKU_TIER_A_PRIORIDAD_INMEDIATA.csv"
with open(path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    print("=== TOP 15 CUENTAS TIER A (SPEED-TO-SELL: 3 A 7 DIAS) ===")
    for i, r in enumerate(reader):
        if i < 15:
            print(f"{i+1:02d}. {r['Entidad']:<25} | {r['Categoria']:<7} | Score: {r['TMPI_Score']} | Sede: {r['Sede']:<16} | {r['Dominio']}")
