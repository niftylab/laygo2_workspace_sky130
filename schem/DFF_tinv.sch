v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N -30 -40 20 -40 {
lab=IN}
N -10 230 40 230 {
lab=CLK}
N 140 230 170 230 {
lab=ICLKB}
N 270 230 300 230 {
lab=CLKB}
N 180 -40 300 -40 {
lab=#net1}
N 460 -40 500 -40 {
lab=OUT}
N 2.5 0 20 -0 {
lab=ICLKB}
N 2.5 20 20 20 {
lab=ICLK}
N 100 80 100 90 {
lab=VSS}
N 100 -110 100 -100 {
lab=VDD}
N 380 -110 380 -100 {
lab=VDD}
N 290 0 300 0 {
lab=ICLK}
N 290 20 300 20 {
lab=ICLKB}
N 380 80 380 90 {
lab=VSS}
N 150 170 150 230 {
lab=ICLKB}
C {latch.sym} -30 10 0 0 {name=X_latch1}
C {latch.sym} 250 10 0 0 {name=X_latch2}
C {ipin.sym} -20 -40 0 0 {name=p1 lab=IN}
C {iopin.sym} 0 -180 0 1 {name=p2 lab=VDD}
C {iopin.sym} 0 -150 0 1 {name=p3 lab=VSS}
C {lab_pin.sym} 100 -110 0 0 {name=l1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 100 90 0 0 {name=l3 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 380 90 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {ipin.sym} 0 230 0 0 {name=p4 lab=CLK}
C {inv.sym} 10 230 0 0 {name=X_INV1}
C {lab_pin.sym} 90 200 1 0 {name=l5 sig_type=std_logic lab=VDD}
C {inv.sym} 140 230 0 0 {name=X_INV2}
C {lab_pin.sym} 90 260 3 0 {name=l6 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 220 260 3 0 {name=l7 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 220 200 1 0 {name=l8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 300 230 2 0 {name=l9 sig_type=std_logic lab=ICLK}
C {lab_pin.sym} 2.5 20 0 0 {name=l10 sig_type=std_logic lab=ICLK}
C {lab_pin.sym} 2.5 0 0 0 {name=l11 sig_type=std_logic lab=ICLKB}
C {lab_pin.sym} 290 20 0 0 {name=l12 sig_type=std_logic lab=ICLKB}
C {lab_pin.sym} 290 0 0 0 {name=l13 sig_type=std_logic lab=ICLK}
C {opin.sym} 490 -40 0 0 {name=p5 lab=OUT}
C {lab_pin.sym} 380 -110 0 0 {name=l2 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 150 170 0 0 {name=l14 sig_type=std_logic lab=ICLKB}
