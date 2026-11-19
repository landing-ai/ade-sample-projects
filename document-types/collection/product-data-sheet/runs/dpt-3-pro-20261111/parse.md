# Preliminary Datasheet
Subject to change without notice

[logo: Wolfspeed]

# HAB900C33LM4

3300 V, 900 A, Silicon Carbide, Half-Bridge Module

- **V<sub>DS</sub>**: 3300 V
- **R<sub>DS(on)</sub>**: 2 mΩ

## **Technical Features**

* Fully SiC MOSFET-based for Ultra-Low Loss
* Industry-Compatible Package Footprint
* High Junction Temperature (175 °C) Operation
* Low Stray Inductance (<10 nH)
* Soft Reverse Recovery from Gen 4 Body Diode
* Sintered Die Attach and Copper Die Top System
* Low-Thermal Resistance Copper Baseplate

**Typical Applications**

* Solar & Wind-Power Infrastructure
* Grid-Scale Energy Storage
* Rail Traction
* Heavy-Duty E-Mobility: Transportation and Mining
* Marine and Aerospace Propulsion

**System Benefits**

* Increased System Efficiency due to Low Switching & Conduction Losses of SiC
* Improved Power Cycling Capabilities for Increased System Lifetime
* Enhanced Durability and Reduced System Cost
* Enables Two-level Conversion for 2000 V or Greater DC Systems

## Maximum Parameters (Verified by Design)

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr>
<tr><td>Drain-Source Voltage</td><td>V<sub>DS</sub></td><td></td><td></td><td>3300</td><td rowspan="3">V</td><td></td><td></td></tr>
<tr><td>Gate-Source Voltage, Maximum Value</td><td>V<sub>GS(max)</sub></td><td>-10</td><td></td><td>23</td><td>Transient</td><td rowspan="2">Note 1<br>Fig. 16</td></tr>
<tr><td>Gate-Source Voltage, Recommended</td><td>V<sub>GS(op)</sub></td><td></td><td>-5/+18</td><td></td><td>Static</td></tr>
<tr><td rowspan="2">DC Continuous Drain Current</td><td rowspan="2">I<sub>D</sub></td><td></td><td></td><td>1200</td><td rowspan="4">A</td><td>V<sub>GS</sub> = 18 V, T<sub>C</sub> = 25 °C, T<sub>VJ</sub> ≤ 175 °C</td><td rowspan="4">Notes<br>2, 3, 4<br>Fig. 11</td></tr>
<tr><td></td><td>908</td><td></td><td>V<sub>GS</sub> = 18 V,  T<sub>C</sub> = 90 °C, T<sub>VJ</sub> ≤ 175 °C</td></tr>
<tr><td>DC Source-Drain Current (Body Diode)</td><td>I<sub>SD(BD)</sub></td><td></td><td>876</td><td></td><td>V<sub>GS</sub> = -5 V,  T<sub>C</sub> = 90 °C, T<sub>VJ</sub> ≤ 175 °C</td></tr>
<tr><td>Pulsed Drain-Source Current</td><td>I<sub>DM</sub></td><td></td><td></td><td>3600</td><td>t<sub>Pmax</sub> limited by T<sub>VJmax</sub><br>V<sub>GS</sub> = 18 V,  T<sub>C</sub> = 25 °C</td></tr>
<tr><td>Power Dissipation</td><td>P<sub>D</sub></td><td></td><td>7282</td><td></td><td>W</td><td>T<sub>C</sub> = 25 °C, T<sub>VJ</sub> ≤ 175 °C</td><td>Note 5<br>Fig. 12</td></tr>
<tr><td>Virtual Junction Temperature</td><td>T<sub>VJ(op)</sub></td><td>-55</td><td></td><td>175</td><td>°C</td><td></td><td></td></tr>
</table>

Note (1): Recommended turn-on gate voltage is 18 V with ±5 % regulation tolerance
Note (2): Current limit at T<sub>C</sub> = 25 °C imposed by package
Note (3): Typical current limit calculated by I<sub>D(max)</sub> = √(P<sub>D</sub>/R<sub>DS(typ)</sub>(T<sub>VJ(max)</sub>,I<sub>D(max)</sub>))
Note (4): Verified by design
Note (5): P<sub>D</sub> = (T<sub>VJ</sub> - T<sub>C</sub>)/R<sub>TH(JC,typ)</sub>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice..

<!-- PAGE BREAK -->

HAB900C33LM4

**Preliminary Datasheet**
**Subject to change without notice**

[logo] 2

