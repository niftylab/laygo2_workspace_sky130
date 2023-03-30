v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N -210 -120 -140 -120 {
lab=CLKB}
N -210 -80 -140 -80 {
lab=IN}
N -210 -40 -140 -40 {
lab=CLK}
N -70 -40 -70 0 {
lab=VSS}
N -70 -160 -70 -120 {
lab=VDD}
N 0 -80 140 -80 {
lab=#net1}
N 280 -80 390 -80 {
lab=OUT}
N 220 100 260 100 {
lab=CLK}
N 220 180 260 180 {
lab=CLKB}
N 150 60 150 100 {
lab=VDD}
N 150 180 150 220 {
lab=VSS}
N 40 140 80 140 {
lab=#net1}
N 40 -80 40 140 {
lab=#net1}
N 200 -160 200 -120 {
lab=VDD}
N 200 -40 200 0 {
lab=VSS}
N 220 140 320 140 {
lab=OUT}
N 320 -80 320 140 {
lab=OUT}
C {ipin.sym} -200 -120 0 0 {name=p1 lab=CLKB}
C {ipin.sym} -200 -80 0 0 {name=p2 lab=IN}
C {ipin.sym} -200 -40 0 0 {name=p3 lab=CLK}
C {iopin.sym} -190 -220 0 0 {name=p4 lab=VDD}
C {iopin.sym} -190 -200 0 0 {name=p5 lab=VSS}
C {lab_pin.sym} -70 -160 0 0 {name=l1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -70 0 0 0 {name=l2 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 200 0 0 0 {name=l3 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 200 -160 0 0 {name=l4 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 260 100 0 1 {name=l5 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 260 180 0 1 {name=l6 sig_type=std_logic lab=CLKB}
C {lab_pin.sym} 150 60 0 0 {name=l7 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 150 220 0 0 {name=l8 sig_type=std_logic lab=VSS}
C {opin.sym} 380 -80 0 0 {name=p6 lab=OUT}
C {xschem_lib/tinv.sym} -140 -40 0 0 {name=X_tinv1 NF=NF}
C {xschem_lib/inv.sym} 140 -40 0 0 {name=X_inv1 NF=NF}
C {xschem_lib/tinv_small.sym} 220 180 0 1 {name=X_tinv_small1}
