Preliminary Datasheet
Subject to change without notice


Wolfspeed®


HAB900C33LM4
3300 V, 900 A, Silicon Carbide, Half-Bridge Module


V<sub>DS</sub>  3300 V 
R<sub>DS(on)</sub>  2 mΩ 

# Technical Features

- Fully SiC MOSFET-based for Ultra-Low Loss
- Industry-Compatible Package Footprint
- High Junction Temperature (175 °C) Operation
- Low Stray Inductance (<10 nH)
- Soft Reverse Recovery from Gen 4 Body Diode
- Sintered Die Attach and Copper Die Top System
- Low-Thermal Resistance Copper Baseplate
[Power module with circuit diagram]


**Typical Applications**
 - Solar & Wind-Power Infrastructure
 - Grid-Scale Energy Storage
 - Rail Traction
 - Heavy-Duty E-Mobility: Transportation and Mining
 - Marine and Aerospace Propulsion
**System Benefits**
 - Increased System Efficiency due to Low Switching &
Conduction Losses of SiC
 - Improved Power Cycling Capabilities for Increased
System Lifetime
 - Enhanced Durability and Reduced System Cost
 - Enables Two-level Conversion for 2000 V or Greater
DC Systems


Maximum Parameters (Verified by Design)

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr>
<tr><td>Drain-Source Voltage</td><td>V<sub>DS</sub></td><td></td><td></td><td>3300</td><td rowspan="3">V</td><td></td><td></td></tr>
<tr><td>Gate-Source Voltage, Maximum Value</td><td>V<sub>GS(max)</sub></td><td>-10</td><td></td><td>23</td><td>Transient</td><td rowspan="2">Note 1<br>Fig. 16</td></tr>
<tr><td>Gate-Source Voltage, Recommended</td><td>V<sub>GS(op)</sub></td><td></td><td>-5/+18</td><td></td><td>Static</td></tr>
<tr><td rowspan="2">DC Continuous Drain Current</td><td rowspan="2">I<sub>D</sub></td><td></td><td></td><td>1200</td><td rowspan="4">A</td><td>V<sub>GS</sub> = 18 V, T<sub>C</sub> = 25 °C, T<sub>VJ</sub> ≤ 175 °C</td><td rowspan="4">Notes<br>2, 3, 4<br>Fig. 11</td></tr>
<tr><td></td><td>908</td><td></td><td>V<sub>GS</sub> = 18 V, T<sub>C</sub> = 90 °C, T<sub>VJ</sub> ≤ 175 °C</td></tr>
<tr><td>DC Source-Drain Current (Body Diode)</td><td>I<sub>SD(BD)</sub></td><td></td><td>876</td><td></td><td>V<sub>GS</sub> = -5 V, T<sub>C</sub> = 90 °C, T<sub>VJ</sub> ≤ 175 °C</td></tr>
<tr><td>Pulsed Drain-Source Current</td><td>I<sub>DM</sub></td><td></td><td></td><td>3600</td><td>t<sub>Pmax</sub> limited by T<sub>VJmax</sub><br>V<sub>GS</sub> = 18 V, T<sub>C</sub> = 25 °C</td></tr>
<tr><td>Power Dissipation</td><td>P<sub>D</sub></td><td></td><td>7282</td><td></td><td>W</td><td>T<sub>C</sub> = 25 °C, T<sub>VJ</sub> ≤ 175 °C</td><td>Note 5<br>Fig. 12</td></tr>
<tr><td>Virtual Junction Temperature</td><td>T<sub>VJ(op)</sub></td><td>-55</td><td></td><td>175</td><td>°C</td><td></td><td></td></tr>
</table>

Note (1): Recommended turn-on gate voltage is 18 V with ±5 % regulation tolerance
Note (2): Current limit at T<sub>C</sub> = 25 °C imposed by package
Note (3): Typical current limit calculated by $I_{D(max)} = \sqrt{(P_D/R_{DS(typ)}(T_{VJ(max)}, I_{D(max)}))}$
Note (4): Verified by design
Note (5): $P_D = (T_{VJ} - T_C)/R_{TH(JC,typ)}$


Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice..


<!-- PAGE BREAK -->

HAB900C33LM4


**Preliminary Datasheet**
**Subject to change without notice**


⚡ 2


MOSFET Characteristics (Per Position) (T<sub>VJ</sub> = 25 °C Unless Otherwise Specified)

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr>
<tr><td>Drain-Source Breakdown Voltage</td><td>V<sub>(BR)DSS</sub></td><td>3300</td><td></td><td></td><td rowspan="3">V</td><td>V<sub>GS</sub> = 0 V, T<sub>VJ</sub> = -55 °C</td><td></td></tr>
<tr><td rowspan="2">Gate Threshold Voltage</td><td rowspan="2">V<sub>GS(th)</sub></td><td>2.6</td><td>3.5</td><td>4.4</td><td>V<sub>DS</sub> = V<sub>GS</sub>, I<sub>D</sub> = 530 mA</td><td></td></tr>
<tr><td></td><td>2.6</td><td></td><td>V<sub>DS</sub> = V<sub>GS</sub>, I<sub>D</sub> = 530 mA, T<sub>VJ</sub> = 175 °C</td><td></td></tr>
<tr><td>Zero Gate Voltage Drain Current</td><td>I<sub>DSS</sub></td><td></td><td>20</td><td>400</td><td>µA</td><td>V<sub>GS</sub> = 0 V, V<sub>DS</sub> = 3300 V</td><td></td></tr>
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

