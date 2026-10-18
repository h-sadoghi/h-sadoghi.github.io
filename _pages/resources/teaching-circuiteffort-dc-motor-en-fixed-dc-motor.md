---
layout: legacy_page
title: DC Motor
permalink: /resources/teaching-circuiteffort-dc-motor-en-fixed-dc-motor/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/circuiteffort/DC_Motor_en_fixed_DC_Motor/
legacy_group: Circuits and electronics
legacy_dir: ltr
lang: en
---

{% raw %}

## Table of Contents

<!-- prettier-ignore -->
* TOC
{:toc}

<div markdown="1">

  <h1>⚙️ DC Motor</h1>

</div>

<hr>

<h2>✨ Author Information</h2>
<p>
<b>👤 Name:</b> <i>Ehsan Esfehani</i><br>
<b>🏫 Affiliation:</b> Department of Computer Engineering, Ferdowsi University of Mashhad<br>
<b>🔗 LinkedIn:</b> <a href="https://www.linkedin.com/in/ehsan-esfehani-067b45340/" target="_blank">linkedin.com/in/ehsanesfehani</a><br>
<b>💻 GitHub:</b> <a href="https://github.com/ehsan-esf0" target="_blank">github.com/ehsanesfehani</a>
</p>

<hr>

<div align="center" markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/4-1-60a2b8f4a6-480.webp 480w, /assets/img/legacy/4-1-60a2b8f4a6-800.webp 800w, /assets/img/legacy/4-1-60a2b8f4a6-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 1" src="/assets/img/legacy/4-1-60a2b8f4a6.jpg" width="30%"></picture>
<picture><source type="image/webp" srcset="/assets/img/legacy/5-1-9da5aa113e-480.webp 480w, /assets/img/legacy/5-1-9da5aa113e-800.webp 800w, /assets/img/legacy/5-1-9da5aa113e-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 2" src="/assets/img/legacy/5-1-9da5aa113e.jpg" width="30%"></picture>
<picture><source type="image/webp" srcset="/assets/img/legacy/dc-5c2b9615f0-480.webp 480w, /assets/img/legacy/dc-5c2b9615f0-800.webp 800w, /assets/img/legacy/dc-5c2b9615f0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 3" src="/assets/img/legacy/dc-5c2b9615f0.jpg" width="30%"></picture>

</div>

## ⚙️ Why Do We Call It a DC Motor? {#why-do-we-call-it-a-dc-motor}

The term **DC** stands for _Direct Current_.  
In this type of motor, the power supply provides **current that flows in only one direction**, meaning the positive and negative terminals remain constant.

As a result, the magnetic field produced by the windings also has a constant direction.  
With the help of components such as the **commutator** and **brushes**, the motor maintains a continuous and unidirectional torque that keeps the rotor spinning.
Therefore, it is called a **Direct Current Motor (DC Motor)** — in contrast to **AC motors**, which operate using alternating current that changes direction periodically.

## 🧲 Basic concepts of magnetism {#basic-concepts-of-magnetism}

By understanding how a motor works you can learn a lot about magnets, electromagnets and electricity in general. An electric motor uses magnets to create motion. If you have ever played with magnets, you know about the fundamental law of all magnets: Opposites attract and likes repel.

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/42xu-f-353a4e0e42.gif" alt="DC Motor Animation">

<div markdown="1">

So, if you have two bar magnets with their ends marked "north" and "south," then the north end of one magnet will attract the south end of the other. On the other hand, the north end of one magnet will repel the north end of the other (and south will repel south). Inside an electric motor, these attracting and repelling forces create rotational motion.

</div>

</div>

## 🌟 The Beginning of the Story {#the-beginning-of-the-story}

From basic magnetic concepts, we know that opposite poles attract while like poles repel.
Now, imagine we fix one magnet at its center and bring another magnet close to it.
As the opposite poles face each other, an attractive force is created — strong enough to cause a rotational motion around the fixed center.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 5" src="/assets/img/legacy/how-does-an-electric-motor-work-dc-motor-1-1-e4a1ed541b.gif">

</div>

However, this rotation lasts only until the unlike poles align.
Once the opposite poles face each other directly, the magnetic forces balance, and the motion comes to a stop.
To overcome this limitation, we need to continuously change the polarity of the external magnet, ensuring that a constant torque keeps the system spinning.

This simple observation forms the foundation of how motion is sustained in a DC motor, where clever engineering ensures that the poles are switched at just the right moment.

According to Ampère’s Law, when an electric current passes through a conductor, it produces a magnetic field around it.
So, instead of using a permanent magnet, we can use a coil of wire to create the same effect.
By winding the wire into several loops, the magnetic fields of each turn combine, forming a stronger, unified field — very similar to that of a bar magnet.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 6" src="/assets/img/legacy/how-does-an-electric-motor-work-dc-motor-3-cb7e0c6c1f.gif">

</div>

Now, by simply changing the direction of the current in the coil, we can also change the polarity of this magnetic field.
This means we no longer need to physically rotate or flip magnets — we can achieve the same motion electronically, just by reversing the current.

When we place a current-carrying coil between the north and south poles of a magnet, something fascinating happens.
According to the Lorentz force law, every segment of the coil carrying current inside a magnetic field experiences a mechanical force.
These forces act in opposite directions on the two sides of the coil — one side is pushed upward, and the other is pushed downward.

This pair of forces creates a torque, causing the coil to rotate around its axis.
The stronger the current or the magnetic field, the greater the torque, and thus the faster the rotation.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 7" src="/assets/img/legacy/how-does-an-electric-motor-work-dc-motor-4-e1fd5e5923.gif">

</div>

However, this rotation still faces a limitation: after half a turn, the direction of the forces reverses, and the motion would stop if nothing changed.

To take one step closer to a practical motor, we now place the two sides of the coil between the magnetic poles — one near the north pole and the other near the south pole.
This arrangement ensures that each side of the coil experiences a magnetic field in opposite directions.

Next, we bend the coil into a loop, creating a structure that can rotate freely around its center.
When current flows through this loop, one side of the coil is pushed upward while the other side is pushed downward, due to the interaction between the magnetic field and the electric current — a direct application of the Lorentz force.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 8" src="/assets/img/legacy/how-does-an-electric-motor-work-dc-motor-5-3d9957fd4e.gif">

</div>

This loop now becomes the rotating part of our system — the armature.
It transforms the invisible flow of electric current into visible motion, marking the true beginning of the DC motor’s rotation.

At this point, we face a critical challenge.
As the coil rotates, the direction of the current in each side must reverse every half turn; otherwise, the forces on both sides will cancel out, and the rotation will stop.
In other words, to maintain continuous motion, the current must switch direction periodically.

But manually changing the current every half turn is impossible — the motor needs to do it automatically.
This is where the commutator and brushes come to the rescue.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 9" src="/assets/img/legacy/how-does-an-electric-motor-work-dc-motor-6-4f3c36f417.gif">

</div>

