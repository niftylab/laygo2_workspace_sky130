v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 40 -170 40 -110 {
lab=VDD}
N -110 -140 -110 -110 {
lab=VDD}
N -110 -140 40 -140 {
lab=VDD}
N 190 -140 190 -110 {
lab=VDD}
N 40 -140 190 -140 {
lab=VDD}
N -110 -80 -70 -80 {
lab=VDD}
N -70 -140 -70 -80 {
lab=VDD}
N 40 -80 80 -80 {
lab=VDD}
N 80 -140 80 -80 {
lab=VDD}
N 190 -80 230 -80 {
lab=VDD}
N 230 -140 230 -80 {
lab=VDD}
N 190 -140 230 -140 {
lab=VDD}
N 40 -50 40 -0 {
lab=Y}
N -110 -50 -110 -30 {
lab=Y}
N -110 -30 40 -30 {
lab=Y}
N 190 -50 190 -30 {
lab=Y}
N 40 -30 190 -30 {
lab=Y}
N 40 60 40 100 {
lab=#net1}
N 40 160 40 200 {
lab=#net2}
N 190 -30 250 -30 {
lab=Y}
N 40 260 40 310 {
lab=VSS}
N 40 230 80 230 {
lab=VSS}
N 80 230 80 290 {
lab=VSS}
N 40 290 80 290 {
lab=VSS}
N 40 130 80 130 {
lab=VSS}
N 80 130 80 230 {
lab=VSS}
N 40 30 80 30 {
lab=VSS}
N 80 30 80 130 {
lab=VSS}
N -170 -80 -150 -80 {
lab=a}
N -20 -80 0 -80 {
lab=b}
N 130 -80 150 -80 {
lab=c}
N -20 30 0 30 {
lab=a}
N -20 130 0 130 {
lab=b}
N -20 230 0 230 {
lab=c}
N -180 30 -150 30 {
lab=a}
N -180 70 -150 70 {
lab=b}
N -180 110 -150 110 {
lab=a}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 20 30 0 0 {name=M1
L=0.15
W=1.2
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 20 130 0 0 {name=M2
L=0.15
W=1.2
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 20 230 0 0 {name=M3
L=0.15
W=1.2
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 20 -80 0 0 {name=M4
L=0.15
W=2.4
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} -130 -80 0 0 {name=M5
L=0.15
W=2.4
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 170 -80 0 0 {name=M6
L=0.15
W=2.4
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {iopin.sym} 40 -160 3 0 {name=p1 lab=VDD}
C {opin.sym} 250 -30 0 0 {name=p2 lab=Y}
C {iopin.sym} 40 300 1 0 {name=p3 lab=VSS}
C {lab_pin.sym} -170 -80 0 0 {name=l2 sig_type=std_logic lab=a}
C {lab_pin.sym} -20 -80 0 0 {name=l1 sig_type=std_logic lab=b}
C {lab_pin.sym} 130 -80 0 0 {name=l3 sig_type=std_logic lab=c
}
C {lab_pin.sym} -20 30 0 0 {name=l4 sig_type=std_logic lab=a}
C {lab_pin.sym} -20 130 0 0 {name=l5 sig_type=std_logic lab=b}
C {lab_pin.sym} -20 230 0 0 {name=l6 sig_type=std_logic lab=c}
C {ipin.sym} -170 30 0 0 {name=p4 lab=A}
C {lab_pin.sym} -150 30 0 1 {name=l7 sig_type=std_logic lab=a}
C {ipin.sym} -170 70 0 0 {name=p5 lab=B}
C {lab_pin.sym} -150 70 0 1 {name=l8 sig_type=std_logic lab=b}
C {ipin.sym} -170 110 0 0 {name=p6 lab=C}
C {lab_pin.sym} -150 110 0 1 {name=l9 sig_type=std_logic lab=c}