Diode Characteristics (Per Position) (T<sub>VJ</sub> = 25 °C Unless Otherwise Specified)

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td><td>Note</td></tr>
<tr><td rowspan="2">Body Diode Forward Voltage</td><td rowspan="2">V<sub>SD</sub></td><td></td><td>5.7</td><td></td><td rowspan="2">V</td><td>V<sub>GS</sub> = -5 V, I<sub>SD</sub> = 900 A</td><td rowspan="2">Fig. 7</td></tr>
<tr><td></td><td>4.7</td><td></td><td>V<sub>GS</sub> = -5 V, I<sub>SD</sub> = 900 A, T<sub>VJ</sub> = 175 °C</td></tr>
</table>

Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- PAGE BREAK -->

HAB900C33LM4


**Preliminary Datasheet**
**Subject to change without notice**


⚡ 3


Module Physical Characteristics

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Conditions</td></tr>
<tr><td>Package Resistance</td><td>R<sub>pkg</sub></td><td></td><td>0.19</td><td></td><td>mΩ</td><td>T<sub>c</sub> = 25 °C, Note 6</td></tr>
<tr><td>Stray Inductance</td><td>L<sub>Stray</sub></td><td></td><td>9.5</td><td></td><td>nH</td><td>Between DC+ and DC-, f = 10 MHz</td></tr>
<tr><td>Storage Temperature</td><td>T<sub>Stg</sub></td><td>-55</td><td></td><td>150</td><td>°C</td><td></td></tr>
<tr><td>Weight</td><td>W</td><td></td><td>745</td><td></td><td>g</td><td></td></tr>
<tr><td rowspan="3">Mounting Torque</td><td rowspan="3">M<sub>S</sub></td><td>3.5</td><td>4.5</td><td>5.5</td><td rowspan="3">N-m</td><td>Baseplate, M6 bolts</td></tr>
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

Temperature Sensor (NTC) Characteristics

<table>
<tr><td>Parameter</td><td>Symbol</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td><td>Test Conditions</td></tr>
<tr><td>Resistance at 25 °C</td><td>R<sub>25</sub></td><td></td><td>4700</td><td></td><td>Ω</td><td>T<sub>NTC</sub> = 25 °C</td></tr>
<tr><td>Tolerance of R<sub>25</sub></td><td></td><td></td><td>±1</td><td></td><td>%</td><td></td></tr>
<tr><td>Beta Value for 25 °C to 85 °C</td><td>B<sub>25/80</sub></td><td></td><td>3435</td><td></td><td>K</td><td></td></tr>
<tr><td>Beta Value for 0 °C to 100 °C</td><td>B<sub>0/100</sub></td><td></td><td>3399</td><td></td><td>K</td><td></td></tr>
<tr><td>Tolerance of B<sub>25/85</sub></td><td></td><td></td><td>±1</td><td></td><td>%</td><td></td></tr>
<tr><td>Maximum Power Dissipation</td><td>P<sub>25</sub></td><td></td><td>50</td><td></td><td>mW</td><td>T<sub>NTC</sub> = 25°C</td></tr>
</table>

Steinhart & Hart Coefficients for NTC Resistance & NTC Temperature Computation (T in K)
ln(R/R<sub>25</sub>) = A + B/T + C/T<sup>2</sup> + D/T<sup>3</sup>  1/T = A<sub>1</sub> + B<sub>1</sub> ln(R/R<sub>25</sub>) + C<sub>1</sub> ln<sup>2</sup>(R/R<sub>25</sub>) + D<sub>1</sub> ln<sup>3</sup>(R/R<sub>25</sub>)

<table>
<tr><td>A</td><td>B</td><td>C</td><td>D</td><td>A<sub>1</sub></td><td>B<sub>1</sub></td><td>C<sub>1</sub></td><td>D<sub>1</sub></td></tr>
<tr><td>-1.289E+01</td><td>4.245E+03</td><td>-8.749E+04</td><td>-9.588E+06</td><td>3.354E-03</td><td>3.001E-04</td><td>5.085E-06</td><td>2.188E-07</td></tr>
</table>

Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- PAGE BREAK -->

HAB900C33LM4


**Preliminary Datasheet**
**Subject to change without notice**


4


<figure type="CHART">Typical Performance 

