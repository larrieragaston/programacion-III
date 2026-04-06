#!/usr/bin/env python3
"""Strip PDF boilerplate, split apunte vs guía de ejercicios, normalize section headings."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
APUNTE = DOCS / "apunte.md"
EJERCICIOS = DOCS / "ejercicios.md"
EJ_AD = DOCS / "ejercicios-adicionales.md"

CC_BLOCK = re.compile(
    r"Esta obra está bajo una Licencia Creative Commons.*?"
    r"https://creativecommons\.org/licenses/by-nc-sa/4\.0/deed\.es\s*",
    re.DOTALL,
)
PAGE_HEADER = re.compile(r"## Página \d+\s*\n", re.MULTILINE)
PROF_BLOCK = re.compile(
    r"Prof\. Lic\. Carlos E\. Cimino.*?\nProf\. Dr\. Diego Corsi.*?\nProf\. Gastón Larriera.*?\n\n",
    re.DOTALL,
)
PAGE_NUM = re.compile(r"^-\d+-$\n?", re.MULTILINE)

SECTION_REPLACEMENTS: list[tuple[str, str]] = [
    (r"^1\. PROGRAMAS COMO EXPRESIONES\s*$", "## 1. Programas como expresiones"),
    (r"^2\. SINTAXIS DEL CÁLCULO LAMBDA\s*$", "## 2. Sintaxis del cálculo lambda"),
    (r"^2\.1\. Convenciones\s*$", "### 2.1 Convenciones"),
    (r"^3\. VARIABLES LIBRES Y LIGADAS\s*$", "## 3. Variables libres y ligadas"),
    (r"^4\. REGLAS DE CONVERSIÓN\s*$", "## 4. Reglas de conversión"),
    (r"^4\.1\. Regla de conversión Alfa \(α\)\s*$", "### 4.1 Regla de conversión Alfa (α)"),
    (r"^4\.2\. Regla de conversión Beta \(β\)\s*$", "### 4.2 Regla de conversión Beta (β)"),
    (r"^4\.3\. Regla de conversión Eta \(η\)\s*$", "### 4.3 Regla de conversión Eta (η)"),
    (r"^5\. ESTRATEGIAS DE REDUCCIÓN\s*$", "## 5. Estrategias de reducción"),
    (r"^5\.1\. Call-by-name\s*$", "### 5.1 Call-by-name"),
    (r"^5\.2\. Orden normal\s*$", "### 5.2 Orden normal"),
    (r"^5\.3\. Call-by-value\s*$", "### 5.3 Call-by-value"),
    (r"^5\.4\. Orden aplicativo\s*$", "### 5.4 Orden aplicativo"),
    (r"^5\.5\. Comparación de estrategias\s*$", "### 5.5 Comparación de estrategias"),
    (r"^6\. REPRESENTACIÓN DE VALORES DE VERDAD\. FUNCIONES LÓGICAS\s*$", "## 6. Representación de valores de verdad · Funciones lógicas"),
    (r"^7\. REPRESENTACIÓN DE NÚMEROS\. FUNCIONES NUMÉRICAS Y RELACIONALES\s*$", "## 7. Representación de números · Funciones numéricas y relacionales"),
    (r"^8\. COMBINADORES\s*$", "## 8. Combinadores"),
    (r"^9\. PARES Y LISTAS\s*$", "## 9. Pares y listas"),
]


def strip_boilerplate(s: str) -> str:
    s = PAGE_HEADER.sub("\n", s)
    s = PROF_BLOCK.sub("", s)
    s = PAGE_NUM.sub("", s)
    s = CC_BLOCK.sub("", s)
    return s


def apply_section_headings(s: str) -> str:
    for pat, repl in SECTION_REPLACEMENTS:
        s = re.sub(pat, repl, s, flags=re.MULTILINE)
    return s


def strip_frontmatter(s: str) -> str:
    if s.startswith("---"):
        parts = s.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip()
    return s


def split_ejercicios(text: str) -> tuple[str, str]:
    marker = "\nEjercicios\n\nhttp://"
    if marker not in text:
        return text, ""
    theory, tail = text.split(marker, 1)
    return theory.rstrip(), "http://" + tail.strip()


def main() -> None:
    raw = APUNTE.read_text(encoding="utf-8")
    raw = strip_frontmatter(raw)
    raw = re.sub(r"^# Apunte — Cálculo λ\s*\n*", "", raw)
    raw = re.sub(r"^<div class=\"doc-print-header\"[\s\S]*?</div>\s*\n*", "", raw)

    theory, ej_tail = split_ejercicios(raw)
    theory = strip_boilerplate(theory)
    theory = apply_section_headings(theory)
    theory = re.sub(r"\n{3,}", "\n\n", theory).strip()

    header = '''---
title: Apunte — Cálculo λ
description: Teoría de cálculo lambda (sintaxis, semántica, combinadores).
---

<div class="doc-print-header">
  <div class="doc-print-header__row">
    <span class="doc-print-header__utn">Universidad Tecnológica Nacional</span>
    <span class="doc-print-header__sep">·</span>
    <span class="doc-print-header__inspt">INSPT</span>
  </div>
  <div class="doc-print-header__course">Programación III · Ciclo lectivo 2026</div>
  <div class="doc-print-header__doc-title">Cálculo lambda (λ-calculus)</div>
  <div class="doc-print-header__author">Prof. Gastón A. Larriera</div>
</div>

'''

    APUNTE.write_text(header + "# Apunte — Cálculo λ\n\n" + theory + "\n", encoding="utf-8")

    if ej_tail:
        urls = re.findall(r"https?://[^\s)]+", ej_tail)
        body = ej_tail
        for u in urls:
            body = body.replace(u, "")
        body = strip_boilerplate(body)
        body = apply_section_headings(body)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        url_block = "\n".join(f"- {u}" for u in urls)

        EJERCICIOS.write_text(
            """---
