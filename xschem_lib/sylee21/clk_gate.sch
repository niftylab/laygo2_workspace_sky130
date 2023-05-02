v {xschem version=3.1.0 file_version=1.2
}
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
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/inv.sym} -170 40 0 0 {name=X_inv1 NF=2}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/latch.sym} 40 70 0 0 {name=X_latch1 NF=2}
C {devices/ipin.sym} -220 0 0 0 {name=p1 lab=CK_I}
C {devices/iopin.sym} 120 -110 3 0 {name=p2 lab=VDD}
C {devices/iopin.sym} 120 90 1 0 {name=p3 lab=VSS}
C {devices/lab_wire.sym} -110 -40 1 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} -110 40 2 0 {name=p11 sig_type=std_logic lab=VSS}
C {devices/ipin.sym} -220 -50 0 0 {name=p4 lab=EN}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/nand.sym} 260 0 0 0 {name=X_nand1 NF=2}
C {devices/lab_wire.sym} 290 -80 1 0 {name=p7 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} 290 20 2 0 {name=p10 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 460 -70 1 0 {name=p8 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} 460 10 2 0 {name=p9 sig_type=std_logic lab=VSS}
C {devices/opin.sym} 560 -30 0 0 {name=p5 lab=CK_O}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/inv.sym} 400 10 0 0 {name=X_inv2 NF=2}
