v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 140 130 180 130 {
lab=clk_bar}
N 320 130 340 130 {
lab=clk_buf}
N -20 130 -0 130 {
lab=CLK}
N 160 -120 230 -120 {
lab=#net1}
N 220 -70 230 -70 {
lab=clk_buf}
N 220 -40 230 -40 {
lab=clk_bar}
N -10 -70 -0 -70 {
lab=clk_bar}
N -10 -40 -0 -40 {
lab=clk_buf}
N 80 0 80 10 {
lab=#net2}
N 310 0 310 10 {
lab=#net3}
N -10 -120 -0 -120 {
lab=I}
N 80 -170 80 -160 {
lab=VDD}
N 310 -170 310 -160 {
lab=VDD}
N 390 -120 410 -120 {
lab=O}
N 60 80 60 90 {
lab=VDD}
N 240 80 240 90 {
lab=VDD}
N 60 170 60 180 {
lab=#net4}
N 240 170 240 180 {
lab=#net5}
C {xschem_lib/DFFRAM_full_custom/latch.sym} 0 0 0 0 {name=X_latch1 NF=2}
C {xschem_lib/DFFRAM_full_custom/latch.sym} 230 0 0 0 {name=X_latch2 NF=2}
C {xschem_lib/DFFRAM_full_custom/inv.sym} 0 170 0 0 {name=X_inv1 NF=2}
C {xschem_lib/DFFRAM_full_custom/inv.sym} 180 170 0 0 {name=X_inv2 NF=2}
C {iopin.sym} 180 -240 0 0 {name=p1 lab=VDD}
C {iopin.sym} 180 -210 0 0 {name=p2 lab=VSS}
C {ipin.sym} -10 -120 0 0 {name=p3 lab=I}
C {ipin.sym} -20 130 0 0 {name=p4 lab=CLK}
C {opin.sym} 410 -120 0 0 {name=p5 lab=O}
C {lab_pin.sym} 160 130 1 0 {name=l1 sig_type=std_logic lab=clk_bar}
C {lab_pin.sym} -10 -70 0 0 {name=l2 sig_type=std_logic lab=clk_bar}
C {lab_pin.sym} 220 -40 0 0 {name=l3 sig_type=std_logic lab=clk_bar}
C {lab_pin.sym} 340 130 2 0 {name=l4 sig_type=std_logic lab=clk_buf}
C {lab_pin.sym} -10 -40 0 0 {name=l5 sig_type=std_logic lab=clk_buf}
C {lab_pin.sym} 220 -70 0 0 {name=l6 sig_type=std_logic lab=clk_buf}
C {lab_pin.sym} 80 -170 0 0 {name=l7 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 310 -170 0 0 {name=l8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 60 80 1 0 {name=l9 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 240 80 1 0 {name=l10 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 80 10 3 0 {name=l11 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 310 10 3 0 {name=l12 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 240 180 3 0 {name=l13 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 60 180 3 0 {name=l14 sig_type=std_logic lab=VSS}
