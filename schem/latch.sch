v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N -5 20 50 20 {
lab=CLK}
N -5 -10 50 -10 {
lab=IN}
N -5 -40 50 -40 {
lab=CLKB}
N 105 30 105 65 {
lab=VSS}
N 105 -85 105 -50 {
lab=VDD}
N 175 -10 287.5 -10 {
lab=#net1}
N 337.5 -75 337.5 -40 {
lab=VDD}
N 337.5 20 337.5 55 {
lab=VSS}
N 390 160 445 160 {
lab=OUT}
N 335 200 335 235 {
lab=VSS}
N 335 85 335 120 {
lab=VDD}
N 390 130 412.5 130 {
lab=CLK}
N 390 190 412.5 190 {
lab=CLKB}
N 237.5 160 265 160 {
lab=#net1}
N 237.5 -10 237.5 160 {
lab=#net1}
N 445 160 500 160 {
lab=OUT}
N 500 -10 500 160 {
lab=OUT}
N 390 -10 500 -10 {
lab=OUT}
N 386.25 -10 390 -10 {
lab=OUT}
N 500 -10 535 -10 {
lab=OUT}
C {/usr/local/share/xschem/xschem_library/ipin.sym} 2.5 -10 0 0 {name=p1 lab=IN}
C {/usr/local/share/xschem/xschem_library/opin.sym} 527.5 -10 0 0 {name=p6 lab=OUT}
C {/usr/local/share/xschem/xschem_library/ipin.sym} 2.5 20 0 0 {name=p2 lab=CLK}
C {inv.sym} 257.5 -10 0 0 {name=X_INV1}
C {iopin.sym} 35 -180 2 0 {name=p7 lab=VDD}
C {iopin.sym} 35 -150 0 1 {name=p13 lab=VSS}
C {/usr/local/share/xschem/xschem_library/ipin.sym} 1.25 -40 0 0 {name=p4 lab=CLKB}
C {tinv.sym} 10 -10 0 0 {name=X_tinv1}
C {lab_pin.sym} 105 65 0 0 {name=l1 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 105 -85 0 0 {name=l2 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 337.5 -75 0 0 {name=l3 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 337.5 55 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {tinv.sym} 430 160 0 1 {name=X_tinv2}
C {lab_pin.sym} 335 235 0 1 {name=l5 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 335 85 0 1 {name=l6 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 412.5 130 0 1 {name=l7 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 412.5 190 0 1 {name=l8 sig_type=std_logic lab=CLKB}
