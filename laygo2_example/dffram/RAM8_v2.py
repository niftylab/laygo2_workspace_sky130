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
import copy
# Parameter definitions #############
# Variables
cell_type = 'ram8_v2'
nf = 1
nf_inv = 2
words_num = 8 # must be an even number
abut = [0,0]
# Templates
tpmos_name = 'pmos'
tnmos_name = 'nmos'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
r45_name = 'routing_45_basic'
# Design hierarchy
libname = 'dffram'
ref_dir_template = './laygo2_example/' #export this layout's information into the yaml in this dir 
ref_dir_export = './laygo2_example/dffram/'
ref_dir_MAG_exported = './laygo2_example/dffram/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlogic_prim = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_ver2/logic_ver2_templates.yaml')
tlogic_adv = laygo2.interface.yaml.import_template(filename=ref_dir_template+'dffram/dffram_templates.yaml')

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34, r45 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name], grids[r45_name]

cellname = cell_type+'_'+str(nf)+'x'
print('--------------------')
print('Now Creating '+cellname)

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create instances.
print("Create instances")
words=list()
buf_in = list()
buf_out = list()
buf_we = list()
buf_sel = list()
# netname={'I0':'SCAN_GATE_VALUE','I1':'DFF_DAT/O','EN0':'SCAN_GATE','EN1':'INV_GATE/O','O':'MUX_DAT/O','VSS':'VSS','VDD':'VDD:'}
#_netname['SEL'] = 'SEL0'
for i in range(int(words_num/2)):
    words.append(tlogic_adv['word_v2_'+str(nf)+'x'].generate(name='word'+str(i*2+1)))
    words.append(tlogic_adv['word_v2_'+str(nf)+'x'].generate(name='word'+str((i+1)*2),transform='MX'))

for i in range(words_num):
    buf_sel.append(tlogic_prim['ck_buf_'+str(nf_inv)+'x'].generate(name='buf_sel'+str(i+1)))
for i in range(32):
    buf_in.append(tlogic_prim['ck_buf_'+str(nf_inv)+'x'].generate(name='buf_in'+str(i+1),transform='MY'))  
    buf_out.append(tlogic_prim['ck_buf_'+str(nf_inv)+'x'].generate(name='buf_out'+str(i+1),transform='MY'))   
for i in range(4):
    buf_we.append(tlogic_prim['ck_buf_'+str(nf_inv)+'x'].generate(name='buf_we'+str(i+1))) 
#dec8 = tlogic_adv['dec3x8_'+str(nf_inv)+'x'].generate(name='dec8')
# pA0 = dsn.pin(name='A0', grid=r34, mn=r34.mn.bbox(dec8.pins['A0']))
# pA1 = dsn.pin(name='A1', grid=r34, mn=r34.mn.bbox(dec8.pins['A1']))
# pA2 = dsn.pin(name='A2', grid=r34, mn=r34.mn.bbox(dec8.pins['A2']))
# pEN = dsn.pin(name='EN', grid=r34, mn=r34.mn.bbox(dec8.pins['EN']))
buf_ck = tlogic_prim['ck_buf_'+str(nf_inv)+'x'].generate(name='buf_ck', transform='MY')
buf_re = tlogic_prim['ck_buf_'+str(nf_inv)+'x'].generate(name='buf_re')

dummy0 = tlogic_prim['space_8x'].generate(name='dummy0')
dummy1 = tlogic_prim['space_4x'].generate(name='dummy1')
dummy2 = tlogic_prim['space_14x'].generate(name='dummy2')
dummy3 = tlogic_prim['space_14x'].generate(name='dummy3')
dummy4 = tlogic_prim['space_14x'].generate(name='dummy4')
# 4. Place instances.
mn_ref = [0,0]
for i in range(int(words_num/2)):
    dsn.place(grid=pg, inst=words[i*2], mn=mn_ref)
    mn_ref = pg.mn.top_left(words[i*2]) + pg.mn.height_vec(words[i*2+1])
    dsn.place(grid=pg, inst=words[i*2+1], mn=mn_ref)
    mn_ref = pg.mn.top_left(words[i*2+1])