The commutator is a split ring connected to the rotating coil, while the brushes are stationary metal or carbon contacts that supply current to it.
As the coil spins, the commutator automatically reverses the connection of the current in the loop at just the right moment.
This clever mechanism ensures that the torque always acts in the same rotational direction, keeping the coil spinning smoothly and endlessly.

To make our design more powerful and efficient, we can add more loops of wire to the rotating coil.
Each additional loop interacts with the magnetic field, producing its own force and contributing to the overall torque.
When these loops are properly arranged, their magnetic effects combine, resulting in smoother and stronger rotation.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 10" src="/assets/img/legacy/how-does-an-electric-motor-work-dc-motor-7-4171c076f7.gif">

</div>

In practical DC motors, the armature consists of multiple coils wound around an iron core.
This core amplifies the magnetic field and ensures that the torque remains nearly constant throughout the rotation.
The commutator distributes current to each coil in sequence, maintaining a continuous flow of energy and motion.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 11" src="/assets/img/legacy/how-does-an-electric-motor-work-dc-motor-1-d3ab40a54d.gif">

</div>

With this enhancement, our once simple coil evolves into a fully functional DC motor — a brilliant machine that converts electrical energy into steady mechanical motion, powering countless devices in our daily lives.

In order to enhance the performance and industrial applicability of our DC motor, we focus on designing a stronger and more efficient rotor.
This improvement is achieved by adding an additional ferromagnetic core layer to the rotor structure.
The inclusion of this core increases the magnetic permeability of the magnetic circuit, allowing a greater portion of the magnetic flux generated by the stator field to be effectively coupled with the armature windings.

As a result, the magnetic flux linkage and induced electromotive force (EMF) are both improved, leading to a significant increase in the developed torque.
This not only enhances the mechanical power output but also improves energy conversion efficiency and reduces magnetic losses within the rotor.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 12" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-00ed8d6b8e.gif">

</div>

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 13" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-37509d65cb.gif">

</div>

When the magnetic field inside the iron core of the rotor or stator changes with time, small circulating currents, known as eddy currents, are induced within the core material.
These currents flow in closed loops inside the metal and cause unwanted power losses in the form of heat.
To minimize these losses, the core is built using thin laminated sheets of iron, separated by insulating layers.
This structure limits the path of eddy currents and greatly improves the efficiency of the motor.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 14" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-5e9307bfad.gif">

</div>

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 15" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-3070a2dad8.gif">

</div>

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 16" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-8c2962da26.gif">

</div>

Next, the armature coils are added around the laminated iron core of the rotor.
These coils are made of copper windings, arranged in multiple loops to efficiently interact with the magnetic field produced by the stator.
Each loop is carefully insulated to prevent short circuits and to ensure uniform current distribution.
The terminals of these coils are then connected to the commutator segments, which serve as the electrical interface between the rotating armature and the stationary brushes.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 17" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-6123077919.gif">

</div>

At this stage, the carbon brushes are installed to complete the electrical circuit between the external power supply and the rotating commutator.

These brushes are usually made of carbon or graphite, chosen for their good electrical conductivity and self-lubricating properties, which reduce wear during continuous contact.

They are mounted in brush holders that press them lightly against the commutator surface using springs, ensuring stable electrical connection as the rotor spins.

The brushes allow current to flow into and out of the armature windings without twisting the wires, while the commutator segments automatically reverse the current direction at the right moments.
This system enables smooth torque production and unidirectional rotation, making the DC motor highly reliable and efficient in industrial applications.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 18" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-e70e0c804d.gif">

</div>

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 19" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-8e242b0651.gif">

</div>

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 20" src="/assets/img/legacy/how-a-dc-motor-works-full-breakdown-with-3d-animation-the-science-work-acf3babb82.gif">

</div>

Up to this point, the stator we examined was a fixed magnetic structure, typically made of permanent magnets.
Now, applying Ampère’s Law, we replace the permanent magnetic field with electromagnetic field windings, effectively converting the stator into an electromagnet.

According to Ampère’s Law, an electric current flowing through a conductor generates a magnetic field around it; therefore, by winding insulated copper coils around the stator poles and supplying them with current, we can control the magnetic field strength dynamically.
This modification allows the motor to produce a variable and stronger magnetic flux, enhancing torque generation and enabling speed control through field current regulation.

Such a configuration is used in shunt, series, and compound DC motors, making them highly suitable for industrial and variable-load applications.

## 📑 Examining the said concepts {#examining-the-said-concepts}

### Faraday's Law of Induction {#faradays-law-of-induction}

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/magnetic-flux-2-96d97e9d71.webp" alt="DC Motor Animation">

<div markdown="1">

### Magnetic Flux {#magnetic-flux}

Magnetic flux describes how much magnetic field passes through a given surface $like a loop of wire.  
It depends on three things: the magnetic field strength $B$, the area of the loop $A$, and the angle $\theta$ between the field and the surface.

The formula is:

$$
\Phi_B = B \cdot A \cdot \cos \theta
$$

</div>

</div>

### Faraday's Law of Induction {#faradays-law-of-induction-2}

**Faraday’s Law** states that any change in magnetic flux through a circuit induces an electromotive force $emf).  
This induced emf can drive a current if the circuit is closed.

The law is written as:

$$
\mathcal{E} = -\frac{d\Phi_B}{dt}
$$

- $\mathcal{E}$ = induced emf $voltage)
- $\Phi_B$ = magnetic flux
- the minus sign comes from **Lenz’s Law**, meaning the induced emf always opposes the change in flux.

<p align="center">
  <picture><source type="image/webp" srcset="/assets/img/legacy/emf-induction-4f65d72ccd-480.webp 480w, /assets/img/legacy/emf-induction-4f65d72ccd-800.webp 800w, /assets/img/legacy/emf-induction-4f65d72ccd-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 22" src="/assets/img/legacy/emf-induction-4f65d72ccd.png"></picture>
</p>

### Changing Magnetic Flux {#changing-magnetic-flux}

A changing magnetic flux is what produces an induced current.  
There are three main ways to change $\Phi_B$:

<div align="center" markdown="1">