<description>The figure is a line chart displaying output characteristics for a device, specifically Drain-Source Current (IDS) in Amperes versus Drain-Source Voltage (VDS) in Volts. The chart illustrates performance across various junction temperatures ranging from -40 °C to 175 °C. The conditions are specified as tp < 350 μs and VGS = 18 V. The chart shows multiple linear curves sloping upwards from the origin (0,0), with steeper slopes corresponding to lower temperatures (-40 °C, 25 °C) and shallower slopes corresponding to higher temperatures (100 °C, 125 °C, 150 °C, 175 °C).</description> Figure 1. Output Characteristics for Various Junction Temperatures <table><tr><td>Drain-Source Voltage (VDS) (V)</td><td>Drain-Source Current (IDS) (A) at -40 °C</td><td>Drain-Source Current (IDS) (A) at 25 °C</td><td>Drain-Source Current (IDS) (A) at 100 °C</td><td>Drain-Source Current (IDS) (A) at 125 °C</td><td>Drain-Source Current (IDS) (A) at 150 °C</td><td>Drain-Source Current (IDS) (A) at 175 °C</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>~1000</td><td>~700</td><td>~400</td><td>~350</td><td>~300</td><td>~250</td></tr><tr><td>2</td><td>~2000</td><td>~1400</td><td>~800</td><td>~700</td><td>~600</td><td>~500</td></tr><tr><td>3</td><td>-</td><td>-</td><td>~1200</td><td>~1050</td><td>~900</td><td>~750</td></tr><tr><td>4</td><td>-</td><td>-</td><td>~1600</td><td>~1400</td><td>~1200</td><td>~1000</td></tr><tr><td>5</td><td>-</td><td>-</td><td>~2000</td><td>~1750</td><td>~1500</td><td>~1250</td></tr><tr><td>6</td><td>-</td><td>-</td><td>-</td><td>-</td><td>~1800</td><td>~1500</td></tr></table></figure>

<table>
<tr><td rowspan="10">Normalized On-resistance (p.u.)</td><td>3.0</td><td>tp &lt; 350 µs</td><td></td><td></td><td></td><td></td></tr>
<tr><td rowspan="2">2.5</td><td>V<sub>GS</sub> = 18 V</td><td></td><td>175 °C</td><td>[diagonal line]</td><td>[diagonal line]</td></tr>
<tr><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td rowspan="2">2.0</td><td></td><td rowspan="2">____________________________________________________________<br>____________________________________________________________</td><td rowspan="3">150 °C<br><br>125 °C<br><br>100 °C</td><td>[diagonal line]</td><td>[diagonal line]</td></tr>
<tr><td rowspan="2"><br><br></td><td>[diagonal line]</td><td>[diagonal line]</td></tr>
<tr><td rowspan="3">1.5<br><br><br><br><br>1.0</td><td></td><td>[line segment]</td><td>[line segment]</td></tr>
<tr><td></td><td></td><td>25 °C</td><td></td><td>[line segment]</td></tr>
<tr><td></td><td></td><td>0 °C</td><td>[line segment]</td><td>[line segment]</td></tr>
<tr><td></td><td></td><td></td><td></td><td>[line segment]</td><td>[line segment]</td></tr>
<tr><td>0.5</td><td></td><td></td><td>-40 °C</td><td>[line segment]</td><td>[line segment]</td></tr>
</table>

0 500 1000 1500 2000
Drain-Source Current, I<sub>DS</sub> (A)
**Figure 2.** Normalized On-State Resistance vs. Drain Current
for Various Junction Temperatures

<figure type="CHART">Figure 3. Normalized On-State Resistance vs. Junction Temperature. 

<description>The image displays a line chart showing the relationship between Normalized On-resistance (p.u.) on the y-axis and Virtual Junction Temperature, Tvj (°C) on the x-axis. The curve starts at approximately 0.7 p.u. at -40°C and increases non-linearly to 2.5 p.u. at 175°C. A text box in the upper left corner specifies the test conditions: tp < 350 µs, VGS = 18 V, and IDS = 900 A.</description><table><thead><tr><th>Virtual Junction Temperature, Tvj (°C)</th><th>Normalized On-resistance (p.u.)</th></tr></thead><tbody><tr><td>-40</td><td>0.7</td></tr><tr><td>-25</td><td>0.75</td></tr><tr><td>0</td><td>0.85</td></tr><tr><td>25</td><td>1.0</td></tr><tr><td>50</td><td>1.2</td></tr><tr><td>75</td><td>1.4</td></tr><tr><td>100</td><td>1.65</td></tr><tr><td>125</td><td>1.9</td></tr><tr><td>150</td><td>2.2</td></tr><tr><td>175</td><td>2.5</td></tr></tbody></table></figure>

<figure type="CHART">

<description>A line chart titled "Figure 4. Transfer Characteristic for Various Junction Temperatures" displays the relationship between Drain-Source Current (I_DS in A) on the y-axis and Gate-Source Voltage (V_GS in V) on the x-axis for a MOSFET under various junction temperatures. The chart includes a box in the upper-left corner specifying test conditions: "tp < 350 µs" and "V_DS = 20 V". Multiple curves are plotted, representing temperatures of -40 °C, 25 °C, 100 °C, 125 °C, 150 °C, and 175 °C. An arrow points towards the top-left, indicating the direction of increasing temperature. The x-axis ranges from 0 to 9 V, and the y-axis ranges from 0 to 2400 A. The grid lines provide a scale for reading the values.</description><table><thead><tr><th>Gate-Source Voltage, V_GS (V)</th><th>Drain-Source Current, I_DS (A) at -40°C</th><th>Drain-Source Current, I_DS (A) at 25°C</th><th>Drain-Source Current, I_DS (A) at 100°C</th><th>Drain-Source Current, I_DS (A) at 125°C</th><th>Drain-Source Current, I_DS (A) at 150°C</th><th>Drain-Source Current, I_DS (A) at 175°C</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>2</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>4</td><td>~100</td><td>~200</td><td>~300</td><td>~350</td><td>~400</td><td>~450</td></tr><tr><td>6</td><td>~600</td><td>~800</td><td>~900</td><td>~1000</td><td>~1100</td><td>~1200</td></tr><tr><td>8</td><td>~1200</td><td>~1600</td><td>~1800</td><td>~2000</td><td>~2200</td><td>~2400</td></tr></tbody></table></figure>

