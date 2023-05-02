v {xschem version=3.1.0 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 130 0 150 0 {
lab=O}
N -60 -90 -60 -10 {
lab=#net1}
N -60 -10 10 -10 {
lab=#net1}
N -60 10 -60 90 {
lab=#net2}
N -60 10 10 10 {
lab=#net2}
N -150 140 -150 150 {
lab=VSS}
N -150 20 -150 40 {
lab=VDD}
N -150 -40 -150 -20 {
lab=VSS}
N -150 -150 -150 -140 {
lab=VDD}
N -230 -110 -200 -110 {
lab=A}
N -230 -70 -200 -70 {
lab=B}
N -230 70 -200 70 {
lab=C}
N -230 110 -200 110 {
lab=D}
N 60 -60 60 -50 {
lab=VDD}
N 60 50 60 60 {
lab=VSS}
N 60 -80 60 -60 {
lab=VDD}
N 60 60 60 80 {
lab=VSS}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/nand.sym} -180 120 0 0 {name=X_nand2 NF=2}
C {devices/iopin.sym} -150 -150 3 0 {name=p1 lab=VDD}
C {devices/iopin.sym} -150 150 1 0 {name=p4 lab=VSS}
C {devices/ipin.sym} -230 -110 0 0 {name=p7 lab=A}
C {devices/ipin.sym} -230 -70 0 0 {name=p8 lab=B}
C {devices/ipin.sym} -230 70 0 0 {name=p9 lab=C}
C {devices/ipin.sym} -230 110 0 0 {name=p10 lab=D}
C {devices/opin.sym} 150 0 0 0 {name=p11 lab=O}
C {devices/lab_pin.sym} 60 -80 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 60 80 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -150 20 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -150 -20 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/nand.sym} -180 -60 0 0 {name=X_nand1 NF=2}
C {/Users/brianlsy/Desktop/brianlsy/git_workspace/fork/laygo2_workspace_sky130/xschem_lib/sylee21/nor.sym} 40 10 0 0 {name=X_nand3 NF=2}
