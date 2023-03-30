v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N -50 -40 80 -40 {
lab=Y}
N 80 -40 80 -0 {
lab=Y}
N 80 60 80 100 {
lab=#net1}
N -50 -100 80 -100 {
lab=VDD}
N -50 -70 -20 -70 {
lab=VDD}
N -20 -100 -20 -70 {
lab=VDD}
N 80 -70 100 -70 {
lab=VDD}
N 100 -100 100 -70 {
lab=VDD}
N 80 160 80 190 {
lab=VSS}
N 20 -120 20 -100 {
lab=VDD}
N 100 -110 100 -100 {
lab=VDD}
N 20 -110 100 -110 {
lab=VDD}
N -90 -70 -90 30 {
lab=A}
N 20 -70 40 -70 {
lab=B}
N 20 130 40 130 {
lab=B}
N 80 -20 150 -20 {
lab=Y}
N 80 130 110 130 {
lab=VSS}
N 110 130 110 180 {
lab=VSS}
N 80 180 110 180 {
lab=VSS}
N 80 30 110 30 {
lab=VSS}
N 110 30 110 130 {
lab=VSS}
N -90 130 20 130 {}
N -90 30 -90 130 {}
N 20 -70 20 30 {}
N 20 30 40 30 {}
N -130 0 20 0 {}
N -130 100 -90 100 {}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 60 30 0 0 {name=M1
L=0.15
W=1.2
nf=1
mult=NF
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 60 130 0 0 {name=M2
L=0.15
W=1.2
nf=1
mult=NF
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {opin.sym} 150 -20 0 0 {name=p1 lab=Y}
C {ipin.sym} -120 0 0 0 {name=p2 lab=A}
C {iopin.sym} 20 -110 3 0 {name=p3 lab=VDD}
C {iopin.sym} 80 180 1 0 {name=p4 lab=VSS}
C {ipin.sym} -120 100 0 0 {name=p5 lab=B}
C {sky130_fd_pr/pfet_01v8.sym} -70 -70 0 0 {name=M3
L=0.15
W=2.4
nf=1
mult=NF
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 60 -70 0 0 {name=M4
L=0.15
W=2.4
nf=1
mult=NF
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