ref_width = pg.mn(words[0].pins['Di31'])[0,0] # (word's boundary)<--->(first Di pin)
for i in range(4):
    mn_ref[0] = pg.mn(words[0].pins['Di'+str(31-i*8)])[0,0] - ref_width
    if i == 1:
        mn_ref[0] -= pg.mn(tlogic_prim['dff_1x'].bbox())[1,0]*2 + pg.mn(tlogic_prim['tinv_'+str(nf*2)+'x'].bbox())[1,0]
    mn_ref = mn_ref + pg.mn.width_vec(buf_in[31])
    for j in range(8):
        dsn.place(grid=pg, inst=buf_in[8*(3-i)+(7-j)], mn=mn_ref)
        mn_ref = mn_ref + pg.mn.width_vec(buf_out[8*(3-i)+(7-j)]) - abut
        dsn.place(grid=pg, inst=buf_out[8*(3-i)+(7-j)], mn=mn_ref)
        mn_ref = mn_ref + pg.mn.width_vec(buf_in[8*(3-i)+(7-j)])

# decoder
mn_ref = pg.mn.bottom_right(buf_out[16])
#dsn.place(grid=pg, inst=dec8, mn=mn_ref)

# clk buffer
ref_width = pg.mn(tlogic_prim['inv_2x'].bbox())[1,0] - pg.mn(tlogic_prim['inv_2x'].pins()['O'])[1,0]
mn_ref[0] = pg.mn(words[0].pins['CLK'])[0,0] - ref_width
mn_ref = mn_ref + pg.mn.width_vec(buf_ck)
dsn.place(grid=pg, inst=buf_ck, mn=mn_ref)

# SEL buffer
mn_ref = pg.mn.bottom_right(buf_ck)+abut # for initial calib -> add abut
for i in range(8):
    dsn.place(grid=pg, inst=buf_sel[i], mn=mn_ref-abut)
    mn_ref = pg.mn.bottom_right(buf_sel[i])

# WE & RE Buffer
mn_ref = pg.mn.bottom_right(buf_out[24])
dsn.place(grid=pg, inst=buf_we[3],mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_we[3])
dsn.place(grid=pg, inst=buf_we[2],mn=mn_ref)

mn_ref = pg.mn.bottom_right(buf_sel[7])
dsn.place(grid=pg, inst=buf_we[1],mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_out[8])
dsn.place(grid=pg, inst=buf_we[0],mn=mn_ref)

mn_ref = pg.mn.bottom_right(buf_we[0])
dsn.place(grid=pg, inst=buf_re, mn=mn_ref)

# Dummy
mn_ref = pg.mn.bottom_right(buf_we[2])
dsn.place(grid=pg, inst=dummy0, mn=mn_ref)
#mn_ref = pg.mn.bottom_right(dec8)
#dsn.place(grid=pg, inst=dummy1, mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_re)
dsn.place(grid=pg, inst=dummy2, mn=mn_ref)
dsn.place(grid=pg, inst=dummy3, mn=pg.mn.bottom_right(dummy2))
dsn.place(grid=pg, inst=dummy4, mn=pg.mn.bottom_right(dummy3))
# for i in range(3):
#     dsn.place(grid=pg, inst=buf_sel[i], mn=mn_ref)
#     mn_ref = pg.mn.bottom_right(buf_sel[i])
# for i in range(3,8):
#     dsn.place(grid=pg, inst=buf_sel[i], mn=mn_ref)
#     mn_ref = pg.mn.bottom_right(buf_sel[i])

# dsn.place(grid=pg, inst=buf_we[0], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[0])
# dsn.place(grid=pg, inst=buf_we[1], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[1])
# dsn.place(grid=pg, inst=buf_ck, mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_ck)

# dsn.place(grid=pg, inst=buf_we[2], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[2])
# dsn.place(grid=pg, inst=buf_we[3], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[3])

# 5. Create and place wires.
print("Create wires")
# WE
# rWE=[None]*4
# for i in range(4):
#     _mn = [r34.mn(words[0].pins['WE'+str(i)])[0], r34.mn(words[words_num-1].pins['WE'+str(i)])[1]]
#     rWE[i] = dsn.route(grid=r34, mn=_mn, via_tag=[False, False])
# #RE
# _mn = [r34.mn(words[0].pins['RE'])[0], r34.mn(words[words_num-1].pins['RE'])[1]]
# rRE = dsn.route(grid=r34, mn=_mn, via_tag=[False,False])

