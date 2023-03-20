###########################################
#                                         #
#        8x32 RAM Layout Generator        #
#        Created by HyungJoo Park         #   
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
# Parameter definitions #############
# Variables
cell_type = 'ram32_v2'
nf=2
words_num = 32 # must be an even number
buffer_num = 8+4+1 # number of buffers
# Templates
tpmos_name = 'pmos_sky'
tnmos_name = 'nmos_sky'
tptap_name = 'ptap_sky'
tntap_name = 'ntap_sky'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_basic_name = 'routing_23_basic'
r23_cmos_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
# Design hierarchy
libname = 'logic_advanced'
ref_dir_template = './laygo2_example/' #export this layout's information into the yaml in this dir 
ref_dir_export = './laygo2_example/logic_advance/'
ref_dir_MAG_exported = './laygo2_example/logic_advance/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlogic_prim = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic/logic_generated_templates.yaml')
tlogic_adv = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_advance/logic_advanced_templates.yaml')

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23_cmos, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_cmos_name], grids[r23_basic_name], grids[r34_name]

cellname = cell_type+'_'+str(nf)+'x'
print('--------------------')
print('Now Creating '+cellname)

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
words=list()
for i in range(words_num):
    words.append(tlogic_adv['word_2row_'+str(nf)+'x'].generate(name='word'+str(i)))

buf_clk0 = tlogic_prim['buffer_'+str(24)+'x'].generate(name='buf_clk0')
buf_clk1 = tlogic_prim['buffer_'+str(24)+'x'].generate(name='buf_clk1')
dec4 = tlogic_adv['dec2x4_'+str(nf)+'x'].generate(name='dec4', transform='MX')
dec8 = []
for i in range(4):
    dec8.append(tlogic_adv['dec3x8_'+str(nf)+'x'].generate(name='dec8_'+str(i), transform='MX'))
buf_we=[]
buf_sel = []
buf_in = []
buf_out = []
for i in range(2):
    buf_we.append(tlogic_prim['buffer_'+str(12)+'x'].generate(name='buf_we'+str(i*2), transform='MX'))
    buf_we.append(tlogic_prim['buffer_'+str(12)+'x'].generate(name='buf_we'+str(i*2+1)))
for i in range(words_num):
    buf_sel.append(tlogic_prim['buffer_'+str(12)+'x'].generate(name='buf_sel'+str(i)))
for i in range(words_num):
    buf_in.append(tlogic_prim['buffer_'+str(14)+'x'].generate(name='buf_in'+str(i)))
    buf_out.append(tlogic_prim['buffer_'+str(14)+'x'].generate(name='buf_out'+str(i)))
# NTAP0 = templates[tntap_name].generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
# PTAP0 = templates[tptap_name].generate(name='MPT0', transform='MX',params={'nf':2, 'tie':'TAP0'})
# NTAP1 = templates[tntap_name].generate(name='MNT1', params={'nf':2, 'tie':'TAP0'})
# PTAP1 = templates[tptap_name].generate(name='MPT1', transform='MX',params={'nf':2, 'tie':'TAP0'})

# 4. Place instances.

# WORD lines
mn_ref = [0,0]
for i in range(words_num):
    dsn.place(grid=pg, inst=words[i], mn=mn_ref)
    mn_ref = pg.mn.top_left(words[i])
