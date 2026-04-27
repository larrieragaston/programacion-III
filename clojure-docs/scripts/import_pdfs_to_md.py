#!/usr/bin/env python3
"""
Extrae texto de los PDF fuente y genera los .md (re-ejecutar tras cambios en PDF).
Uso: python3 scripts/import_pdfs_to_md.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SRC = ROOT / "source-pdfs"

RE_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

INDEX_MD = """---
layout: home

hero:
  name: Clojure
  tagline: Material del módulo sobre programación funcional en Clojure — datos, evaluación, formas especiales, funciones de orden superior y macros — con ejercicios iniciales y guía práctica. Programación III · INSPT · UTN.
  actions:
    - theme: brand
      text: Apunte teórico
      link: /apunte
    - theme: alt
      text: Ejercicios iniciales
      link: /ejercicios-iniciales
    - theme: alt
      text: Guía de ejercicios
      link: /ejercicios
---
"""

APUNTE_FRONT = """---
title: Apunte teórico — Clojure
description: Teoría de Clojure — datos, colecciones, evaluación, formas especiales, funciones y macros. Programación III, INSPT.
---

# Apunte teórico — Clojure

Este apunte acompaña **Programación III** en la carrera de **Informática** (INSPT — UTN). El objetivo no es cubrir todas las APIs de la JVM ni el ecosistema completo del lenguaje, sino ofrecer una base para **programar en Clojure** con enfoque **funcional**: datos y colecciones, evaluación de expresiones, formas especiales y macros, y la relación con la tradición **Lisp** y con ideas del **cálculo λ** (funciones como valores, reducción de expresiones, recursión y orden superior). Cuestiones como tipado estático avanzado, despliegue en producción o el universo de librerías Java quedan fuera de este apunte. El material se organiza en unidades con ejemplos de la consola **REPL** (`user=>`).

"""

EJERCICIOS_FRONT = """---
title: Guía de ejercicios — Clojure
description: Ejercicios de la guía del apunte de Clojure — Programación III, INSPT.
pageClass: ejercicios
---

"""

INICIALES_FRONT = """---
title: Ejercicios iniciales — Clojure
description: Práctica introductoria de Clojure antes de la guía del apunte — Programación III, INSPT.
pageClass: ejercicios-iniciales
---

