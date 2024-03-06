###########################################
#                                         #
#       4 to 1 MUX Layout Generator       #
#        Created by HyungJoo Park         #   
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
from laygo2.object.netmap import NetMap
# Parameter definitions #############
# Variables
cell_type = 'mux4to1'
nf_list = [2,4]
# Templates
tpmos_name = 'pmos'
tnmos_name = 'nmos'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
# Design hierarchy
libname = 'logic_ver2'
ref_dir_template = './laygo2_example/logic_ver2/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_example/logic_ver2/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_ver2_templates.yaml')
#print(templates[tpmos_name], templates[tnmos_name], sep="\n")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]

abut = [4,0]
for nf in nf_list:
    cellname = cell_type+'_'+str(nf)+'x'
    print('--------------------')
    print('Now Creating '+cellname)

# 2. Create a design hierarchy
    lib = laygo2.object.database.Library(name=libname)
    dsn = laygo2.object.database.Design(name=cellname, libname=libname)
    lib.append(dsn)

# 3. Create istances.
    #print("Create instances")
    tgate = list()
    for i in range(6):
        tgate.append(tlib['tgate_'+str(nf)+'x'].generate(name='tgate'+str(i)))

# 4. Place instances.
    cursor = [0,0]
    for i in range(6):
        dsn.place(grid=pg, inst=tgate[i], mn=cursor)
        cursor = pg.mn.bottom_right(tgate[i])-abut
   
   # 5. Create and place wires.
    print("Create wires")
   
    # A_bar <-> A connect
    _mn = [r23.mn(tgate[0].pins['ENB'])[1], r23.mn(tgate[1].pins['EN'])[1]]
    dsn.route(grid=r23, mn=_mn, via_tag=[False, True])
    _mn = [r23.mn(tgate[1].pins['ENB'])[1], r23.mn(tgate[2].pins['EN'])[1]]
    dsn.route(grid=r23, mn=_mn, via_tag=[False, True])   
    _mn = [r23.mn(tgate[2].pins['ENB'])[1], r23.mn(tgate[3].pins['EN'])[1]]
    dsn.route(grid=r23, mn=_mn, via_tag=[False, True])

    _track = [None, r23.mn(tgate[0].pins['EN'])[0][1]+1]
    mn_list=[r23.mn(tgate[0].pins['EN'])[0], r23.mn(tgate[1].pins['ENB'])[0]]
    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
    mn_list=[r23.mn(tgate[2].pins['EN'])[0], r23.mn(tgate[3].pins['ENB'])[0]]
    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
    _track = [None, (r34.mn(tgate[0].pins['EN'])[0][1]+r34.mn(tgate[0].pins['EN'])[1][1])/2]
    mn_list=[r34.mn(tgate[1].pins['EN'])[0], r34.mn(tgate[2].pins['ENB'])[0]]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
    
    # 1stage out <-> 2stage in (internal)
    _mn = [r12.mn(tgate[0].pins['O'])[1], r12.mn(tgate[1].pins['O'])[1]]
    dsn.route(grid=r12, mn=_mn, via_tag=[False, False])
    _mn = [r12.mn(tgate[2].pins['O'])[1], r12.mn(tgate[3].pins['O'])[1]]
    dsn.route(grid=r12, mn=_mn, via_tag=[False, False])

    _track = [None, r34.mn(tgate[0].pins['O'])[0][1]]
    mn_list=[r34.mn(tgate[1].pins['O'])[0], r34.mn(tgate[4].pins['I'])[0]]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

    _track = [None, (r34.mn(tgate[0].pins['EN'])[0][1]+r34.mn(tgate[0].pins['EN'])[1][1])/2]
    mn_list=[r34.mn(tgate[3].pins['O'])[0], r34.mn(tgate[5].pins['I'])[0]]
    dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

    # 2stage out
    _mn = [r12.mn(tgate[4].pins['O'])[1], r12.mn(tgate[5].pins['O'])[1]]
    dsn.route(grid=r12, mn=_mn, via_tag=[False, False])

    # C1
    _mn = [r23.mn(tgate[4].pins['ENB'])[1], r23.mn(tgate[5].pins['EN'])[1]]
    dsn.route(grid=r23, mn=_mn, via_tag=[False, True])
    # C1_bar
    _track = [None, r23.mn(tgate[0].pins['EN'])[0][1]+1]
    mn_list=[r23.mn(tgate[4].pins['EN'])[0], r23.mn(tgate[5].pins['ENB'])[0]]
    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)            
