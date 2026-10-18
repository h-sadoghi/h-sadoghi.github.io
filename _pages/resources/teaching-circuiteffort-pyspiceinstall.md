---
layout: legacy_page
title: PySpice Installation Manual
permalink: /resources/teaching-circuiteffort-pyspiceinstall/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/circuiteffort/PyspiceInstall/
legacy_group: Circuits and electronics
legacy_dir: ltr
lang: en
---

{% raw %}

# PySpice Installation Manual

## Electric and Electronic Circuits

**Authors: Sania Dolat, Ali Saadatpour**

### Fall 2024

This document focuses on the installation of the PySpice library. Various methods are available for installing this library, ensuring the inclusion of numerous components such as diodes and MOSFETs. It is crucial that this library is installed correctly; otherwise, numerous issues may arise. Therefore, it is highly recommended to follow the steps outlined in this document.

## Installation Using Repository

To install the library, download it from the repository or copy the link into your browser. Then follow the instructions to download, extract, and install using Python's pip.

**Repository Links:**

- [PySpice Github Repository](https://github.com/PySpice-org/PySpice)
- [Direct Download Zip](https://github.com/PySpice-org/PySpice/archive/refs/heads/master.zip)

**Installation Commands:**  
In the next step, using the command below, we navigate to that path using our Python package manager and install it. Open CMD and enter the following command.

```bash
pip install --target="C:\Program Files\PySpice-master" PySpice
pip3 install PySpice
```

> **Note**: Before executing this command above, please Remove exclamation mark.

If you notice, Python uses cached data. (It's the same package that we downloaded from the repository.)

## Update Path Instructions

If you have extracted the Zip file to a different path, update the command above to suit your preferred path.

### Note

In the next step, add this to the system path as well, Follow the steps below according to the image.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/a1-5dd51d02ef-480.webp 480w, /assets/img/legacy/a1-5dd51d02ef-800.webp 800w, /assets/img/legacy/a1-5dd51d02ef-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/a1-5dd51d02ef.jpg" alt="PySpiceinstallation1"></picture>

</div>

</div>

<div class="caption" markdown="1">

add this to the system path as well

</div>

Again!! If you have extracted the Zip file to a different path, update the command above to suit your preferred path.

## Verification of Installation

Check if Python recognizes the PySpice package by using the following command in Command Prompt:

**Verification Command:**

```bash
pip show PySpice
```

## Result

The output of the command above is as follows:

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/a2-e663a20128-480.webp 480w, /assets/img/legacy/a2-e663a20128-800.webp 800w, /assets/img/legacy/a2-e663a20128-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/a2-e663a20128.jpg" alt="PySpiceinstallation2"></picture>

</div>

</div>

<div class="caption" markdown="1">

The output of the command

</div>

And also, for added assurance, run the following command inside a Python file:

```python
import PySpice.Spice.Simulation as simulation
print(dir(simulation))
```

## Handling Installation Errors

If you encounter an error, it might be due to a missing DLL file within the installed Python packages. Follow the link below to download the required DLL and follow the outlined steps to resolve the issue.

**DLL Download Link:**

- [ngspice_x86-64 DLL File](https://www.dropbox.com/scl/fi/6qguzxdrcgz4bsmugolzg/ngspice_x86-64.zip?rlkey=ilt2u17l25mlk9nuab4999yg3&st=exupnbrh&dl=0)

### After downloading

follow the path below:

```
C:\Users\<ur_local_username>\AppData\Local\Programs\Python\Python312\Lib\site-packages
```

## Comment

Replace `<ur_local_username>` with your local username. In the opened folder, create a folder named `Spice64_dll` and open it. Then again, in the opened folder, create a folder named `dll-vs` and open it. Inside this folder, extract the file `ngspice_x86-64.zip` (the file placed in Dropbox).

After completing these installation steps, you can perform an example. Let's do the following example:

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.HighLevelElement import SinusoidalVoltageSource
from PySpice.Unit import *
import matplotlib.pyplot as plt
from PySpice.Spice.Library import SpiceLibrary
import numpy as np

dc_offset = 1@u_V
ac_amplitude = 100@u_mV

# Create a circuit
circuit = Circuit('RC Circuit')
#SinusoidalVoltageSource('input', circuit.gnd, 'input',circuit.gnd)
#source = circuit.V('input', 'in', circuit.gnd, dc_offset)
#SinusoidalVoltageSource('input','input',circuit.gnd)
#AcLine()
#('input', circuit.gnd, 'L', rms_voltage=230@u_V, frequency=50@u_Hz)
source=circuit.V(50, 'input', circuit.gnd, 1000 )#@ u_V)
circuit.R(1, 'input', 'output', 1 @ u_kΩ)
circuit.R(2, 'output', circuit.gnd, 2 @ u_kΩ)
#circuit.SinusoidalVoltageSource('input', 'input', circuit.gnd, amplitude=220, frequency=50)
# Simulate the circuit

InputData=np.array([])
OutputData=np.array([])

for voltage in (0,100,3000):
    source.dc_value = voltage
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()
    #analysis = simulator.transient(step_time=0.01 @ u_ms, end_time=50 @ u_ms)
    InputData=np.append(InputData,analysis['input'])
    OutputData=np.append(OutputData,analysis['output'])

# Plot the results
plt.figure(figsize=(10, 6))

plt.plot(InputData,OutputData)

# Add labels and legend
plt.xlabel('Input Voltage')
plt.ylabel('Output Voltage')
plt.title('Voltage Divider Circuit Analysis')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
```

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/a3-8cceb21568-480.webp 480w, /assets/img/legacy/a3-8cceb21568-800.webp 800w, /assets/img/legacy/a3-8cceb21568-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/a3-8cceb21568.jpg" alt="PySpice Installation Step 3"></picture>

</div>

</div>

<div class="caption" markdown="1">

Execution Result

</div>

{% endraw %}