**MOSFET Characteristics (Per Position) (T<sub>VJ</sub> = 25 °C Unless Otherwise Specified)**

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr>
<tr><td>Drain-Source Breakdown Voltage</td><td>V<sub>(BR)DSS</sub></td><td>3300</td><td></td><td></td><td rowspan="3">V</td><td>V<sub>GS</sub> = 0 V, T<sub>VJ</sub> = -55 °C</td><td></td></tr>
<tr><td rowspan="2">Gate Threshold Voltage</td><td rowspan="2">V<sub>GS(th)</sub></td><td>2.6</td><td>3.5</td><td>4.4</td><td>V<sub>DS</sub> = V<sub>GS</sub>, I<sub>D</sub> = 530 mA</td><td></td></tr>
<tr><td></td><td>2.6</td><td></td><td>V<sub>DS</sub> = V<sub>GS</sub>, I<sub>D</sub> = 530 mA, T<sub>VJ</sub> = 175 °C</td><td></td></tr>
<tr><td>Zero Gate Voltage Drain Current</td><td>I<sub>DSS</sub></td><td></td><td>20</td><td>400</td><td>μA</td><td>V<sub>GS</sub> = 0 V, V<sub>DS</sub> = 3300 V</td><td></td></tr>
<tr><td>Gate-Source Leakage Current</td><td>I<sub>GSS</sub></td><td></td><td>200</td><td>5000</td><td>nA</td><td>V<sub>GS</sub> = 18 V, V<sub>DS</sub> = 0 V</td><td></td></tr>
<tr><td rowspan="2">Drain-Source On-State Resistance<br>(Devices Only)</td><td rowspan="2">R<sub>DS(on)</sub></td><td></td><td>2.0</td><td>2.6</td><td rowspan="2">mΩ</td><td>V<sub>GS</sub> = 18 V, I<sub>D</sub> = 900 A</td><td rowspan="2">Fig. 2<br>Fig. 3</td></tr>
<tr><td></td><td>5.0</td><td></td><td>V<sub>GS</sub> = 18 V, I<sub>D</sub> = 900 A, T<sub>VJ</sub> = 175 °C</td></tr>
<tr><td rowspan="2">Transconductance</td><td rowspan="2">g<sub>fs</sub></td><td></td><td>617</td><td></td><td rowspan="2">S</td><td>V<sub>DS</sub> = 20 V, I<sub>DS</sub> = 900 A</td><td rowspan="2">Fig. 4</td></tr>
<tr><td></td><td>619</td><td></td><td>V<sub>DS</sub> = 20 V, I<sub>DS</sub> = 900 A, T<sub>VJ</sub> = 175 °C</td></tr>
<tr><td>Internal Gate Resistance</td><td>R<sub>G(int)</sub></td><td></td><td>0.5</td><td></td><td>Ω</td><td>f = 100 kHz</td><td></td></tr>
<tr><td>Input Capacitance</td><td>C<sub>iss</sub></td><td></td><td>159.9</td><td></td><td rowspan="2">nF</td><td rowspan="3">V<sub>GS</sub> = 0 V, V<sub>DS</sub> = 1800 V,<br>V<sub>AC</sub> = 25 mV, f = 100 kHz</td><td rowspan="3">Fig. 9</td></tr>
<tr><td>Output Capacitance</td><td>C<sub>oss</sub></td><td></td><td>2.4</td><td></td></tr>
<tr><td>Reverse Transfer Capacitance</td><td>C<sub>rss</sub></td><td></td><td>6.7</td><td></td><td>pF</td></tr>
<tr><td>FET Thermal Resistance, Junction to Heatsink</td><td>R<sub>th JHS</sub></td><td></td><td>0.021</td><td></td><td>°C/W</td><td></td><td></td></tr>
</table>

**Diode Characteristics (Per Position) (T<sub>VJ</sub> = 25 °C Unless Otherwise Specified)**

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr>
<tr><td rowspan="2">Body Diode Forward Voltage</td><td rowspan="2">V<sub>SD</sub></td><td></td><td>5.7</td><td></td><td rowspan="2">V</td><td>V<sub>GS</sub> = -5 V, I<sub>SD</sub> = 900 A</td><td rowspan="2">Fig. 7</td></tr>
<tr><td></td><td>4.7</td><td></td><td>V<sub>GS</sub> = -5 V, I<sub>SD</sub> = 900 A, T<sub>VJ</sub> = 175 °C</td></tr>
</table>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>®</sup>, the Wolfspeed logo, the Wolfstreak logo, WolfPACK<sup>®</sup>, Wolfspeed WolfPACK<sup>®</sup>, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

# Preliminary Datasheet
Subject to change without notice

[logo] 3

**Module Physical Characteristics**

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td></tr>
<tr><td>Package Resistance</td><td>R<sub>pkg</sub></td><td></td><td>0.19</td><td></td><td>mΩ</td><td>T<sub>C</sub> = 25 °C, Note 6</td></tr>
<tr><td>Stray Inductance</td><td>L<sub>Stray</sub></td><td></td><td>9.5</td><td></td><td>nH</td><td>Between DC+ and DC-, f = 10 MHz</td></tr>
<tr><td>Storage Temperature</td><td>T<sub>Stg</sub></td><td>-55</td><td></td><td>150</td><td>°C</td><td></td></tr>
<tr><td>Weight</td><td>W</td><td></td><td>745</td><td></td><td>g</td><td></td></tr>
<tr><td rowspan="3">Mounting Torque</td><td rowspan="3">M<sub>s</sub></td><td>3.5</td><td>4.5</td><td>5.5</td><td rowspan="3">N-m</td><td>Baseplate, M6 bolts</td></tr>
<tr><td>8</td><td>12</td><td>16</td><td>Power Terminals, M8 bolts</td></tr>
<tr><td>0.5</td><td>0.7</td><td>1.3</td><td>Auxiliary Terminals, M3 bolts</td></tr>
<tr><td>Case Isolation Voltage</td><td>V<sub>isol</sub></td><td>6</td><td></td><td></td><td>kV</td><td>AC, 50 Hz, 1 min</td></tr>
<tr><td>Comparative Tracking Index</td><td>CTI</td><td>600</td><td></td><td></td><td></td><td></td></tr>
<tr><td rowspan="2">Clearance Distance</td><td rowspan="2"></td><td></td><td>11</td><td></td><td rowspan="4">mm</td><td>Terminal to Terminal</td></tr>
<tr><td></td><td>33</td><td></td><td>Terminal to Baseplate</td></tr>
<tr><td rowspan="2">Creepage Distance</td><td rowspan="2"></td><td></td><td>23</td><td></td><td>Terminal to Terminal</td></tr>
<tr><td></td><td>45</td><td></td><td>Terminal to Baseplate</td></tr>
</table>

Note (6): Total Effective Resistance (Per Switch Position) = MOSFET R<sub>DS(on)</sub> + Switch Position Package Resistance

**Temperature Sensor (NTC) Characteristics**

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Test Conditions</td></tr>
<tr><td>Resistance at 25 °C</td><td>R<sub>25</sub></td><td></td><td>4700</td><td></td><td>Ω</td><td>T<sub>NTC</sub> = 25 °C</td></tr>
<tr><td>Tolerance of R<sub>25</sub></td><td></td><td></td><td>±1</td><td></td><td>%</td><td></td></tr>
<tr><td>Beta Value for 25 °C to 85 °C</td><td>B<sub>25/80</sub></td><td></td><td>3435</td><td></td><td>K</td><td></td></tr>
<tr><td>Beta Value for 0 °C to 100 °C</td><td>B<sub>0/100</sub></td><td></td><td>3399</td><td></td><td>K</td><td></td></tr>
<tr><td>Tolerance of B<sub>25/85</sub></td><td></td><td></td><td>±1</td><td></td><td>%</td><td></td></tr>
<tr><td>Maximum Power Dissipation</td><td>P<sub>25</sub></td><td></td><td>50</td><td></td><td>mW</td><td>T<sub>NTC</sub> = 25°C</td></tr>
</table>