title: Guía de ejercicios — Cálculo λ
description: Ejercicios de la guía del apunte e intérpretes en línea.
---

<div class="doc-print-header doc-print-header--compact">
  <div class="doc-print-header__row">
    <span class="doc-print-header__utn">Universidad Tecnológica Nacional · INSPT</span>
  </div>
  <div class="doc-print-header__course">Programación III · 2026</div>
  <div class="doc-print-header__doc-title">Guía de ejercicios — Cálculo λ</div>
  <div class="doc-print-header__author">Prof. Gastón A. Larriera</div>
</div>

# Guía de ejercicios

## Intérpretes en línea

"""
            + url_block
            + "\n\n## Enunciados\n\n"
            + body
            + "\n",
            encoding="utf-8",
        )

    if EJ_AD.exists():
        ad = EJ_AD.read_text(encoding="utf-8")
        ad = strip_frontmatter(ad)
        ad = re.sub(
            r"^# Ejercicios adicionales[^\n]*\n+",
            "",
            ad,
        )
        ad = strip_boilerplate(ad)
        ad_h = """---
title: Ejercicios adicionales — Cálculo λ
---

<div class="doc-print-header doc-print-header--compact">
  <div class="doc-print-header__row">
    <span class="doc-print-header__utn">Universidad Tecnológica Nacional · INSPT</span>
  </div>
  <div class="doc-print-header__course">Programación III · 2026</div>
  <div class="doc-print-header__doc-title">Ejercicios adicionales — Cálculo λ</div>
  <div class="doc-print-header__author">Prof. Gastón A. Larriera</div>
</div>

# Ejercicios adicionales

"""
        EJ_AD.write_text(ad_h + ad.lstrip(), encoding="utf-8")

    print("Updated", APUNTE, "and", EJERCICIOS if ej_tail else "(no split)")


if __name__ == "__main__":
    main()