# mn_list = [r34.mn(buf_re.pins['O'])[0], r34.mn.bbox(rRE)[1]]
# _track = [None, mn_list[0][1] - 4]
# rRe_int = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# # DEC
# _track = [ None, r34.bbox(dec8.pins['Y0'])[1][1]]
# for i in range(8):
#     _mn = [r34.mn(dec8.pins['Y'+str(i)])[0], r34.mn(buf_sel[i].pins['I'])[0]]
#     dsn.route_via_track(grid=r34, mn=_mn, track=_track)
#     _track[1] += 1

# # SEL
# track_dist = [-1,0,0,0,0,0,-1,0]
# for i in range(words_num):
#     _mn = r34.mn(buf_sel[i].pins['O'])[0] + [track_dist[i],0]
#     mn_list = [r34.mn(words[i].pins['SEL'])[0], [_mn[0],r34.mn(words[i].pins['SEL'])[0,1]], _mn]
#     dsn.route(grid=r34, mn=mn_list, via_tag=[False,True,False])
#     dsn.via(grid=r23, mn=r23.mn(buf_sel[i].pins['O'])[0] + [track_dist[i],0])

# # clk
# _mn = [r34.mn(buf_ck.pins['O'])[1], r34.mn(words[0].pins['CLK'])[0]]
# rclk_buf = dsn.route(grid=r34, mn=_mn, via_tag=[False,False])

# # Di
# rDi_internal = [0]*32
# for i in range(4):
#     if i ==1: # buffer and DFF not aligned area
#         continue
#     for j in range(8):
#         _mn = [r34.mn(buf_in[8*(3-i)+(7-j)].pins['O'])[1], r34.mn(words[0].pins['Di'+str(8*(3-i)+(7-j))])[0]]
#         rDi_internal[8*(3-i)+(7-j)] = dsn.route(grid=r34, mn=_mn, via_tag=[False,False])
# # Do
# rDo_internal = [0]*32
# for i in range(4):
#     if i ==1: # buffer and DFF not aligned area
#         continue
#     for j in range(8):
#         _mn = [r34.mn(buf_out[8*(3-i)+(7-j)].pins['I'])[1], r34.mn(words[0].pins['Do'+str(8*(3-i)+(7-j))])[0]]
#         rDo_internal[8*(3-i)+(7-j)] = dsn.route(grid=r34, mn=_mn, via_tag=[False,False])

# # Di & Do for i = 1
# i=1
# for j in range(8):
#     _mn = [r34.mn(words[7].pins['Di'+str(8*(3-i)+(7-j))])[1], r34.mn(words[0].pins['Di'+str(8*(3-i)+(7-j))])[0]]
#     rDi_internal[8*(3-i)+(7-j)] = dsn.route(grid=r34, mn=_mn, via_tag=[False,False])
#     _mn = [r34.mn(words[7].pins['Do'+str(8*(3-i)+(7-j))])[1], r34.mn(words[0].pins['Do'+str(8*(3-i)+(7-j))])[0]]
#     rDo_internal[8*(3-i)+(7-j)] = dsn.route(grid=r34, mn=_mn, via_tag=[False,False])    

#     # cursor_y : y value for horizontal track, set to middle height of each word
#     cursor_y = int(( r45.mn(words[7-j].pins['Do'+str(8*(3-i)+(7-j))])[1,1] + r45.mn(words[7-j].pins['Do'+str(8*(3-i)+(7-j))])[0,1] ) / 2)
#     _track = [r45.mn(buf_in[8*(3-i)+(7-j)].pins['O'])[0][0] + 4, None]
#     mn_list = [ r45.mn(buf_in[8*(3-i)+(7-j)].pins['O'])[1], [r45.mn(words[7-j].pins['Di'+str(8*(3-i)+(7-j))])[0,0],cursor_y] ]
#     dsn.route_via_track(grid=r45, mn=mn_list, track=_track)
#     dsn.via(grid=r34,mn=mn_list[0])    
#     dsn.via(grid=r34,mn=mn_list[1])
#     cursor_y -= 1
#     _track = [r45.mn(buf_out[8*(3-i)+(7-j)].pins['I'])[0][0] - 2, None]
#     mn_list = [ r45.mn(buf_out[8*(3-i)+(7-j)].pins['I'])[1], [ r45.mn(words[7-j].pins['Do'+str(8*(3-i)+(7-j))])[1,0],cursor_y ] ]
#     dsn.route_via_track(grid=r45, mn=mn_list, track=_track)
#     dsn.via(grid=r34,mn=mn_list[0])
#     dsn.via(grid=r34,mn=mn_list[1])