**Steinhart & Hart Coefficients for NTC Resistance & NTC Temperature Computation (T in K)**

$$\ln\left(\frac{R}{R_{25}}\right) = A + \frac{B}{T} + \frac{C}{T^2} + \frac{D}{T^3} \qquad \frac{1}{T} = A_1 + B_1\ln\left(\frac{R}{R_{25}}\right) + C_1\ln^2\left(\frac{R}{R_{25}}\right) + D_1\ln^3\left(\frac{R}{R_{25}}\right)$$

<table>
<tr><td>A</td><td>B</td><td>C</td><td>D</td><td>A<sub>1</sub></td><td>B<sub>1</sub></td><td>C<sub>1</sub></td><td>D<sub>1</sub></td></tr>
<tr><td>-1.289E+01</td><td>4.245E+03</td><td>-8.749E+04</td><td>-9.588E+06</td><td>3.354E-03</td><td>3.001E-04</td><td>5.085E-06</td><td>2.188E-07</td></tr>
</table>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

# Preliminary Datasheet
Subject to change without notice

[logo] 4

<figure type="CHART">Typical Performance



<description>Line chart titled Figure 1 showing output characteristics for various junction temperatures. Axes: x-axis labeled Drain-Source Voltage, VDS (V), ticks 0 to 7 in steps of 1; y-axis labeled Drain-Source Current, IDS (A), ticks 0 to 2400 in steps of 400. Inset box at upper left reads tp < 350 µs and VGS = 18 V. Six straight lines radiate from the origin (0,0). The steepest two lines are labeled -40 °C and 25 °C, reaching about 2400 A at roughly 3.3 V and 5.0 V respectively. A fourth line from (1.5 V, about 1880 A) descends to (6.3 V, about 280 A) and is labeled -40 °C near its start, with labels 100 °C, 125 °C, 150 °C and 175 °C along the lower lines, which reach about 1950 A, 1620 A, 1400 A and 1200 A at 7 V respectively. Caption below reads: Figure 1. Output Characteristics for Various Junction Temperatures.</description>

<table><tr><th>Junction Temperature</th><th>Approx. VDS at IDS = 2400 A</th><th>Approx. IDS at VDS = 7 V</th></tr><tr><td>-40 °C</td><td>about 3.3 V</td><td>not reached within range (line terminates near 1.5 V to 6.3 V segment)</td></tr><tr><td>25 °C</td><td>about 5.0 V</td><td>not reached within range</td></tr><tr><td>100 °C</td><td>not reached</td><td>about 1950 A</td></tr><tr><td>125 °C</td><td>not reached</td><td>about 1620 A</td></tr><tr><td>150 °C</td><td>not reached</td><td>about 1400 A</td></tr><tr><td>175 °C</td><td>not reached</td><td>about 1200 A</td></tr></table></figure>

<table>
<tr><td rowspan="10">Normalized On-resistance (p.u.)</td><td></td><td>tp &lt; 350 µs</td><td></td><td></td><td></td><td></td></tr>
<tr><td rowspan="2">2.5</td><td>V<sub>GS</sub> = 18 V</td><td></td><td>175 °C</td><td>[image: curve line]</td><td>[image: curve line]</td></tr>
<tr><td>[image: curve line]</td><td>[image: curve line]</td><td>[image: curve line]</td><td></td><td></td></tr>
<tr><td rowspan="2">2.0</td><td>[image: curve line]</td><td rowspan="2"></td><td rowspan="3">150 °C<br>125 °C<br>100 °C</td><td>[image: curve line]</td><td>[image: curve line]</td></tr>
<tr><td rowspan="2"></td><td>[image: curve line]</td><td>[image: curve line]</td></tr>
<tr><td rowspan="3">1.5<br>1.0</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td>25 °C</td><td></td><td></td></tr>
<tr><td></td><td></td><td>0 °C</td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>0.5</td><td></td><td></td><td>-40 °C</td><td></td><td></td></tr>
</table>

0 500 1000 1500 2000

Drain-Source Current, I<sub>DS</sub> (A)

**Figure 2.** Normalized On-State Resistance vs. Drain Current for Various Junction Temperatures

<figure type="CHART">**Figure 3.** Normalized On-State Resistance vs. Junction Temperature



<description>Line chart showing Normalized On-resistance (p.u.) on the y-axis (0.0 to 3.0, ticks every 0.5) versus Virtual Junction Temperature, T_VJ (°C), on the x-axis (-50 to 200, ticks every 25). A grid is present. An info box in the upper left reads: tp < 350 µs, V_GS = 18 V, I_DS = 900 A. A single black curve starts at about 0.68 p.u. at -40 °C, rises through about 0.85 at 0 °C, 1.0 at 25 °C, 1.2 at 50 °C, 1.4 at 75 °C, 1.6 at 100 °C, 1.9 at 125 °C, 2.15 at 150 °C, and ends at about 2.5 p.u. at 175 °C, with a convex upward (accelerating) slope.</description>

<table><thead><tr><th>Virtual Junction Temperature, T_VJ (°C)</th><th>Normalized On-resistance (p.u.)</th></tr></thead><tbody><tr><td>-40</td><td>0.68</td></tr><tr><td>0</td><td>0.85</td></tr><tr><td>25</td><td>1.00</td></tr><tr><td>50</td><td>1.18</td></tr><tr><td>75</td><td>1.38</td></tr><tr><td>100</td><td>1.60</td></tr><tr><td>125</td><td>1.85</td></tr><tr><td>150</td><td>2.15</td></tr><tr><td>175</td><td>2.50</td></tr></tbody></table></figure>

