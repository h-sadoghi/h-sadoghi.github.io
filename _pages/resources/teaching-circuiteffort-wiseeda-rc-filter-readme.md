---
layout: legacy_page
title: WiseEDA-like RC low-pass filter design — implementation notes
permalink: /resources/teaching-circuiteffort-wiseeda-rc-filter-readme/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://github.com/hadisadoghiyazdi1971/hadisadoghiyazdi1971.github.io/blob/master/teaching/circuiteffort/wiseEDA_rc_filter/README.md
legacy_group: Circuits and electronics
legacy_dir: ltr
lang: en
---

{% raw %}

# WiseEDA-like RC Lowpass Filter Design

### Automated RC Low‑Pass Filter Synthesis using ngspice + PSO

---

## Overview

This project is an **independent, simplified implementation inspired by the WiseEDA framework**, focused specifically on **RC low‑pass filter design**.  
The system automates the entire design flow — from user intent to optimized circuit values — using:

- **ngspice** for accurate circuit simulation
- **Particle Swarm Optimization (PSO)** for parameter optimization
- **Optional LLM-based parsing (Gemini API)** for free‑text user input

The goal is to demonstrate how modern EDA concepts (simulation + optimization + intent parsing) can be applied even to simple analog circuits.

---

## Key Features

- **Free‑text + Form-based Inputs**  
  Users can specify filter requirements either via structured forms or natural language text.

- **Topology Selection**  
  Small library of RC low‑pass topologies:

  - Equal RC cascade
  - Staggered cutoff cascade
  - Fully free R/C cascade

- **Automatic Netlist Generation**  
  Generates valid ngspice netlists based on topology and parameters.

- **Closed‑Loop Optimization**  
  Iterative optimization loop using:

  - ngspice AC simulation
  - PSO (Particle Swarm Optimization)

- **Advanced Scoring Functions**

  - Area‑to‑Target scoring
  - Weighted penalty scoring
  - Proper DC normalization

- **Real‑World Constraints**

  - E‑series resistor snapping (E12 / E24 / E48 / E96)
  - Component bounds and limits

- **Result Export**
  - Downloadable ZIP including results and configuration

---

## System Architecture

```
User Input
   │
   ├── Form Input
   └── Free Text ──► LLM (Gemini) ──► Parsed Draft
                         │
                    Parser / Validator
                         │
                   Topology Selection
                         │
                   Netlist Generation
                         │
                    ngspice Simulation
                         │
                   Scoring Function
                         │
                  PSO Optimization Loop
                         │
                    Best RC Values
```

---

## Backend Setup

### 1️⃣ Create Virtual Environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Backend Dependencies:**

- FastAPI
- Uvicorn
- Pydantic v2
- httpx
- python-dotenv

---

### 3️⃣ Install ngspice

Make sure **ngspice** is installed and available in your PATH:

```bash
ngspice -v
```

> ⚠️ ngspice is required for all simulations and optimization loops.

---

### 4️⃣ Run Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at:

```
http://localhost:8000
```

Health check:

```
GET /health
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open in browser:

```
http://localhost:5173
```

Frontend provides:

- Step‑by‑step wizard
- Topology selection
- Visualization of results

---

## LLM‑Based Free‑Text Parsing (Optional)

The system can optionally use an **LLM (Gemini API)** to convert free‑text user input into a structured JSON design draft.

### Example User Input:

> “Design a 3‑stage RC low‑pass filter with 1 kHz cutoff and at least 40 dB attenuation.”

This text is converted into a validated schema (`ParsedDraft`) used directly by the optimizer.

---

### Environment Variables (Backend)

Set the following variables:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
export GEMINI_MODEL="gemini-2.5-flash-lite"
# Optional:
# export GEMINI_API_BASE_URL="https://generativelanguage.googleapis.com/v1beta"
```

| Variable              | Description                                 |
| --------------------- | ------------------------------------------- |
| `GEMINI_API_KEY`      | **Required** – Gemini API key               |
| `GEMINI_MODEL`        | Optional – default: `gemini-2.5-flash-lite` |
| `GEMINI_API_BASE_URL` | Optional – Gemini REST endpoint             |

If the API key is **not set**, the system still works using the **local rule‑based parser** (`/parse_request`).

---

## Optimization Details

- **Optimizer:** Particle Swarm Optimization (PSO)
- **Variables:** R and C values per stage
- **Objective Functions:**
  - `area_to_target`
  - `weighted_penalty`
- **Simulation:** AC sweep using ngspice
- **Evaluation Metrics:**
  - Passband loss (Ap)
  - Stopband attenuation (As)
  - Penalized deviation at fp and fs

---

## Project Structure (Backend)

```
backend/
 ├── app/
 │   ├── main.py          # FastAPI entry point
 │   ├── routes.py        # API routes
 │   ├── engine.py        # Optimization loop
 │   ├── optimizer.py    # PSO implementation
 │   ├── scoring.py      # Cost functions
 │   ├── netlist.py      # ngspice netlist generation
 │   ├── ngspice.py      # ngspice interface
 │   ├── topologies.py   # RC topology library
 │   ├── parser.py       # Input parsing
 │   ├── llm.py          # Gemini LLM integration
 │   ├── models.py       # Pydantic data models
 │   └── e_series.py     # E‑series rounding
 └── requirements.txt
```

---

## Future Improvements

- Smarter topology suggestion using LLM
- Noise and tolerance analysis
- Support for HP / BP filters
- Monte‑Carlo simulation
- Comparison with classical Butterworth / Chebyshev designs

<!-- separate-source-code -->

[Original source-code directory](https://github.com/hadisadoghiyazdi1971/hadisadoghiyazdi1971.github.io/tree/master/teaching/circuiteffort/wiseEDA_rc_filter). The separate application is not embedded or started by this academic site.

{% endraw %}
