v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 120 -110 120 -90 {
lab=VDD}
N 120 70 120 90 {
lab=VSS}
N -220 0 -170 0 {
lab=CK_I}
N -30 0 40 0 {
lab=#net1}
N 40 30 40 100 {
lab=CK_I}
N -200 100 40 100 {
lab=CK_I}
N -200 0 -200 100 {
lab=CK_I}
N -220 -50 40 -50 {
lab=EN}
N 40 100 40 160 {
lab=CK_I}
N 40 160 240 160 {
lab=CK_I}
N 240 -10 240 160 {
lab=CK_I}
N 200 -50 240 -50 {
lab=#net2}
N 380 -30 400 -30 {
lab=#net3}
N 540 -30 560 -30 {
lab=CK_O}
C {xschem_lib/DFFRAM_full_custom/inv.sym} -170 40 0 0 {name=X_inv1 NF=2}
C {xschem_lib/DFFRAM_full_custom/latch.sym} 40 70 0 0 {name=X_latch1 NF=2}
C {ipin.sym} -220 0 0 0 {name=p1 lab=CK_I}
C {iopin.sym} 120 -110 3 0 {name=p2 lab=VDD}
C {iopin.sym} 120 90 1 0 {name=p3 lab=VSS}
C {lab_wire.sym} -110 -40 1 0 {name=l1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -110 40 2 0 {name=l2 sig_type=std_logic lab=VSS}
C {ipin.sym} -220 -50 0 0 {name=p4 lab=EN}
C {xschem_lib/DFFRAM_full_custom/nand.sym} 260 0 0 0 {name=X_nand1 NF=2}
C {lab_wire.sym} 290 -80 1 0 {name=l3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 290 20 2 0 {name=l4 sig_type=std_logic lab=VSS}
C {xschem_lib/DFFRAM_full_custom/inv.sym} 400 10 0 0 {name=X_inv2 NF=12}
C {lab_wire.sym} 460 -70 1 0 {name=l5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 460 10 2 0 {name=l6 sig_type=std_logic lab=VSS}
C {opin.sym} 560 -30 0 0 {name=p5 lab=CK_O}