<figure type="CHART">Figure 4. Transfer Characteristic for Various Junction Temperatures



<description>Line chart titled with a boxed note at top-left reading "tp < 350 µs" and "V_DS = 20 V". X-axis: "Gate-Source Voltage, V_GS (V)" ranging from 0 to 8 (ticks at 0, 2, 4, 6, 8). Y-axis: "Drain-Source Current, I_DS (A)" ranging from 0 to 2400 (ticks at 0, 400, 800, 1200, 1600, 2000, 2400). Light gray grid lines. Six curves start near zero around V_GS 2.5 to 3 V and rise steeply with increasing V_GS. An arrow pointing toward upper-left labeled 175 °C, 150 °C, 125 °C, 100 °C, 25 °C, and -40 °C indicates temperature ordering: the curves for 175 °C, 150 °C, 125 °C, and 100 °C are the top-left cluster reaching 2400 A near V_GS 8-9 V, the 25 °C curve crosses about 800 A near V_GS 6 V, and the -40 °C curve is the lowest, reaching about 1200 A at V_GS 9 V. Curves are black, solid, and nearly parallel at high current.</description></figure>

<figure type="CHART">**Figure 5.** 3<sup>rd</sup> Quadrant Characteristic vs. Junction Temperatures at V<sub>GS</sub> = 18 V



<description><table><thead><tr><th>Source-Drain Voltage, V<sub>SD</sub> (V)</th><th>Source-Drain Current, I<sub>SD</sub> (A) at -40 °C (approx.)</th><th>at 25 °C (approx.)</th><th>at 100 °C (approx.)</th><th>at 125 °C (approx.)</th><th>at 150 °C (approx.)</th><th>at 175 °C (approx.)</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>400</td><td>580</td><td>270</td><td>250</td><td>240</td><td>210</td></tr><tr><td>2</td><td>1200</td><td>1150</td><td>550</td><td>520</td><td>500</td><td>440</td></tr><tr><td>3</td><td>2000</td><td>1700</td><td>850</td><td>800</td><td>760</td><td>680</td></tr><tr><td>4</td><td>-</td><td>-</td><td>1150</td><td>1080</td><td>1030</td><td>930</td></tr><tr><td>5</td><td>-</td><td>-</td><td>1450</td><td>1380</td><td>1300</td><td>1170</td></tr><tr><td>6</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>1400</td></tr><tr><td>8</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr></tbody></table>Chart axes: X-axis Source-Drain Voltage, V<sub>SD</sub> (V), 0 to 8; Y-axis Source-Drain Current, I<sub>SD</sub> (A), 0 to 2400. Note inside plot: tp &lt; 350 µs, V<sub>GS</sub> = 18 V. Curves are labeled -40 °C, 25 °C, 100 °C, 125 °C, 150 °C, and 175 °C; the -40 °C and 25 °C curves are the steepest, rising to about 2400 A near 3 V and 3.2 V respectively, while the 100 °C to 175 °C curves form a fan of progressively shallower lines, with 175 °C the lowest and ending near 380 A at about 6.8 V.</description></figure>

<figure type="CHART">Figure 6. 3rd Quadrant Characteristic vs. Junction Temperatures at VGS = 0 V (Body Diode)



<description>Line chart with x-axis labeled "Source-Drain Voltage, VSD (V)" ranging 0 to 8 with ticks at every 1 V, and y-axis labeled "Source-Drain Current, ISD (A)" ranging 0 to 2400 A with ticks at every 400 A. Inset box at upper left reads "tp < 300 µs" and "VGS = 0 V". Six curves rise from near zero current at about 1.5 to 2 V; they converge near 2.5 to 3 V at roughly 200 A, then diverge. The -40 °C curve is the steepest, reaching about 2400 A near 7 V, with the 25 °C curve close behind. Curves for 100 °C, 125 °C, 150 °C and 175 °C are progressively lower, ending near 1650, 1500, 1400 and 1350 A at 8 V. Curve labels -40 °C, 25 °C, 100 °C, 125 °C, 150 °C and 175 °C are placed along a downward-sloping arrow running from upper left to lower right, indicating decreasing temperature order from top-left to bottom-right.</description></figure>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

# Preliminary Datasheet
Subject to change without notice

[logo]
5

<figure type="CHART">Typical Performance



<description>Line chart titled Figure 7. 3rd Quadrant Characteristic vs. Junction Temperatures at VGS = -5 V (Body Diode). X-axis: Source-Drain Voltage, VSD (V), ticks 0 to 7. Y-axis: Source-Drain Current, ISD (A), ticks 0 to 2400 in steps of 400. Inset box in upper left reads tp < 350 µs, VGS = -5 V. Curves start near 0 current at about 2.3 V and rise nonlinearly. Five curves labeled 175 °C, 150 °C, 100 °C, 25 °C and -40 °C; the 175 °C curve is steepest and reaches the top of the plot near 2400 A at about 6.6 V, 150 °C reaches about 1900 A at 7 V, a dashed curve (100 °C) and the 25 °C and -40 °C curves finish near 1450 to 1600 A at 7 V, with -40 °C the lowest at about 1000 A at 6.5 V region. A large arrow runs from the lower right toward the upper left indicating increasing temperature.</description>

<table><tr><th>Source-Drain Voltage VSD (V)</th><th>Approx. Source-Drain Current ISD (A) at 175 °C</th><th>Approx. ISD (A) at 150 °C</th><th>Approx. ISD (A) at 100 °C</th><th>Approx. ISD (A) at 25 °C</th><th>Approx. ISD (A) at -40 °C</th></tr><tr><td>3</td><td>~250</td><td>~200</td><td>~150</td><td>~120</td><td>~80</td></tr><tr><td>4</td><td>~700</td><td>~600</td><td>~500</td><td>~420</td><td>~350</td></tr><tr><td>5</td><td>~1200</td><td>~1050</td><td>~900</td><td>~800</td><td>~700</td></tr><tr><td>6</td><td>~1800</td><td>~1500</td><td>~1400</td><td>~1400</td><td>~1100</td></tr><tr><td>7</td><td>~2400</td><td>~1900</td><td>~1500</td><td>~1550</td><td>~1600</td></tr></table></figure>