<figure type="CHART">

<description>The image displays a line chart showing the 3rd Quadrant Characteristic of a device, plotting Source-Drain Current (ISD) in Amperes on the y-axis versus Source-Drain Voltage (VSD) in Volts on the x-axis. The chart illustrates the relationship at various junction temperatures: -40 °C, 25 °C, 100 °C, 125 °C, 150 °C, and 175 °C. The condition specified is tp < 350 μs and VGS = 18 V. The lines originate from the origin (0,0) and slope upwards, with the slope decreasing as temperature increases.</description> <table><thead><tr><th>Source-Drain Voltage, VSD (V)</th><th>ISD (A) at -40 °C</th><th>ISD (A) at 25 °C</th><th>ISD (A) at 100 °C</th><th>ISD (A) at 125 °C</th><th>ISD (A) at 150 °C</th><th>ISD (A) at 175 °C</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>800</td><td>650</td><td>450</td><td>400</td><td>350</td><td>300</td></tr><tr><td>2</td><td>1600</td><td>1300</td><td>900</td><td>800</td><td>700</td><td>600</td></tr><tr><td>3</td><td>2400</td><td>1950</td><td>1350</td><td>1200</td><td>1050</td><td>900</td></tr><tr><td>4</td><td>-</td><td>-</td><td>1800</td><td>1600</td><td>1400</td><td>1200</td></tr><tr><td>5</td><td>-</td><td>-</td><td>2250</td><td>2000</td><td>1750</td><td>1500</td></tr><tr><td>6</td><td>-</td><td>-</td><td>-</td><td>-</td><td>2100</td><td>1800</td></tr><tr><td>7</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>2100</td></tr></tbody></table> Figure 5. 3rd Quadrant Characteristic vs. Junction Temperatures at VGS = 18 V</figure>

<figure type="CHART">

<description>The figure is a line chart titled 'Figure 6. 3rd Quadrant Characteristic vs. Junction Temperatures at VGS = 0 V (Body Diode)'. It plots Source-Drain Current, ISD (A) on the y-axis (ranging from 0 to 2400) against Source-Drain Voltage, VSD (V) on the x-axis (ranging from 0 to 8). A box in the top-left corner indicates test conditions: 'tp < 300 μs' and 'VGS = 0 V'. The chart displays six curves representing different junction temperatures (-40 °C, 25 °C, 100 °C, 125 °C, 150 °C, and 175 °C). As temperature increases, the curves shift, generally showing higher current at a given voltage for lower temperatures in the linear region, with an arrow pointing from the top-left to the bottom-right indicating the direction of increasing temperature. The curves intersect near the 2.5V-3V mark.</description><table><thead><tr><th>VSD (V)</th><th>-40 °C</th><th>25 °C</th><th>100 °C</th><th>125 °C</th><th>150 °C</th><th>175 °C</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>2</td><td>approx 150</td><td>approx 150</td><td>approx 150</td><td>approx 150</td><td>approx 150</td><td>approx 150</td></tr><tr><td>4</td><td>1300</td><td>800</td><td>700</td><td>650</td><td>600</td><td>550</td></tr><tr><td>6</td><td>2000</td><td>1250</td><td>1100</td><td>1000</td><td>900</td><td>850</td></tr><tr><td>8</td><td>2400</td><td>1650</td><td>1500</td><td>1350</td><td>1250</td><td>1200</td></tr></tbody></table></figure>

Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- PAGE BREAK -->

HAB900C33LM4


**Preliminary Datasheet**
**Subject to change without notice**


5 [LIGHTNING_BOLT_SYMBOL]


<figure type="CHART">Typical Performance



<description>The image is a line chart titled "3rd Quadrant Characteristic vs. Junction Temperatures at VGS = -5 V (Body Diode)". The chart plots Source-Drain Current (ISD) in Amperes (A) on the y-axis against Source-Drain Voltage (VSD) in Volts (V) on the x-axis. The y-axis ranges from 0 to 2400 A in increments of 400. The x-axis ranges from 0 to 7 V in increments of 1. A text box in the upper left corner specifies "tp < 350 μs" and "VGS = -5 V". The chart displays multiple curves representing different junction temperatures (-40 °C, 25 °C, 100 °C, 150 °C, and 175 °C). An arrow indicates the direction of increasing temperature. As the temperature increases, the current increases for a given voltage. The curves generally show an exponential-like rise starting around 2.5 V.</description>

<table>
  <thead>
    <tr>
      <th>VSD (V)</th>
      <th>ISD (A) (-40 °C)</th>
      <th>ISD (A) (25 °C)</th>
      <th>ISD (A) (100 °C)</th>
      <th>ISD (A) (150 °C)</th>
      <th>ISD (A) (175 °C)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0-2.5</td>
      <td>~0</td>
      <td>~0</td>
      <td>~0</td>
      <td>~0</td>
      <td>~0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>~50</td>
      <td>~100</td>
      <td>~150</td>
      <td>~200</td>
      <td>~250</td>
    </tr>
    <tr>
      <td>4</td>
      <td>~400</td>
      <td>~500</td>
      <td>~600</td>
      <td>~700</td>
      <td>~800</td>
    </tr>
    <tr>
      <td>5</td>
      <td>~800</td>
      <td>~950</td>
      <td>~1100</td>
      <td>~1200</td>
      <td>~1350</td>
    </tr>
    <tr>
      <td>6</td>
      <td>~1200</td>
      <td>~1350</td>
      <td>~1500</td>
      <td>~1700</td>
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
</table>

