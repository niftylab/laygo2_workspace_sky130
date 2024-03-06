###########################################
#                                         #
#     DFF driven byte Layout Generator    #
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
cell_type = 'byte_dff_left'
nf_inv=2
nf=1
abut=[0,0]
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
buf_re0 = tlogic_prim['inv_'+str(nf_inv*3)+'x'].generate(name='buf_RE0',transform='MY')
buf_re1 = tlogic_prim['inv_'+str(nf_inv*3)+'x'].generate(name='buf_RE1',transform='MY')
inv_and = tlogic_prim['inv_'+str(nf_inv)+'x'].generate(name='inv_and',transform='MY')
nand = tlogic_prim['nand_'+str(nf_inv)+'x'].generate(name='nand',transform='MY')
cgate = tlogic_adv['cgate_'+str(nf_inv)+'x'].generate(name='cgate0',transform='MY')
tap0= tlogic_prim['space_2x'].generate(name='space0')
tap1= tlogic_prim['space_2x'].generate(name='space1')
tap2= tlogic_prim['space_2x'].generate(name='space2')
cells=list()
for i in range(8):
    cells.append(tlogic_prim['dff_'+str(nf)+'x'].generate(name='dff_'+str(i)))
    cells.append(tlogic_prim['tinv_'+str(nf_inv)+'x'].generate(name='tinv'+str(i)))
# 4. Place instances.
dsn.place(grid=pg, inst=tap0, mn=[0,0])
cursor = pg.mn.bottom_right(tap0)
for i in range(8):
    dsn.place(grid=pg, inst=cells[i], mn=cursor)
    cursor = pg.mn.bottom_right(cells[i]) - abut
dsn.place(grid=pg, inst=tap1, mn=cursor+abut)
cursor = pg.mn.bottom_right(tap1)
for i in range(8,len(cells)):
    dsn.place(grid=pg, inst=cells[i], mn=cursor)
    cursor = pg.mn.bottom_right(cells[i]) - abut
dsn.place(grid=pg, inst=tap2, mn=cursor+abut)
cursor = pg.mn.bottom_right(tap2)
dsn.place(grid=pg, inst=buf_re1, mn=cursor+pg.mn.width_vec(buf_re1))
dsn.place(grid=pg, inst=buf_re0, mn=pg.mn.bottom_right(buf_re1)+pg.mn.width_vec(buf_re0))
dsn.place(grid=pg, inst=cgate, mn=pg.mn.bottom_right(buf_re0)+pg.mn.width_vec(cgate))
dsn.place(grid=pg, inst=inv_and, mn=pg.mn.bottom_right(cgate)+pg.mn.width_vec(inv_and))
dsn.place(grid=pg, inst=nand, mn=pg.mn.bottom_right(inv_and)+pg.mn.width_vec(nand))
# 5. Create and place wires.
print("Create wires")

# RE_buf
mn_list = [r34.mn(buf_re1.pins['O'])[0]]
for i in range(8):
    mn_list.append(r34.mn(cells[2*i+1].pins['EN'])[0]) # ~= cells[i].tinv.pins[EN]
#track_re = [None, r34.mn(buf_re1.pins['O'])[1,1]]
track_re = [None, r34.mn(buf_re1.pins['O'])[0,1]-1]
rsel = dsn.route_via_track(grid=r34, mn=mn_list, track=track_re)

# RE_bar
mn_list = [r34.mn(buf_re0.pins['O'])[0]]
for i in range(8):
    mn_list.append(r34.mn(cells[2*i+1].pins['ENB'])[0]) # ~= cells[i].tinv.pins[ENB]
track_rebar = [None,track_re[1]+1]
dsn.route_via_track(grid=r34, mn=mn_list, track=track_rebar)

# RE buf internal
mn_list = [r23.mn(buf_re0.pins['O'])[0], r23.mn(buf_re1.pins['I'])[0]]
_track = [None, (r23.mn(buf_re0.pins['O'])[0,1] + r23.mn(buf_re0.pins['O'])[1,1])/2]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# Nand_inv
mn_list = [ r23.mn(nand.pins['OUT'])[0], r23.mn(inv_and.pins['I'])[0] ]
_track = [None, (r23.mn(inv_and.pins['I'])[0,1]+r23.mn(inv_and.pins['I'])[1,1])/2]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# clock en
mn_list = [r34.mn(inv_and.pins['O'])[0], r34.mn(cgate.pins['EN'])[0] ]
_track = [None,(r34.mn(cgate.pins['EN'])[0,1]+r34.mn(cgate.pins['EN'])[1,1])/2]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# clk flip flop
mn_list = [r34.mn(cgate.pins['CK_O'])[0]]
for i in range(8):
    mn_list.append(r34.mn(cells[2*i].pins['CLK'])[0])
