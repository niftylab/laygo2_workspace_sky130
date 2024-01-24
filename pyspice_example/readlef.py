import parselef
import yaml
from parselef import lef_parser
lef_osu = lef_parser.LefParser("./sky130_osu_sc_t12/12T_hs/lef/sky130_osu_sc_12T_hs.lef")
lef_osu.parse()
# print(lef_osu.layer_dict.items())
# print(lef_osu.via_dict.items())
libname = 'sky130_osu_sc_12T_hs'
macro = lef_osu.macro_dict['sky130_osu_sc_12T_hs__dff_1']
print(macro.name.replace(libname+'__', ''))
print(type(macro.info['ORIGIN']))
print(macro.info['SIZE'])
for pin in macro.info['PIN']:
    print("Pin:", pin.name)
    print("Property:",pin.info['USE'], pin.info['DIRECTION'])
    port = pin.info['PORT']
    print('   port: ')
    for layer in port.info['LAYER']:
        print("   ",layer.name)
        for shape in layer.shapes:
            print("      ",shape.points[0][0], shape.points[0][1],shape.points[1][0],shape.points[1][1])


#lef_osu.draw_cells('sky130_osu_sc_12T_hs__inv_1','sky130_osu_sc_12T_hs__nand2_1')