<figure type="CHART">**Figure 8.** Typical Capacitances vs. Drain to Source Voltage (0 - 200 V)


<description>Log-scale line chart of Capacitance (nF) on the vertical axis (ticks 0.01, 0.1, 1, 10, 100, 1000) versus Drain-Source Voltage, V_DS (V) on the horizontal axis (ticks 0, 50, 100, 150, 200). A text box in the plot reads T_VJ = 25 °C, V_AC = 25 mV, f = 100 kHz. Three curves are labeled: C_iss starts near 200 nF at 0 V, dropping quickly to about 170 nF and staying nearly flat to 200 V; C_oss starts near 70 nF at 0 V, falls to about 5 nF at 50 V, and decreases gradually to about 2.3 nF at 200 V; C_rss starts near 60 nF at 0 V, falls to about 1.8 nF at 20 V, about 0.4 nF at 50 V, about 0.1 nF at 150 V, and ends near 0.06 nF at 200 V.</description>
<table><tr><th>V_DS (V)</th><th>C_iss (nF)</th><th>C_oss (nF)</th><th>C_rss (nF)</th></tr><tr><td>0</td><td>~200</td><td>~70</td><td>~60</td></tr><tr><td>20</td><td>~175</td><td>~20</td><td>~1.8</td></tr><tr><td>50</td><td>~170</td><td>~5</td><td>~0.4</td></tr><tr><td>100</td><td>~170</td><td>~3.5</td><td>~0.2</td></tr><tr><td>150</td><td>~170</td><td>~2.7</td><td>~0.1</td></tr><tr><td>200</td><td>~170</td><td>~2.3</td><td>~0.06</td></tr></table></figure>

<figure type="CHART">**Figure 9.** Typical Capacitances vs. Drain to Source Voltage (0 - 3300V)



<description><table><tr><th>Drain-Source Voltage, V_DS (V)</th><th>Ciss (nF, approx.)</th><th>Coss (nF, approx.)</th><th>Crss (nF, approx.)</th></tr><tr><td>0</td><td>~150</td><td>~100</td><td>~100</td></tr><tr><td>100</td><td>~150</td><td>~5</td><td>~0.5</td></tr><tr><td>500</td><td>~150</td><td>~4</td><td>~0.2</td></tr><tr><td>1000</td><td>~150</td><td>~3</td><td>~0.1</td></tr><tr><td>1500</td><td>~150</td><td>~2.5</td><td>~0.08</td></tr><tr><td>2000</td><td>~150</td><td>~2.3</td><td>~0.07</td></tr><tr><td>2500</td><td>~150</td><td>~2.2</td><td>~0.06</td></tr><tr><td>3000</td><td>~150</td><td>~2.1</td><td>~0.06</td></tr><tr><td>3300</td><td>~150</td><td>~2.1</td><td>~0.06</td></tr></table>

<description>Line chart with log-scale y-axis Capacitance (nF) from 0.01 to 1000 and linear x-axis Drain-Source Voltage, V_DS (V) from 0 to 3300. Three curves are labeled: Ciss is nearly flat at about 150 nF across the full range; Coss drops steeply from about 100 nF near 0 V to about 2 nF by 3300 V; Crss drops steeply from about 100 nF near 0 V to about 0.06 nF by 3300 V. A box in the upper right reads T_VJ = 25 °C, V_AC = 25 mV, f = 100 kHz.</description></figure>

<figure type="CHART">**Figure 10.** Threshold Voltage vs. Junction Temperature



<description>Line chart showing Threshold Voltage, V_TH (V) on the y-axis (0 to 6, gridlines every 1 V) versus Virtual Junction Temperature, T_VJ (°C) on the x-axis (-50 to 200, ticks every 25 °C). A text box in the upper left reads "V_GS = V_DS, I_DS = 530 mA". A single black curve starts at about 4.2 V at -40 °C, decreases gradually to about 3.7 V at 0 °C, about 3.5 V at 25 °C, about 3.1 V at 100 °C, and ends at about 2.75 V near 175 °C, with a slightly steeper slope at low temperatures.</description>

<table><thead><tr><th>Virtual Junction Temperature, T_VJ (°C)</th><th>Threshold Voltage, V_TH (V)</th></tr></thead><tbody><tr><td>-40</td><td>4.2</td></tr><tr><td>-25</td><td>4.0</td></tr><tr><td>0</td><td>3.7</td></tr><tr><td>25</td><td>3.5</td></tr><tr><td>50</td><td>3.35</td></tr><tr><td>75</td><td>3.2</td></tr><tr><td>100</td><td>3.1</td></tr><tr><td>125</td><td>2.95</td></tr><tr><td>150</td><td>2.85</td></tr><tr><td>175</td><td>2.75</td></tr></tbody></table></figure>

<figure type="CHART">Figure 11. Continuous Drain Current Derating vs. Case Temperature

<description>Line chart with grid. X-axis: Case Temperature, TC (°C), ticks from -75 to 175 in steps of 25. Y-axis: Drain-Source DC Current, IDS (DC) (A), ticks from 0 to 1600 in steps of 200. Solid black curve: flat horizontal segment labeled 'Package Limit' at 1200 A from about -50 °C to 25 °C, then a curve decreasing from about 1200 A at 25 °C through about 850 A at 100 °C to about 500 A at 150 °C, where it drops vertically to 0 A at 150 °C. Dashed black line: continues the derating slope from about 1480 A at -55 °C down to the 1200 A point at 25 °C. Box in upper right labeled 'Conditions: TVJ ≤ 175 °C'.</description><table><thead><tr><th>Case Temperature TC (°C)</th><th>Drain-Source DC Current IDS (A)</th></tr></thead><tbody><tr><td>-55</td><td>1480</td></tr><tr><td>-50</td><td>1200</td></tr><tr><td>25</td><td>1200</td></tr><tr><td>50</td><td>1100</td></tr><tr><td>75</td><td>980</td></tr><tr><td>100</td><td>850</td></tr><tr><td>125</td><td>700</td></tr><tr><td>150</td><td>500</td></tr><tr><td>150</td><td>0</td></tr></tbody></table></figure>