_track = [None, track_rebar[1]+1]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# cell internal
for i in range(8):
    # dff_out <--> tinv_in    
    mn_list = [r34.mn(cells[2*i].pins['O_bar'])[0], r34.mn(cells[2*i+1].pins['I'])[0]]
    _track = [None, (r34.mn(cells[2*i+1].pins['I'])[0,1] + r34.mn(cells[2*i+1].pins['I'])[1,1])/2]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(tap0), r12.mn.bottom_right(nand)])
rvss1 = Rect(xy = [pg.abs2phy(pg.mn.bottom_left(tap0)-[0,1]), pg.abs2phy(pg.mn.top_right(tap0)+[0,1])], layer=['metal3','drawing'])
dsn.append(rvss1)
#dsn.via(grid=r45, mn=r45.mn.bottom_left(tap0))
dsn.via(grid=r45, mn=r45.mn.bottom_left(tap0)+[1,0])
#dsn.via(grid=r45, mn=r45.mn.bottom_left(tap0)+[2,0])
rvss2 = Rect(xy = [pg.abs2phy(pg.mn.bottom_left(tap2)-[0,1]), pg.abs2phy(pg.mn.top_right(tap2)+[0,1])], layer=['metal3','drawing'])
dsn.append(rvss2)
#dsn.via(grid=r45, mn=r45.mn.bottom_left(tap2))
dsn.via(grid=r45, mn=r45.mn.bottom_left(tap2)+[1,0])
#dsn.via(grid=r45, mn=r45.mn.bottom_left(tap2)+[2,0])
# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(tap0), r12.mn.top_right(nand)])
rvdd1 = Rect(xy = [pg.abs2phy(pg.mn.bottom_left(tap1)-[0,1]), pg.abs2phy(pg.mn.top_right(tap1)+[0,1])], layer=['metal3','drawing'])
dsn.append(rvdd1)
#dsn.via(grid=r45, mn=r45.mn.top_left(tap1))
dsn.via(grid=r45, mn=r45.mn.top_left(tap1)+[1,0])
#dsn.via(grid=r45, mn=r45.mn.top_left(tap1)+[2,0])
# 6. Create pins.
psel =  dsn.pin(name='SEL', grid=r34, mn=r34.mn.bbox(nand.pins['B']))
pre = dsn.pin(name='RE', grid=r34, mn=r34.mn.bbox(buf_re0.pins['I']))
pwe = dsn.pin(name='WE', grid=r23, mn=r23.mn.bbox(nand.pins['A']))
pclk = dsn.pin(name='CLK', grid=r23, mn=r23.mn.bbox(cgate.pins['CK_I']))
pDo = list()
pDi = list()
for i in range(8):
    # pDo.append(dsn.pin(name='Do<'+str(7-i)+'>', grid=r23, mn=r23.mn.bbox(cells[3*(7-i)+2].pins['O'])))
    # pDi.append(dsn.pin(name='Di<'+str(7-i)+'>', grid=r23, mn=r23.mn.bbox(cells[3*(7-i)].pins['I'])))
    pDo.append(dsn.pin(name='Do'+str(7-i), grid=r23, mn=r23.mn.bbox(cells[2*i+1].pins['O']), direction='vertical'))
    pDi.append(dsn.pin(name='Di'+str(7-i), grid=r23, mn=r23.mn.bbox(cells[2*i].pins['I']), direction='vertical'))
# pA2bar = dsn.pin(name='A2bar', grid=r23, mn=r23.mn.bbox(inv0.pins['O']))

# pvss0 = dsn.pin(name='VSS0', grid=r45, mn=r23.mn.bbox(rvss1), direction='vertical')
# pvss1 = dsn.pin(name='VSS1', grid=r45, mn=r23.mn.bbox(rvss2), direction='vertical')
# pvdd0 = dsn.pin(name='VDD', grid=r45, mn=r23.mn.bbox(rvdd1), direction='vertical')

# 7. Export to physical database.
print("Export design")
grid_table = dict()
grid_table['metal1'] = r34
grid_table['metal2'] = r34
grid_table['metal3'] = r45
via_table = dict()
via_table["via_M3_M4_0"] = ('metal1','metal2')
via_table["via_M4_M5_0"] = ('metal2','metal3')
nMap = NetMap.import_from_design(dsn, grid_table, via_table, orient_first="vertical", layer_names=['metal1','metal2','metal3'], net_ignore = ['VSS','VDD'], lib_ref = "laygo2_example/prj_db/library.yaml")   
# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library="sky130A")

# 8. Export to a template database file.
nat_temp = dsn.export_to_template(obstacle_layers=['metal1','metal2','metal3'])
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')