"""


def pdftotext(pdf: Path) -> str:
    r = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        sys.exit(r.returncode)
    return r.stdout


def clean_line(s: str) -> str:
    return RE_CONTROL.sub("", s).rstrip()


def strip_boilerplate(s: str) -> str:
    lines_out: list[str] = []
    for line in s.splitlines():
        t = clean_line(line)
        if not t:
            lines_out.append("")
            continue
        tl = t.lower()
        if "creative commons" in tl or "creativecommons.org" in tl:
            continue
        if "en cualquier explotación" in tl or "obra autorizada por la licencia" in tl:
            continue
        if "uso comercial de la obra" in tl or "distribución de las cuales" in tl:
            continue
        if "las cuales se debe hacer con" in tl and len(t) < 120:
            continue
        if re.search(r"-\s*\d+\s*-\s*$", t):
            continue
        if re.match(r"^\s*Prof\. ", t):
            continue
        if t.strip() == "Clojure" and len(t) < 25:
            continue
        lines_out.append(t)
    collapsed: list[str] = []
    prev_blank = True
    for line in lines_out:
        if line == "":
            if not prev_blank:
                collapsed.append("")
            prev_blank = True
        else:
            collapsed.append(line)
            prev_blank = False
    return "\n".join(collapsed).strip()


def is_likely_unit_heading(p: str) -> bool:
    m = re.match(r"^\d+\.\s+(.+)$", p.strip())
    if not m or len(p) > 88:
        return False
    title = m.group(1)
    letters = [c for c in title if c.isalpha()]
    if len(letters) < 3:
        return False
    up = sum(1 for c in letters if c.isupper())
    return (up / len(letters)) >= 0.45


def split_numbered_subsections(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    parts = re.split(r"\s+(?=\d+\.\d+\.\s+)", text)
    return [x.strip() for x in parts if x.strip()]


_EXCEPTION_MARKERS = (
    "CompilerException",
    "ClassCastException",
    "StackOverflowError",
    "IndexOutOfBoundsException",
    "RuntimeException",
    "OutOfMemoryError",
    "ArityException",
    "IllegalArgumentException",
    "NullPointerException",
)


def _split_repl_merged_prose(chunk: str) -> list[str]:
    """Separa comentario español pegado tras una línea user=> (artefacto del PDF)."""
    chunk = chunk.strip()
    m = re.match(
        r"^(user=>[^\n]+?)(\s{3,})([A-Za-záéíóúÁÉÍÓÚÑ\u00bf\u00a1].+)$",
        chunk,
        re.DOTALL,
    )
    if m:
        code = m.group(1).strip()
        prose = m.group(3).strip()
        if not any(x in prose for x in _EXCEPTION_MARKERS) and len(prose) > 12:
            out: list[str] = [f"```clojure\n{code}\n```"]
            if re.search(r"\s+Limitaremos el estudio", prose):
                a, b = re.split(r"\s+(?=Limitaremos el estudio)", prose, maxsplit=1)
                out.append(a.strip())
                out.append(b.strip())
            else:
                out.append(prose)
            return out
    return [f"```clojure\n{chunk}\n```"]


def fence_repl_chunks(text: str) -> str:
    if "user=>" not in text:
        return text
    chunks = re.split(r"(?=\buser=>)", text)
    out: list[str] = []
    for ch in chunks:
        ch = ch.strip()
        if not ch:
            continue
        if ch.startswith("user=>"):
            parts = _split_repl_merged_prose(ch)
            for p in parts:
                if p.startswith("```"):
                    out.append(f"\n\n{p}\n\n")
                else:
                    out.append(f"\n\n{p}\n\n")
        else:
            out.append(ch)
    return "".join(out)


def polish_plain_text(s: str) -> str:
    s = re.sub(r"\s+•\s+", "\n\n- ", s)
    s = re.sub(r"(?m)^•\s+", "- ", s)
    s = maybe_wrap_wide_table(s)
    s = fence_repl_chunks(s)
    return s.strip()


def maybe_wrap_wide_table(p: str) -> str:
    if p.startswith("#"):
        return p
    if len(p) < 200:
        return p
    if p.count("  ") < 10:
        return p
    if re.search(r"\bSí\b", p) and re.search(r"\bNo\b", p) and p.count("Sí") >= 4:
        return "```text\n" + p + "\n```"
    return p


def process_piece(piece: str, *, theory: bool) -> list[str]:
    piece = piece.strip()
    if not piece:
        return []
    if theory and re.match(r"^\d+\.\s+", piece) and is_likely_unit_heading(piece):
        return [f"## {piece}"]
    if re.match(r"^\d+\.\d+\.\s+", piece):
        m = re.match(r"^(\d+\.\d+\.\s+.{3,55}?)\s+(\S.{40,})$", piece)
        if m:
            return [f"### {m.group(1).strip()}", polish_plain_text(m.group(2).strip())]
        return [f"### {piece}"]
    if re.match(r"^[a-z]\)\s", piece) and len(piece) < 240:
        return [f"#### {piece}"]
    if re.match(r"^[IVXLCDM]+\)\s", piece) and len(piece) < 240:
        return [f"#### {piece}"]
    return [polish_plain_text(piece)]


def flow_to_markdown(body: str, *, theory: bool) -> str:
    body = strip_boilerplate(body)
    paras: list[str] = []
    buf: list[str] = []
    for line in body.split("\n"):
        line = clean_line(line)
        if not line:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        stripped = line.strip()
        flush_types = (
            re.match(r"^\d+\.\d+\.\s", stripped),
            re.match(r"^[a-z]\)\s", stripped),
            re.match(r"^[IVXLCDM]+\)\s", stripped),
            re.match(r"^\d+\.\s", stripped),
        )
        if any(flush_types):
            if buf:
                paras.append(" ".join(buf))
                buf = []
            paras.append(stripped)
            continue
        if buf and (line.startswith(" ") or line.startswith("\t")):
            buf[-1] = f"{buf[-1]} {stripped}"
        else:
            buf.append(stripped)
    if buf:
        paras.append(" ".join(buf))

    md_parts: list[str] = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        for sub in split_numbered_subsections(p):
            md_parts.extend(process_piece(sub, theory=theory))

    raw = "\n\n".join(x for x in md_parts if x)
    return postprocess_clojure_markdown(raw)


def postprocess_clojure_markdown(md: str) -> str:
    md = re.sub(r"\bClojure Clojure\b", "Clojure", md, count=1)
    md = re.sub(
        r"\n\n[^\n#`]{0,120}distribución de las cuales se debe hacer con\s*\n\n",
        "\n\n",
        md,
    )
    _row = (
        r"\(λx\.Mul x x\) 3\s+"
        r"\(\(lambda \(x\) \(\* x x\)\) 3\)\s+"
        r"\(\(fn \[x\] \(\* x x\)\) 3\)"
    )
    _triple_html = (
        '<div class="lambda-lisp-clojure-compare-wrap">\n\n'
        '<table class="lambda-lisp-clojure-compare">\n'
        "<thead>\n<tr>\n"
        '<th scope="col">Cálculo Lambda</th>\n'
        '<th scope="col">Lisp</th>\n'
        '<th scope="col">Clojure</th>\n'
        "</tr>\n</thead>\n"
        "<tbody>\n<tr>\n"
        "<td><code>(λx.Mul x x) 3</code></td>\n"
        "<td><code>((lambda (x) (* x x)) 3)</code></td>\n"
        "<td><code>((fn [x] (* x x)) 3)</code></td>\n"
        "</tr>\n</tbody>\n</table>\n\n"
        "</div>"
    )
    md = re.sub(
        rf"(Cálculo Lambda \(con combinadores\)\s+Lisp\s+Clojure\s+)({_row})\s+(Algunas características)",
        _triple_html + r"\n\n\3",
        md,
        count=1,
    )
    # Si ya estaba como bloque ```text``` (regeneración parcial / copia vieja)
    md = re.sub(
        r"```text\nCálculo Lambda \(con combinadores\)\s+Lisp\s+Clojure.*?\(λx\.Mul x x\).*?\(\(fn \[x\].*?\)\)\n```",
        _triple_html,
        md,
        count=1,
        flags=re.DOTALL,
    )
    _old_pipe = (
        "| Cálculo Lambda (con combinadores) | Lisp | Clojure |\n"
        "| --- | --- | --- |\n"
        "| `(λx.Mul x x) 3` | `((lambda (x) (* x x)) 3)` | `((fn [x] (* x x)) 3)` |"
    )
    if _old_pipe in md:
        md = md.replace(_old_pipe, _triple_html, 1)
    return md


def split_apunte(full: str) -> tuple[str, str]:
    m = re.search(r"(?m)^\s{10,}Ejercicios\s*$", full)
    if not m:
        raise RuntimeError("No se encontró la sección 'Ejercicios' en el apunte PDF.")
    theory = full[: m.start()].strip()
    exercises = full[m.start() :].strip()
    return theory, exercises


def ejercicios_to_markdown(block: str, title: str) -> str:
    block = strip_boilerplate(block)
    lines = [ln.rstrip() for ln in block.splitlines()]
    if lines and lines[0].strip() == "Ejercicios":
        lines = lines[1:]
    body = flow_to_markdown(chr(10).join(lines), theory=False)
    return f"{EJERCICIOS_FRONT}# {title}\n\n{body}"


def iniciales_to_markdown(text: str) -> str:
    t = strip_boilerplate(text)
    lines = [ln for ln in t.splitlines() if ln.strip()]
    title = "Ejercicios iniciales"
    body_lines: list[str] = []
    for ln in lines:
        if "Ejercicios iniciales" in ln:
            title = "Ejercicios iniciales"
            continue
        body_lines.append(ln)
    body = flow_to_markdown("\n".join(body_lines), theory=False)
    return f"{INICIALES_FRONT}# {title}\n\n{body}"


def main() -> None:
    apunte_pdf = SRC / "Clojure - Apunte.pdf"
    inic_pdf = SRC / "Clojure - Ejercicios iniciales.pdf"
    if not apunte_pdf.exists() or not inic_pdf.exists():
        print("Faltan PDF en source-pdfs/", file=sys.stderr)
        sys.exit(1)

    full_apunte = pdftotext(apunte_pdf)
    theory, ex_apunte = split_apunte(full_apunte)

    apunte_body = flow_to_markdown(theory, theory=True).lstrip()
    if not apunte_body.startswith("## Introducción"):
        apunte_body = f"## Introducción\n\n{apunte_body}"
    (DOCS / "apunte.md").write_text(f"{APUNTE_FRONT}{apunte_body}", encoding="utf-8")

    ej_md = ejercicios_to_markdown(ex_apunte, "Guía de ejercicios")
    (DOCS / "ejercicios.md").write_text(ej_md, encoding="utf-8")

    inic_text = pdftotext(inic_pdf)
    (DOCS / "ejercicios-iniciales.md").write_text(iniciales_to_markdown(inic_text), encoding="utf-8")

    (DOCS / "index.md").write_text(INDEX_MD, encoding="utf-8")
    print("OK:", DOCS / "index.md", DOCS / "ejercicios-iniciales.md", DOCS / "apunte.md", DOCS / "ejercicios.md")


if __name__ == "__main__":
    main()