<figure type="CHART">Figure 12. Maximum Power Dissipation Derating vs. Case Temperature



<description><table><tr><th>Case Temperature, T_C (°C)</th><th>FET Power Dissipation, P_D (W)</th></tr><tr><td>-55</td><td>11100</td></tr><tr><td>-25</td><td>9700</td></tr><tr><td>0</td><td>8400</td></tr><tr><td>25</td><td>7200</td></tr><tr><td>50</td><td>6000</td></tr><tr><td>75</td><td>4800</td></tr><tr><td>100</td><td>3700</td></tr><tr><td>125</td><td>2500</td></tr><tr><td>150</td><td>1200</td></tr></table>Conditions: T_VJ ≤ 175 °C. Line chart with a single straight descending line from about 11100 W at -55 °C to about 1200 W at 150 °C, plotted on gridded axes with y-axis from 0 to 12000 W and x-axis from -75 to 175 °C.</description></figure>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

**Preliminary Datasheet**
**Subject to change without notice**

[logo] 6

<figure type="CHART">**Definitions**

**Figure 13.** Turn-off Transient Definitions



<description>Line chart showing turn-off transient waveforms over time with three traces. The top purple trace is Gate – Source Voltage, V_GS (V), starting high in a flat region, labeled 90% V_GS at its falling edge, then decreasing gradually and leveling off at a lower value. The middle dark blue trace is Drain – Source Voltage, V_DS (V), starting low, rising sharply after the gate transition to a peak, then settling at a high plateau. The bottom cyan trace is Source Current, I_S (A), starting high, falling sharply through a peak region, then dropping to a low baseline. Horizontal dashed reference lines and bracket annotations mark intervals: t_d(off) spans from the gate 90% point to the start of the current fall; t_f is marked near the current fall; t_off spans the full turn-off interval from the gate 90% point to the end of the current fall. Labels mark 90% I_S and 10% I_S on the current trace, 10% V_DS on the drain trace, and dv/dt_OFF and di/dt_OFF as peak rate-of-change markers on the transition. A bracket labeled E_OFF = ∫ V_DS x I_S spans the overlap of voltage and current. Footnote: *Peak rate of change for a sliding 5 ns window.</description></figure>

<figure type="CHART">Figure 14. Turn-on Transient Definitions



<description>This is a timing waveform chart showing turn-on transient definitions with time on the horizontal axis and voltage/current on the vertical axis. Three curves are plotted: Gate – Source Voltage, V_GS (V) in purple, rising from a low baseline on the left to a high plateau on the right, with a horizontal reference line at its 10% level and a sharp rise around the center; Source Current, I_S (A) in light cyan, staying high on the left, dropping sharply in the middle, then spiking and ringing with oscillations before settling at a moderate level on the right, with markers at 10% I_S and 90% I_S; Drain – Source Voltage, V_DS (V) in dark blue, starting low on the left, rising sharply in the middle, then dropping with ringing oscillations to a low level on the right, with a marker at 10% V_DS. Dashed vertical guide lines delimit the time intervals t_d(on), t_on, and t_r, and a double-headed arrow labeled E_ON = ∫ V_DS x I_S spans the switching interval at the bottom. Two markers labeled *di/dt_ON and dv/dt_ON* point to the steepest transition region, with a footnote reading *Peak rate of change for a sliding 5 ns window.</description></figure>

<figure type="CHART">**Figure 15.** Reverse Recovery Definitions

Reverse Recovery Current, I_RR (A)



<description>Line chart of reverse recovery current versus time. The curve starts at a flat plateau labeled I_F on the left y-axis, then falls steeply through a 0 A crossing, reaches a negative trough labeled I_RRM, rises back through a second 0 A crossing, and then oscillates with decaying amplitude around the zero line. A dashed bracket marked t_rr spans from the first 0 A crossing to the second, subdivided into t_f (falling interval, left) and t_s (storage/softer interval, right). A hatched region between the curve and zero line, labeled Q_RR, fills the area between the two crossings below zero. A tick-marked slope annotation *di/dt_RR sits on the steep falling edge near the first crossing. A footnote at lower left reads: *Peak rate of change for a sliding 5 ns window during the falling event</description></figure>

<figure type="CHART">**Figure 16.** V<sub>GS</sub> Transient Definitions



<description>Line chart titled "Gate - Source Voltage, V<sub>GS</sub> (V)" in purple on a white background with a bordered frame. The y-axis has labeled levels at 23 V, 18 V, -5 V, and -10 V, with a faint gray zero line in the middle. The waveform starts at 18 V, drops sharply with a small undershoot and ringing to -10 V, then settles at -5 V. It then rises sharply to a peak of about 23 V with a small overshoot and ringing, and settles back at 18 V. Dashed horizontal reference lines extend from 18 V, -5 V, -10 V, and 23 V across the chart. Two vertical double-headed arrows are shown: V<sub>GS-Static</sub> spans from 18 V down to -5 V, and V<sub>GS-Dynamic</sub> spans from 23 V down to -10 V.</description>

<table><thead><tr><th>Level</th><th>Value</th></tr></thead><tbody><tr><td>Initial steady state</td><td>18 V</td></tr><tr><td>Transient peak (high)</td><td>23 V</td></tr><tr><td>Transient minimum (low)</td><td>-10 V</td></tr><tr><td>Static level after transient</td><td>-5 V</td></tr><tr><td>V<sub>GS-Static</sub></td><td>18 V to -5 V</td></tr><tr><td>V<sub>GS-Dynamic</sub></td><td>23 V to -10 V</td></tr></tbody></table></figure>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>®</sup>, the Wolfspeed logo, the Wolfstreak logo, WolfPACK<sup>®</sup>, Wolfspeed WolfPACK<sup>®</sup>, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

# **Preliminary Datasheet**
**Subject to change without notice**