|                                                                                                                                                                 **Change the magnetic field $B$**                                                                                                                                                                  |                                                                                                                                                                                        **Change the area $A$**                                                                                                                                                                                         |                                                                                                                                                                                        **Change the angle $θ$**                                                                                                                                                                                        |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| <picture><source type="image/webp" srcset="/assets/img/legacy/75-orig-1e9806a421-480.webp 480w, /assets/img/legacy/75-orig-1e9806a421-800.webp 800w, /assets/img/legacy/75-orig-1e9806a421-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 23" src="/assets/img/legacy/75-orig-1e9806a421.jpg"></picture> | <picture><source type="image/webp" srcset="/assets/img/legacy/magnetic-flux-02-0245586403-480.webp 480w, /assets/img/legacy/magnetic-flux-02-0245586403-800.webp 800w, /assets/img/legacy/magnetic-flux-02-0245586403-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 24" src="/assets/img/legacy/magnetic-flux-02-0245586403.jpg"></picture> | <picture><source type="image/webp" srcset="/assets/img/legacy/magnetic-flux-03-263d78089c-480.webp 480w, /assets/img/legacy/magnetic-flux-03-263d78089c-800.webp 800w, /assets/img/legacy/magnetic-flux-03-263d78089c-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 25" src="/assets/img/legacy/magnetic-flux-03-263d78089c.jpg"></picture> |
|                                                                                                                                                            Move a magnet closer or farther from a coil.                                                                                                                                                            |                                                                                                                                                                                 Expand or shrink the size of the loop.                                                                                                                                                                                 |                                                                                                                                                                                 Rotate the loop in the magnetic field.                                                                                                                                                                                 |
|                                                                                                                                                         $\mathcal{E} = -A \cos\theta \cdot \frac{dB}{dt}$                                                                                                                                                          |                                                                                                                                                                           $\mathcal{E} = -B \cos\theta \cdot \frac{dA}{dt}$                                                                                                                                                                            |                                                                                                                                                                        $\mathcal{E} = +B A \sin\theta \cdot \frac{d\theta}{dt}$                                                                                                                                                                        |

</div>

<div align="center" markdown="1">

<!-- 🧲 Image Section -->

  <!-- 📘 Text Section -->

<div markdown="1">

    <h3>🌀 Lenz’s Law – Nature’s Opposition to Change</h3>
    <p>
    According to <b>Lenz’s Law</b>, the direction of an <b>induced current</b> is always such that it <b>opposes the change</b> that produced it.
    In other words, whenever a changing magnetic field induces a current in a loop, the magnetic field created by that current acts <b>against the original change</b>.
    </p>

  <p>
    This principle preserves the <b>law of conservation of energy</b>.  
    If the induced current were to assist the change instead of opposing it, the system would continuously generate energy, creating motion or electricity from nothing — an impossibility.  
    Therefore, nature always resists change to maintain equilibrium.
    </p>

$$\mathcal{E} = -\frac{d\Phi_B}{dt}$$

The negative sign $−$ indicates that the induced electromotive force $emf$ acts in the <b>opposite direction</b> to the change in magnetic flux $\Phi_B$.  
This elegant interaction between change and resistance ensures that <b>electromagnetic systems</b> — from generators to DC motors — operate in harmony with the laws of physics.

<div align="left" markdown="1">

<h3>⚡ The Role of Faraday’s and Lenz’s Laws in DC Motors</h3>

<p>
<b>Faraday’s Law</b> explains how a change in magnetic flux induces an <b>electromotive force فemf)</b> in a conductor.  
In a DC motor, as the coil rotates within the magnetic field, the magnetic flux passing through the loop changes continuously.  
This changing flux induces an emf in the opposite direction of the supply voltage, known as the <b>back emf</b>.  
The back emf naturally regulates the motor’s speed — as the motor spins faster, the effective current decreases, keeping the motion stable.
</p>

<p>
<b>Lenz’s Law</b> defines the <b>direction</b> of this induced emf.  
It ensures that the induced current always acts <b>against the cause that produced it</b> — in this case, the motion that changes the magnetic flux.  
This provides a natural <b>feedback mechanism</b> within the motor, preventing uncontrolled acceleration and maintaining balance between electrical input and mechanical output.
</p>

<p>
Together, these two laws form the <b>electromagnetic foundation</b> of every DC motor:  
Faraday tells us <i>“how much”</i> emf is produced, while Lenz tells us <i>“in which direction”</i>.  
Their combined effect allows the DC motor to convert electrical energy into smooth, stable, and controlled mechanical motion.
</p>

</div>

## ⚡ Ampère’s Law {#ampres-law}

Ampère’s Law is a fundamental principle of electromagnetism that relates the magnetic field around a closed path to the electric current passing through it.  
It provides a direct link between **magnetism** and **electric current flow**, forming one of **Maxwell’s Equations**.

$$
\oint_{\partial S} \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{\text{enc}}
$$

#### 🔹 Example: Magnetic Field Around a Long Straight Wire {#example-magnetic-field-around-a-long-straight-wire}

Consider a long, straight conductor carrying a steady current $I$.  
By symmetry, the magnetic field at a distance $4 r$ from the wire is circular and has a constant magnitude.  
Applying Ampère’s Law:

$$
\oint \mathbf{B} \cdot d\mathbf{l} = B2\pi r = \mu_0 I
$$

Therefore,

$$
B = \frac{\mu_0 I}{2\pi r}
$$

This shows that the magnetic field forms **concentric circles** around the wire and decreases inversely with distance $r$.  
The direction of $mathbf{B}$ follows the **right-hand rule**.

#### 🔹 Differential (Local) Form {#differential-local-form}

Using **Stokes’ theorem**, the integral form can be converted to its differential form:

$$
\nabla \times \mathbf{B} = \mu_0 \mathbf{J}
$$

where $mathbf{J}$ is the **current density vector** ($A/m²$).  
This means that the curl (circulation) of the magnetic field at any point is proportional to the local current density.

#### 🔹 The Ampère–Maxwell Law {#the-ampremaxwell-law}

When electric fields vary with time, Maxwell introduced the concept of **displacement current**, extending Ampère’s Law to its more general form:

$$
\nabla \times \mathbf{B} = \mu_0 \left( \mathbf{J} + \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t} \right)
$$

or, equivalently, in integral form:

$$
\oint_{\partial S} \mathbf{B} \cdot d\mathbf{l} = \mu_0 \left( I_{\text{enc}} + \varepsilon_0 \frac{d\Phi_E}{dt} \right)
$$

Here $\ varepsilon_0$ is the **permittivity of free space**, and $frac{d\Phi_E}{dt}$ is the **rate of change of electric flux** through the surface.  
This addition makes the law consistent even when no real current flows (as in a capacitor charging).

#### 💡 Physical Interpretation {#physical-interpretation}

Ampère’s Law reveals that:

- Electric currents produce **circulating magnetic fields**.
- The strength and direction of the magnetic field depend on the **magnitude and geometry** of the current distribution.
- Together with Faraday’s Law, it shows the deep connection between **changing electric and magnetic fields**.

#### 🧭 Summary of Forms {#summary-of-forms}

$$
\begin{aligned}
\text{Integral Form:} \quad & \oint \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{\text{enc}} \\
\text{Differential Form:} \quad & \nabla \times \mathbf{B} = \mu_0 \mathbf{J} \\
\text{Generalized Form:} \quad & \nabla \times \mathbf{B} = \mu_0 \left( \mathbf{J} + \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t} \right)
\end{aligned}
$$

Ampère’s Law is thus a cornerstone of classical electromagnetism, elegantly linking **current flow** to the **magnetic field** it produces.

## 🪧 Lorentz force {#lorentz-force}

In electromagnetism, the Lorentz force is the force exerted on a charged particle by electric and magnetic fields. It determines how charged particles move in electromagnetic environments and underlies many physical phenomena, from the operation of electric motors and particle accelerators to the behavior of plasmas.