Figure 7. 3rd Quadrant Characteristic vs. Junction Temperatures at VGS = -5 V (Body Diode)</figure>

<figure type="CHART">

<description>A log-linear line chart titled "Figure 8. Typical Capacitances vs. Drain to Source Voltage (0 - 200 V)" displays three curves representing capacitance values (Ciss, Coss, Crss) in nanofarads (nF) on the y-axis against Drain-Source Voltage (VDS) in volts on the x-axis, ranging from 0 to 200 V. The y-axis is logarithmic, spanning from 0.01 to 1000 nF. A box inset in the lower-left area provides test conditions: "Tvj = 25 °C", "VAC = 25 mV", and "f = 100 kHz".</description><table><tr><th>Drain-Source Voltage (V)</th><th>Ciss (nF)</th><th>Coss (nF)</th><th>Crss (nF)</th></tr><tr><td>0</td><td>~200</td><td>~70</td><td>~70</td></tr><tr><td>25</td><td>~180</td><td>~10</td><td>~1.5</td></tr><tr><td>50</td><td>~180</td><td>~5</td><td>~0.4</td></tr><tr><td>100</td><td>~180</td><td>~3</td><td>~0.2</td></tr><tr><td>200</td><td>~180</td><td>~2</td><td>~0.06</td></tr></table></figure>

<figure type="CHART">

<description>The figure is a line chart titled 'Figure 9. Typical Capacitances vs. Drain to Source Voltage (0 - 3300V)'. It plots capacitance (nF) on the y-axis (logarithmic scale, ranging from 0.01 to 1000) against Drain-Source Voltage (V_DS) on the x-axis (linear scale, ranging from 0 to 3300 V). The chart displays three curves representing C_iss, C_oss, and C_rss. An inset box indicates the test conditions: T_VJ = 25 °C, V_AC = 25 mV, and f = 100 kHz.</description> <table><thead><tr><th>Voltage (V)</th><th>C_iss (nF)</th><th>C_oss (nF)</th><th>C_rss (nF)</th></tr></thead><tbody><tr><td>0</td><td>~180</td><td>~180</td><td>~180</td></tr><tr><td>100</td><td>~180</td><td>~15</td><td>~2</td></tr><tr><td>500</td><td>~180</td><td>~5</td><td>~0.2</td></tr><tr><td>1000</td><td>~180</td><td>~3</td><td>~0.1</td></tr><tr><td>1500</td><td>~180</td><td>~2.5</td><td>~0.08</td></tr><tr><td>2000</td><td>~180</td><td>~2.3</td><td>~0.07</td></tr><tr><td>2500</td><td>~180</td><td>~2.2</td><td>~0.06</td></tr><tr><td>3000</td><td>~180</td><td>~2.1</td><td>~0.06</td></tr><tr><td>3300</td><td>~180</td><td>~2.1</td><td>~0.06</td></tr></tbody></table></figure>

<figure type="CHART">

<description>A line chart showing the relationship between Threshold Voltage (V_TH) and Virtual Junction Temperature (T_VJ). The x-axis represents the Virtual Junction Temperature ranging from -50 to 200 °C. The y-axis represents the Threshold Voltage ranging from 0 to 6 V. A single curve plots the data points, showing a downward trend as temperature increases. A text box in the upper left corner indicates the test conditions: V_GS = V_DS and I_DS = 530 mA.</description><table><thead><tr><th>Virtual Junction Temperature, T_VJ (°C)</th><th>Threshold Voltage, V_TH (V)</th></tr></thead><tbody><tr><td>-50</td><td>~4.2</td></tr><tr><td>0</td><td>~3.7</td></tr><tr><td>50</td><td>~3.4</td></tr><tr><td>100</td><td>~3.0</td></tr><tr><td>150</td><td>~2.8</td></tr><tr><td>175</td><td>~2.7</td></tr></tbody></table>Figure 10. Threshold Voltage vs. Junction Temperature</figure>

<figure type="CHART">

<description>A line chart titled 'Figure 11. Continuous Drain Current Derating vs. Case Temperature' illustrating the relationship between Drain-Source DC Current (IDS) in Amperes and Case Temperature (TC) in degrees Celsius. The chart includes a 'Package Limit' constant line and a derating curve. The conditions box specifies Tvj <= 175 °C.</description><table><thead><tr><th>Case Temperature (°C)</th><th>Drain-Source DC Current (A)</th></tr></thead><tbody><tr><td>-50</td><td>1200 (Package Limit) / ~1480 (Derating Curve)</td></tr><tr><td>25</td><td>1200</td></tr><tr><td>150</td><td>500</td></tr></tbody></table></figure>

<figure type="CHART">