# WE
# mn_list = [r34.mn.bbox(rWE[0])[1], r34.mn(buf_we[0].pins['O'])[0]]
# _track = [None, r34.mn(buf_we[0].pins['O'])[1,1] +1 - r34.mn.height_vec(words[0])[1] ]
# dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# mn_ref = (r34.mn(buf_we[1].pins['O'])[1] + r34.mn(buf_we[1].pins['O'])[0])/2
# mn_list = [mn_ref, r34.mn.bbox(rWE[1])[1]]
# _track = [None, mn_ref[1] - r34.mn.height_vec(words[0])[1] ]
# dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# mn_ref = r34.mn(buf_we[2].pins['O'])[0]
# mn_list = [mn_ref, r34.mn.bbox(rWE[2])[1]]
# _track = [None, mn_ref[1] - r34.mn.height_vec(words[0])[1]*2 - 2]
# dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# mn_ref = r34.mn(buf_we[3].pins['O'])[1] + [0,2]
# mn_list = [mn_ref, r34.mn.bbox(rWE[3])[1]]
# _track = [None, mn_ref[1] - r34.mn.height_vec(words[0])[1]]
# dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# #VDD , VSS
# _mn_rail = [r12.mn.bottom_left(words[0]), r12.mn.bottom_right(words[0])]
# for i in range(words_num+2):
#     dsn.route(grid=r12, mn=_mn_rail)
#     _mn_rail[0] += r12.mn.height_vec(words[0])
#     _mn_rail[1] += r12.mn.height_vec(words[0])
# _mn_rail = [r12.mn.top_left(buf_in[31]), r12.mn.top_right(buf_in[0])]
# # bridging VDD, VSS for LVS
# mn_ref = [0,0]
# mn_list=[[0,0]]
# for i in range(int(words_num/2)):
#     mn_list.append(r23.mn.height_vec(words[0])*2*(i+1))
# _track = [-2, None]
# rvss = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# mn_list = [r23.mn.top_right(words[0])-[2,0]]
# for i in range(int(words_num/2)):
#     mn_list.append( mn_list[0] + r23.mn.height_vec(words[0])*2*(i+1))
# _track = [mn_list[0][0]+4, None]
# rvdd = dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# # # 6. Create pins.
# pA0 = dsn.pin(name='A0', grid=r34, mn=r34.mn.bbox(dec8.pins['A0']))
# pA1 = dsn.pin(name='A1', grid=r34, mn=r34.mn.bbox(dec8.pins['A1']))
# pA2 = dsn.pin(name='A2', grid=r34, mn=r34.mn.bbox(dec8.pins['A2']))
# pEN = dsn.pin(name='EN', grid=r34, mn=r34.mn.bbox(dec8.pins['EN']))
pWE = list()
for idx, buf in enumerate(buf_we):
    pWE.append(dsn.pin(name='WE'+str(idx), grid=r34, mn=r34.mn.bbox(buf.pins['I'])))
pRe = dsn.pin(name='RE', grid=r34, mn=r34.mn.bbox(buf_re.pins['I']))
pclk = dsn.pin(name='CLK', grid=r34, mn=r34.mn.bbox(buf_ck.pins['I']))
pDo = list()
pDi = list()
for i in range(4):
    for j in range(8):
        pDo.append(dsn.pin(name='Do'+str(8*(3-i)+(7-j))+'_buf', grid=r34, mn=r34.mn.bbox(buf_out[8*(3-i)+(7-j)].pins['O'])))
        pDi.append(dsn.pin(name='Di'+str(8*(3-i)+(7-j)), grid=r34, mn=r34.mn.bbox(buf_in[8*(3-i)+(7-j)].pins['I'])))
# # For LVS 
# pvss0 = dsn.pin(name='VSS', grid=r23, mn=r23.mn.bbox(rvss[-1]))
# pvdd0 = dsn.pin(name='VDD', grid=r23, mn=r23.mn.bbox(rvdd[-1]))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')