[logo] 7

<figure type="DIAGRAM">Schematic and Pin Out



<description>Line-drawing schematic of a rectangular power module package viewed from above, with a rounded-corner outline and mounting holes at each corner. Three large square-ended terminals with circular holes run along the top edge and three similar terminals along the bottom edge. The central area contains a stylized zigzag arrow logo. Small circular pin terminals are arranged around the perimeter: on the left side labeled 12, 13, 14, 15, and on the right side labeled 11, 10, 9, 8. Numbered pins 3, 4, 5 sit along the upper inner edge, and numbered pins 1, 2, 6, 7 sit in the lower inner area. Rectangular bays with circular holes appear in the lower and upper blocks, indicating mounting or power connections.</description>

Package Dimensions (mm)</figure>

<figure type="DIAGRAM">1,2
9
10
11
12
3,4,5
13
14
15
8
6,7
-t°


<description>Electrical schematic of a half-bridge power module with two stacked MOSFET switches, each with an antiparallel diode. The top MOSFET has drain terminals 1,2 connected at the top node and gate pin 10 and Kelvin/source-sense pin 11 on its left side, with pin 9 tied to the top drain node. The bottom MOSFET has gate pin 14 and source-sense pin 15 on its left side, with pin 8 tied to the bottom source node, and terminals 6,7 at the bottom. The midpoint node between the two devices connects to terminals 3,4,5 on the right and pin 12 on the left. A thermistor symbol labeled -t° connects from the lower node to pin 13 on the right, serving as a temperature sensor.</description></figure>

<figure type="ILLUSTRATION">1 2 3 4 5 6 7 8 9 10 11 12 13 14 15


<description>Isometric line drawing of a power semiconductor module (IGBT-style) with a rectangular plastic housing and a ribbed lower skirt with mounting holes at the corners of its base flange. Two raised terminal blocks sit at the left and right ends, each with round bolt holes; circled callout numbers 1, 2, 6 and 7 point to the left-side terminals and housing features, and 3, 4 and 5 point to the right-side terminals. The center of the top surface has a recessed control area with a raised central panel, with callouts 8 and 9 on the center-left and 10 and 11 on the front-right gate or signal terminal area. Small connector and component housings sit along the rear edge, with callouts 13, 14 and 15 on the rear-center connectors and 12 on a small rear-right feature. Thin leader lines connect each numbered circle to its part. The drawing uses black outlines on a white background with no shading or color.</description></figure>

<figure type="DIAGRAM"><description>Mechanical dimensioned drawing (top view) of a power module housing with a rectangular outline. Top edge has three large circular terminal screw bosses labeled 3, 4, 5 inside the housing and a callout at top reading "8× M3 ∇ 5 MAX" pointing to small screw holes, and "7× M8 ∇ 15 MAX" pointing to the large terminal bosses. Four corner mounting holes labeled A2, A3, A4 (top right area), B3, and A1, A7, A8, A9 along edges with leader-box labels C1–C10 and B1–B3 on the sides. Left and right side have small terminal posts numbered 12, 13, 14, 15 on the left and 11, 10, 9, 8 on the right with leader labels C5, C4, C2, C1 and C8, C7, C6, C3. Lower half has two large rectangular power terminal blocks each with a circular screw boss, labeled B2 and B1, and a central large arrow-like logo/marking. Bottom-left has a connector cluster labeled C10 and a circular marking. Dimension lines show overall height 68.96±0.75 on the left and width 73.24±0.30 at the bottom, with 0 datum markers at the bottom and right side. Numbered signal pins 1–7 are arranged in two groups inside the housing near the center.</description></figure>

<figure type="DIAGRAM">Mechanical side-view technical drawing (engineering line drawing) of a tall rectangular component oriented vertically. The left portion has stepped outline profiles with several rectangular protrusions and notches at varying heights, including a larger block near the upper-left and a recessed section in the middle-left. The central-right portion contains a series of about five evenly spaced vertical ribs or fins running top to bottom, drawn as thin parallel lines with rounded bands. A thin rectangular plate or flange lies at the far right edge. Three purple-labeled dimension/reference markers appear along the bottom, labeled "B", "C1" (or "CT"), and "A" (with a "0" beside it), each with a thin leader line extending upward to the body of the drawing.</figure>

<table>
<tr><td colspan="3">DIMENSION TABLE</td></tr>
<tr><td>SYMBOL</td><td>DIMENSION</td><td>TOLERANCE</td></tr>
<tr><td>[image: A1 symbol]</td><td>2× 6.5</td><td>±1.0</td></tr>
<tr><td>[image: A2 symbol]</td><td>2× 133.5</td><td>±1.0</td></tr>
<tr><td>[image: A3 symbol]</td><td>140</td><td>±0.75</td></tr>
<tr><td>[image: A4 symbol]</td><td>144</td><td>±0.5</td></tr>
<tr><td>[image: A5 symbol]</td><td>2× 6.9</td><td>±0.75</td></tr>
<tr><td>[image: AB tag]</td><td>2× 92.9</td><td>±0.75</td></tr>
<tr><td>[image: A7 tag]</td><td>99.8</td><td>±0.5</td></tr>
<tr><td>[image: A8 tag]</td><td>4</td><td>±0.3</td></tr>
<tr><td>[image: B1 tag]</td><td>2× 11</td><td>±0.5</td></tr>
<tr><td>[image: B2 tag]</td><td>2× 40.5</td><td>±0.5</td></tr>
<tr><td>[image: B3 tag]</td><td>3× 133.5</td><td>±0.5</td></tr>
<tr><td>[image: B4 tag]</td><td>3× 26.9</td><td>±0.5</td></tr>
<tr><td>[image: B5 tag]</td><td>49.9</td><td>±0.5</td></tr>
<tr><td>[image: B6 tag]</td><td>3× 72.9</td><td>±0.5</td></tr>
<tr><td>[image: B7 tag]</td><td>40</td><td>±0.75</td></tr>
<tr><td>[image: C1 tag]</td><td>57</td><td>±0.4</td></tr>
<tr><td>[image: C2 tag]</td><td>66.5</td><td>±0.4</td></tr>
<tr><td>[image: C3 tag]</td><td>57</td><td>±0.6</td></tr>
<tr><td>[image: C4 tag]</td><td>79.5</td><td>±0.4</td></tr>
<tr><td>[image: C5 label tag]</td><td>110.5</td><td>±0.4</td></tr>
<tr><td>[image: C6 label tag]</td><td>82.3</td><td>±0.5</td></tr>
<tr><td>[image: C7 label tag]</td><td>101</td><td>±0.4</td></tr>
<tr><td>[image: C8 label tag]</td><td>110.5</td><td>±0.4</td></tr>
<tr><td>[image: C9 label tag]</td><td>4× 8.9</td><td>±0.6</td></tr>
<tr><td>[image: C10 label tag]</td><td>4× 90.9</td><td>±0.6</td></tr>
<tr><td>[image: C11 label tag]</td><td>35</td><td>±0.75</td></tr>
</table>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

