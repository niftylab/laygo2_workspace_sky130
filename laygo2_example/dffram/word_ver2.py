###########################################
#                                         #
#       32bit WORD Layout Generator       #
#        Created by HyungJoo Park         #   
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
from laygo2.object.physical import Rect
from laygo2.object.netmap import NetMap
# Parameter definitions #############
# Variables
cell_type = 'word_v3'
nf = 1
nf_inv = 2
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

# 3. Create istances.
print("Create instances")
cells=list()
cells.append(tlogic_adv['byte_dff_left_'+str(nf)+'x'].generate(name='byte4'))
cells.append(tlogic_adv['byte_dff_left_'+str(nf)+'x'].generate(name='byte3'))
cells.append(tlogic_adv['byte_dff_right_'+str(nf)+'x'].generate(name='byte2'))  
cells.append(tlogic_adv['byte_dff_right_'+str(nf)+'x'].generate(name='byte1'))  
tap0 = tlogic_prim['space_2x'].generate(name='space0')
buf_sel = list()
buf_sel.append(tlogic_prim['inv_2x'].generate(name='buf_sel0'))
buf_sel.append(tlogic_prim['inv_6x'].generate(name='buf_sel1'))
buf_ck = list()
buf_ck.append(tlogic_prim['inv_'+str(nf_inv)+'x'].generate(name='buf_ck0'))
buf_ck.append(tlogic_prim['inv_'+str(nf_inv*4)+'x'].generate(name='buf_ck1'))
gate_RE = list()
gate_RE.append(tlogic_prim['nand_'+str(nf_inv)+'x'].generate(name='gt_re0'))
gate_RE.append(tlogic_prim['inv_'+str(nf_inv)+'x'].generate(name='gt_re1'))
gate_RE.append(tlogic_prim['inv_'+str(nf_inv*3)+'x'].generate(name='gt_re2'))
gate_RE.append(tlogic_prim['inv_'+str(nf_inv*9)+'x'].generate(name='gt_re3'))
inck = tnmos.generate(name='MNCK', params={'nf': nf_inv, 'tie': 'S'})
ipck = tpmos.generate(name='MP0', transform='MX', params={'nf': nf_inv, 'tie': 'S'})
in0 = tnmos.generate(name='MN0', params={'nf': nf_inv})
in1 = tnmos.generate(name='MN1', params={'nf': nf_inv})
in2 = tnmos.generate(name='MN2', params={'nf': nf_inv})
indec = list()
for i in range(3):
    indec.append(tnmos.generate(name='MNdec'+str(i), params={'nf': nf_inv}))
ipdmy = list()
for i in range(3):
    ipdmy.append(tpmos.generate(name='MPdmy'+str(i), transform='MX', params={'nf': nf_inv}))
# NTAP0 = templates[tntap_name].generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
# PTAP0 = templates[tptap_name].generate(name='MPT0', transform='MX',params={'nf':2, 'tie':'TAP0'})
# NTAP1 = templates[tntap_name].generate(name='MNT1', params={'nf':2, 'tie':'TAP0'})
# PTAP1 = templates[tptap_name].generate(name='MPT1', transform='MX',params={'nf':2, 'tie':'TAP0'})

# 4. Place instances.
#pg_list = [cells[0], cells[1], tap0, cells[2], cells[3]]
pg_list = [cells[0], cells[1], tap0, buf_ck[0], buf_ck[1], inck]
# cursor = 3
# for cell in buf_ck:
#     pg_list.insert(cursor,cell)
#     cursor += 1
# for cell in gate_RE:
#     pg_list.insert(cursor,cell)
#     cursor += 1
# for cell in buf_sel:
#     pg_list.insert(cursor,cell)
#     cursor += 1
cursor = [0,0]
for inst in pg_list:
    dsn.place(grid=pg, inst=inst, mn=cursor)
    cursor = pg.mn.bottom_right(inst)
#dsn.place(grid=pg, inst=inck, mn=pg.mn.bottom_right(buf_ck[1]))
dsn.place(grid=pg, inst=ipck, mn=pg.mn.top_left(inck) + pg.mn.height_vec(ipck))
cursor = pg.mn.bottom_right(inck)
for i in range(3):
    dsn.place(grid=pg, inst=indec[i], mn=cursor)
    cursor = pg.mn.top_left(indec[i]) + pg.mn.height_vec(ipdmy[i])
    dsn.place(grid=pg, inst=ipdmy[i], mn=cursor)
    cursor = pg.mn.bottom_right(indec[i])
pg_list = list()
pg_list.extend(gate_RE)
pg_list.extend(buf_sel)
pg_list.append(cells[2])
pg_list.append(cells[3])
for inst in pg_list:
    dsn.place(grid=pg, inst=inst, mn=cursor)
    cursor = pg.mn.bottom_right(inst)
# 5. Create and place wires.
print("Create wires")

track_selbuf = [None, r34.mn(buf_sel[1].pins['O'])[1,1]+1]
track_clkbuf = [None, r34.mn(buf_sel[1].pins['O'])[1,1]]
track_rebuf = [None, r34.mn(buf_sel[1].pins['O'])[1,1]-1]
# sel_buf
mn_selbuf = [r34.mn(buf_sel[1].pins['O'])[0]]
for i in range(4):
    mn_selbuf.append(r34.mn(cells[i].pins['SEL'])[0])
