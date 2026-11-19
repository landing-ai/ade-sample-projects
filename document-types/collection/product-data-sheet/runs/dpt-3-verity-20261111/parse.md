Preliminary Datasheet
Subject to change without notice

Wolfspeed®


HAB900C33LM4
3300 V, 900 A, Silicon Carbide, Half-Bridge Module

[X]
DS
DS(on)
3300 V
2 mQ

<figure type="DIAGRAM">### Technical Features
- Fully SiC MOSFET-based for Ultra-Low Loss
- Industry-Compatible Package Footprint
- High Junction Temperature (175 °C) Operation
- Low Stray Inductance (<10 nH)
- Soft Reverse Recovery from Gen 4 Body Diode
- Sintered Die Attach and Copper Die Top System
- Low-Thermal Resistance Copper Baseplate



<description>The figure presents a technical overview of a power electronics module. To the left is a list of seven key technical features. To the right, the visual components include a photograph of the physical module, which is a rectangular, dark gray, multi-terminal power semiconductor device with a copper baseplate and metal screw terminals on top. Next to the photograph is an electrical circuit diagram representing the module's internal configuration. The diagram depicts a half-bridge topology consisting of two MOSFETs stacked vertically. The top MOSFET has gate (G1) and source (S1) terminals, and the bottom MOSFET has gate (G2) and source (S2) terminals. The midpoint between the two MOSFETs is connected to an AC terminal. The top drain connects to a DC+ terminal, and the bottom source connects to a DC- terminal. A negative temperature coefficient (NTC) thermistor is shown connected to the DC- node and an NTC terminal.</description></figure>

Typical Applications
- Solar & Wind-Power Infrastructure
- Grid-Scale Energy Storage
- Rail Traction
- Heavy-Duty E-Mobility: Transportation and Mining
- Marine and Aerospace Propulsion
System Benefits
- Increased System Efficiency due to Low Switching &
Conduction Losses of SiC
- Improved Power Cycling Capabilities for Increased
System Lifetime
- Enhanced Durability and Reduced System Cost
- Enables Two-level Conversion for 2000 V or Greater
DC Systems

Maximum Parameters (Verified by Design)

<table><tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr><tr><td>Drain-Source Voltage</td><td>V<sub>DS</sub></td><td></td><td></td><td>3300</td><td rowspan="3">V</td><td></td><td></td></tr><tr><td>Gate-Source Voltage, Maximum Value</td><td>VGs(max)</td><td>-10</td><td></td><td>23</td><td>Transient</td><td rowspan="2">Note 1 Fig. 16</td></tr><tr><td>Gate-Source Voltage, Recommended</td><td>VGs(op)</td><td></td><td>-5/+18</td><td></td><td>Static</td></tr><tr><td rowspan="2">DC Continuous Drain Current</td><td rowspan="2">l<sub>D</sub></td><td></td><td></td><td>1200</td><td rowspan="4">A</td><td>V<sub>Gs</sub> = 18 V, Tc=l 25 °C, Tw ≤ 175 °C</td><td rowspan="4">Notes 2,3,4 Fig. 11</td></tr><tr><td></td><td>908</td><td></td><td>V<sub>Gs</sub> = 18 V, Tc= 90 °C, Tw ≤ 175 °C</td></tr><tr><td>DC Source-Drain Current (Body Diode)</td><td>I<sub>SD(BD)</sub></td><td></td><td>876</td><td></td><td>V<sub>Gs</sub> = -5 V, T<sub>C</sub>= 90 °C, Tw ≤ 175 °C</td></tr><tr><td>Pulsed Drain-Source Current</td><td>l<sub>DM</sub></td><td></td><td></td><td>3600</td><td>t<sub>pmax</sub> limited by Tw<sub>m</sub>a<sub>x</sub> V<sub>Gs</sub> = 18 V, T<sub>C</sub>= 25 °C</td></tr><tr><td>Power Dissipation</td><td>P<sub>D</sub></td><td></td><td>7282</td><td></td><td>W</td><td>Tc = 25 °C, Tw ≤ 175 °C</td><td>Note 5 Fig. 12</td></tr><tr><td>Virtual Junction Temperature</td><td>Tvu(op)</td><td>-55</td><td></td><td>175</td><td>°C</td><td></td><td></td></tr></table>

Note (1): Recommended turn-on gate voltage is 18 V with ±5 % regulation tolerance
Note (2): Current limit at T<sub>c</sub> = 25 <sup>°</sup>C imposed by package
Note (3): Typical current limit calculated by lb(ma<sub>x</sub>) = V(P<sub>D</sub>/R<sub>D</sub>s<sub>(typ</sub>) (Tvu(ma<sub>x</sub>),ID(<sub>m</sub>a<sub>x</sub>)))
Note (4): Verified by design
Note (5): P<sub>D</sub> = (Tvu - Tc)/RTH<sub>J</sub>c,<sub>yP</sub>)

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Te: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolispeed, Inc. All rights reserved. Wolfspeed<sup>®</sup>, the Wolfspeed logo, the Wolfstreak logo, WoliPACK<sup>®</sup>, Wolispeed WoliPACK<sup>®</sup>, and the Wolfspeed WoliPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice..

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet
Subject to change without notice

⚡ 2


MOSFET Characteristics (Per Position) (T<sub>vy</sub> = 25 °C Unless Otherwise Specified)

