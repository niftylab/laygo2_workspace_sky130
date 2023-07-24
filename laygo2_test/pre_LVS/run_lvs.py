#lvs 구동하는 파일

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
import netmap_template as nMap

f = open("abs_gds.txt", "rt")

while true:
    line = f.readline()
    if line=='':
        break
    if line[0] == '#':
        continue
    