<div markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/magnetic-force-on-wire-with-electrons-svg-8b99acd4fc-480.webp 480w, /assets/img/legacy/magnetic-force-on-wire-with-electrons-svg-8b99acd4fc-800.webp 800w, /assets/img/legacy/magnetic-force-on-wire-with-electrons-svg-8b99acd4fc-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/magnetic-force-on-wire-with-electrons-svg-8b99acd4fc.png" alt="DC Motor Animation"></picture>

<div markdown="1">

The Lorentz force F acting on a point particle with electric charge q, moving with velocity v, due to an external electric field E and magnetic field B, is given by (SI definition of quantities)

$$
 \vec{F} = q \left( \vec{E} + \vec{v} \times \vec{B} \right)
$$

</div>

</div>

Here, × is the vector cross product, and all quantities in bold are vectors. In component form, the force is written as:

$$
\begin{aligned}
F_x &= q\left(E_x + v_y B_z - v_z B_y\right),\\
F_y &= q\left(E_y + v_z B_x - v_x B_z\right),\\
F_z &= q\left(E_z + v_x B_y - v_y B_x\right).
\end{aligned}
$$

<div align="left" markdown="1">

<h3>⚙️ The Role of Ampère’s Law in DC Motors</h3>

<p>
<b>Ampère’s Law</b> is responsible for the creation of magnetic fields around the current-carrying coils in a DC motor.  
When current flows through the armature windings, it generates magnetic fields that interact with the field from the permanent magnets.  
This interaction establishes the magnetic environment where torque is produced.  
In short, Ampère’s Law explains how <b>electrical current creates the magnetic field</b> needed for motor operation.
</p>

</div>

<div align="left" markdown="1">

<h3>🧲 The Role of Lorentz Force in DC Motors</h3>

<p>
The <b>Lorentz Force Law</b> describes how the magnetic field acts on the current-carrying conductors of the armature.  
This interaction produces a mechanical force that causes the armature to rotate, generating useful torque.  
In essence, the Lorentz force is what <b>turns electrical energy into mechanical motion</b> inside the DC motor.
</p>

</div>

# 🔧 Engine components {#engine-components}

## 1️⃣ The Stator in a DC Motor {#1-the-stator-in-a-dc-motor}

The **stator** is the stationary component of a direct current (DC) motor.  
It provides the magnetic field that interacts with the rotor (armature) windings to produce motion.  
In the absence of the stator, the rotor would have no magnetic environment in which to operate, and the motor would fail to convert electrical energy into mechanical energy.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 27" src="/assets/img/legacy/df-f8-1f-h1matthieslichtmaschine700169810046677-3c51d84745.webp" width="20%">
  <picture><source type="image/webp" srcset="/assets/img/legacy/stator-c40545f725-480.webp 480w, /assets/img/legacy/stator-c40545f725-800.webp 800w, /assets/img/legacy/stator-c40545f725-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 28" src="/assets/img/legacy/stator-c40545f725.jpg" width="20%"></picture>
  <picture><source type="image/webp" srcset="/assets/img/legacy/what-is-a-stator-fb4587c3d2-480.webp 480w, /assets/img/legacy/what-is-a-stator-fb4587c3d2-800.webp 800w, /assets/img/legacy/what-is-a-stator-fb4587c3d2-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 29" src="/assets/img/legacy/what-is-a-stator-fb4587c3d2.png" width="20%"></picture>

</div>

### Structure of the Stator {#structure-of-the-stator}

Structurally, the stator forms the outer frame of the motor and remains fixed during operation.  
Depending on the design and application, it can be constructed in two main ways:

1. **Permanent magnets** – often used in small DC motors due to their simplicity and cost-effectiveness.
2. **Field windings** – used in larger or industrial machines, where an electromagnet provides a stronger and more controllable magnetic field.

The stator is typically cylindrical, enclosing the rotor at the center, and its materials are chosen to guide and strengthen the magnetic flux efficiently.

### Function of the Stator {#function-of-the-stator}

The primary role of the stator is to create a **steady magnetic field**.  
When current flows through the rotor windings, the interaction between the magnetic field of the stator and the current-carrying conductors produces a force, according to **Lorentz’s law**.  
This electromagnetic force generates torque on the rotor, leading to continuous rotation.

In summary, the stator acts as the _magnetic backbone_ of the motor, ensuring that electrical energy is consistently transformed into mechanical output.

## 2️⃣ The Rotor in a DC Motor {#2-the-rotor-in-a-dc-motor}

The **rotor**, also known as the **armature**, is the rotating component of a direct current (DC) motor.  
It is located at the center of the motor and is responsible for converting electrical energy into mechanical energy through electromagnetic interaction.  
Without the rotor, the motor would not be able to deliver torque or perform useful mechanical work.

<div align="center" markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/various-motor-rotor-tici-ac4cc04bce-480.webp 480w, /assets/img/legacy/various-motor-rotor-tici-ac4cc04bce-800.webp 800w, /assets/img/legacy/various-motor-rotor-tici-ac4cc04bce-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 30" src="/assets/img/legacy/various-motor-rotor-tici-ac4cc04bce.jpg" width="20%"></picture>
<picture><source type="image/webp" srcset="/assets/img/legacy/615guzeytcl-deeb832cad-480.webp 480w, /assets/img/legacy/615guzeytcl-deeb832cad-800.webp 800w, /assets/img/legacy/615guzeytcl-deeb832cad-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 31" src="/assets/img/legacy/615guzeytcl-deeb832cad.jpg" width="20%"></picture>
<picture><source type="image/webp" srcset="/assets/img/legacy/8ysm63qq-29dbe01eb0-480.webp 480w, /assets/img/legacy/8ysm63qq-29dbe01eb0-800.webp 800w, /assets/img/legacy/8ysm63qq-29dbe01eb0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 32" src="/assets/img/legacy/8ysm63qq-29dbe01eb0.jpg" width="20%"></picture>

</div>

### Structure of the Rotor {#structure-of-the-rotor}

The rotor is typically composed of:

1. **Armature windings** – copper coils placed in slots on the rotor core, which carry current.
2. **Laminated iron core** – designed to concentrate and guide the magnetic flux, while minimizing eddy current losses.
3. **Shaft** – the central axis that transmits mechanical power to external loads.

The windings of the rotor are connected to the **commutator**, which ensures that the current direction in each coil changes appropriately to maintain continuous torque in one direction.

### Function of the Rotor {#function-of-the-rotor}

The rotor’s primary function is to rotate and deliver mechanical power.  
When current flows through its windings, the conductors experience a force due to the magnetic field of the stator.  
According to **Lorentz’s law**, this force produces torque on the rotor.

As the rotor turns:

- The **commutator** switches the direction of current in the windings.
- This ensures that the torque always acts in a consistent direction, allowing for smooth rotation.

Thus, the rotor is the dynamic element of the motor, directly responsible for the conversion of electrical input into rotational mechanical output.

## 3️⃣ The Commutator in a DC Motor {#3-the-commutator-in-a-dc-motor}