dsn.route_via_track(grid=r34, mn=mn_selbuf, track=track_selbuf)
# clk_buf
mn_clkbuf = [r34.mn(buf_ck[1].pins['O'])[0]]
for i in range(4):
    mn_clkbuf.append(r34.mn(cells[i].pins['CLK'])[0])
dsn.route_via_track(grid=r34, mn=mn_clkbuf, track=track_clkbuf)
# RE_buf
mn_rebuf = [r34.mn(gate_RE[-1].pins['O'])[0]]
for i in range(4):
    mn_rebuf.append(r34.mn(cells[i].pins['RE'])[0])
dsn.route_via_track(grid=r34, mn=mn_rebuf, track=track_rebuf)

# sel
track_sel = [None, r34.mn(buf_sel[1].pins['O'])[0,1]-2]
mn_sel = [r34.mn(gate_RE[0].pins['A'])[1],r34.mn(buf_sel[0].pins['I'])[1]]
rsel = dsn.route_via_track(grid=r34, mn=mn_sel, track=track_sel)

# internal
_track = [None, (r23.mn(buf_sel[1].pins['O'])[0,1] + r23.mn(buf_sel[1].pins['O'])[1,1])/2]
mn_int = [r23.mn(buf_sel[0].pins['O'])[0], r23.mn(buf_sel[1].pins['I'])[0]]
dsn.route_via_track(grid=r23, mn=mn_int, track=_track)

mn_int = [r23.mn(buf_ck[0].pins['O'])[0], r23.mn(buf_ck[1].pins['I'])[0]]
dsn.route_via_track(grid=r23, mn=mn_int, track=_track)

mn_int = [r23.mn(gate_RE[0].pins['OUT'])[0], r23.mn(gate_RE[1].pins['I'])[0]]
dsn.route_via_track(grid=r23, mn=mn_int, track=_track)
mn_int = [r23.mn(gate_RE[1].pins['O'])[0], r23.mn(gate_RE[2].pins['I'])[0]]
dsn.route_via_track(grid=r23, mn=mn_int, track=_track)
mn_int = [r23.mn(gate_RE[2].pins['O'])[0], r23.mn(gate_RE[3].pins['I'])[0]]
dsn.route_via_track(grid=r23, mn=mn_int, track=_track)

# VSS
rvss0 = dsn.route(grid=r23, mn=[r23.mn.bottom_left(cells[0]), r23.mn.bottom_right(cells[3])])
# VDD
rvdd0 = dsn.route(grid=r23, mn=[r23.mn.top_left(cells[0]), r23.mn.top_right(cells[3])])
rvdd1 = Rect(xy = [pg.abs2phy(pg.mn.bottom_left(tap0))-[0,2], pg.abs2phy(pg.mn.top_right(tap0))+[0,2]], layer=['metal3','drawing'])
dsn.append(rvdd1)
#dsn.via(grid=r23, mn=r23.mn.top_left(tap0))
dsn.via(grid=r23, mn=r23.mn.top_left(tap0)+[1,0])
#dsn.via(grid=r23, mn=r23.mn.top_left(tap0)+[2,0])
# # 6. Create pins.
psel = dsn.pin(name='SEL', grid=r34, mn=r34.mn.bbox(rsel[-1]))
pwe = list()
for i in range(4):
    pwe.append(dsn.pin(name='WE'+str(3-i), grid=r34, mn=r34.mn.bbox(cells[i].pins['WE'])))
pclk = dsn.pin(name='CLK', grid=r34, mn=r34.mn.bbox(buf_ck[0].pins['I']))
pre = dsn.pin(name='RE', grid=r34, mn=r34.mn.bbox(gate_RE[0].pins['B']))
pDo = list()
pDi = list()
for i in range(4):
    for j in range(8):
        pDo.append(dsn.pin(name='Do'+str(8*(3-i)+j), grid=r34, mn=r34.mn.bbox(cells[i].pins['Do'+str(j)]), direction='vertical'))
        pDi.append(dsn.pin(name='Di'+str(8*(3-i)+j), grid=r34, mn=r34.mn.bbox(cells[i].pins['Di'+str(j)]), direction='vertical'))
pvss = list()
pvdd = list()
# temp pin for PEX
dsn.pin(name='VSS',grid=r12, mn=r12.mn.bbox(rvss0))
dsn.pin(name='VDD',grid=r12, mn=r12.mn.bbox(rvdd0))
# for num, cell in enumerate(cells):
#     pvss.append(dsn.pin(name='VSS'+str(num)+'_0', grid=r45, mn=r45.mn.bbox(cell.pins['VSS0']), direction='vertical'))
#     pvdd.append(dsn.pin(name='VDD'+str(num)+'_0', grid=r45, mn=r45.mn.bbox(cell.pins['VDD']), direction='vertical'))
#     pvss.append(dsn.pin(name='VSS'+str(num)+'_1', grid=r45, mn=r45.mn.bbox(cell.pins['VSS1']), direction='vertical'))
#pvdd.append(dsn.pin(name='VDD'+str(len(cells))+'_0', grid=r45, mn=r45.mn.bbox(rvdd1), direction='vertical'))
# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library="sky130A")

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()#(obstacle_layers=['metal1','metal2','metal3'])
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')