<description>The figure is a line chart titled "Maximum Power Dissipation Derating vs. Case Temperature". It displays the relationship between Case Temperature (T_C in °C) on the x-axis and FET Power Dissipation (P_D in W) on the y-axis. The x-axis ranges from -75 to 175 with increments of 25. The y-axis ranges from 0 to 12000 with increments of 2000. A single solid black line plots the derating, starting at approximately (T_C = -60, P_D ≈ 11200) and sloping downwards to approximately (T_C = 150, P_D ≈ 1200). An inset box in the top-right corner states: "Conditions: T_VJ ≤ 175 °C". The chart uses a dashed grid background.</description> <table><thead><tr><th>Case Temperature (T_C, °C)</th><th>FET Power Dissipation (P_D, W)</th></tr></thead><tbody><tr><td>-60 (approx)</td><td>11200 (approx)</td></tr><tr><td>150</td><td>1200 (approx)</td></tr></tbody></table> Figure 12. Maximum Power Dissipation Derating vs. Case Temperature</figure>

Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- PAGE BREAK -->

HAB900C33LM4


**Preliminary Datasheet**
**Subject to change without notice**


6


<figure type="CHART">Definitions



<description>This figure is a multi-line chart illustrating Turn-off Transient Definitions for power electronics, showing three superimposed waveforms over time. The top purple line represents the Gate-Source Voltage (VGS), which drops from a high level. The middle dark blue line represents the Drain-Source Voltage (VDS), which rises. The bottom light blue line represents the Source Current (IS), which drops to zero. Various timing parameters are annotated: td(off) (turn-off delay time), tf (fall time), and toff (turn-off time). Specific percentage points (90% VGS, 90% IS, 10% VDS, 10% IS) are marked. Slopes for switching rates are indicated as *dv/dtoff and *di/dtoff. The energy loss during turn-off is defined as EOFF = ∫ VDS x IS. An asterisk note at the bottom left reads: '*Peak rate of change for a sliding 5 ns window'.</description>

Figure 13. Turn-off Transient Definitions

<table><tr><td>Waveform</td><td>Color</td><td>Behavior</td></tr><tr><td>Gate-Source Voltage (VGS)</td><td>Purple</td><td>Decreases from high to low level</td></tr><tr><td>Drain-Source Voltage (VDS)</td><td>Dark Blue</td><td>Increases from low to high level</td></tr><tr><td>Source Current (IS)</td><td>Light Blue</td><td>Decreases from high to zero</td></tr></table></figure>

<figure type="CHART">

<description>The figure is a multi-line chart illustrating 'Turn-on Transient Definitions' for a power electronic device. It displays three overlapping waveforms over time: Gate-Source Voltage (V_GS) in purple, Source Current (I_S) in light blue, and Drain-Source Voltage (V_DS) in dark blue.</description> <table><tr><td>Waveform</td><td>Description</td></tr><tr><td>Gate-Source Voltage (V_GS)</td><td>Purple line showing a rising voltage transition.</td></tr><tr><td>Source Current (I_S)</td><td>Light blue line showing a rapid increase from 0 to peak current, with ringing after the transition.</td></tr><tr><td>Drain-Source Voltage (V_DS)</td><td>Dark blue line showing a rapid decrease from a high state to 0.</td></tr></table> 

<description>Key timing parameters and definitions are marked on the chart:</description> <ul><li>t_d(on): Delay time between the start of V_GS rise and the start of I_S rise.</li><li>t_r: Rise time for I_S.</li><li>t_on: Total turn-on time, defined as t_d(on) + t_r.</li><li>di/dt_ON: Peak rate of change for source current in a sliding 5 ns window.</li><li>dv/dt_ON: Peak rate of change for drain-source voltage in a sliding 5 ns window.</li><li>E_ON: Energy loss during turn-on, represented by the integral of the product of V_DS and I_S (∫ V_DS x I_S).</li></ul> 

<description>The chart includes annotations for 10% and 90% threshold points for V_GS, I_S, and V_DS to define the switching intervals. The figure title is 'Figure 14. Turn-on Transient Definitions'.</description></figure>

<figure type="CHART">

<description>The figure illustrates the characteristics of a reverse recovery current waveform, labeled 'Reverse Recovery Current, IRR (A)' on the y-axis. The curve shows the transition of current from a forward state (IF) down to a negative peak (IRRM) and then oscillating before settling. Key parameters are defined: 'trr' represents the total reverse recovery time, which is subdivided into 'tf' (fall time) and 'ts' (storage time). The area under the curve between the zero-crossing points is shaded and labeled 'QRR' (reverse recovery charge). A specific slope segment on the falling edge is marked '*di/dtRR', with an annotation below noting: '*Peak rate of change for a sliding 5 ns window during the falling event'. The x-axis indicates zero current levels at the start and end of the recovery phase. Figure 15. Reverse Recovery Definitions.</description> <table><tr><td>Parameter</td><td>Description</td></tr><tr><td>IF</td><td>Forward current</td></tr><tr><td>IRRM</td><td>Peak reverse recovery current</td></tr><tr><td>trr</td><td>Total reverse recovery time</td></tr><tr><td>tf</td><td>Fall time</td></tr><tr><td>ts</td><td>Storage time</td></tr><tr><td>QRR</td><td>Reverse recovery charge</td></tr><tr><td>di/dtRR</td><td>Peak rate of change (sliding 5 ns window)</td></tr></table></figure>

<figure type="CHART">