The **commutator** is a mechanical switching device used in direct current (DC) motors.  
It is mounted on the shaft of the rotor and consists of several copper segments arranged in a cylindrical form.  
The commutator works in combination with the brushes to ensure that current in the rotor windings is reversed at the correct time, so that the torque produced by the motor always acts in the same direction.

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 33" src="/assets/img/legacy/sparking-in-vacuum-cleaner-collector5-113689a6c9.webp" width="20%">
  <img loading="lazy" alt="DC Motor — illustration 34" src="/assets/img/legacy/commutator-e8bb7382ca.webp" width="20%">
  <picture><source type="image/webp" srcset="/assets/img/legacy/commutator-86973cd175-480.webp 480w, /assets/img/legacy/commutator-86973cd175-800.webp 800w, /assets/img/legacy/commutator-86973cd175-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 35" src="/assets/img/legacy/commutator-86973cd175.jpg" width="20%"></picture>

</div>

### Structure of the Commutator {#structure-of-the-commutator}

- The commutator is made up of **copper segments**, insulated from each other by mica or another insulating material.
- These segments are connected to the ends of the rotor (armature) windings.
- As the rotor spins, the commutator rotates with it, while brushes slide over its surface to maintain electrical contact.

In essence, the commutator serves as a rotating switch that automatically reverses current flow in each coil of the rotor.

### Function of the Commutator {#function-of-the-commutator}

The primary function of the commutator is to **reverse the direction of current** in the rotor windings every half turn.  
This ensures that the torque generated by the electromagnetic interaction between the rotor and the stator always points in the same rotational direction.

Without a commutator:

- The current direction would remain unchanged.
- After half a revolution, the forces on the rotor conductors would reverse, and the rotor would stop or oscillate back and forth.

Thus, the commutator is essential for continuous and unidirectional rotation in a brushed DC motor.

## 4️⃣ The Brushes in a DC Motor {#4-the-brushes-in-a-dc-motor}

The **brushes** are small but essential components of a direct current (DC) motor.  
They are usually made of carbon or graphite and are placed in contact with the rotating commutator.  
The brushes serve as the interface between the stationary external circuit and the moving rotor windings.

Without brushes, electrical current could not be supplied to the rotor, and the motor would not function.

<div align="center" markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/carbon-brushes-2f68506c07-480.webp 480w, /assets/img/legacy/carbon-brushes-2f68506c07-800.webp 800w, /assets/img/legacy/carbon-brushes-2f68506c07-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 36" src="/assets/img/legacy/carbon-brushes-2f68506c07.jpg" width="15%"></picture>
<picture><source type="image/webp" srcset="/assets/img/legacy/615e1qcedzl-af1d8744f1-480.webp 480w, /assets/img/legacy/615e1qcedzl-af1d8744f1-800.webp 800w, /assets/img/legacy/615e1qcedzl-af1d8744f1-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 37" src="/assets/img/legacy/615e1qcedzl-af1d8744f1.jpg" width="15%"></picture>

</div>

### Structure of the Brushes {#structure-of-the-brushes}

- Brushes are commonly made of **carbon** or **graphite**, sometimes mixed with copper for better conductivity.
- They are housed in **brush holders**, which press them against the surface of the commutator using springs.
- Their sliding contact allows continuous electrical connection, even as the commutator rotates.

### Function of the Brushes {#function-of-the-brushes}

The main function of the brushes is to **deliver current** from the external DC source to the rotor windings through the commutator.  
As the motor runs:

- The brushes remain stationary while the commutator rotates beneath them.
- The brushes conduct electricity into the correct segments of the commutator, ensuring that the rotor windings receive the proper current flow.

This system allows the motor to maintain continuous torque and smooth operation.

### Importance of Brush Material {#importance-of-brush-material}

- **Carbon/graphite** brushes are preferred because they provide good conductivity while also being soft enough not to damage the commutator surface.
- However, brushes wear down over time and require maintenance or replacement, which is one of the disadvantages of brushed DC motors.

<div align="center" markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/electric-motors-chapter-2-fig3-960-x-500-e3c873cffb-480.webp 480w, /assets/img/legacy/electric-motors-chapter-2-fig3-960-x-500-e3c873cffb-800.webp 800w, /assets/img/legacy/electric-motors-chapter-2-fig3-960-x-500-e3c873cffb-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 38" src="/assets/img/legacy/electric-motors-chapter-2-fig3-960-x-500-e3c873cffb.png" width="40%" ></picture>

</div>

## 🔢 Governing Equations of a DC Motor {#governing-equations-of-a-dc-motor}

- Armature Circuit
- Mechanical System

## ⚡️ 1. Armature Electrical Circuit {#1-armature-electrical-circuit}

<div markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/equivalent-circuit-of-an-armature-controlled-dc-motor-9964612e54-480.webp 480w, /assets/img/legacy/equivalent-circuit-of-an-armature-controlled-dc-motor-9964612e54-800.webp 800w, /assets/img/legacy/equivalent-circuit-of-an-armature-controlled-dc-motor-9964612e54-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/equivalent-circuit-of-an-armature-controlled-dc-motor-9964612e54.png" alt="DC Motor Animation"></picture>

<div markdown="1">

### 🔹 Governing Equation (Kirchhoff’s Voltage Law): {#governing-equation-kirchhoffs-voltage-law}

$$
v_a(t) = R_a i_a(t) + L_a \frac{di_a(t)}{dt} + e(t)
$$

The **back EMF** is proportional to the angular speed of the motor:

$$
e(t) = K_e \, \omega(t)
$$

</div>

</div>

## ⚙️ 2. Mechanical System (Rotor Dynamics) {#2-mechanical-system-rotor-dynamics}

<div markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/chatgpt-image-oct-10-2025-12-47-07-pm-128e7d305c-480.webp 480w, /assets/img/legacy/chatgpt-image-oct-10-2025-12-47-07-pm-128e7d305c-800.webp 800w, /assets/img/legacy/chatgpt-image-oct-10-2025-12-47-07-pm-128e7d305c-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/chatgpt-image-oct-10-2025-12-47-07-pm-128e7d305c.png" alt="DC Motor Animation"></picture>

<div markdown="1">

This part represents the **rotational motion** of the motor shaft.

### 🔹 Governing Equation (Newton’s Second Law for Rotation): {#governing-equation-newtons-second-law-for-rotation}

$$
J \frac{d\omega(t)}{dt} = T_m(t) - T_L(t) - B \, \omega(t)
$$

The **developed torque** is proportional to the armature current:

$$
T_m(t) = K_t \, i_a(t)
$$

</div>

</div>

$$
J \frac{d\omega(t)}{dt}
= K_t \left( \frac{V_a(t) - K_e , \omega(t) - L_a \frac{di_a(t)}{dt}}{R_a} \right)

* B , \omega(t)
* T_L(t)
$$

This equation describes the overall **dynamic behavior** of a DC motor. When a voltage $V_a(t)$ is applied to the armature, a current $i_a(t)$ flows through it and generates an **electromagnetic torque** $ K_t i_a(t) $. This torque accelerates the rotor and increases the angular speed $ \omega(t) $. However, two opposing torques act against this motion:

