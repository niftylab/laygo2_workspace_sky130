###########################################
#                                         #
#         RAM32 Layout Generator          #
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
cell_type = 'ram32'
nf=2
words_num = 8 # must be an even number
buffer_num = 8+4+1 # number of buffers
ram8s_num = 4
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
tlogic_prim = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic/logic_generated_templates.yaml')
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

# 3. Create instances.
print("Create instances")
# RAM8s
ram8s=list()
for i in range(ram8s_num):
    if i % 2 == 1 :
        ram8s.append(tv2laygo[f'ram8_{nf}x'].generate(name=f'RAM8_{i}'))
    else :
        ram8s.append(tv2laygo[f'ram8_{nf}x'].generate(name=f'RAM8_{i}', transform='MX'))
# DEC2x4
dec4 = tv2laygo[f'dec2x4_{nf}x'].generate(name='dec4')
# Buffers
buf_clk14 = tv2laygo['buffer_14x'].generate(name='buf_clk14')
buf_clk36 = tv2laygo['buffer_36x'].generate(name='buf_clk36')
buf_clk72 = [tv2laygo['buffer_36x'].generate(name='buf_clk_ram'),\
            tv2laygo['buffer_36x'].generate(name='buf_clk_outreg0'),\
            tv2laygo['buffer_36x'].generate(name='buf_clk_outreg1')]
buf_we = []
for i in range(4):
    buf_we.append(tv2laygo['buffer_36x'].generate(name=f'buf_we_{i}'))
buf_en = tv2laygo['buffer_24x'].generate(name='buf_en', transform='MX')
buf_a = []  # buf sel
for i in range(5):
    buf_a.append(tv2laygo['buffer_24x'].generate(name=f'buf_a_{i}', transform='MX'))
# Input Buffer
buf_in = []
for i in range(32):
    buf_in.append(tv2laygo['buffer_24x'].generate(name=f'buf_in_{i}'))
# Output Reg
outreg = []
for i in range(32):
    outreg.append(tlogic_prim[f'dff_{nf}x'].generate(name=f'OUTREG_{i}'))

# NTAP0 = templates[tntap_name].generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
# PTAP0 = templates[tptap_name].generate(name='MPT0', transform='MX',params={'nf':2, 'tie':'TAP0'})
# NTAP1 = templates[tntap_name].generate(name='MNT1', params={'nf':2, 'tie':'TAP0'})
# PTAP1 = templates[tptap_name].generate(name='MPT1', transform='MX',params={'nf':2, 'tie':'TAP0'})

