---
layout: legacy_page
title: Street-lighting control with AMI meter clocks
permalink: /projects/legacy-project-2/
description: Research and engineering project — archived description
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/projects/project-2/
legacy_group: Engineering projects
importance: 21
category: work
img: assets/img/legacy/astronomicalclocks-e0acda7ee0.png
legacy_dir: ltr
lang: en
---

{% raw %}
<picture><source type="image/webp" srcset="/assets/img/legacy/astronomicalclocks-e0acda7ee0-480.webp 480w, /assets/img/legacy/astronomicalclocks-e0acda7ee0-800.webp 800w, /assets/img/legacy/astronomicalclocks-e0acda7ee0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/astronomicalclocks-e0acda7ee0.png" alt="astronomicalclocks1"></picture>

# Street lighting control system — using the internal clock of AMI meters to replace conventional astronomical clocks

**Cooperation:** <a href="https://research.meedc.ir/" target="_blank"><strong>Research Office, Mashhad Electricity Distribution Company</strong></a>

---

## Abstract

This report proposes a practical industrial solution to replace standalone astronomical clocks in street lighting controllers by using the internal clock of AMI (Advanced Metering Infrastructure) smart meters installed in street distribution panels. Time and date are read from the meter via the RS-485 port using the DLMS/COSEM protocol (Low Security Level — LLS). This reduces maintenance (battery replacement), avoids clock drift and noise-induced errors, and leverages existing infrastructure for more reliable on/off scheduling.

---

## 1. Problem statement

**Problems observed with conventional astronomical clocks:**

- Internal battery failure causing clock resets and incorrect sunrise/sunset calculations.
- Susceptibility to electrical noise and interference that corrupts timekeeping.
- Result: street lamps ON during daylight or OFF after dark → energy waste and safety issues.

<div markdown="1">
  <div markdown="1">
    <picture><source type="image/webp" srcset="/assets/img/legacy/nightime-6035ca9c98-480.webp 480w, /assets/img/legacy/nightime-6035ca9c98-800.webp 800w, /assets/img/legacy/nightime-6035ca9c98-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/nightime-6035ca9c98.png" alt="NighTime"></picture>
  </div>
  <div markdown="1">
    <picture><source type="image/webp" srcset="/assets/img/legacy/daytime-3003256089-480.webp 480w, /assets/img/legacy/daytime-3003256089-800.webp 800w, /assets/img/legacy/daytime-3003256089-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/daytime-3003256089.png" alt="DayTime"></picture>
  </div>
</div>

**Desired behaviour:** accurate automatic switching aligned to true local sunrise/sunset, with low maintenance and high reliability.

---

## 2. Proposed solution (high level)

Use the **internal real-time clock of AMI smart meters** (already present in street distribution panels) as the authoritative time source for the lighting controller. The lighting controller polls the meter over **RS-485** using **DLMS/COSEM** (LLS) to read the meter clock (COSEM Clock object). The controller then applies local sunrise/sunset logic (or a schedule) to actuate street lights.

---

## 3. Why this is viable — standards & technologies

- AMI provides two-way communication and time-synchronized data which utilities already use for operations. See an AMI overview:  
  <a href="https://www.ibm.com/think/topics/advanced-metering-infrastructure" target="_blank"><strong>What is Advanced Metering Infrastructure (IBM)</strong></a>

- DLMS/COSEM is the international, field-proven standard suite for smart meter data models and exchanges (adopted as IEC 62056). See DLMS UA:  
  <a href="https://www.dlms.com/" target="_blank"><strong>DLMS User Association (DLMS UA)</strong></a>

- IEC 62056 defines the DLMS/COSEM suite (official IEC publication):  
  <a href="https://webstore.iec.ch/en/publication/71751" target="_blank"><strong>IEC 62056 DLMS/COSEM — IEC webstore</strong></a>

- The COSEM object model includes a **Clock** (Class ID 8) object which provides date/time values retrievable by clients (see implementation notes):  
  <a href="https://www.gurux.fi/DLMSIntro" target="_blank"><strong>Gurux DLMS/COSEM introduction (Clock class reference)</strong></a>

- RS-485 is a robust industrial serial physical layer commonly used to connect meters and controllers in multidrop topologies:  
  <a href="https://en.wikipedia.org/wiki/RS-485" target="_blank"><strong>RS-485 overview (Wikipedia)</strong></a>  
  Technical design guidance (application note):  
  <a href="https://www.ti.com/lit/pdf/slla272" target="_blank"><strong>RS-485 design guide (TI application note, PDF)</strong></a>

---

## 4. Protocol & security considerations

- **DLMS/COSEM security modes:** Lowest/LLS/High. For reading a meter's clock in low-risk contexts, utilities commonly use LLS (password/basic). However, LLS provides minimal protection and should be assessed with corporate cyber policies. See discussion of DLMS security basics:  
  <a href="https://icube.ch/Security/security1.html" target="_blank"><strong>DLMS security basics (overview)</strong></a>

- **Best practice:**
  - Prefer authenticated sessions where possible.
  - Validate time values (e.g., monotonic checks, cross-check with a secondary source occasionally).
  - Maintain logging and tamper-detection (e.g., sudden large time jumps should trigger fallbacks).
  - Use LLS only if organizational risk assessment permits it for time reads; otherwise use higher DLMS security (HLS).

---

## 5. System architecture (recommended)

The system architecture consists of three main components:

- AMI Smart Meter (Clock): Provides the internal time.

- Lighting Controller: Reads the clock from the meter via RS-485 using DLMS/COSEM protocol.

- Switch/Relay Unit: The controller actuates this to turn street lights ON/OFF.

flowchart
A[AMI Smart Meter (Clock)] -- RS-485 / DLMS-COSEM --> B[Lighting Controller]
B --> C[Switch / Relay / Contactor]
C --> D[Street Lights]

