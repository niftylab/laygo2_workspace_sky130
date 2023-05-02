v {xschem version=3.1.0 file_version=1.2
}
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
lab=VSS}
N 310 0 310 10 {
lab=VSS}
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
lab=VSS}
N 240 170 240 180 {
lab=#net2}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/latch.sym} 0 0 0 0 {name=X_latch1 NF=2}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/latch.sym} 230 0 0 0 {name=X_latch2 NF=2}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/inv.sym} 0 170 0 0 {name=X_inv1 NF=2}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/inv.sym} 180 170 0 0 {name=X_inv2 NF=2}
C {devices/iopin.sym} 180 -240 0 0 {name=p1 lab=VDD}
C {devices/iopin.sym} 180 -210 0 0 {name=p2 lab=VSS}
C {devices/ipin.sym} -10 -120 0 0 {name=p3 lab=I}
C {devices/ipin.sym} -20 130 0 0 {name=p4 lab=CLK}
C {devices/opin.sym} 410 -120 0 0 {name=p5 lab=O}
C {devices/lab_pin.sym} 160 130 1 0 {name=p18 sig_type=std_logic lab=clk_bar}
C {devices/lab_pin.sym} -10 -70 0 0 {name=p7 sig_type=std_logic lab=clk_bar}
C {devices/lab_pin.sym} 220 -40 0 0 {name=p12 sig_type=std_logic lab=clk_bar}
C {devices/lab_pin.sym} 340 130 2 0 {name=p6 sig_type=std_logic lab=clk_buf}
C {devices/lab_pin.sym} -10 -40 0 0 {name=p8 sig_type=std_logic lab=clk_buf}
C {devices/lab_pin.sym} 220 -70 0 0 {name=p11 sig_type=std_logic lab=clk_buf}
C {devices/lab_pin.sym} 80 -170 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 310 -170 0 0 {name=p10 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 60 80 1 0 {name=p16 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 240 80 1 0 {name=p14 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 80 10 3 0 {name=p15 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 310 10 3 0 {name=p13 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 240 180 3 0 {name=p19 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 60 180 3 0 {name=p17 sig_type=std_logic lab=VSS}