1. The **frictional torque** $B\omega(t)$ , which grows with speed, and
2. The **load torque** $T_L(t)$ , caused by the external mechanical load.

As the motor speeds up, the **back electromotive force (back EMF)** $K_e \omega(t)$ also increases, reducing the armature current and, consequently, the produced torque. This feedback effect causes the motor to reach a **steady-state speed**, where the developed torque equals the opposing torques. In summary, the equation shows that a DC motor exhibits a **self-regulating and stable behavior** — any change in load or applied voltage dynamically affects the speed until a new equilibrium is established.

# 🧩 Study of DC Motor Types {#study-of-dc-motor-types}

```md
DC MOTORS
│
├── Permanent Magnet Type
│ ├── PMDC (Permanent Magnet DC Motor)
│ └── BLDC (Brushless DC Motor)
│ ├── Inrunner
│ └── Outrunner
│
├──── Wound Field Type
├── Shunt Wound DC Motor
├── Series Wound DC Motor
└── Compound Wound DC Motor
├── Cumulative Compound
└── Differential Compound
Separately Excited DC Motor
```

## 1️⃣ Permanent Magnet DC Motor (PMDC) {#1-permanent-magnet-dc-motor-pmdc}

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/dl-dc-motors-500x500-4f1319afc1.webp" alt="DC Motor Animation">

<div markdown="1">

A Permanent Magnet DC motor (PMDC motor) is a type of DC motor that uses a permanent magnet to create the magnetic field required for the operation of a DC motor.

Permanent Magnet DC Motor
Have you ever used a battery operated toy? The motor that drives these toys is nothing but a permanent magnet DC motor or PMDC motor. These types of motors are simple in construction.

They are commonly used as a starter motor in automobiles, windshield wipers, washers, blowers used in heaters and air conditioners, to raise and lower windows – and they are extensively used in toys.

</div>

</div>

Since the magnetic field strength of a permanent magnet is fixed, external control of this field in a PMDC motor is not possible.

Thus permanent magnet DC motor is used where there is no need to control the speed of the motor (which is usually done by controlling the magnetic field). Small fractional and sub-fractional KW motors are often constructed using a permanent magnet.

Working Principle of Permanent Magnet DC Motor or PMDC Motor
As we said earlier the working principle of PMDC motor is just similar to the general working principle of DC motor. That is when a carrying conductor comes inside a magnetic field, a mechanical force will be experienced by the conductor and the direction of this force is governed by Fleming’s left hand rule.

As in a permanent magnet DC motor, the armature is placed inside the magnetic field of a permanent magnet; the armature rotates in the direction of the generated force.

Here each conductor of the armature experiences the mechanical force $F = B.I.L$ Newton where, B is the magnetic field strength in Tesla $weber / m2$, I is the current in Ampere flowing through that conductor and L is the length of the conductor in meter comes under the magnetic field.

Each conductor of the armature experiences a force and the compilation of those forces produces a torque, which tends to rotate the armature.

<div markdown="1">

<img loading="lazy" src="/assets/img/legacy/equivalent-circuit-of-pmdc-c91fbb93d5.gif" alt="DC Motor Animation">

<div markdown="1">

As in the PMDC motor, the field is produced by a permanent magnet, there is no need for drawing field coils in the equivalent circuit of a permanent magnet DC motor.

The supply voltage to the armature will have armature resistance drop and the rest of the supply voltage is countered by the back emf of the motor. Hence the voltage equation of the motor is given by,

$$
V = E + I R_a
$$

Where, I is armature current and R is armature resistance of the motor.

</div>

</div>

#### ✅ **Advantages** {#advantages}

1. **Simple construction** – No field winding is required.
2. **High efficiency** – No field copper losses occur.
3. **Compact size and lightweight** – Fewer components make it smaller and lighter.
4. **Quick response** – Fast speed response to voltage changes.
5. **Reliable operation** – Fewer electrical parts mean less maintenance.

#### ❌ **Disadvantages** {#disadvantages}

1. **Limited speed control** – Magnetic field cannot be varied (fixed flux).
2. **Demagnetization risk** – Permanent magnets can lose magnetism due to excessive current or high temperature.
3. **High cost of magnets** – Especially when using rare-earth materials like neodymium.
4. **Not suitable for high-power applications** – Because magnet strength and size limit torque output.
5. **Field weakening not possible** – Difficult to achieve speeds higher than the rated speed.

### 🔩 **Applications** {#applications}

1. **Automotive systems** – Used in car wipers, blowers, fans, and electric windows.
2. **Portable tools** – Such as electric drills, screwdrivers, and saws.
3. **Robotics** – For small actuators, wheel drives, and motion control.
4. **Household appliances** – Like hair dryers, mixers, and vacuum cleaners.
5. **Computer and office equipment** – In printers, disk drives, and scanners.
6. **Battery-powered devices** – Ideal for toys, e-bikes, and small mobility vehicles.
7. **Medical instruments** – Used in pumps and precision devices where compactness and efficiency are essential.

## 2️⃣ Brushless DC Motor (BLDC) {#2-brushless-dc-motor-bldc}

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/gif-28e2c1e58e.gif" alt="Brushless DC Motor">

<div markdown="1">

A brushless DC motor (also known as a BLDC motor or BL motor) is an electronically commuted DC motor which does not have brushes. The controller provides pulses of current to the motor windings which control the speed and torque of the synchronous motor.

BLDC motors produce significant torque across a broad speed range, thanks to permanent magnets rotating around a stationary armature. Their electronic commutation offers flexible capabilities, ensuring smooth operation and steady torque even when stationary.

</div>

</div>

<div align="center" markdown="1">

    Your browser does not support the video tag.

</div>

### Electronic Speed Controller {#electronic-speed-controller}

**1. Microcontroller:**
It acts as the brain of the ESC — it detects the rotor position and precisely controls the timing of the phase switching to drive the motor efficiently.

**2. MOSFET Drivers (Transistor Stage):**
These high-speed electronic switches turn the current on and off rapidly to generate the correct waveform for each motor winding.

**3. Sensor Circuit (Sensor / Sensorless):**
This part detects the rotor’s position.

- In **sensor-based** ESCs, **Hall sensors** are used to measure the rotor’s magnetic field.
- In **sensorless** ESCs, the controller estimates the rotor position using the **back EMF (electromotive force)** generated by the motor during rotation.

**4. Control Input (PWM Signal):**
This signal comes from an **Arduino**, flight controller, or other control unit.
It determines the motor’s speed by adjusting the duty cycle or pulse width of the control signal.

<div align="center" markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/brushless-motor-48818aba75-480.webp 480w, /assets/img/legacy/brushless-motor-48818aba75-800.webp 800w, /assets/img/legacy/brushless-motor-48818aba75-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 44" src="/assets/img/legacy/brushless-motor-48818aba75.png" width="20%" ></picture>

<div markdown="1">