<picture><source type="image/webp" srcset="/assets/img/legacy/flowchart-ami1-9e87439322-480.webp 480w, /assets/img/legacy/flowchart-ami1-9e87439322-800.webp 800w, /assets/img/legacy/flowchart-ami1-9e87439322-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/flowchart-ami1-9e87439322.png" alt="Flowchart_AMI11"></picture>

**Key components**

- Meter: exposes COSEM Clock object via DLMS/COSEM (LN or SN referencing).
- Lighting controller: small embedded controller or PLC with RS-485 interface and DLMS/COSEM client stack.
- Communication: twisted-pair RS-485 cable with proper termination, biasing resistors and surge protection.
- Fallback: maintain local astronomical schedule (on-board astronomical clock) to use when meter time is unavailable or invalid.

---

## 6. Implementation steps (practical)

1. **Inventory & compatibility check:** identify meter models in the target panels and confirm DLMS/COSEM support and accessibility via the meter RS-485 port.
2. **Obtain DLMS object addresses:** find the meter's Clock logical name / attribute index (Clock Class ID = 8). Test with a DLMS client tool (e.g., Gurux tools).
3. **Develop controller client:** implement a lightweight DLMS/COSEM client supporting LN or SN referencing and RS-485 physical layer. Poll the clock at a safe interval (e.g., every 1–5 minutes).
4. **Time validation logic:** implement sanity checks (e.g., leap checks, drift thresholds, monotonic time), and a fallback to local astronomical calculation if invalid.
5. **Security & operations:** choose appropriate DLMS security level; maintain password storage and audit logs; test for failure modes and cyber-hardening.
6. **Pilot deployment:** run a small pilot in a subset of panels; log results (uptime, false ON/OFF events, latency), tune polling interval and validation thresholds.
7. **Roll-out & monitoring:** deploy widely if pilot is successful; include remote monitoring dashboards.

---

## 7. Advantages & limitations

**Advantages**

- Uses existing meter infrastructure — reduces extra hardware and maintenance (no battery swaps).
- Potentially more accurate and synchronized time (especially if meters are NTP/GPS-synced at the head-end).
- Centralized management possibility through head-end systems.

<div markdown="1">
  <div markdown="1">
    <picture><source type="image/webp" srcset="/assets/img/legacy/hardware1-fbb4cfb203-480.webp 480w, /assets/img/legacy/hardware1-fbb4cfb203-800.webp 800w, /assets/img/legacy/hardware1-fbb4cfb203-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/hardware1-fbb4cfb203.png" alt="Hardware 1"></picture>
  </div>
  <div markdown="1">
    <picture><source type="image/webp" srcset="/assets/img/legacy/hardware2-35226fa0c3-480.webp 480w, /assets/img/legacy/hardware2-35226fa0c3-800.webp 800w, /assets/img/legacy/hardware2-35226fa0c3-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/hardware2-35226fa0c3.png" alt="Hardware 2"></picture>
  </div>
  <div markdown="1">
    <picture><source type="image/webp" srcset="/assets/img/legacy/hardware3-1419982e03-480.webp 480w, /assets/img/legacy/hardware3-1419982e03-800.webp 800w, /assets/img/legacy/hardware3-1419982e03-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/hardware3-1419982e03.png" alt="Hardware 3"></picture>
  </div>
</div>

**Limitations & risks**

- If meter clock is itself wrong (misconfiguration or attack), lights may misbehave — require validation/fallback.
- RS-485 cabling practices must be robust (termination, surge protection) to avoid noise-induced errors.
- DLMS LLS has weak security — evaluate against organizational policy.

---

## Installation of a prototype and testing in one of the electricity corridors of District 9 of <a href="https://en.wikipedia.org/wiki/Mashhad" target="_blank"><strong>Mashhad</strong></a>.

<picture><source type="image/webp" srcset="/assets/img/legacy/mashhadcon-062509d271-480.webp 480w, /assets/img/legacy/mashhadcon-062509d271-800.webp 800w, /assets/img/legacy/mashhadcon-062509d271-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/mashhadcon-062509d271.png" alt="MashhadCon1"></picture>

Manufacturing 30 samples of the aforementioned device based on changing the structure of existing watches (by reverse engineering and changing the program of existing microcontrollers and adding the required hardware components) Installation in 30 locations in the holy city of <a href="https://en.wikipedia.org/wiki/Mashhad" target="_blank"><strong>Mashhad</strong></a> and successful exit from this test.
Efforts to finalize the design and present the design in a national format for mass production

## 8. References (select)

- <a href="https://www.dlms.com/" target="_blank"><strong>DLMS User Association — Official site</strong></a>
- <a href="https://webstore.iec.ch/en/publication/71751" target="_blank"><strong>IEC 62056 — DLMS/COSEM (IEC webstore)</strong></a>
- <a href="https://www.gurux.fi/DLMSIntro" target="_blank"><strong>Gurux — DLMS/COSEM introduction and Clock (Class 8) notes</strong></a>
- <a href="https://en.wikipedia.org/wiki/RS-485" target="_blank"><strong>RS-485 overview (practical considerations)</strong></a>
- <a href="https://icube.ch/Security/security1.html" target="_blank"><strong>DLMS security basics — LLS/HLS overview</strong></a>

---

## 9. Appendix — Example DLMS Clock read (conceptual)

A DLMS LN-read request for the Clock (Class ID = 8) attribute (AttributeIndex = 2, depending on vendor) will return a COSEM DateTime structure. Use existing DLMS client libraries (e.g., Gurux, vendor SDKs) to decode the returned DateTime to UTC/local time, then apply local timezone/astronomical rules.
{% endraw %}