<description>This chart illustrates the VGS transient definitions for a gate-source voltage waveform. The Y-axis represents the Gate-Source Voltage (VGS) in volts. The waveform is a rectangular pulse that transitions between an upper level of 18 V and a lower level of -5 V. The transition from 18 V to -5 V includes a negative overshoot down to -10 V with subsequent ringing. The transition from -5 V to 18 V includes a positive overshoot up to 23 V with subsequent ringing. The chart labels two key parameters: VGS-Static, indicating the difference between the steady-state levels (18 V and -5 V), and VGS-Dynamic, indicating the full excursion range between the peaks of the overshoot (23 V and -10 V).</description><table><thead><tr><th>Feature</th><th>Value/Description</th></tr></thead><tbody><tr><td>Vertical Axis Label</td><td>Gate - Source Voltage, VGS (V)</td></tr><tr><td>High Level Steady State</td><td>18 V</td></tr><tr><td>Low Level Steady State</td><td>-5 V</td></tr><tr><td>Negative Overshoot Peak</td><td>-10 V</td></tr><tr><td>Positive Overshoot Peak</td><td>23 V</td></tr><tr><td>VGS-Static Range</td><td>Between 18 V and -5 V</td></tr><tr><td>VGS-Dynamic Range</td><td>Between 23 V and -10 V</td></tr></tbody></table>Figure 16. VGS Transient Definitions</figure>

Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- PAGE BREAK -->

HAB900C33LM4


**Preliminary Datasheet**
**Subject to change without notice**


7 [LIGHTNING BOLT SYMBOL]


<figure type="DIAGRAM">Schematic and Pin Out



<description>The figure is a technical line drawing representing the pin layout and schematic of a rectangular electronic power module component. The device features a series of screw terminals or mounting holes along the top, bottom, and sides. The central area contains a lightning-bolt-like logo. Numbered pins are arranged in two columns along the sides: pins 12, 13, 14, 15 are on the left side, and pins 11, 10, 9, 8 are on the right side. Smaller numbered pins 3, 4, 5 are aligned along the top inner edge, while pins 6, 1 and 7, 2 are arranged in pairs near the bottom inner edge. The component has a distinct rectangular footprint with multiple connection points, indicating it is an industrial power semiconductor or similar high-power electronic device.</description>

Package Dimensions (mm)</figure>

<figure type="DIAGRAM">

<description>This is a schematic diagram of a power module circuit featuring two N-channel MOSFETs arranged in a half-bridge configuration. The top MOSFET is connected to terminals 1, 2, and 9 at the drain. Its source is connected to terminals 10 and 11 (gate/source drive). The bottom MOSFET has its drain connected to terminals 12, 3, 4, and 5. The bottom MOSFET's source is connected to terminals 14 and 15 (gate/source drive) and is also connected to terminal 8 and terminals 6, 7. A thermistor, indicated by the symbol '-t°', is connected between the bottom MOSFET's source node and terminal 13. Each MOSFET includes an intrinsic body diode.</description></figure>

<figure type="DIAGRAM">

<description>This is a technical diagram of an electronic power module, likely an IGBT or similar semiconductor power device, depicted in an isometric line drawing view. The module has a rectangular base with a multi-layered heat sink or casing structure. On the top surface, there are several large power terminals (labeled 1 through 7 and 12 through 15) and smaller signal or control connectors (labeled 8 through 11). The labels are indicated by circled numbers pointing to specific features of the assembly. The drawing style is a clean, technical CAD-style wireframe representation, focusing on the mechanical and electrical interface points of the component.</description></figure>

<figure type="DIAGRAM">

<description>This is a detailed mechanical engineering diagram of an electronic component, likely a power module, viewed from the top-down perspective. The diagram displays various mounting points, terminals, and connector pins labeled with alphanumeric codes.</description>

### Key Annotations and Dimensions
- **Top section:** 
  - "8x M3 ⬇ 5 MAX"
  - "7x M8 ⬇ 15 MAX"
- **Left vertical dimension:** "68.96±0.75"
- **Bottom horizontal dimension:** "73.24±0.30"

### Labeled Points and Connectors
- **Markers (A-series):** A1, A2, A3, A4, A5, A6, A7
- **Markers (B-series):** B1, B2, B3, B4, B5, B6
- **Markers (C-series):** C1, C2, C3, C4, C5, C6, C7, C8, C9, C10

### Terminal Numbering
- The component features numbered terminals visible in the central area:
  - Top row: 3, 4, 5
  - Middle-left: 12, 13, 14, 15
  - Middle-right: 11, 10, 9, 8
  - Bottom-middle: 6, 7, 1, 2

### Central Logo
- A stylized lightning bolt logo is centered in the main rectangular body of the component.</figure>

<figure type="DIAGRAM">

<description>This is a technical line drawing, specifically a side-profile view of a mechanical or electronic component assembly. The drawing is presented in a vertical orientation. The main body of the object features a series of vertical, parallel grooves or ribs along its length, suggesting a heat sink or a modular connector housing. On the left side, there are distinct rectangular cutouts and stepped features. At the bottom of the image, there are three callout markers pointing to specific features of the component: a hexagonal marker labeled 'B7', a hexagonal marker labeled 'C11', and a hexagonal marker labeled 'A8'. To the far right of the A8 marker, there is a small, unlabeled '0' digit.</description> B7 C11 A8 0</figure>

