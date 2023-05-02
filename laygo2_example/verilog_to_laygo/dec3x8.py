###########################################
#                                         #
#   dec3x8 Layout Generator from .v code  #
#               Created by                #
#           H.J. PARK, S.Y. Lee           #
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech

from parse_from_v import info_from_verilog_code

# Parameter definitions #############
# Variables
cell_type = 'dec3x8'
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
libname = 'verilog_to_laygo'
ref_dir_template = f'./laygo2_example/{libname}'        # reference logic library
ref_dir_export = f'./laygo2_example/{libname}'
ref_dir_MAG_exported = f'./laygo2_example/{libname}/TCL'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tv2laygolib = laygo2.interface.yaml.import_template(filename=f"{ref_dir_template}/{libname}_templates.yaml")
tlib = laygo2.interface.yaml.import_template(filename=f"./laygo2_example/logic/logic_generated_templates.yaml")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23_cmos, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_cmos_name], grids[r23_basic_name], grids[r34_name]

nf=2
cellname = f"{cell_type}_{nf}x"
print('--------------------')
print('Now Creating '+cellname)


# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)


# 3. Create instances.
print("Create instances")
# input verilog file
# verilog_filename = f"{cellname}.v"
verilog_filename = f"{cellname}_post_synth.v"
name, paramlist, decl_info, inst_info = info_from_verilog_code(f"./laygo2_example/{libname}/verilog_codes/{verilog_filename}")

print()
print(name)
print(paramlist)
print(decl_info)
for i in inst_info :
    print(i)

PINS = dict()
for portname in decl_info["Input"]+decl_info["Output"]+decl_info["Input"]:
    PINS[portname] = portname
WIRES = decl_info["Wire"]

instances = []; instances_tlib = []
for instance in inst_info:
    instances_tlib.append(instance["Module"])
    if instance["Module"] == "inv_2x":
        instances.append(tlib[instance["Module"]].generate(name=instance["name"], netmap=instance["portlist"]))
    else:
        instances.append(tv2laygolib[instance["Module"]].generate(name=instance["name"], netmap=instance["portlist"]))

# 4. Place instances.
inv0, inv1, inv2 = instances[1], instances[2], instances[0]
ands = instances[3:]

NTAP0 = templates[tntap_name].generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
PTAP0 = templates[tptap_name].generate(name='MPT0', transform='MX',params={'nf':2, 'tie':'TAP0'})
NTAP1 = templates[tntap_name].generate(name='MNT1', params={'nf':2, 'tie':'TAP0'})
PTAP1 = templates[tptap_name].generate(name='MPT1', transform='MX',params={'nf':2, 'tie':'TAP0'})

# 4. Place instances.
dsn.place(grid=pg, inst=inv0, mn=[0,0])
dsn.place(grid=pg, inst=inv1, mn=pg.mn.bottom_right(inv0))
dsn.place(grid=pg, inst=inv2, mn=pg.mn.bottom_right(inv1))
mn_left = pg.mn.bottom_right(inv2)
for i in range(2):
    dsn.place(grid=pg, inst=ands[i], mn=mn_left)
    mn_left = pg.mn.bottom_right(ands[i])
dsn.place(grid=pg, inst=NTAP0, mn=mn_left)
dsn.place(grid=pg, inst=PTAP0, mn=pg.mn.top_left(NTAP0) + pg.mn.height_vec(PTAP0))
mn_left = pg.mn.bottom_right(NTAP0)
for i in range(2,5):
    dsn.place(grid=pg, inst=ands[i], mn=mn_left)
    mn_left = pg.mn.bottom_right(ands[i])
dsn.place(grid=pg, inst=NTAP1, mn=mn_left)
dsn.place(grid=pg, inst=PTAP1, mn=pg.mn.top_left(NTAP1) + pg.mn.height_vec(PTAP1))
mn_left = pg.mn.bottom_right(NTAP1)
for i in range(5,8):
    dsn.place(grid=pg, inst=ands[i], mn=mn_left)
    mn_left = pg.mn.bottom_right(ands[i])