#    # C0_bar
#    mn_list=[]
#    mn_list.append(r34.mn(tgate[0].pins['ENB'])[1])
#    mn_list.append(r34.mn(tgate[1].pins['EN'])[1])
#    mn_list.append(r34.mn(tgate[1].pins['ENB'])[1])
#    mn_list.append(r34.mn(tgate[2].pins['EN'])[1])

#    _track = [None, (r23.mn(tinv_small0.pins['I'])[0,1]+r23.mn(tinv_small0.pins['I'])[1,1])/2]
#    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
#    # 2nd M2
#    mn_list=[]
#    mn_list.append(r34.mn(inv2.pins['I'])[0])
#    mn_list.append(r34.mn(tinv0.pins['O'])[0])
#    mn_list.append(r34.mn(tinv_small0.pins['O'])[0])
#    _track = [None, r23.mn(tinv0.pins['O'])[0,1]]
#    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
#    # 3rd M2
#    mn_list=[]
#    mn_list.append(r34.mn(inv3.pins['I'])[0])
#    mn_list.append(r34.mn(tinv1.pins['O'])[0])
#    mn_list.append(r34.mn(tinv_small1.pins['O'])[0])
#    _track = [None, r23.mn(tinv1.pins['O'])[0,1]]
#    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
#    # 4th M2
#    mn_list=[]
#    mn_list.append(r34.mn(inv3.pins['O'])[0])
#    mn_list.append(r34.mn(tinv_small1.pins['I'])[0]) 
#    _track = [None, r23.mn(inv3.pins['O'])[0,1]]
#    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
  
   # VSS
    rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(tgate[0]), r12.mn.bottom_right(tgate[5])])
   
   # VDD
    rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(tgate[0]), r12.mn.top_right(tgate[5])])
   
   # 6. Create pins.
    pX0 = dsn.pin(name='X0', grid=r34, mn=r34.mn.bbox(tgate[0].pins['I']))
    pX0 = dsn.pin(name='X1', grid=r34, mn=r34.mn.bbox(tgate[1].pins['I']))
    pX0 = dsn.pin(name='X2', grid=r34, mn=r34.mn.bbox(tgate[2].pins['I']))
    pX0 = dsn.pin(name='X3', grid=r34, mn=r34.mn.bbox(tgate[3].pins['I']))
    pC0 = dsn.pin(name='C0', grid=r34, mn=r34.mn.bbox(tgate[0].pins['ENB']))
    pC0_bar = dsn.pin(name='C0bar', grid=r34, mn=r34.mn.bbox(tgate[0].pins['EN']))
    pC1 = dsn.pin(name='C1', grid=r34, mn=r34.mn.bbox(tgate[4].pins['ENB']))
    pC1_bar = dsn.pin(name='C1bar', grid=r34, mn=r34.mn.bbox(tgate[4].pins['EN']))
    pout0 = dsn.pin(name='O', grid=r34, mn=r34.mn.bbox(tgate[5].pins['O']))
    pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
    pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))
   
    # 7. Export to physical database.
    print("Export design")
    grid_table = dict()
    grid_table['metal1'] = r34
    grid_table['metal2'] = r34
    via_table = dict()
    via_table["via_M3_M4_0"] = ('metal1','metal2')
    via_table["via_M4_M5_0"] = ('metal2','metal3')
    nMap = NetMap.import_from_design(dsn, grid_table, via_table, orient_first="vertical", layer_names=['metal1','metal2'], net_ignore = ['VSS','VDD'], lib_ref = "laygo2_example/prj_db/library.yaml")
    # Uncomment for BAG export
    laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library="sky130A")
    # 8. Export to a template database file.
    nat_temp = dsn.export_to_template(metal_table=grid_table, net_ignore = ['VSS','VDD'])
    laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')