**Preliminary Datasheet**
**Subject to change without notice**

[logo] 8

## Supporting Links & Tools

### Evaluation Tools & Support

* [LTspice and PLECS Models](#)
* [SpeedFit® Design Simulator](#)
* [Technical Support Forum](#)

**Dual-Channel Gate Driver Board**

* [CGD12HB00D: Differential Transceiver Daughter Board Companion Tool for Differential Gate Drivers](CGD12HB00D)
* [CGD1700HB2M-UNA: Wolfspeed Gate Driver Board](CGD1700HB2M-UNA)
* [EVAL-ADUM4146WHB1Z: Analog Devices® Gate Driver Board](EVAL-ADUM4146WHB1Z)
* [UCC21710QDWEVM-054: Texas Instruments® Gate Driver Board](UCC21710QDWEVM-054)

**Application Notes**

* [PRD-08407: LM Module Platform Mounting Guide](PRD-08407)
* [PRD-04814: Design Options for Wolfspeed® Silicon Carbide MOSFET Gate Bias Power Supplies](PRD-04814)
* [PRD-09301: Gate Driver Design for SiC Power Modules](PRD-09301)
* [PRD-06379: Environmental Considerations for Power Electronics Systems](PRD-06379)
* [PRD-07845: Power Module Baseplate Capacitance and Electromagnetic Compatibility](PRD-07845)
* [PRD-07933: Wolfspeed Power Module Thermal Interface Material Application User Guide](PRD-07933)
* [PRD-08376: Thermal Characterization Methods and Applications](PRD-08376)
* [PRD-08710: Measuring Stray Inductance in Power Electronics Systems](PRD-08710)
* [PRD-08911: Considerations for Current Balancing in Paralleled SiC Power Modules](PRD-08911)
* [PRD-09035: Power Module RC Thermal Models User Guide](PRD-09035)

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

**Preliminary Datasheet**

[logo] 9

# Notes & Disclaimers

WOLFSPEED PROVIDES TECHNICAL AND RELIABILITY DATA, DESIGN RESOURCES, APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, AND OTHER RESOURCES "AS IS" AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, WITH RESPECT THERETO, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, SUITABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF THIRD-PARTY INTELLECTUAL PROPERTY RIGHTS.

This document and the information contained herein are subject to change without notice. Any such change shall be evidenced by the publication of an updated version of this document by Wolfspeed. No communication from any employee or agent of Wolfspeed or any third party shall effect an amendment or modification of this document. No responsibility is assumed by Wolfspeed for any infringement of patents or other rights of third parties which may result from use of the information contained herein. No license is granted by implication or otherwise under any patent or patent rights of Wolfspeed.

The information contained in this document (excluding examples, as well as figures or values that are labeled as “typical”) constitutes Wolfspeed’s sole published specifications for the subject product. “Typical” parameters are the average values expected by Wolfspeed in large quantities and are provided for informational purposes only. Any examples provided herein have not been produced under conditions intended to replicate any specific end use. Product performance can and does vary due to a number of factors.

This product has not been designed or tested for use in, and is not intended for use in, any application in which failure of the product would reasonably be expected to cause death, personal injury, or property damage. For purposes of (but without limiting) the foregoing, this product is not designed, intended, or authorized for use as a critical component in equipment implanted into the human body, life-support machines, cardiac defibrillators, and similar emergency medical equipment; air traffic control systems; or equipment used in the planning, construction, maintenance, or operation of nuclear facilities. Notwithstanding any application-specific information, guidance, assistance, or support that Wolfspeed may provide, the buyer of this product is solely responsible for determining the suitability of this product for the buyer's purposes, including without limitation (1) selecting the appropriate Wolfspeed products for the buyer's application, (2) designing, validating, and testing the buyer's application, and (3) ensuring the buyer's application meets applicable standards and any other legal, regulatory, and safety-related requirements.

**RoHS Compliance**

The levels of RoHS restricted materials in this product are below the maximum concentration values (also referred to as the threshold limits) permitted for such substances, or are used in an exempted application, in accordance with EU Directive 2011/65/EC (RoHS2), as implemented January 2, 2013. RoHS Declarations for this product can be obtained from your Wolfspeed representative or from the Product Documentation sections of www.wolfspeed.com.

## REACh Compliance

REACh substances of high concern (SVHCs) information is available for this product. Since the European Chemical Agency (ECHA) has published notice of their intent to frequently revise the SVHC listing for the foreseeable future, please contact your Wolfspeed representative to ensure you get the most up-to-date REACh SVHC Declaration. REACh banned substance information (REACh Article 67) is also available upon request.

- **Contact info**: 4600 Silicon Drive<br>Durham, NC 27703 USA<br>Tel: +1.919.313.5300<br>www.wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>®</sup> and the Wolfstreak logo are registered trademarks and the Wolfspeed logo is a trademark of Wolfspeed, Inc.
PATENT: https://www.wolfspeed.com/legal/patents

*The information in this document is subject to change without notice.*

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- doc_id=parse-01m7ryd9xx7jnrr86ptwrwqtb9 -->