<table>
<tr><td colspan="3">DIMENSION TABLE</td></tr>
<tr><td>SYMBOL</td><td>DIMENSION</td><td>TOLERANCE</td></tr>
<tr><td>A1</td><td>2x 6.5</td><td>±1.0</td></tr>
<tr><td>A2</td><td>2x 133.5</td><td>±1.0</td></tr>
<tr><td>A3</td><td>140</td><td>±0.75</td></tr>
<tr><td>[A4 icon]</td><td>144</td><td>±0.5</td></tr>
<tr><td>[A5 icon]</td><td>2×6.9</td><td>±0.75</td></tr>
<tr><td>[A6 icon]</td><td>2×92.9</td><td>±0.75</td></tr>
<tr><td>[A7 icon]</td><td>99.8</td><td>±0.5</td></tr>
<tr><td>[A8 icon]</td><td>4</td><td>±0.3</td></tr>
<tr><td>[B1 icon]</td><td>2×11</td><td>±0.5</td></tr>
<tr><td>[B2 icon]</td><td>2×40.5</td><td>±0.5</td></tr>
<tr><td>[B3 icon]</td><td>3×133.5</td><td>±0.5</td></tr>
<tr><td>[B4 icon]</td><td>3×26.9</td><td>±0.5</td></tr>
<tr><td>[B5 icon]</td><td>49.9</td><td>±0.5</td></tr>
<tr><td>B6</td><td>3× 72.9</td><td>±0.5</td></tr>
<tr><td>B7</td><td>40</td><td>±0.75</td></tr>
<tr><td>C1</td><td>57</td><td>±0.4</td></tr>
<tr><td>C2</td><td>66.5</td><td>±0.4</td></tr>
<tr><td>C3</td><td>57</td><td>±0.6</td></tr>
<tr><td>[C4 icon]</td><td>79.5</td><td>±0.4</td></tr>
<tr><td>[C5 icon]</td><td>110.5</td><td>±0.4</td></tr>
<tr><td>[C6 icon]</td><td>82.3</td><td>±0.5</td></tr>
<tr><td>[C7 icon]</td><td>101</td><td>±0.4</td></tr>
<tr><td>[C8 icon]</td><td>110.5</td><td>±0.4</td></tr>
<tr><td>[C9]</td><td>4 × 8.9</td><td>±0.6</td></tr>
<tr><td>[C10]</td><td>4 × 90.9</td><td>±0.6</td></tr>
<tr><td>[C11]</td><td>35</td><td>±0.75</td></tr>
</table>

Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- PAGE BREAK -->

HAB900C33LM4


**Preliminary Datasheet**
**Subject to change without notice**


8


# Supporting Links & Tools

## Evaluation Tools & Support

- LTspice and PLECS Models
- SpeedFit<sup>®</sup> Design Simulator
- Technical Support Forum


Dual-Channel Gate Driver Board
- CGD12HB00D: Differential Transceiver Daughter Board Companion Tool for Differential Gate Drivers
- CGD1700HB2M-UNA: Wolfspeed Gate Driver Board
- EVAL-ADUM4146WHB1Z: Analog Devices<sup>®</sup> Gate Driver Board
- UCC21710QDWEVM-054: Texas Instruments<sup>®</sup> Gate Driver Board


# Application Notes

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


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- PAGE BREAK -->

HAB900C33LM4


Preliminary Datasheet


9


# Notes & Disclaimers

WOLFSPEED PROVIDES TECHNICAL AND RELIABILITY DATA, DESIGN RESOURCES, APPLICATION OR OTHER DESIGN
ADVICE, WEB TOOLS, AND OTHER RESOURCES “AS IS” AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES,
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
“typical”) constitutes Wolfspeed’s sole published specifications for the subject product. “Typical” parameters are
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


**RoHS Compliance**
The levels of RoHS restricted materials in this product are below the maximum concentration values (also
referred to as the threshold limits) permitted for such substances, or are used in an exempted application, in
accordance with EU Directive 2011/65/EC (RoHS2), as implemented January 2, 2013. RoHS Declarations for this
product can be obtained from your Wolfspeed representative or from the Product Documentation sections of
www.wolfspeed.com.


**REACH Compliance**
REACH substances of high concern (SVHCs) information is available for this product. Since the European Chemical
Agency (ECHA) has published notice of their intent to frequently revise the SVHC listing for the foreseeable future,
please contact your Wolfspeed representative to ensure you get the most up-to-date REACH SVHC Declaration.
REACH banned substance information (REACH Article 67) is also available upon request.


Contact info: 
4600 Silicon Drive 
Durham, NC 27703 USA 
Tel: +1.919.313.5300 
www.wolfspeed.com/power 

© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed® and the Wolfstreak logo are registered trademarks and the Wolfspeed logo is a trademark of Wolfspeed, Inc.
PATENT: https://www.wolfspeed.com/legal/patents


The information in this document is subject to change without notice.


Preliminary Rev. 1, May 2026


4600 Silicon Drive | Durham, NC 27703 | Tel: +1.919.313.5300 | wolfspeed.com/power


© 2026 Wolfspeed, Inc. All rights reserved. Wolfspeed®, the Wolfspeed logo, the Wolfstreak logo, WolfPACK®, Wolfspeed WolfPACK®, and the Wolfspeed WolfPACK logo are registered
trademarks of Wolfspeed, Inc. The information in this document is subject to change without notice.


<!-- doc_id=parse-01m4ytm5rbsz29dbv70hq5rjkn -->