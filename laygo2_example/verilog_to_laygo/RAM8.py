###########################################
#                                         #
#       32bit WORD Layout Generator       #
#        Created by Sungyoung Lee         #   
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
# Parameter definitions #############
# Variables
cell_type = 'ram8'
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
libname = 'verilog_to_laygo'
ref_dir_template = './laygo2_example/' #export this layout's information into the yaml in this dir 
ref_dir_export = f'./laygo2_example/{libname}/'
ref_dir_MAG_exported = f'./laygo2_example/{libname}/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
# tlogic_prim = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic/logic_generated_templates.yaml')
# tlogic_adv = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_advance/logic_advanced_templates.yaml')
tv2laygo = laygo2.interface.yaml.import_template(filename=ref_dir_template+'verilog_to_laygo/verilog_to_laygo_templates.yaml')

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
    if i % 2 == 0 :
        words.append(tv2laygo['word_32bit_'+str(nf)+'x'].generate(name='word'+str(i)))
    else :
        words.append(tv2laygo['word_32bit_'+str(nf)+'x'].generate(name='word'+str(i), transform='MX'))
buf_clk = tv2laygo['buffer_'+str(24)+'x'].generate(name='buf_clk')
dec8 = tv2laygo['dec3x8_'+str(nf)+'x'].generate(name='dec8')
buf_we=[]
buf_sel = []
for i in range(4):
    buf_we.append(tv2laygo['buffer_'+str(24)+'x'].generate(name='buf_we'+str(i)))
for i in range(8):
    buf_sel.append(tv2laygo['buffer_'+str(12)+'x'].generate(name='buf_sel'+str(i)))
# NTAP0 = templates[tntap_name].generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
# PTAP0 = templates[tptap_name].generate(name='MPT0', transform='MX',params={'nf':2, 'tie':'TAP0'})
# NTAP1 = templates[tntap_name].generate(name='MNT1', params={'nf':2, 'tie':'TAP0'})
# PTAP1 = templates[tptap_name].generate(name='MPT1', transform='MX',params={'nf':2, 'tie':'TAP0'})

# 4. Place instances.
mn_ref = [0,0]
for i in range(int(words_num/2)):
    dsn.place(grid=pg, inst=words[i*2], mn=mn_ref)
    dsn.place(grid=pg, inst=words[i*2+1], 
        mn=pg.mn.top_left(words[i*2]) + pg.mn.height_vec(words[i*2+1]))
    mn_ref = pg.mn.top_left(words[i*2+1])