# 5. Create and place wires.
print("Create wires")

# A0bar
mn_list = [r23.mn(inv0.pins['O'])[0], r23.mn(ands[0].pins['C'])[0], r23.mn(ands[2].pins['C'])[0],
    r23.mn(ands[4].pins['C'])[0], r23.mn(ands[6].pins['C'])[0]]
_track = [None, r23.mn(inv0.pins['O'])[0,1]-2]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# A0
mn_list = [r23.mn(inv0.pins['I'])[0], r23.mn(ands[1].pins['C'])[0], r23.mn(ands[3].pins['C'])[0],
    r23.mn(ands[5].pins['C'])[0], r23.mn(ands[7].pins['C'])[0]]
_track = [None, r23.mn(inv0.pins['I'])[0,1]+1]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# A1bar
mn_list = [r23.mn(inv1.pins['O'])[1], r23.mn(ands[0].pins['D'])[1], r23.mn(ands[1].pins['D'])[1],
    r23.mn(ands[4].pins['D'])[1], r23.mn(ands[5].pins['D'])[1]]
_track = [None, r23.mn(inv1.pins['O'])[1,1]-1]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
# A1
mn_list = [r23.mn(inv1.pins['I'])[0], r23.mn(ands[2].pins['D'])[0], r23.mn(ands[3].pins['D'])[0],
    r23.mn(ands[6].pins['D'])[0], r23.mn(ands[7].pins['D'])[0]]
_track = [None, r23.mn(inv1.pins['I'])[0,1]+2]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# A2bar
mn_list = [r23.mn(inv2.pins['O'])[1], r23.mn(ands[0].pins['B'])[1], r23.mn(ands[1].pins['B'])[1],
    r23.mn(ands[2].pins['B'])[1], r23.mn(ands[3].pins['B'])[1]]
_track = [None, r23.mn(inv2.pins['O'])[0,1]-1]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
# A2
mn_list = [r23.mn(inv2.pins['I'])[0], r23.mn(ands[4].pins['B'])[0], r23.mn(ands[5].pins['B'])[0],
    r23.mn(ands[6].pins['B'])[0], r23.mn(ands[7].pins['B'])[0]]
_track = [None, r23.mn(inv2.pins['I'])[0,1]+3]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
#Enable
mn_list=[]
for i in range(8):
    mn_list.append(r34.mn(ands[i].pins['A'])[0])
_track = [None, r34.mn(ands[0].pins['A'])[0,1]]
rEN = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(instances[0]), r12.mn.bottom_right(instances[-1])])
# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(instances[0]), r12.mn.top_right(instances[-1])])


# 6. Create pins.
cur_pins = []
for p in PINS.keys(): # PINS.keys() : pin names
    # current order
    for n, i in enumerate(instances):
        cur_netnames = [x.netname for x in i.pins.values()] # netnames in instance i
        if PINS[p] in cur_netnames:   # p : pin names user defines, PINS[p] : netnames corresponding to pin name p
            if p in [pin.netname for pin in cur_pins]: continue     # only save each pins once
            cur_port_key = list(i.pins.keys())[cur_netnames.index(PINS[p])] # cur_netnames is from i.pins.values (converted to string)
            
            P = p
            if '[' in list(p) and p.count('[') == p.count(']'):
                print(P, end=" --> "); P=p.replace('[', ''); P=P.replace(']', '')
            print(P)
            
            cur_pins.append(dsn.pin(name=P, grid=r23_cmos, mn=r23_cmos.mn.bbox(i.pins[cur_port_key])))
                                      # name as user defined pin name (p)       # need pin name of the instance i (cur_port_key)
                                                                                # that is connected to the netname PINS[p]
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=f"{ref_dir_MAG_exported}/{libname}_{cellname}.tcl", cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')


# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=f"{ref_dir_export}/{libname}_templates.yaml", mode='append')