# (SELECT & CLK & WE) BUFFERS
dsn.place(grid=pg, inst=buf_we[3], mn=mn_ref)
mn_ref=pg.mn.bottom_right(buf_we[3])
dsn.place(grid=pg, inst=buf_clk0, mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_clk0)
for i in range(words_num):
    if i == int(words_num/2):
        mn_ref[0] = pg.mn(words[0].pins['WE<0>'])[1,0]-5  # align right WE buffer and right DFF_byte cell
        dsn.place(grid=pg, inst=buf_we[1], mn=mn_ref)
        mn_ref = pg.mn.bottom_right(buf_we[1])
    dsn.place(grid=pg, inst=buf_sel[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_sel[i])
# WE BUFFERs & DECODERs
mn_ref = pg.mn.top_left(buf_we[3]) + pg.mn.height_vec(buf_we[2])
dsn.place(grid=pg, inst=buf_we[2], mn=mn_ref)
mn_ref = pg.mn.top_right(buf_we[2])

dsn.place(grid=pg, inst=dec4, mn=mn_ref)
mn_ref = pg.mn.top_right(dec4)
dsn.place(grid=pg, inst=dec8[2], mn=mn_ref)
mn_ref = pg.mn.top_right(dec8[2])
dsn.place(grid=pg, inst=dec8[0], mn=mn_ref)

mn_ref = [pg.mn.top_left(buf_we[1])[0],mn_ref[1]]
dsn.place(grid=pg, inst=buf_we[0], mn=mn_ref)
mn_ref = pg.mn.top_right(buf_we[0])  
dsn.place(grid=pg, inst=dec8[1], mn=mn_ref)
mn_ref = pg.mn.top_right(dec8[1])
dsn.place(grid=pg, inst=dec8[3], mn=mn_ref)
# for i in range(4):
#     if i ==2:
#         mn_ref = [pg.mn.top_left(buf_we[1])[0],mn_ref[1]]
#         dsn.place(grid=pg, inst=buf_we[0], mn=mn_ref)
#         mn_ref = pg.mn.top_right(buf_we[0])  
#     dsn.place(grid=pg, inst=dec8[i], mn=mn_ref)
#     mn_ref = pg.mn.top_right(dec8[i])
mn_ref = pg.mn.top_left(buf_we[2])
for i in range(int(words_num/2)):
    dsn.place(grid=pg, inst=buf_in[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_in[i])

mn_ref = pg.mn.top_left(buf_we[0])
for i in range(int(words_num/2), words_num):
    dsn.place(grid=pg, inst=buf_in[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_in[i])

# dsn.place(grid=pg, inst=buf_we[2], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[2])
# dsn.place(grid=pg, inst=buf_we[3], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[3])
# dsn.place(grid=pg, inst=buf_clk1, mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_clk1)

# 5. Create and place wires.
print("Create wires")
# WE
rwe = [0,0,0,0]
mn_list=[]
for i in range(words_num):
    mn_list.append(r23.mn(words[i].pins['WE<3>'])[1])
_track = [r23.mn(words[i].pins['WE<3>'])[1,0]-1, None]
rwe[3] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

mn_list=[r34.mn.bbox(rwe[3][-1])[1], r34.mn(buf_we[3].pins['O'])[0]]
_track = [r34.mn.bbox(rwe[3][-1])[1,0] ,None]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
dsn.via(grid=r34, mn = mn_list[1])
mn_list=[]

for i in range(words_num):
    mn_list.append(r23.mn(words[i].pins['WE<2>'])[1])
_track = [r23.mn(words[i].pins['WE<2>'])[1,0]+2, None]
rwe[2] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

mn_list=[r34.mn.bbox(rwe[2][-1])[1], r34.mn(buf_we[2].pins['O'])[0]]
_track = [r34.mn.bbox(rwe[2][-1])[1,0],None]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
dsn.via(grid=r34, mn = mn_list[1])
mn_list=[]

for i in range(words_num):
    mn_list.append(r23.mn(words[i].pins['WE<1>'])[1])
_track = [r23.mn(words[i].pins['WE<1>'])[1,0]-1, None]
rwe[1] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

mn_list=[r23.mn.bbox(rwe[1][-1])[1], r23.mn(buf_we[1].pins['O'])[0]+[0,1]]
_track = [r23.mn.bbox(rwe[1][-1])[1,0],None]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
dsn.via(grid=r23, mn = mn_list[1])
mn_list=[]

for i in range(words_num):
    mn_list.append(r23.mn(words[i].pins['WE<0>'])[1])
_track = [r23.mn(words[i].pins['WE<0>'])[1,0]+2, None]
rwe[0] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

mn_list=[r23.mn.bbox(rwe[0][-1])[1], r23.mn(buf_we[0].pins['O'])[0]+[0,1]]
_track = [r23.mn.bbox(rwe[0][-1])[1,0],None]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
dsn.via(grid=r23, mn = mn_list[1])
mn_list=[]
# Decoder
# EN
mn_list = [[r34.mn(buf_we[2].pins['I'])[1,0]-2, r34.mn(dec4.pins['A0'])[1,1]+2], r34.mn(dec4.pins['EN'])[0]]
_track = [r34.mn(dec4.pins['EN'])[0,0], None]
rEN = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
# A4
mn_list = [[r34.mn(buf_we[2].pins['I'])[1,0]-2, r34.mn(dec4.pins['A0'])[1,1]+1], r34.mn(dec4.pins['A1'])[1]+[0,1], r34.mn(dec4.pins['A1'])[0]]
rA0, vA0, _rA0 = dsn.route(grid=r34, mn=mn_list, via_tag=[False, True, False])
#A3
mn_list = [r34.mn(buf_we[2].pins['I'])[1]-[2,0], r34.mn(dec4.pins['A0'])[1]]
rA1, vA1 = dsn.route(grid=r34, mn=mn_list, via_tag=[False,True])

_track = [None, r34.mn(dec4.pins['A1'])[1,1]-1]
# A2
mn_list = []
for i in range(4):
    mn_list.append(r34.mn(dec8[i].pins['A2'])[1])
_trk = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
mn_list = [[r34.mn(buf_we[2].pins['I'])[1,0]-2, _track[1]], r34.mn(_trk[-1])[0]]
rA2 = dsn.route(grid=r34, mn=mn_list, via_tag=[False, False])
_track[1] -= 1
# A1
mn_list = []
for i in range(4):
    mn_list.append(r34.mn(dec8[i].pins['A1'])[1])
_trk = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
mn_list = [[r34.mn(buf_we[2].pins['I'])[1,0]-2, _track[1]], r34.mn(_trk[-1])[0]]
rA1 = dsn.route(grid=r34, mn=mn_list, via_tag=[False, False])
_track[1] -= 1
# A0
mn_list = []
for i in range(4):
    mn_list.append(r34.mn(dec8[i].pins['A0'])[1])
_trk = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
mn_list = [[r34.mn(buf_we[2].pins['I'])[1,0]-2, _track[1]], r34.mn(_trk[-1])[0]]
rA0 = dsn.route(grid=r34, mn=mn_list, via_tag=[False, False])

# Decoder4 - Decoder8
mn_list = [r34.mn(dec4.pins['Y0'])[1], r34.mn(dec8[0].pins['EN'])[0]]
_track = [None, mn_list[0][1]]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
mn_list = [r34.mn(dec4.pins['Y1'])[1], r34.mn(dec8[1].pins['EN'])[0]]
_track = [None, mn_list[0][1]-1]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

mn_list = [r34.mn(dec4.pins['Y2'])[0], r34.mn(dec8[2].pins['EN'])[0]]
_track = [None, mn_list[0][1]+2]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
mn_list = [r34.mn(dec4.pins['Y3'])[0], r34.mn(dec8[3].pins['EN'])[0]]
_track = [None, mn_list[0][1]+1]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
# Decoder - buffer
_height = [4, 3, 1, -1, -3, -5, -7, -8]
_k = 1
for i in range(8):
    mn_list = [r23.mn(dec8[0].pins['Y'+str(i)])[0], r23.mn(buf_sel[15-i].pins['I'])[1]]
    _fold = False
    for j in range(8):
        if mn_list[0][0] == r23.mn(buf_sel[15-j].pins['O'])[1,0]:
            _fold = True
            break
    if _fold == True:
        _track = [None, mn_list[0][1] + _k]
        dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
        _k -= 1
    else: 
        _track = [None,r23.mn(buf_sel[15-i].pins['I'])[1,1] + _height[i]]
        dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
_k = 1
for i in range(8):
    mn_list = [r23.mn(dec8[1].pins['Y'+str(i)])[0], r23.mn(buf_sel[16+i].pins['I'])[1]]
    _fold = False
    for j in range(8):
        if mn_list[0][0] == r23.mn(buf_sel[16+j].pins['O'])[1,0]:
            _fold = True
            break
    if _fold == True:
        _track = [None, mn_list[0][1] + _k]
        dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
        _k -= 1
    else:         
        _track = [None,r23.mn(buf_sel[16+i].pins['I'])[1,1] + _height[7-i]]
        dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
_k = 1    
for i in range(8):
    mn_list = [r23.mn(dec8[2].pins['Y'+str(i)])[0], r23.mn(buf_sel[7-i].pins['I'])[1]]
    _fold = False
    for j in range(8):
        if mn_list[0][0] == r23.mn(buf_sel[7-j].pins['O'])[1,0]:
            _fold = True
            break
    if _fold == True:
        _track = [None, mn_list[0][1] + _k]
        dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
        _k -= 1
    else: 
        _track = [None,r23.mn(buf_sel[7-i].pins['I'])[1,1] + _height[7-i]]
        dsn.route_via_track(grid=r23, mn=mn_list, track=_track)  
_k = 1
for i in range(8):
    mn_list = [r23.mn(dec8[3].pins['Y'+str(i)])[0], r23.mn(buf_sel[24+i].pins['I'])[1]]
    _fold = False
    for j in range(8):
        if mn_list[0][0] == r23.mn(buf_sel[24+j].pins['O'])[1,0]:
            _fold = True
            break
    if _fold == True:
        _track = [None, mn_list[0][1] + _k]
        dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
        _k -= 1
    else: 
        _track = [None,r23.mn(buf_sel[24+i].pins['I'])[1,1] + _height[i]]
        dsn.route_via_track(grid=r23, mn=mn_list, track=_track)  

# SEL
_track = [r34.mn(words[0].pins['SEL'])[1,0]+2, None]
_vec = [0,-4]
for i in range(8):
    mn_list = [r34.mn(words[i].pins['SEL'])[1],r34.mn(buf_sel[15-i].pins['O'])[0]+_vec]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    mn_list[0] = r34.mn(buf_sel[15-i].pins['O'])[0]
    dsn.route(grid=r34, mn=mn_list, via_tag=[False, True])
    _track[0] = _track[0] + 1
    _vec[1] = _vec[1] + 1
for i in range(16,24):
    mn_list = [r34.mn(words[i].pins['SEL'])[1],r34.mn(buf_sel[23-i].pins['O'])[0]+_vec]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    mn_list[0] = r34.mn(buf_sel[23-i].pins['O'])[0]
    dsn.route(grid=r34, mn=mn_list, via_tag=[False, True])
    _track[0] = _track[0] + 1
    _vec[1] = _vec[1] + 1
_vec[1] = _vec[1] - 1
for i in range(8,16):
    mn_list = [r34.mn(words[i].pins['SEL'])[1],r34.mn(buf_sel[i+8].pins['O'])[0]+_vec]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    mn_list[0] = r34.mn(buf_sel[i+8].pins['O'])[0]
    dsn.route(grid=r34, mn=mn_list, via_tag=[False, True])
    _track[0] = _track[0] + 1
    _vec[1] = _vec[1] - 1
for i in range(24,32):
    mn_list = [r34.mn(words[i].pins['SEL'])[1],r34.mn(buf_sel[i].pins['O'])[0]+_vec]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    mn_list[0] = r34.mn(buf_sel[i].pins['O'])[0]
    dsn.route(grid=r34, mn=mn_list, via_tag=[False, True])
    _track[0] = _track[0] + 1
    _vec[1] = _vec[1] - 1    
# CLK
mn_list=[r34.mn(words[0].pins['CLK'])[0], r34.mn(words[words_num-1].pins['CLK'])[0]]
rclk0 = dsn.route(grid=r34, mn=mn_list, via_tag=[False,False])
mn_list=[r34.mn(words[0].pins['CLK'])[1], r34.mn(words[words_num-1].pins['CLK'])[1]]
rclk1 = dsn.route(grid=r34, mn=mn_list, via_tag=[False,False])

# Di< >
rDi = [0]*32
buf_dist=[-2, -2, -3, -5, -5, -2, -10, -13]
pin_dist = r34.mn(words[1].pins['Di<'+str(i)+'>'])[1] - r34.mn(words[0].pins['Di<'+str(i)+'>'])[1]
# lower pin
for i in range(24,32):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Di<'+str(i)+'>'])[1])
    _track = [r23.mn(words[0].pins['Di<'+str(i)+'>'])[1,0]-1, None]
    rDi[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

    mn_buf = r34.mn(buf_in[31-i].pins['O'])[0]+[buf_dist[31-i],0]
    mn_list = [r34.mn(buf_in[31-i].pins['O'])[0], r34.mn.bbox(rDi[i][-1])[1] - pin_dist*(i-24)]
    _track = [mn_buf[0], None]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    dsn.via(grid=r34, mn = mn_list[0])
buf_dist=[-10, -2, -2, -15, -7, -3, -10, -7]
for i in range(8,16):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Di<'+str(i)+'>'])[1])
    _track = [r23.mn(words[0].pins['Di<'+str(i)+'>'])[1,0]-1, None]
    rDi[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

    mn_buf = r34.mn(buf_in[31-i].pins['O'])[0]+[buf_dist[15-i],0]
    mn_list = [r34.mn(buf_in[31-i].pins['O'])[0], r34.mn.bbox(rDi[i][-1])[1] - pin_dist*(i-8)]
    _track = [mn_buf[0], None]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    dsn.via(grid=r34, mn = mn_list[0])
#upper pin
buf_dist = [-2, -6, -9, -5, -3, -6, -9, -11]
for i in range(16,24):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Di<'+str(i)+'>'])[1])
    _track = [r23.mn(words[0].pins['Di<'+str(i)+'>'])[1,0]+1, None]
    rDi[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

    mn_buf = r34.mn(buf_in[31-i].pins['O'])[0]+[buf_dist[23-i],0]
    mn_list = [r34.mn(buf_in[31-i].pins['O'])[0], r34.mn.bbox(rDi[i][-1])[1] - pin_dist*(23-i)]
    _track = [mn_buf[0], None]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    dsn.via(grid=r34, mn = mn_list[0])
buf_dist = [-2, -6, -5, -4, -3, -2, -9, -8]
for i in range(8):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Di<'+str(i)+'>'])[1])
    _track = [r23.mn(words[0].pins['Di<'+str(i)+'>'])[1,0]+1, None]
    rDi[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

    mn_buf = r34.mn(buf_in[31-i].pins['O'])[0]+[buf_dist[7-i],0]
    mn_list = [r34.mn(buf_in[31-i].pins['O'])[0], r34.mn.bbox(rDi[i][-1])[1] - pin_dist*(7-i)]
    _track = [mn_buf[0], None]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    dsn.via(grid=r34, mn = mn_list[0])
# Do< >
rDo = [0]*32
# lower pin
for i in range(24,32):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Do<'+str(i)+'>'])[1])
    _track = [r23.mn(words[0].pins['Do<'+str(i)+'>'])[1,0]-2, None]
    rDo[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
for i in range(8,16):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Do<'+str(i)+'>'])[1])
    _track = [r23.mn(words[0].pins['Do<'+str(i)+'>'])[1,0]-2, None]
    rDo[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
#upper pin
for i in range(16,24):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Do<'+str(i)+'>'])[0])
    _track = [r23.mn(words[0].pins['Do<'+str(i)+'>'])[0,0]+2, None]
    rDo[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
for i in range(8):
    mn_list = []
    for j in range(words_num):
        mn_list.append(r23.mn(words[j].pins['Do<'+str(i)+'>'])[0])
    _track = [r23.mn(words[0].pins['Do<'+str(i)+'>'])[0,0]+2, None]
    rDo[i] = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)


# # VSS
# rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(cells[0]), r12.mn.bottom_right(cells[3])])
# # VDD
# rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(cells[0]), r12.mn.top_right(cells[3])])

# # 6. Create pins.
# psel_bar = dsn.pin(name='SelBar', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[0].pins['SelBar']))
pwe = list()
for i in range(4):
    pwe.append(dsn.pin(name='WE<'+str(i)+'>', grid=r23, mn=r23.mn.bbox(rwe[i][-1])))
# pclk = dsn.pin(name='CLK', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[0].pins['CLK']))
# pDo = list()
# pDi = list()
# for i in range(4):
#     for j in range(8):
#         pDo.append(dsn.pin(name='Do<'+str(8*(3-i)+(7-j))+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[i].pins['Do<'+str(j)+'>'])))
#         pDi.append(dsn.pin(name='Di<'+str(8*(3-i)+(7-j))+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[i].pins['Di<'+str(j)+'>'])))
# pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
# pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')