### Inner Rotor Design

In an inner rotor design, the rotor is located in the centre of the motor and the stator winding surround the rotor. As the rotor is located in the core, rotor magnets do not insulate heat inside and heat get dissipated easily. Due to this reason, inner rotor designed motor produces a large amount of torque and validly used.

</div>

</div>

<div align="center" markdown="1">

<picture><source type="image/webp" srcset="/assets/img/legacy/bldc-motor-9e88809bda-480.webp 480w, /assets/img/legacy/bldc-motor-9e88809bda-800.webp 800w, /assets/img/legacy/bldc-motor-9e88809bda-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="DC Motor — illustration 45" src="/assets/img/legacy/bldc-motor-9e88809bda.png" width="20%" ></picture>

<div markdown="1">

### Outer Rotor Design

In outer rotor design, the rotor surrounds the winding which is located in the core of the motor. The magnets in the rotor trap the heat of the motor inside and do not allow to dissipate from the motor. Such type of designed motor operates at lower rated current and has low cogging torque.

</div>

</div>

## Arduino Brushless Motor Control {#arduino-brushless-motor-control}

<div align="center" markdown="1">

  <img loading="lazy" alt="DC Motor — illustration 46" src="/assets/img/legacy/arduino-bldc-motor-control-circuit-diagram-schematic-1024x558-ad9a8b371f.webp" width="50%" >

</div>

- **Brushless Motor (BLDC):**
  Converts electrical energy into rotational motion using electronic commutation instead of brushes.

- **ESC 30A (Electronic Speed Controller):**
  Controls the speed and direction of the BLDC motor by switching the current between motor phases; “30A” indicates it can handle up to 30 amps of current.

- **Li-Po Battery (Lithium-Polymer Battery):**
  Provides a lightweight, high-current power source for the ESC and motor.

- **Arduino Board:**
  Sends PWM control signals to the ESC, acting as the central controller of the system.

- **Potentiometer:**
  Functions as a variable resistor used to adjust the motor’s speed by changing the input signal to the Arduino.

- **Breadboard and Jump Wires:**
  Used to build and connect the electronic circuit temporarily without soldering.

### Arduino Code for BLDC {#arduino-code-for-bldc}

```c
/*
        Arduino Brushless Motor Control
     by Dejan, https://howtomechatronics.com
*/

#include <Servo.h>

Servo ESC;     // create servo object to control the ESC

int potValue;  // value from the analog pin

void setup() {
  // Attach the ESC on pin 9
  ESC.attach(9,1000,2000); // (pin, min pulse width, max pulse width in microseconds)
}

void loop() {
  potValue = analogRead(A0);   // reads the value of the potentiometer (value between 0 and 1023)
  potValue = map(potValue, 0, 1023, 0, 180);   // scale it to use it with the servo library (value between 0 and 180)
  ESC.write(potValue);    // Send the signal to the ESC
}
```

#### ✅ **Advantages** {#advantages-2}

1. **No brushes or mechanical commutator** – eliminating friction, wear, and sparking.
2. **High efficiency** – reduced mechanical losses.
3. **Quiet and smooth operation** – less noise and vibration.
4. **Longer life and reliability** – fewer mechanical parts to wear out.
5. **Precise speed and torque control** – thanks to electronic commutation.
6. **Quick dynamic response** – can accelerate or decelerate rapidly.

#### ❌ **Disadvantages** {#disadvantages-2}

1. **Higher cost** – need for the electronic controller and sensors.
2. **Design complexity** – more sophisticated control electronics and firmware.
3. **Thermal and demagnetization concerns** – excessive heat can weaken magnets or damage insulation.

### 🔩 **Applications** {#applications-2}

1. **Electric vehicles (EVs) and e-bikes** – for efficient propulsion.
2. **Drones and RC aircraft** – lightweight, high-speed motors.
3. **Computer cooling fans, HDDs, and optical drives** – quiet, reliable motion.
4. **Robotics and CNC machinery** – for precise motion control.
5. **Medical devices** – where quiet, reliable, and compact motors are needed.
6. **Household appliances** – e.g. washing machines, air conditioners.
7. **Industrial automation** – servo systems, actuators, and positioning modules.

## 3️⃣ Separately Excited DC Motor {#3-separately-excited-dc-motor}

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/separately-excited-dc-motor-af5c1c2df0.gif" alt="Separately Excited DC Motor">

<div markdown="1">

A **Separately Excited DC Motor** is a type of DC motor in which the **field winding** is powered by a **separate external DC source**, distinct from the supply to the armature.
This separation ensures that the armature current does not pass through the field winding, allowing independent control of flux (field strength) and armature current.
Thus, torque can be varied by adjusting the field flux ($Φ$), independently of the armature current ($Iₐ$).

</div>

</div>

Because the field and armature are driven from different supplies, the flux is (for practical design) often held nearly constant.
When a DC voltage is applied to the armature, it produces current Iₐ; the armature conducts in a magnetic field produced by the separately powered field winding, generating torque per the usual relation.
Voltage equation for the armature:

$$
V_a = E_b + I_a R_a
$$

where ($E_b$) is the back EMF, ($R_a$) is the armature resistance.
Because flux is assumed constant, **speed – armature current** and **torque – armature current** characteristics resemble those of a shunt motor.

#### ✅ **Advantages** {#advantages-3}

1. **Independent control of flux and armature current** – better flexibility in speed/torque control.
2. **Good speed regulation** – can maintain speed under varying loads by controlling field.
3. **Wide range of speed control** – by adjusting field voltage or armature voltage.
4. **Stable operation under load changes**.

#### ❌ **Disadvantages** {#disadvantages-3}

1. Needs **two separate power supplies**, increasing complexity and cost.
2. More **complicated circuitry** compared to motors where field and armature share supply.
3. Requires careful design to avoid instability when fields are weakened.

### 🔩 **Applications** {#applications-3}

- Industrial drives requiring precise speed control
- Machine tools
- Traction systems (locomotives)
- Rolling mills, printing machines
- Applications where wide speed range is required

## 4️⃣ Shunt DC Motor (Shunt WDM) {#4-shunt-dc-motor-shunt-wdm}

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/shunt-dc-motor-85da3148c8.gif" alt="Shunt DC Motor Diagram">

<div markdown="1">

A **Shunt Wound DC Motor** (or **Shunt DC Motor**) is a type of self-excited DC motor where the **field winding** is connected in **parallel (shunt)** with the **armature winding**.
Because both windings are supplied from the same voltage but have separate branches, the **field current (Iₑ or $I_sh$)** and **armature current (Iₐ)** flow independently.
The field winding has many turns of fine wire (higher resistance) so that only a small current flows through it, producing a relatively **constant magnetic flux**.

</div>

</div>

Since the flux is nearly constant, the speed variation with load is small, making the shunt motor a **constant speed motor**.
When load increases, speed tends to drop slightly, which causes **back EMF ($E_b$)** to fall, increasing armature current and thus torque to counter the load — this self-regulation helps maintain speed.
The voltage equation for the armature branch is:

$$V = E_b + I_a R_a$$

And since field circuit is parallel,

$$V = I_{sh} R_{sh}$$

where ($R_{sh}$) is the shunt field resistance.

#### ✅ **Advantages** {#advantages-4}

1. **Good speed regulation** under varying loads
2. **Relatively constant speed** — less speed drop under load
3. **Simple control of speed** by adjusting field current or armature voltage
4. **Stable operation** in many industrial applications

#### ❌ **Disadvantages** {#disadvantages-4}

1. Reduced torque when field current is weakened significantly
2. Starting torque is lower compared to series motors
3. Requires external resistance in armature circuit during start to limit current
4. If field winding opens (break), motor acts like series motor and speed can go dangerously high

### 🔩 **Applications** {#applications-4}

- Machine tools
- Lathes, drills, mills
- Fans, blowers
- Centrifugal pumps
- Mixers and conveyors
- Applications where **constant speed** is required even with varying load

## 5️⃣ Series DC Motor (Series WDM) {#5-series-dc-motor-series-wdm}

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/series-dc-motor-00f3964cd8.gif" alt="Series DC Motor Diagram">

<div markdown="1">

A **Series Wound DC Motor**, or simply a **Series DC Motor**, is a type of self-excited DC motor where the **field winding** is connected **in series** with the **armature winding**.
Because they are in series, the **same current** flows through both the field winding and the armature.

</div>

</div>

In a series motor, the field winding is designed with **fewer turns** of **thicker wire**, because it must carry the full armature current.
The magnetic flux ($Φ$) in the motor is approximately proportional to the armature current ($Iₐ$). As load increases, the armature current increases, which increases flux and hence torque.

The voltage (supply) equation is:

$$V = E_b + I (R_s + R_a)$$

where ($R_s$) is the series field winding resistance and ($R_a$) is armature resistance.

Because torque ($T ∝ Φ \cdot I$), and since ($Φ \propto I$), the torque is roughly proportional to ($I^2$). This gives **very high starting torque**.

However, **speed regulation is poor**: when load increases, current increases, flux increases, so speed drops significantly.

Also, **running the motor without load is dangerous**, because with very low current, flux drops and speed can increase excessively (overspeed).

#### ✅ **Advantages** {#advantages-5}

1. **Very high starting torque** — useful for heavy loads.
2. **Simple construction** — few design complications.
3. **Good for intermittent operation under heavy load.**

#### ❌ **Disadvantages** {#disadvantages-5}

1. **Poor speed regulation** — large speed variations with load.
2. **Cannot be run safely at no load** — risk of overspeed.
3. **Higher wear** on brushes and commutator due to high currents.
4. **Not suited for precision speed control.**

### 🔩 **Applications** {#applications-5}

- Traction systems like electric trains and trolleys
- Cranes, hoists, elevators
- Starter motors in automobiles
- Heavy load conveyors
- Lifting equipment and machines requiring strong torque at start

## 6️⃣ Compound DC Motor (CWDM) {#6-compound-dc-motor-cwdm}

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/dc-compound-motor-a453bc9759.gif" alt="Compound DC Motor">

<div markdown="1">

A **Compound Wound DC Motor** (also called a **DC Compound Motor**) is a self-excited DC motor that uses **both series and shunt field windings** to produce its magnetic flux.
This design combines the high starting torque of a series-wound motor with the good speed regulation of a shunt-wound motor.
In a compound motor, part of the field winding is connected **in series** with the armature, and part is connected in **parallel (shunt)** with the armature.

</div>

</div>

Depending on how the windings are connected and how their fluxes interact, compound motors may be **cumulatively compounded** (series and shunt fluxes aid each other) or **differentially compounded** (fluxes oppose each other).
They can also be categorized by connection style into **long-shunt** and **short-shunt** compounds, depending on whether the shunt winding bypasses the series winding or not.

<div markdown="1">

  <img loading="lazy" src="/assets/img/legacy/dc-compound-motor-2-13-2-15-cdd7d946a6.gif" alt="Compound DC Motor Circuit">

<div markdown="1">

In operation, both field windings generate flux. The **series field** contributes flux proportional to armature current, giving high torque at startup; the **shunt field** provides a relatively constant flux that helps stabilize speed under varying load.
Because of this dual contribution, the motor can maintain a more constant speed under load changes than a pure series motor, while still delivering higher starting torque than a pure shunt motor.

</div>

</div>

#### ✅ **Advantages** {#advantages-6}

1. **High starting torque** – thanks to the series winding component.
2. **Better speed regulation** – owing to the shunt winding flux.
3. **Versatile performance** – the compound motor's behavior can be tailored by adjusting the ratio of series to shunt flux.
4. **Reduced risk of overspeed** – the shunt field helps prevent runaway when load is light.

#### ❌ **Disadvantages** {#disadvantages-6}

1. **More complex construction** – requires both series and shunt windings, more design effort.
2. **Higher cost** – more materials and winding work.
3. **Compensation trade-offs** – differential compounding can cause unstable performance; improper design might reduce regulation or torque.
4. **Maintenance considerations** – more winding parts to inspect over time.

### 🔩 **Applications** {#applications-6}

1. **Rolling mills** – where starting torque and stable speed under load are needed.
2. **Elevators and hoists** – to lift loads smoothly with control.
3. **Press machines, shears, and stamping machines** – for high torque at start and stable speed in operation.
4. **Printing presses and conveyors** – where variable loads occur but speed stability is important.
5. **Cranes and large machinery** – in industrial settings requiring both torque and regulation.

# References

<a href="https://www.electronics-tutorials.ws/dc/dcmotors.html" target="_blank">
<strong>Electronics Tutorials – DC Motors</strong>
</a>

<a href="https://en.wikipedia.org/wiki/DC_motor" target="_blank">
<strong>Wikipedia – DC Motor</strong>
</a>

<a href="https://circuitdigest.com/tutorial/dc-motor-working-and-types-of-dc-motor" target="_blank">
<strong>Circuit Digest – Working and Types of DC Motor</strong>
</a>

<a href="https://www.electrical4u.com/dc-motor-types-and-characteristics/" target="_blank">
<strong>Electrical4U – DC Motor Types and Characteristics</strong>
</a>

<a href="https://www.elprocus.com/dc-motor-working-principle-types-and-its-applications/" target="_blank">
<strong>Elprocus – DC Motor Working Principle, Types, and Applications</strong>
</a>

<a href="https://www.theengineeringknowledge.com/dc-motor-types-working-applications/" target="_blank">
<strong>The Engineering Knowledge – DC Motor: Types, Working & Applications</strong>
</a>

# 🎥 Video References

The GIFs and visual animations in this article are adapted from reputable YouTube educational sources for better understanding of DC motor concepts:

- [**Jared Owen**](https://www.youtube.com/@JaredOwen)
- [**The Science Works**](https://www.youtube.com/@TheScienceWorks)
- [**Sabin Civil Engineering**](https://www.youtube.com/@SabinCivilEngineering)
  {% endraw %}