# 4. Place instances.
mn_ref = [0, 0]
# CLK, WE
dsn.place(grid=pg, inst=buf_clk14, mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_clk14)
dsn.place(grid=pg, inst=buf_clk36, mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_clk36)
for i in range(len(buf_clk72)):
    dsn.place(grid=pg, inst=buf_clk72[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_clk72[i])
for i in range(4):
    dsn.place(grid=pg, inst=buf_we[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_we[i])
mn_ref = pg.mn.top_left(buf_clk14)
# RAM 8x4
for i in range(int(ram8s_num/2)):
    dsn.place(grid=pg, inst=ram8s[i*2], mn=mn_ref + pg.mn.height_vec(ram8s[0]))
    mn_ref = pg.mn.top_left(ram8s[i*2])
    dsn.place(grid=pg, inst=ram8s[i*2+1], mn=mn_ref)
    mn_ref = pg.mn.top_left(ram8s[i*2+1])
# A, En, DEC4, input_buf
mn_ref += pg.mn.height_vec(buf_a[0])
for i in range(5):
    dsn.place(grid=pg, inst=buf_a[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_right(buf_a[i]) + pg.mn.height_vec(buf_a[i])
dsn.place(grid=pg, inst=buf_en, mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_en)
dsn.place(grid=pg, inst=dec4, mn=mn_ref)
mn_ref = pg.mn.top_right(ram8s[-1]) - pg.mn.width_vec(buf_in[0])
for i in range(32):
    dsn.place(grid=pg, inst=buf_in[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_left(buf_in[i]) - pg.mn.width_vec(buf_in[i])
mn_ref = pg.mn.bottom_right(ram8s[0]) - pg.mn.width_vec(outreg[0]) - pg.mn.height_vec(outreg[0])
# outreg
for i in range(32):
    dsn.place(grid=pg, inst=outreg[i], mn=mn_ref)
    mn_ref = pg.mn.bottom_left(outreg[i]) - pg.mn.width_vec(outreg[i])


# # 5. Create and place wires.
# print("Create wires")
# rA = []
# # A<4>, A<3>, EN  --->  dec2x4
# _mn = [r34.mn(buf_a[4].pins['O'])[1], r34.mn(dec4.pins['A1'])[1]]   # A4
# _track = [None, r34.mn(buf_a[4].pins['O'])[1][1] - 5]
# rA.append(dsn.route_via_track(grid = r34, mn = _mn, track = _track))
# _mn = [r34.mn(buf_a[3].pins['O'])[1], r34.mn(dec4.pins['A0'])[1]]   # A3
# _track = [None, r34.mn(buf_a[3].pins['O'])[1][1] - 4]
# rA.append(dsn.route_via_track(grid = r34, mn = _mn, track = _track))
# _mn = [r34.mn(buf_en.pins['O'])[1], r34.mn(dec4.pins['EN'])[0]]   # EN
# _track = [None, r34.mn(dec4.pins['EN'])[0][1]]
# rEN = dsn.route_via_track(grid = r34, mn = _mn, track = _track)
# # dec2x4  --->  RAM8 EN     X 4
# rEN_RAM8 = []; x = [-11, -7, -3, 0]
# for i in range(4):
#     _mn = [r34.mn(dec4.pins[f'Y{i}'])[0] + np.array([0, 1]),\
#             np.array([r34.mn(dec4.pins[f'Y{i}'])[0][0], r34.mn(dec4.pins[f'Y{i}'])[0][1] - i + 1]),\
#             np.array([r34.mn(ram8s[i].pins['EN'])[(i%2 + 1)%2][0] + x[i], r34.mn(dec4.pins[f'Y{i}'])[0][1] - i + 1]),\
#             np.array([r34.mn(ram8s[i].pins['EN'])[(i%2 + 1)%2][0] + x[i], r34.mn(ram8s[i].pins['EN'])[(i%2 + 1)%2][1]]),\
#             r34.mn(ram8s[i].pins['EN'])[(i%2 + 1)%2]]   # Y0 Y1 Y2 Y3
#     rEN_RAM8.append(dsn.route(grid = r34, mn = _mn))
# # A<2>, A<1>, A<0>  --->  RAM8 A[2:0]   X 4
# rA_RAM8 = []; y = [-7, -6, -5]
# for i in range(3):
#     _mn = [r34.mn(ram8s[j].pins[f'A<{i}>'])[1] for j in range(ram8s_num)]\
#         + [np.array([r34.mn(ram8s[-1].pins[f'A<{i}>'])[1][0], r34.mn(buf_a[i].pins['O'])[1][1] + y[i]])]\
#         + [r34.mn(buf_a[i].pins['O'])[1] + np.array([0, y[i]])]
#     rA_RAM8.append(dsn.route(grid = r34, mn = _mn, via_tag = [False]+[True for _ in range(len(_mn) - 1)]))
# # buf_clk   --->    RAM8 clk   X 4
# rbuf_clk = []
#     # buf clk14 -> buf clk 36
# _mn = [np.mean(r34.mn(buf_clk14.pins['O']), axis=0, dtype=int),\
#        np.mean(r34.mn(buf_clk36.pins['I']), axis=0, dtype=int)]
# rbuf_clk.append(dsn.route(grid = r34, mn = _mn, via_tag = [True, True]))
#     # buf clk36 -> buf clk 36 * 3
# for i in range(len(buf_clk72)):
#     _mn = [np.mean(r34.mn(buf_clk36.pins['O']), axis=0, dtype=int) + np.array([0, i - 1]),\
#         np.mean(r34.mn(buf_clk72[i].pins['I']), axis=0, dtype=int) + np.array([0, i - 1])]
#     rbuf_clk.append(dsn.route(grid = r34, mn = _mn, via_tag = [True, True]))
#     # buf clk 72[0] -> buf ram
# _mn = [r34.mn(buf_clk72[0].pins['O'])[1]]\
#     + [np.array([r34.mn(buf_clk72[0].pins['O'])[1][0], r34.mn(buf_clk72[0].pins['O'])[1][1] + 1])]\
#     + [np.array([r34.mn(ram8s[0].pins['CLK'])[0][0], r34.mn(buf_clk72[0].pins['O'])[1][1] + 1])]\
#     + [r34.mn(ram8s[i].pins['CLK'])[0] for i in range(ram8s_num)]
# rram_clk = dsn.route(grid = r34, mn = _mn, via_tag = [False, True, True] + [False for _ in range(4)])
#     # buf clk 72[1], clk 72[2] -> outreg * 32
# routreg_clk = []
#         # clk 72[1]
# _mn = [np.mean(r34.mn(buf_clk72[1].pins['O']), axis=0, dtype=int) + np.array([0, -1])]
# for i in range(0, 32, 2):
#     _mn += [np.mean(r34.mn(outreg[i].pins['CLK']), axis=0, dtype=int) + np.array([0, -1])]
# routreg_clk.append(dsn.route(grid=r34, mn=_mn, via_tag = [True for _ in range(len(_mn))]))
#         # clk 72[2]
# _mn = [np.mean(r34.mn(buf_clk72[2].pins['O']), axis=0, dtype=int) + np.array([0, 1])]
# for i in range(1, 32, 2):
#     _mn += [np.mean(r34.mn(outreg[i].pins['CLK']), axis=0, dtype=int) + np.array([0, 1])]
# routreg_clk.append(dsn.route(grid=r34, mn=_mn, via_tag = [True for _ in range(len(_mn))]))


# # buf WE    --->    RAM WE    X 4
# rWE = []; y = [1, -1, 1, 1]
# for i in range(4):
#     _mn = [r34.mn(buf_we[i].pins['O'])[1]]\
#         + [np.array([r34.mn(buf_we[i].pins['O'])[1][0], r34.mn(buf_we[i].pins['O'])[1][1] + y[i]])]\
#         + [np.array([r34.mn(ram8s[0].pins[f'WE<{i}>'])[1][0], r34.mn(buf_we[i].pins['O'])[1][1] + y[i]])]\
#         + [r34.mn(ram8s[j].pins[f'WE<{i}>'])[1] for j in range(ram8s_num)]
#     rWE.append(dsn.route(grid = r34, mn = _mn, via_tag = [False, True, True] + [False for _ in range(ram8s_num)]))
# # Di, Do    X 32
# # input_buf output  --->  ram8s[2, 3] vacant space use
# rDi = []; rDo = []
# x = [-2, 0, -2, 0, 0, 0, -2, 1,\
#     0, -1, 1, 0, -2, 1, 0, -2,\
#     0, -2, 0, -2, -2, -2, 0, 1,\
#     0, -2, -2, -2, 0, -1, -1, -1]
# y = [-27 + (4*((i%4)//2) - 2) - 2*(i%2) - 14*(i//2) for i in range(32)]
# for i in range(len(x)):  # 32
#     _mn = [r34.mn(buf_in[i].pins['O'])[1]]\
#         + [np.array([r34.mn(buf_in[i].pins['O'])[1][0], r34.mn(buf_in[i].pins['O'])[1][1] - 4])]\
#         + [np.array([r34.mn(buf_in[i].pins['O'])[1][0] + x[i], r34.mn(buf_in[i].pins['O'])[1][1] - 4])]\
#         + [np.array([r34.mn(buf_in[i].pins['O'])[1][0] + x[i], r34.mn(buf_in[i].pins['O'])[1][1] - 4 + y[i]])]\
#         + [np.array([r34.mn(ram8s[-1].pins[f'Di<{i}>'])[1][0], r34.mn(buf_in[i].pins['O'])[1][1] - 4 + y[i]])]
#     rDi.append(dsn.route(grid = r34, mn = _mn, via_tag = [False] + [True for _ in range(len(_mn) - 2)] + [True]))
# # internal Dins / Douts
# for i in range(32):
#     _mn = [r34.mn(ram8s[-1].pins[f'Di<{i}>'])[1], r34.mn(ram8s[0].pins[f'Di<{i}>'])[0]]
#     rDi.append(dsn.route(grid = r34, mn = _mn, via_tag = [False, False]))
#     _mn = [r34.mn(ram8s[-1].pins[f'Do<{i}>'])[1], r34.mn(ram8s[0].pins[f'Do<{i}>'])[0]]
#     rDo.append(dsn.route(grid = r34, mn = _mn, via_tag = [False, False]))
# # ram8s[0, 1] vacant space use --->  output_reg input
# x = [0, -2, 0, 0, 0, 0, 0, -2,\
#     -2, -2, 1, -2, -2, 1, -2,\
#     0, 0, 0, 0, 1, -2, 1 , 0, -2,\
#     2, -2, -2, 0, 0, 0, 0, 0]
# y = [25 - (4*((i%4)//2) - 2) + 2*(i%2) + 14*(i//2) for i in range(32)]
# for i in range(len(x)):
#     _mn = [r34.mn(outreg[i].pins['I'])[1]]\
#         + [r34.mn(outreg[i].pins['I'])[1] + np.array([0, -2])]\
#         + [r34.mn(outreg[i].pins['I'])[1] + np.array([x[i], -2])]\
#         + [r34.mn(outreg[i].pins['I'])[1] + np.array([x[i], y[i]])]\
#         + [np.array([r34.mn(ram8s[0].pins[f'Do<{i}>'])[0][0], r34.mn(outreg[i].pins['I'])[1][1]+ y[i]])]
#     rDo.append(dsn.route(grid= r34, mn = _mn, via_tag = [False] + [True for _ in range(len(_mn) - 2)] + [True]))



# # VSS
# rvss = []; _mn = [r12.mn.bottom_left(buf_clk14), r12.mn.bottom_right(outreg[0])]
# rvss.append(dsn.route(grid=r12, mn=_mn))

# # VDD
# rvdd = []; _mn = [r12.mn.top_left(ram8s[-1]), r12.mn.top_right(ram8s[-1])]
# rvdd.append(dsn.route(grid=r12, mn=_mn))


# # 6. Create pins.
# dA = list()
# for i in range(5):
#     dA.append(dsn.pin(name=f'A<{i}>', grid=r23_cmos, mn=r23_cmos.mn.bbox(buf_a[i].pins['I'])))
# pen = dsn.pin(name='EN', grid=r23_cmos, mn=r23_cmos.mn.bbox(buf_en.pins['I']))
# pwe = list()
# for i in range(4):
#     pwe.append(dsn.pin(name=f'WE<{i}>', grid=r23_cmos, mn=r23_cmos.mn.bbox(buf_we[i].pins['I'])))
# pclk = dsn.pin(name='CLK', grid=r23_cmos, mn=r23_cmos.mn.bbox(buf_clk14.pins['I']))
# pDi = list()
# pDo = list()
# for i in range(32):
#     pDi.append(dsn.pin(name=f'Di<{i}>', grid=r23_cmos, mn=r23_cmos.mn.bbox(buf_in[i].pins['I'])))
#     pDo.append(dsn.pin(name=f'Do<{i}>', grid=r23_cmos, mn=r23_cmos.mn.bbox(outreg[i].pins['O'])))

# pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss[0]))
# pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd[-1]))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')