<table><tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr><tr><td>Drain-Source Breakdown Voltage</td><td>V<sub>(BRjDSS</sub></td><td>3300</td><td></td><td></td><td rowspan="3">V</td><td>V<sub>Gs</sub> = 0 V, Tw = -55 °C</td><td></td></tr><tr><td rowspan="2">Gate Threshold Voltage</td><td rowspan="2">V<sub>GS(th)</sub></td><td>2.6</td><td>3.5</td><td>4.4</td><td>V<sub>DS</sub> = V<sub>Gs</sub>, I<sub>D</sub> = 530 mA</td><td></td></tr><tr><td></td><td>2.6</td><td></td><td>V<sub>DS</sub> = V<sub>Gs</sub>, l<sub>D</sub> = 530 mA, Tw = 175 °C</td><td></td></tr><tr><td>Zero Gate Voltage Drain Current</td><td>l<sub>DSS</sub></td><td></td><td>20</td><td>400</td><td>µA</td><td>V<sub>G</sub>s = 0 V, V<sub>DS</sub> = 3300 V</td><td></td></tr><tr><td>Gate-Source Leakage Current</td><td>I<sub>Gss</sub></td><td></td><td>200</td><td>5000</td><td>nA</td><td>V<sub>G</sub>S = 18 V, V<sub>DS</sub> = 0 V</td><td></td></tr><tr><td rowspan="2">Drain-Source On-State Resistance (Devices Only)</td><td rowspan="2">R<sub>DS(on)</sub></td><td></td><td>2.0</td><td>2.6</td><td rowspan="2">mn</td><td>V<sub>G</sub>s = 18 V, l<sub>D</sub> = 900 A</td><td rowspan="2">Fig. 2 Fig. 3</td></tr><tr><td></td><td>5.0</td><td></td><td>V<sub>Gs</sub> = 18 V, l<sub>D</sub> = 900 A, Tw = 175 °C</td></tr><tr><td rowspan="2">Transconductance</td><td rowspan="2">Ers</td><td></td><td>617</td><td></td><td rowspan="2">S</td><td>V<sub>DS</sub> = 20 V, I<sub>D</sub>S = 900 A</td><td rowspan="2">Fig. 4</td></tr><tr><td></td><td>619</td><td></td><td>V<sub>DS</sub> = 20 V, l<sub>D</sub>s = 900 A, Tw = 175 °C</td></tr><tr><td>Internal Gate Resistance</td><td>R<sub>G(ine</sub></td><td></td><td>0.5</td><td></td><td>0</td><td>f = 100 kHz</td><td></td></tr><tr><td>Input Capacitance</td><td>C<sub>iss</sub></td><td></td><td>159.9</td><td></td><td rowspan="2">nF</td><td rowspan="3">V<sub>GS</sub> = 0 V, V<sub>DS</sub> = 1800 V, V<sub>AC</sub> = 25 mV, f = 100 kHz</td><td rowspan="3">Fig. 9</td></tr><tr><td>Output Capacitance</td><td>C<sub>oss</sub></td><td></td><td>2.4</td><td></td></tr><tr><td>Reverse Transfer Capacitance</td><td>C<sub>rss</sub></td><td></td><td>6.7</td><td></td><td>pF</td></tr><tr><td>FET Thermal Resistance, Junction to Heatsink</td><td>R<sub>in</sub> JHS</td><td></td><td>0.021</td><td></td><td>°C/W</td><td></td><td></td></tr></table>

Diode Characteristics (Per Position) (T<sub>vU</sub> = 25 °C Unless Otherwise Specified)

<table><tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr><tr><td rowspan="2">Body Diode Forward Voltage</td><td rowspan="2">V<sub>SD</sub></td><td></td><td>5.7</td><td></td><td rowspan="2">V</td><td>V<sub>GS</sub> = -5 V, I<sub>SD</sub> = 900 A</td><td rowspan="2">Fig. 7</td></tr><tr><td></td><td>4.7</td><td></td><td>V<sub>GS</sub> = -5 V, I<sub>SD</sub> = 900 A, T<sub>w</sub> = 175 °C</td></tr></table>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>P</sup>, the Wolfspeed logo, the Wolfstreak logo, WolfPACK<sup>®</sup>, Wolfspeed WoliPACK<sup>®</sup>, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet
Subject to change without notice

[LIGHTNING_BOLT_ICON] 3


Module Physical Characteristics

<table><tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td></tr><tr><td>Package Resistance</td><td>R<sub>pkg</sub></td><td></td><td>0.19</td><td></td><td>mQ</td><td>Tc = 25 °C, Note 6</td></tr><tr><td>Stray Inductance</td><td>Ls<sub>t</sub>r<sub>a</sub>y</td><td></td><td>9.5</td><td></td><td>nH</td><td>Between DC+ and DC-, f = 10 MHz</td></tr><tr><td>Storage Temperature</td><td>T<sub>sig</sub></td><td>-55</td><td></td><td>150</td><td>°C</td><td></td></tr><tr><td>Weight</td><td>W</td><td></td><td>745</td><td></td><td>g</td><td></td></tr><tr><td rowspan="3">Mounting Torque</td><td rowspan="3">M<sub>s</sub></td><td>3.5</td><td>4.5</td><td>5.5</td><td rowspan="3">N-m</td><td>Baseplate, M6 bolts</td></tr><tr><td>8</td><td>12</td><td>16</td><td>Power Terminals, M8 bolts</td></tr><tr><td>0.5</td><td>0.7</td><td>1.3</td><td>Auxiliary Terminals, M3 bolts</td></tr><tr><td>Case Isolation Voltage</td><td>V<sub>isoi</sub></td><td>6</td><td></td><td></td><td>kV</td><td>AC, 50 Hz, 1 min</td></tr><tr><td>Comparative Tracking Index</td><td>CTI</td><td>600</td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">Clearance Distance</td><td rowspan="2"></td><td></td><td>11</td><td></td><td rowspan="4">mm</td><td>Terminal to Terminal</td></tr><tr><td></td><td>33</td><td></td><td>Terminal to Baseplate</td></tr><tr><td rowspan="2">Creepage Distance</td><td rowspan="2"></td><td></td><td>23</td><td></td><td>Terminal to Terminal</td></tr><tr><td></td><td>45</td><td></td><td>Terminal to Baseplate</td></tr></table>

Note (6): Total Effective Resistance (Per Switch Position) = MOSFET Rps(on) + Switch Position Package Resistance

Temperature Sensor (NTC) Characteristics

<table><tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Test Conditions</td></tr><tr><td>Resistance at 25 °C</td><td>R<sub>25</sub></td><td></td><td>4700</td><td></td><td>Q</td><td>T<sub>NTC</sub> = 25 °C</td></tr><tr><td>Tolerance of R<sub>25</sub></td><td></td><td></td><td>±1</td><td></td><td>%</td><td></td></tr><tr><td>Beta Value for 25 °C to 85 °C</td><td>B<sub>25/80</sub></td><td></td><td>3435</td><td></td><td>K</td><td></td></tr><tr><td>Beta Value for 0 °C to 100 °C</td><td>B<sub>0</sub>/<sub>100</sub></td><td></td><td>3399</td><td></td><td>K</td><td></td></tr><tr><td>Tolerance of B<sub>2s</sub>/<sub>85</sub></td><td></td><td></td><td>±1</td><td></td><td>%</td><td></td></tr><tr><td>Maximum Power Dissipation</td><td>P<sub>25</sub></td><td></td><td>50</td><td></td><td>mW</td><td>T<sub>NTC</sub> = 25°C</td></tr></table>

Steinhart & Hart Coefficients for NTC Resistance & NTC Temperature Computation (T in K)
In R = A + ; + Ş<sub>+</sub> Å ; = A<sub>1</sub> + B1 In (Gů<sub>2</sub>) + C, In<sup>2</sup> (r$_) +D<sub>1</sub> In<sup>3</sup> (F§<sub>s</sub>)
A B C D A, B2 C, D. -1.289E-01 4.245EH03 -8.749E-04 -9.588E-06 3335AE=03 3.001EE04 55085EC06 2.188E-07

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Te: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolispeed, Inc. All rights reserved. Wolfspeed<sup>®</sup>, the Wolfspeed logo, the Wolfstreak logo, WoliPACK<sup>®</sup>, Wolispeed WoliPACK<sup>®</sup>, and the Wolfspeed WoliPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet
Subject to change without notice

4


<figure type="CHART">Typical Performance



<description>This is a line chart showing the output characteristics of a semiconductor device, plotting Drain-Source Current (I_DS) in Amperes on the y-axis against Drain-Source Voltage (V_DS) in Volts on the x-axis. The chart displays multiple linear curves representing performance at various junction temperatures: -40°C, 25°C, 100°C, 125°C, 150°C, and 175°C. The curves originate from the origin (0,0) and show that current decreases as temperature increases for a given voltage. The conditions are specified as t_p < 350 μs and V_GS = 18 V.</description>

<table>
  <thead>
    <tr>
      <th>Drain-Source Voltage (V_DS) (V)</th>
      <th>-40°C I_DS (A)</th>
      <th>25°C I_DS (A)</th>
      <th>100°C I_DS (A)</th>
      <th>125°C I_DS (A)</th>
      <th>150°C I_DS (A)</th>
      <th>175°C I_DS (A)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>~800</td>
      <td>~600</td>
      <td>~300</td>
      <td>~250</td>
      <td>~200</td>
      <td>~200</td>
    </tr>
    <tr>
      <td>2</td>
      <td>~1600</td>
      <td>~1200</td>
      <td>~600</td>
      <td>~500</td>
      <td>~400</td>
      <td>~350</td>
    </tr>
    <tr>
      <td>3</td>
      <td>~2400</td>
      <td>~1800</td>
      <td>~900</td>
      <td>~750</td>
      <td>~600</td>
      <td>~550</td>
    </tr>
    <tr>
      <td>4</td>
      <td>-</td>
      <td>~2400</td>
      <td>~1200</td>
      <td>~1000</td>
      <td>~800</td>
      <td>~750</td>
    </tr>
    <tr>
      <td>5</td>
      <td>-</td>
      <td>-</td>
      <td>~1500</td>
      <td>~1250</td>
      <td>~1000</td>
      <td>~900</td>
    </tr>
    <tr>
      <td>6</td>
      <td>-</td>
      <td>-</td>
      <td>~1800</td>
      <td>~1500</td>
      <td>~1200</td>
      <td>~1100</td>
    </tr>
  </tbody>
</table>

Figure 1. Output Characteristics for Various Junction Temperatures</figure>

<figure type="CHART">

<description>The figure is a line chart titled 'Figure 2. Normalized On-State Resistance vs. Drain Current for Various Junction Temperatures'. The chart plots 'Normalized On-resistance (p.u.)' on the y-axis against 'Drain-Source Current, IDS (A)' on the x-axis. The x-axis ranges from 0 to 2000 A, and the y-axis ranges from 0.5 to 3.0. There are multiple data lines, each representing a specific junction temperature: -40 °C, 0 °C, 25 °C, 100 °C, 125 °C, 150 °C, and 175 °C. An inset box in the upper left corner specifies test conditions: 'tp < 350 μs' and 'VGS = 18 V'. The data shows that normalized on-resistance increases with both temperature and drain-source current.</description><table><thead><tr><th>Drain-Source Current, IDS (A)</th><th>-40 °C</th><th>0 °C</th><th>25 °C</th><th>100 °C</th><th>125 °C</th><th>150 °C</th><th>175 °C</th></tr></thead><tbody><tr><td>0</td><td>0.65</td><td>0.8</td><td>1.0</td><td>1.6</td><td>1.85</td><td>2.15</td><td>2.45</td></tr><tr><td>500</td><td>0.65</td><td>0.8</td><td>1.0</td><td>1.6</td><td>1.85</td><td>2.15</td><td>2.45</td></tr><tr><td>1000</td><td>0.65</td><td>0.8</td><td>1.0</td><td>1.65</td><td>1.9</td><td>2.2</td><td>2.5</td></tr><tr><td>1500</td><td>0.7</td><td>0.85</td><td>1.05</td><td>1.65</td><td>1.95</td><td>2.25</td><td>2.6</td></tr><tr><td>2000</td><td>0.7</td><td>0.85</td><td>1.05</td><td>1.7</td><td>2.0</td><td>2.35</td><td>2.7</td></tr></tbody></table></figure>

<figure type="CHART">

<description>The figure is a line chart titled "Figure 3. Normalized On-State Resistance vs. Junction Temperature". The chart plots the Normalized On-resistance (p.u.) on the y-axis against the Virtual Junction Temperature, T_vj (°C) on the x-axis. The y-axis ranges from 0.0 to 3.0 in increments of 0.5. The x-axis ranges from -50 to 200 in increments of 25. A single curve shows an increasing trend, starting near ( -40, 0.7) and rising to approximately (175, 2.5). An inset box in the upper left corner displays the test conditions: "tp < 350 µs", "VGS = 18 V", and "IDS = 900 A".</description> <table><thead><tr><th>Virtual Junction Temperature, T_vj (°C)</th><th>Normalized On-resistance (p.u.)</th></tr></thead><tbody><tr><td>-40</td><td>~0.7</td></tr><tr><td>0</td><td>~0.85</td></tr><tr><td>25</td><td>~1.0</td></tr><tr><td>50</td><td>~1.2</td></tr><tr><td>75</td><td>~1.45</td></tr><tr><td>100</td><td>~1.7</td></tr><tr><td>125</td><td>~1.95</td></tr><tr><td>150</td><td>~2.2</td></tr><tr><td>175</td><td>~2.5</td></tr></tbody></table></figure>

<figure type="CHART">

<description>The figure is a line chart titled "Figure 4. Transfer Characteristic for Various Junction Temperatures." It plots the Drain-Source Current (IDS in Amperes) on the y-axis against the Gate-Source Voltage (VGS in Volts) on the x-axis. The chart displays a family of curves, each representing the transfer characteristic of a device at different junction temperatures: -40 °C, 25 °C, 100 °C, 125 °C, 150 °C, and 175 °C. An arrow indicates the direction of increasing temperature. A text box in the upper-left corner specifies test conditions: "tp < 350 µs" and "VDS = 20 V".</description><table><thead><tr><th>Temperature (°C)</th><th>Trend</th></tr></thead><tbody><tr><td>-40</td><td>Lowest curve, shifts right</td></tr><tr><td>25</td><td>Curve shifts left</td></tr><tr><td>100</td><td>Curve shifts left</td></tr><tr><td>125</td><td>Curve shifts left</td></tr><tr><td>150</td><td>Curve shifts left</td></tr><tr><td>175</td><td>Highest curve, shifts furthest left</td></tr></tbody></table></figure>

<figure type="CHART">

<description>This figure displays the 3rd quadrant characteristic curves of a semiconductor device, plotting Source-Drain Current (ISD) in Amperes against Source-Drain Voltage (VSD) in Volts for various junction temperatures. The chart features a series of linear slopes originating from the origin (0,0), with each line representing a different temperature: -40 °C, 25 °C, 100 °C, 125 °C, 150 °C, and 175 °C. An annotation box in the top-left corner indicates 'tp < 350 µs' and 'VGS = 18 V'. The curves show that current decreases as temperature increases for a given voltage.</description><table><thead><tr><th>Temperature (°C)</th><th>Approximate Slope (ISD/VSD)</th></tr></thead><tbody><tr><td>-40</td><td>Steepest slope</td></tr><tr><td>25</td><td>Second steepest</td></tr><tr><td>100</td><td>Third slope</td></tr><tr><td>125</td><td>Fourth slope</td></tr><tr><td>150</td><td>Fifth slope</td></tr><tr><td>175</td><td>Shallowest slope</td></tr></tbody></table>Figure 5. 3rd Quadrant Characteristic vs. Junction Temperatures at VGS = 18 V</figure>

<figure type="CHART">

<description>The figure is a line chart displaying the 3rd quadrant characteristic of a device, specifically showing the Source-Drain Current (I_SD) in Amperes on the y-axis against the Source-Drain Voltage (V_SD) in Volts on the x-axis. The chart illustrates the body diode behavior at different junction temperatures (-40°C, 25°C, 100°C, 125°C, 150°C, and 175°C) under the condition of t_p < 300 µs and V_GS = 0 V. The curves show that as temperature increases, the current for a given voltage generally decreases, except at lower voltages where they intersect.</description> <table><thead><tr><th>Temperature (°C)</th><th>Trend Description</th></tr></thead><tbody><tr><td>-40°C</td><td>Topmost curve at higher V_SD, indicating highest current.</td></tr><tr><td>25°C</td><td>Second curve from top.</td></tr><tr><td>100°C</td><td>Third curve from top.</td></tr><tr><td>125°C</td><td>Fourth curve from top.</td></tr><tr><td>150°C</td><td>Fifth curve from top.</td></tr><tr><td>175°C</td><td>Bottommost curve at higher V_SD, indicating lowest current.</td></tr></tbody></table> Figure 6. 3rd Quadrant Characteristic vs. Junction Temperatures at V_GS = 0 V (Body Diode)</figure>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolispeed, Inc. All rights reserved. Wolfspeed<sup>®</sup>, the Wolfspeed logo, the Wolistreak logo, WoliPACK<sup>®</sup>, Wolispeed WoliPACK<sup>®</sup>, and the Wolfspeed WoliPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet
Subject to change without notice

0 [ABSTRACT_LIGHTNING_BOLT_SHAPE] 5


<figure type="CHART">Typical Performance



<description>This is a line chart titled 'Typical Performance' showing the 3rd Quadrant Characteristic of a body diode, plotting Source-Drain Current (ISD in Amperes) on the y-axis against Source-Drain Voltage (VSD in Volts) on the x-axis. The chart includes a box in the top-left corner with the parameters 'tp < 350 µs' and 'VGS = -5 V'. Multiple curves are plotted, representing different junction temperatures: -40 °C, 25 °C, 100 °C, 150 °C, and 175 °C. The curves show that current increases with voltage, and for a given voltage, the current increases as the temperature increases, with the 175 °C curve being the highest and the -40 °C curve being the lowest.</description>

Figure 7. 3rd Quadrant Characteristic vs. Junction Temperatures at VGS = -5 V (Body Diode)

<table>
  <thead>
    <tr>
      <th>Source-Drain Voltage (VSD) (V)</th>
      <th>-40 °C (ISD) (A)</th>
      <th>25 °C (ISD) (A)</th>
      <th>100 °C (ISD) (A)</th>
      <th>150 °C (ISD) (A)</th>
      <th>175 °C (ISD) (A)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>~100</td>
      <td>~150</td>
      <td>~200</td>
      <td>~300</td>
      <td>~400</td>
    </tr>
    <tr>
      <td>4</td>
      <td>~400</td>
      <td>~500</td>
      <td>~600</td>
      <td>~800</td>
      <td>~900</td>
    </tr>
    <tr>
      <td>5</td>
      <td>~700</td>
      <td>~850</td>
      <td>~1000</td>
      <td>~1200</td>
      <td>~1400</td>
    </tr>
    <tr>
      <td>6</td>
      <td>~1100</td>
      <td>~1250</td>
      <td>~1400</td>
      <td>~1600</td>
      <td>~1900</td>
    </tr>
    <tr>
      <td>7</td>
      <td>~1500</td>
      <td>~1600</td>
      <td>~1800</td>
      <td>~2100</td>
      <td>~2400</td>
    </tr>
  </tbody>
</table></figure>

<figure type="CHART">

<description>A semi-logarithmic line chart titled 'Figure 8. Typical Capacitances vs. Drain to Source Voltage (0 - 200 V)' showing the relationship between capacitance (nF) and drain-source voltage (V_DS in Volts). The y-axis represents Capacitance (nF) on a logarithmic scale ranging from 0.01 to 1000. The x-axis represents Drain-Source Voltage, V_DS (V) ranging from 0 to 200. Three curves are plotted: C_iss (highest capacitance, relatively flat), C_oss (intermediate capacitance, decreasing with voltage), and C_rss (lowest capacitance, decreasing with voltage). An inset box in the bottom-left corner provides test conditions: 'T_VJ = 25 °C', 'V_AC = 25 mV', and 'f = 100 kHz'.</description><table><thead><tr><th>Drain-Source Voltage, V_DS (V)</th><th>C_iss (nF)</th><th>C_oss (nF)</th><th>C_rss (nF)</th></tr></thead><tbody><tr><td>0</td><td>~200</td><td>~70</td><td>~70</td></tr><tr><td>25</td><td>~180</td><td>~10</td><td>~2</td></tr><tr><td>50</td><td>~170</td><td>~5</td><td>~0.4</td></tr><tr><td>100</td><td>~160</td><td>~3</td><td>~0.2</td></tr><tr><td>150</td><td>~160</td><td>~2.5</td><td>~0.1</td></tr><tr><td>200</td><td>~160</td><td>~2</td><td>~0.06</td></tr></tbody></table></figure>

<figure type="CHART">

<description>The figure is a line chart illustrating the relationship between typical capacitances (Ciss, Coss, Crss) and the Drain-Source Voltage (VDS) for a semiconductor device. The y-axis represents Capacitance in nF on a logarithmic scale ranging from 0.01 to 1000 nF. The x-axis represents Drain-Source Voltage, VDS, in Volts, ranging from 0 to 3000 V. Three curves are plotted: Ciss, which remains relatively flat near 100-200 nF; Coss, which starts high and drops rapidly before leveling off around 2-3 nF; and Crss, which starts very high and drops sharply to below 0.1 nF. An inset box in the upper right corner provides test conditions: TVJ = 25 °C, VAC = 25 mV, and f = 100 kHz. Below the chart is the text: 'Figure 9. Typical Capacitances vs. Drain to Source Voltage (0 - 3300V)'.</description><table><thead><tr><th>Drain-Source Voltage, VDS (V)</th><th>Ciss (nF)</th><th>Coss (nF)</th><th>Crss (nF)</th></tr></thead><tbody><tr><td>0</td><td>~170</td><td>~170</td><td>~170</td></tr><tr><td>500</td><td>~170</td><td>~5</td><td>~0.2</td></tr><tr><td>1000</td><td>~170</td><td>~3</td><td>~0.1</td></tr><tr><td>1500</td><td>~170</td><td>~2.5</td><td>~0.08</td></tr><tr><td>2000</td><td>~170</td><td>~2.3</td><td>~0.06</td></tr><tr><td>2500</td><td>~170</td><td>~2.2</td><td>~0.05</td></tr><tr><td>3000</td><td>~170</td><td>~2.1</td><td>~0.05</td></tr></tbody></table></figure>

<figure type="CHART">

<description>This chart displays the relationship between Threshold Voltage (V_TH) in Volts and Virtual Junction Temperature (T_VJ) in degrees Celsius. The graph shows a single downward-sloping curve indicating that as the junction temperature increases from -50°C to 175°C, the threshold voltage decreases from approximately 4.2V to approximately 2.8V. The conditions for this measurement are specified in the top-left corner as V_GS = V_DS and I_DS = 530 mA.</description><table><thead><tr><th>Virtual Junction Temperature, T_VJ (°C)</th><th>Threshold Voltage, V_TH (V)</th></tr></thead><tbody><tr><td>-50</td><td>~4.2</td></tr><tr><td>0</td><td>~3.7</td></tr><tr><td>50</td><td>~3.4</td></tr><tr><td>100</td><td>~3.1</td></tr><tr><td>150</td><td>~2.9</td></tr><tr><td>175</td><td>~2.8</td></tr></tbody></table>Figure 10. Threshold Voltage vs. Junction Temperature</figure>

<figure type="CHART">

<description>Figure 11 shows a Continuous Drain Current Derating chart. The y-axis represents 'Drain-Source DC Current, IDS (A)' ranging from 0 to 1600. The x-axis represents 'Case Temperature, TC (°C)' ranging from -75 to 175. The graph plots the relationship between drain current and case temperature. A solid line shows the actual derating curve starting at 1200 A at -50°C (labeled 'Package Limit') and extending to 25°C, where it curves downward toward 500 A at 150°C. A dashed line extends from -50°C to 25°C, indicating a theoretical limit above the package limit. An inset box in the top right corner specifies the conditions as 'Tvj ≤ 175 °C'.</description><table><thead><tr><th>Case Temperature (°C)</th><th>Drain-Source DC Current, IDS (A)</th></tr></thead><tbody><tr><td>-50</td><td>1200 (Package Limit)</td></tr><tr><td>25</td><td>1200</td></tr><tr><td>150</td><td>500</td></tr></tbody></table></figure>

<figure type="CHART">

<description>The figure displays a line chart showing the Maximum Power Dissipation Derating versus Case Temperature. The y-axis represents 'FET Power Dissipation, PD (W)' ranging from 0 to 12000, with grid lines every 2000 units. The x-axis represents 'Case Temperature, TC (°C)' ranging from -75 to 175, with grid lines every 25 units. A single downward-sloping straight line indicates the power dissipation decreasing as the case temperature increases. An annotation box in the upper right corner specifies the condition 'Conditions: TVJ ≤ 175 °C'.</description><table><thead><tr><th>Case Temperature, TC (°C)</th><th>FET Power Dissipation, PD (W)</th></tr></thead><tbody><tr><td>-55 (approx)</td><td>11200 (approx)</td></tr><tr><td>150 (approx)</td><td>1200 (approx)</td></tr></tbody></table>Figure 12. Maximum Power Dissipation Derating vs. Case Temperature</figure>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC27703 | Te: +1.919.313.5300 wolfspeed.com/power

@ 2026 Wolispeed, Inc. All rights reserved. Wolfspeed<sup>®</sup>, the Wolfspeed logo, the Wolfstreak logo, WoliPACK<sup>®</sup>, Wolispeed WoliPACK<sup>®</sup>, and the Wolfspeed WoliPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet
Subject to change without notice

6


<figure type="CHART">

<description>The figure is a line chart titled 'Definitions' and 'Figure 13. Turn-off Transient Definitions'. It displays the turn-off transient characteristics of a semiconductor device by plotting three waveforms: Gate-Source Voltage (VGS, purple), Drain-Source Voltage (VDS, blue), and Source Current (IS, cyan). The chart defines various switching parameters. The horizontal axis represents time, while the vertical axis represents voltage or current. Key intervals marked include t_off (total turn-off time), t_d(off) (turn-off delay time), and t_f (fall time). Voltage and current thresholds are indicated at 90% and 10% levels. The chart also notes peak rates of change for a sliding 5 ns window (*dv/dt_OFF and *di/dt_OFF) and defines energy loss E_OFF as the integral of VDS multiplied by IS.</description><table><tr><th>Parameter</th><th>Description</th></tr><tr><td>Gate-Source Voltage (VGS)</td><td>Purple waveform, starts high and decays.</td></tr><tr><td>Drain-Source Voltage (VDS)</td><td>Blue waveform, rises during the transient.</td></tr><tr><td>Source Current (IS)</td><td>Cyan waveform, falls during the transient.</td></tr><tr><td>t_off</td><td>Total turn-off time interval.</td></tr><tr><td>t_d(off)</td><td>Turn-off delay time interval.</td></tr><tr><td>t_f</td><td>Fall time interval.</td></tr><tr><td>*dv/dt_OFF</td><td>Peak rate of change of voltage (sliding 5 ns window).</td></tr><tr><td>*di/dt_OFF</td><td>Peak rate of change of current (sliding 5 ns window).</td></tr><tr><td>E_OFF</td><td>Energy loss calculation, defined as integral of VDS x IS.</td></tr></table></figure>

<figure type="CHART">

<description>The image displays a line chart labeled "Figure 14. Turn-on Transient Definitions," illustrating the relationship between Gate-Source Voltage (V_GS), Source Current (I_S), and Drain-Source Voltage (V_DS) during a switching event. The chart features three primary waveforms: a purple line for V_GS rising, a light blue line for I_S rising, and a dark blue line for V_DS falling. Various time intervals are annotated, including t_d(on), t_on, and t_r, along with markers for 10% and 90% thresholds. Key performance metrics like di/dt_ON, dv/dt_ON, and E_ON (calculated as the integral of V_DS x I_S) are also highlighted. A footnote indicates that *di/dt_ON and dv/dt_ON represent the peak rate of change for a sliding 5 ns window.</description><table><thead><tr><th>Signal</th><th>Color</th><th>Behavior</th></tr></thead><tbody><tr><td>Gate - Source Voltage, V_GS (V)</td><td>Purple</td><td>Rising edge</td></tr><tr><td>Source Current, I_S (A)</td><td>Light Blue</td><td>Rising edge, then oscillating</td></tr><tr><td>Drain - Source Voltage, V_DS (V)</td><td>Dark Blue</td><td>Falling edge, then oscillating</td></tr></tbody></table></figure>

<figure type="CHART">

<description>The figure is a line chart titled "Reverse Recovery Current, I_RR (A)" illustrating the reverse recovery behavior of a diode or switch. The vertical axis represents current (I), and the horizontal axis represents time (t). The waveform begins at a positive forward current level (I_F) and drops sharply as the device turns off. It crosses the zero-current line (0 A), reaches a negative peak current (I_RRM), and then oscillates back toward zero. The area under the negative portion of the curve, between the two zero-crossing points, is shaded and labeled "Q_RR". The total time duration for this reverse recovery event is labeled "t_rr", which is subdivided into two segments: "t_f" (falling time) and "t_s" (storage time). A small tick mark on the downward slope indicates the "*di/dt_RR" (peak rate of change for a sliding 5 ns window during the falling event). The figure is captioned "Figure 15. Reverse Recovery Definitions".</description></figure>

<figure type="CHART">

<description>The figure displays a line graph representing the transient behavior of the Gate-Source Voltage (VGS) over time. The vertical axis represents voltage in Volts. The waveform starts at a high level of 18 V, drops sharply to a low level of -5 V, with an overshoot reaching -10 V during the transition. It then returns to the 18 V level, with an overshoot reaching 23 V during the transition. The graph labels VGS-Static as the difference between the 18 V and -5 V levels, and VGS-Dynamic as the difference between the 23 V and -10 V levels.</description><table><thead><tr><th>Feature</th><th>Voltage Value</th></tr></thead><tbody><tr><td>High Level</td><td>18 V</td></tr><tr><td>Low Level</td><td>-5 V</td></tr><tr><td>High Overshoot</td><td>23 V</td></tr><tr><td>Low Overshoot</td><td>-10 V</td></tr></tbody></table>Figure 16. VGS Transient Definitions</figure>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Te: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>P</sup>, the Wolfspeed logo, the Wolfstreak logo, WolfPACK<sup>®</sup>, Wolfspeed WoliPACK<sup>®</sup>, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet
Subject to change without notice

⚡ 7


<figure type="DIAGRAM">Schematic and Pin Out



<description>The image is a technical line drawing of an electronic component package, likely a power module. The central body of the diagram displays a stylized lightning bolt logo. Surrounding this central area are numbered pin terminals arranged in a rectangular layout. On the left side, the pins are numbered 12, 13, 14, and 15, oriented vertically. On the right side, the pins are numbered 11, 10, 9, and 8, also oriented vertically. Additionally, there are pins labeled 3, 4, 5, 6, 7, 2, and 1 positioned around the inner perimeter of the package. Large circular mounting holes or power terminals are visible at the top, bottom, and corners of the rectangular housing. The overall view is a top-down schematic representation used for identifying pinouts.</description>

Package Dimensions (mm)</figure>

<figure type="DIAGRAM">

<description>This is an electronic circuit diagram representing a power module, likely a half-bridge configuration. The circuit consists of two MOSFETs arranged in a vertical stack, each with an integrated body diode. The top MOSFET is connected to terminals 1, 2, and 9 at the drain, while its gate is connected to terminal 10 and its source is connected to terminal 11. The drain of the bottom MOSFET is connected to the source of the top MOSFET, which is also linked to terminal 12 and terminals 3, 4, and 5. The gate of the bottom MOSFET is connected to terminal 14, and its source is connected to terminal 15. The source of the bottom MOSFET is also connected to terminals 8, 6, and 7. Additionally, a thermistor (labeled '-t°') is connected between the source of the bottom MOSFET and terminal 13.</description></figure>

<figure type="DIAGRAM">

<description>This is a technical line-art diagram of an electronic power module, likely an IGBT module, shown in an isometric perspective. The device features a rectangular housing with multiple electrical terminals and connectors. The image includes 15 distinct callout numbers (1 through 15) pointing to various features of the component. The left side features large, flat terminal pads labeled 1, 2, 6, and 7. The right side features similar terminal pads labeled 3, 4, 5, and 12. A central raised section contains smaller connector interfaces, with callouts 8, 9, 10, 11, 13, 14, and 15 pointing to various pins, headers, and auxiliary terminals on the top surface. The housing has a ribbed side profile indicating cooling fins or structural reinforcement.</description></figure>

<figure type="DIAGRAM">

<description>This figure is a technical engineering diagram, specifically a top-down view of an electronic power module or semiconductor device, likely for mounting purposes. It features a rectangular housing with various screw holes, connection terminals, and reference markers.</description> 

### Transcription and Key Annotations
- **Annotations/Labels:**
  - Top section: "8x M3 5 MAX" (pointing to the smaller screw holes) and "7x M8 15 MAX" (pointing to the larger terminal screw holes).
  - Side/Margin measurements: "68.96±0.75" (vertical distance) and "73.24±0.30" (horizontal distance).
  - Origin/Reference lines: A crosshair line marked "0" horizontally and vertically near the bottom-left area.
- **Reference Markers (Boxed Letters/Numbers):**
  - A-series (A1-A7): Located around the perimeter, likely indicating mounting holes or reference points.
  - B-series (B1-B6): Located near the larger terminal holes.
  - C-series (C1-C10): Located near the smaller control/signal terminals along the left and right edges.
- **Component Features:**
  - Central Logo: A stylized lightning bolt symbol in the center of the module.
  - Numbered Terminals: Terminals labeled 1 through 15 are distributed around the periphery.
  - Mounting Holes: Various circular holes with crosshairs, indicating screw positions.



<description>The diagram uses a standard orthographic projection style with thin lines for the housing structure and thick, bold circles for mounting and connection points. The layout is symmetrical along the vertical axis. Reference markers (A, B, C series) are placed in boxes pointing to specific features to aid in identifying component locations or connection points.</description></figure>

<figure type="DIAGRAM">

<description>The figure is a technical side-profile schematic drawing of a mechanical component, likely an electrical connector or housing. The object is oriented vertically, showing a complex structure with ribbed or grooved sections on the right side and various rectangular cutouts and projections on the left side. The drawing is rendered in clean, black-and-white lines typical of CAD software.</description> B7 C11 A8 0</figure>

<table><tr><td colspan="3">DIMENSION TABLE</td></tr><tr><td>SYMBOL</td><td>DIMENSION</td><td>TOLERANCE</td></tr><tr><td>P1)</td><td>2x 6.5</td><td>±1.0</td></tr><tr><td>(A2&gt;</td><td>2x 133.5</td><td>±1.0</td></tr><tr><td>E3D</td><td>140</td><td>±0.75</td></tr><tr><td>P9)</td><td>144</td><td>±0.5</td></tr><tr><td>(A5&gt;</td><td>2x6.9</td><td>±0.75</td></tr><tr><td>[A5&gt;</td><td>2x92.9</td><td>±0.75</td></tr><tr><td>IAD</td><td>99.8</td><td>±0.5</td></tr><tr><td>PT&gt;</td><td>4</td><td>±0.3</td></tr><tr><td>(81&gt;</td><td>2x-11</td><td>±0.5</td></tr><tr><td>EID</td><td>2x40.5</td><td>±0.5</td></tr><tr><td>[03&gt;</td><td>3x 133.5</td><td>±0.5</td></tr><tr><td>[34)</td><td>3x26.9</td><td>±0.5</td></tr><tr><td>FI5&gt;</td><td>49.9</td><td>±0.5</td></tr><tr><td>BID</td><td>3x72.9</td><td>±0.5</td></tr><tr><td>E15</td><td>40</td><td>±0.75</td></tr><tr><td>[C1&gt;</td><td>57</td><td>±0.4</td></tr><tr><td>[C2&gt;</td><td>66.5</td><td>±0.4</td></tr><tr><td>[C3&gt;</td><td>57</td><td>±0.6</td></tr><tr><td>[CI&gt;</td><td>79.5</td><td>±0.4</td></tr><tr><td>[CD</td><td>110.5</td><td>±0.4</td></tr><tr><td>(0D</td><td>82.3</td><td>±0.5</td></tr><tr><td>(C7&gt;</td><td>101</td><td>±0.4</td></tr><tr><td>[CD</td><td>110.5</td><td>±0.4</td></tr><tr><td>[0E&gt;</td><td>4x8.9</td><td>±0.6</td></tr><tr><td>(C10)</td><td>4x.90.9</td><td>±0.6</td></tr><tr><td>(CT1)</td><td>35</td><td>±0.75</td></tr></table>

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Te: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>P</sup>, the Wolfspeed logo, the Wolfstreak logo, WoliPACK®, Wolfspeed WolíPACK<sup>®</sup>, and the Wolfspeed WolfPACK ogo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet
Subject to change without notice

8


Supporting Links & Tools
Evaluation Tools & Support
- LTspice and PLECS Models
- SpeedFit<sup>®</sup> Design Simulator
- Technical Support Forum

Dual-Channel Gate Driver Board
- CGD12HBOOD: Differential Transceiver Daughter Board Companion Tool for Differential Gate Drivers
- CGD1700HB2M-UNA: Wolfspeed Gate Driver Board
- EVAL-ADUM4146WHB1Z: Analog Devices<sup>®</sup> Gate Driver Board
- UCC21710QDWEVM-054: Texas Instruments<sup>®</sup> Gate Driver Board

Application Notes
- PRD-08407: LM Module Platform Mounting Guide
- PRD-04814: Design Options for Wolfspeed<sup>®</sup> Silicon Carbide MOSFET Gate Bias Power Supplies
- PRD-09301: Gate Driver Design for SiC Power Modules
- PRD-06379: Environmental Considerations for Power Electronics Systems
- PRD-07845: Power Module Baseplate Capacitance and Electromagnetic Compatibility
- PRD-07933: Wolfspeed Power Module Thermal Interface Material Application User Guide
- PRD-08376: Thermal Characterization Methods and Applications
- PRD-08710: Measuring Stray Inductance in Power Electronics Systems
- PRD-08911: Considerations for Current Balancing in Paralleled SiC Power Modules
- PRD-09035: Power Module RC Thermal Models User Guide

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>P</sup>, the Wolfspeed logo, the Wolfstreak logo, WolfPACK<sup>®</sup>, Wolfspeed WoliPACK<sup>®</sup>, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- PAGE BREAK -->

HAB900C33LM4

Preliminary Datasheet

9


Notes & Disclaimers
WOLFSPEED PROVIDES TECHNICAL AND RELIABILITY DATA, DESIGN RESOURCES, APPLICATION OR OTHER DESIGN
ADVICE, WEB TOOLS, AND OTHER RESOURCES "AS IS" AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES,
EXPRESS AND IMPLIED, WITH RESPECT THERETO, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES
OF MERCHANTABILITY, SUITABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF THIRD-
PARTY INTELLECTUAL PROPERTY RIGHTS.

This document and the information contained herein are subject to change without notice. Any such change
shall be evidenced by the publication of an updated version of this document by Wolfspeed. No communication
from any employee or agent of Wolfspeed or any third party shall effect an amendment or modification of this
document. No responsibility is assumed by Wolfspeed for any infringement of patents or other rights of third
parties which may result from use of the information contained herein. No license is granted by implication or
otherwise under any patent or patent rights of Wolfspeed.

The information contained in this document (excluding examples, as well as figures or values that are labeled as
"typical") constitutes Wolfspeed's sole published specifications for the subject product. "Typical" parameters are
the average values expected by Wolfspeed in large quantities and are provided for informational purposes only.
Any examples provided herein have not been produced under conditions intended to replicate any specific end
use. Product performance can and does vary due to a number of factors.

This product has not been designed or tested for use in, and is not intended for use in, any application in which
failure of the product would reasonably be expected to cause death, personal injury, or property damage. For
purposes of (but without limiting) the foregoing, this product is not designed, intended, or authorized for use as a
critical component in equipment implanted into the human body, life-support machines, cardiac defibrillators, and
similar emergency medical equipment; air traffic control systems; or equipment used in the planning, construction,
maintenance, or operation of nuclear facilities. Notwithstanding any application-specific information, guidance,
assistance, or support that Wolfspeed may provide, the buyer of this product is solely responsible for determining
the suitability of this product for the buyer's purposes, including without limitation (1) selecting the appropriate
Wolfspeed products for the buyer's application, (2) designing, validating, and testing the buyer's application, and
(3) ensuring the buyer's application meets applicable standards and any other legal, regulatory, and safety-related
requirements.

RoHS Compliance
The levels of RoHS restricted materials in this product are below the maximum concentration values (also
referred to as the threshold limits) permitted for such substances, or are used in an exempted application, in
accordance with EU Directive 2011/65/EC (RoHS2), as implemented January 2, 2013. RoHS Declarations for this
product can be obtained from your Wolfspeed representative or from the Product Documentation sections of
www.wolfspeed.com.

REACh Compliance
REACh substances of high concern (SVHCs) information is available for this product. Since the European Chemical
Agency (ECHA) has published notice of their intent to frequently revise the SVHC listing for the foreseeable future,
please contact your Wolfspeed representative to ensure you get the most up-to-date REACh SVHC Declaration.
REACh banned substance information (REACh Article 67) is also available upon request.

Contact info:
4600 Silicon Drive
Durham, NC 27703 USA
Tel: +1.919.313.5300
www.wolfspeed.com/power

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>®</sup> and the Wolfstreak logo are registered trademarks and the Wolfspeed logo is a trademark of Wolfspeed, Inc.
PATENT: https//woww.wolfspeed.com/legal/patents

The information in this document is subject to change without notice.

Preliminary Rev. 1, May 2026

4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power

@ 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed<sup>®</sup>, the Wolfspeed logo, the Wolfstreak logo, WolfPACK<sup>®</sup>, Wolfspeed WoliPACK®, and the Wolfspeed WolfPACK ogo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.

<!-- doc_id=parse-01m7rx6v0632m15dc5jx54rjz3 -->