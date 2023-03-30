###########################################
#                                         #
#          Buffer Layout Generator        #
#  Created by Taeho Shin & HyungJoo Park  #   
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
cell_type = 'buffer'
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
ref_dir_template = './laygo2_example/logic'        # reference logic library
ref_dir_export = f'./laygo2_example/{libname}'
ref_dir_MAG_exported = f'./laygo2_example/{libname}/TCL'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlib = laygo2.interface.yaml.import_template(filename=f"{ref_dir_template}/logic_generated_templates.yaml")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23_cmos, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_cmos_name], grids[r23_basic_name], grids[r34_name]

nf_list = [2, 12, 14, 24, 36]
for nf in nf_list:
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
    verilog_filename = f"{cellname}.v"
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
        instances.append(tlib[instance["Module"]].generate(name=instance["name"], netmap=instance["portlist"]))


    # 4. Place instances.
    dsn.place(grid=pg, inst=instances, mn=[0,0])

    # 5. Create and place wires.
    print("Create wires")
    # internal
    rc = laygo2.object.template.routing.RoutingMeshTemplate(grid=r23)
    # Nodes
    rc.add_node(list(dsn.instances.values()))  # Add all instances to the routing mesh as nodes
    # Tracks
    # ------------- to prevent making tracks with only one node ------------- #
    nets_for_count = []
    for node in rc.nodes:
        for net in node.pins.values():
            if net.netname not in ['VDD', 'VSS', 'vdd', 'vss']:
                nets_for_count.append(net.netname)
    # ----------------------------------------------------------------------- #
    # *** define the starting track (parallel to x axis) *** #              #||
    _trk = (r23.mn(instances[1].pins['I'])[0,1] + r23.mn(instances[1].pins['I'])[1,1])/2    #||
    # ****************************************************** #              #||
    m = 0                                                                   #||
    for n, w in enumerate(WIRES):                                           #||
        if nets_for_count.count(w) != 1: # <<================================||
            rc.add_track(name=f"{w}_net", index=[None, _trk + n - m], netname=w)
        else: m += 1
    rinst = rc.generate()
    dsn.place(grid=pg, inst=rinst)

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
                cur_pins.append(dsn.pin(name=p, grid=r23_cmos, mn=r23_cmos.mn.bbox(i.pins[cur_port_key])))
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