# byte_width = int(pg.mn.width_vec(words[7])[0]/4)
dsn.place(grid=pg, inst=buf_clk, mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_clk)
dsn.place(grid=pg, inst=dec8, mn=mn_ref)
mn_ref = pg.mn.bottom_right(dec8)
for i in range(8):
    dsn.place(grid=pg, inst=buf_sel[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_sel[i])

for i in range(4):
    dsn.place(grid=pg, inst=buf_we[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_we[i])

# 5. Create and place wires.
print("Create wires")
# WE
rWE = []; rbuf_we = []; track_y = [3, 2, 4, 0]
for i in range(4):
    # we + buf_we
    _mn = [r34.mn(words[0].pins[f'WE<{i}>'])[0], r34.mn(buf_we[i].pins['O'])[0]]
    _track = [r34.mn(words[0].pins[f'WE<{i}>'])[0][0], r34.mn(buf_we[i].pins['O'])[0][1] + track_y[i]]
    rbuf_we.append(dsn.route_via_track(grid=r34, mn=_mn, track=_track))
    # we in each words
    _mn = [r34.mn(words[0].pins[f'WE<{i}>'])[0], r34.mn(words[words_num-1].pins[f'WE<{i}>'])[1]]
    rWE.append(dsn.route(grid=r34, mn=_mn, via_tag=[False, False]))
# dec output + buf sel + word sel
rDECsel = []; rBUFword = []
for i in range(8):
    # dec output + buf sel
    _mn = [r34.mn(dec8.pins[f'O{i}'])[0], r34.mn(buf_sel[i].pins['I'])[0]]
    _track = [None, r34.mn(buf_sel[i].pins['I'])[0][1] + 1 + i]
    rDECsel.append(dsn.route_via_track(grid=r34, mn=_mn, track=_track))
    # buf sel[:] -> each word sel
    if i not in (0, 3, 4, 5):  # metal 3 error
        x = 0
    else :
        if i == 0: x = 2
        elif i == 3: x = 1
        elif i == 4: x = -2
        elif i == 5: x = 5
        _mn = [r34.mn(buf_sel[i].pins['O'])[0] + np.array([x, 3]), r34.mn(buf_sel[i].pins['O'])[0] + np.array([0, 3])]
        dsn.route(grid=r34, mn=_mn, via_tag=[True, True])
    _mn = [r34.mn(buf_sel[i].pins['O'])[0] + np.array([x, 3]), r34.mn(words[i].pins['SEL'])[0]]
    _track = [r34.mn(buf_sel[i].pins['O'])[0][0] + x, r34.mn(words[i].pins['SEL'])[0][1]]
    rBUFword.append(dsn.route_via_track(grid=r34, mn=_mn, track=_track))
# buf clk + word clk
rBUFclk = []
for i in range(8):
    _mn = [(r34.mn(buf_clk.pins['O'])[0]+r34.mn(buf_clk.pins['O'])[1])/2, r34.mn(words[i].pins['CLK'])[0]]
    _track = [r34.mn(buf_clk.pins['O'])[0][0], None]
    rBUFclk.append(dsn.route_via_track(grid=r34, mn=_mn, track = _track, via_tag=[True for _ in range(len(_mn))]))
# Di & Do
Di = []; Do = []
for i in range(32):
    _mn = [r34.mn(words[0].pins[f'Di<{i}>'])[0], r34.mn(words[words_num-1].pins[f'Di<{i}>'])[1]]
    Di.append(dsn.route(grid=r34, mn=_mn, via_tag=[False, False]))
    _mn = [r34.mn(words[0].pins[f'Do<{i}>'])[0], r34.mn(words[words_num-1].pins[f'Do<{i}>'])[1]]
    Do.append(dsn.route(grid=r34, mn=_mn, via_tag=[False, False]))
# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(words[0]), r12.mn.bottom_right(words[0])])
# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(buf_clk), r12.mn.top_right(words[-1]) + r12.mn.height_vec(dec8)])
# route all vdd / vss
_mn = []
for word in words:
    _mn += [r23.mn.bottom_right(word)]
_mn += [r23.mn.top_right(words[-1])]
_mn += [r23.mn.top_right(words[-1]) + r23.mn.height_vec(dec8)]
rvdd = dsn.route(grid=r23, mn=[_mn[i] - r23.mn.width_vec(words[0]) for i in range(len(_mn))], via_tag=[False for _ in range(len(_mn))])
rvss = dsn.route(grid=r23, mn=_mn, via_tag=[False for _ in range(len(_mn))])
via_vdd = dsn.via(grid=r23, mn=[_mn[i] - r23.mn.width_vec(words[0]) for i in range(1, len(_mn), 2)])
via_vss = dsn.via(grid=r23, mn=[_mn[i] for i in range(0, len(_mn), 2)])


# 6. Create pins.
dA = list()
for i in range(3):
    dA.append(dsn.pin(name=f'A<{i}>', grid=r23_cmos, mn=r23_cmos.mn.bbox(dec8.pins[f'A{i}'])))
pen = dsn.pin(name='EN', grid=r23_cmos, mn=r23_cmos.mn.bbox(dec8.pins['EN']))
pwe = list()
for i in range(4):
    pwe.append(dsn.pin(name=f'WE<{i}>', grid=r23_cmos, mn=r23_cmos.mn.bbox(buf_we[i].pins['I'])))
pclk = dsn.pin(name='CLK', grid=r23_cmos, mn=r23_cmos.mn.bbox(buf_clk.pins['I']))
pDo = list()
pDi = list()
for i in range(32):
    pDo.append(dsn.pin(name=f'Do<{i}>', grid=r34, mn=r23_cmos.mn.bbox(Do[i])))
    pDi.append(dsn.pin(name=f'Di<{i}>', grid=r34, mn=r23_cmos.mn.bbox(Di[i])))
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')