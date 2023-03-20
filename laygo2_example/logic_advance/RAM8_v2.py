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
cell_type = 'ram8_v2'
nf=2
words_num = 8 # must be an even number
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
dec8 = tlogic_adv['dec3x8_'+str(nf)+'x'].generate(name='dec8')
buf_we=[]
buf_sel = []
for i in range(4):
    buf_we.append(tlogic_prim['buffer_'+str(24)+'x'].generate(name='buf_we'+str(i)))
for i in range(8):
    buf_sel.append(tlogic_prim['buffer_'+str(12)+'x'].generate(name='buf_sel'+str(i)))
# NTAP0 = templates[tntap_name].generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
# PTAP0 = templates[tptap_name].generate(name='MPT0', transform='MX',params={'nf':2, 'tie':'TAP0'})
# NTAP1 = templates[tntap_name].generate(name='MNT1', params={'nf':2, 'tie':'TAP0'})
# PTAP1 = templates[tptap_name].generate(name='MPT1', transform='MX',params={'nf':2, 'tie':'TAP0'})

# 4. Place instances.
mn_ref = [0,0]
for i in range(words_num):
    dsn.place(grid=pg, inst=words[i], mn=mn_ref)
    mn_ref = pg.mn.top_left(words[i])

# byte_width = int(pg.mn.width_vec(words[7])[0]/4)
dsn.place(grid=pg, inst=dec8, mn=mn_ref)
mn_ref = pg.mn.bottom_right(dec8)
for i in range(3):
    dsn.place(grid=pg, inst=buf_sel[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_sel[i])
for i in range(3,8):
    dsn.place(grid=pg, inst=buf_sel[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_sel[i])

dsn.place(grid=pg, inst=buf_we[0], mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_we[0])
dsn.place(grid=pg, inst=buf_we[1], mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_we[1])
dsn.place(grid=pg, inst=buf_clk0, mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_clk0)

# dsn.place(grid=pg, inst=buf_we[2], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[2])
# dsn.place(grid=pg, inst=buf_we[3], mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_we[3])
# dsn.place(grid=pg, inst=buf_clk1, mn=mn_ref)
# mn_ref = pg.mn.bottom_right(buf_clk1)

# 5. Create and place wires.
print("Create wires")
# WE
# _mn = [r34.mn(words[0].pins['WE<0>'])[0], r34.mn(words[words_num-1].pins['WE<0>'])[1]]
# rWE0 = dsn.route(grid=r34, mn=_mn, via_tag=[False, False])
# sel_bar
# for i in range(3):
#     mn_list = [r34.mn(cells[i].pins['SelBar'])[0],r34.mn(buf_sel[i].pins['I'])[0]]
#     _track = [None, r34.mn(cells[i].pins['SelBar'])[0,1]]
#     dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
#     mn_list = [r34.mn(buf_sel[i].pins['O'])[0], r34.mn(cells[i+1].pins['SelBar'])[0]]
#     _track = [None, r34.mn(cells[i+1].pins['SelBar'])[0,1]]
#     dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
# # clk
# for i in range(3):
#     mn_list = [r34.mn(cells[i].pins['CLK'])[0],r34.mn(buf_ck[i].pins['I'])[0]]
#     _track = [None, r34.mn(cells[i].pins['CLK'])[0,1]-3]
#     dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
#     mn_list = [r34.mn(buf_ck[i].pins['O'])[0], r34.mn(cells[i+1].pins['CLK'])[0]]
#     _track = [None, r34.mn(cells[i+1].pins['CLK'])[0,1]-3]
#     dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# # VSS
# rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(cells[0]), r12.mn.bottom_right(cells[3])])
# # VDD
# rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(cells[0]), r12.mn.top_right(cells[3])])

# # 6. Create pins.
# psel_bar = dsn.pin(name='SelBar', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[0].pins['SelBar']))
# pwe = list()
# for i in range(4):
#     pwe.append(dsn.pin(name='WE<'+str(3-i)+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[i].pins['WE'])))
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