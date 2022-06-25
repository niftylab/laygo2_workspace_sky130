v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 160 -180 240 -180 {
lab=#net1}
N 160 100 260 100 {
lab=ICLKB}
N 80 -240 80 -220 {
lab=VDD}
N 320 -240 320 -220 {
lab=VDD}
N 400 -180 450 -180 {
lab=Q}
N 400 100 430 100 {
lab=ICLK}
N -30 100 20 100 {
lab=CLK}
N -30 -130 0 -130 {
lab=ICLKB}
N -30 -100 0 -100 {
lab=ICLK}
N 220 -130 240 -130 {
lab=ICLK}
N 220 -100 240 -100 {
lab=ICLKB}
N 80 -60 80 -40 {
lab=VSS}
N 320 -60 320 -40 {
lab=VSS}
N 80 20 80 60 {
lab=VDD}
N 320 20 320 60 {
lab=VDD}
N 320 140 320 180 {
lab=VSS}
N 80 140 80 180 {
lab=VSS}
N -50 -180 -0 -180 {
lab=D}
C {xschem_example/latch.sym} 0 -60 0 0 {name=X_latch1}
C {xschem_example/latch.sym} 240 -60 0 0 {name=X_latch2}
C {xschem_example/inv.sym} 20 140 0 0 {name=X_inv1}
C {xschem_example/inv.sym} 260 140 0 0 {name=X_inv2}
C {ipin.sym} -40 -180 0 0 {name=p1 lab=D}
C {ipin.sym} -20 100 0 0 {name=p2 lab=CLK}
C {iopin.sym} -70 -240 0 0 {name=p3 lab=VSS}
C {iopin.sym} -70 -280 0 0 {name=p4 lab=VDD}
C {opin.sym} 440 -180 0 0 {name=p5 lab=Q}
C {lab_pin.sym} 220 -130 0 0 {name=l1 sig_type=std_logic lab=ICLK}
C {lab_pin.sym} 220 -100 0 0 {name=l2 sig_type=std_logic lab=ICLKB}
C {lab_pin.sym} -30 -130 0 0 {name=l3 sig_type=std_logic lab=ICLKB}
C {lab_pin.sym} -30 -100 0 0 {name=l4 sig_type=std_logic lab=ICLK}
C {lab_pin.sym} 80 -40 0 0 {name=l5 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 430 100 0 1 {name=l11 sig_type=std_logic lab=ICLK}
C {lab_pin.sym} 80 -240 0 0 {name=l12 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 320 -240 0 0 {name=l7 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 80 20 0 0 {name=l9 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 320 20 0 0 {name=l13 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 320 -40 0 0 {name=l6 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 80 180 0 0 {name=l8 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 320 180 0 0 {name=l10 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 230 100 1 0 {name=l14 sig_type=std_logic lab=ICLKB}
