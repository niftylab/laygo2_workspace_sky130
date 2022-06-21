import laygo2.object.database
import laygo2.object.grid

import numpy as np
import yaml
import pprint

# Grid library for target technology.

# Technology parameters
tech_fname = './laygo2_tech/laygo2_tech.yaml'
with open(tech_fname, 'r') as stream:
    try:
        tech_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


# Grid library
def load_grids(templates, libname=None):
    """
    Load grids to a grid library object.

    Parameters
    ----------
    templates: laygo2.object.database.TemplateLibrary
        The template library object that contains via templates.
    """
    if libname is None:
        ln = list(tech_params['grids'].keys())[0]
    else:
        ln = libname
    glib = laygo2.object.database.GridLibrary(name=ln)
    for gn, gdict in tech_params['grids'][ln].items():
        gv = laygo2.object.grid.OneDimGrid(name=gn + '_v', scope=gdict['vertical']['scope'],
                                           elements=gdict['vertical']['elements'])
        gh = laygo2.object.grid.OneDimGrid(name=gn + '_h', scope=gdict['horizontal']['scope'],
                                           elements=gdict['horizontal']['elements'])
        if gdict['type'] == 'placement':  # placement grid
            g = laygo2.object.grid.PlacementGrid(name=gn, vgrid=gv, hgrid=gh)
            glib.append(g)
        elif gdict['type'] == 'routing':  # routing grid
            vwidth = laygo2.object.grid.CircularMapping(elements=gdict['vertical']['width'])
            hwidth = laygo2.object.grid.CircularMapping(elements=gdict['horizontal']['width'])
            vextension = laygo2.object.grid.CircularMapping(elements=gdict['vertical']['extension'])
            hextension = laygo2.object.grid.CircularMapping(elements=gdict['horizontal']['extension'])
            vextension0 = laygo2.object.grid.CircularMapping(elements=gdict['vertical']['extension0'])
            hextension0 = laygo2.object.grid.CircularMapping(elements=gdict['horizontal']['extension0'])
            vlayer = laygo2.object.grid.CircularMapping(elements=gdict['vertical']['layer'], dtype=object)
            hlayer = laygo2.object.grid.CircularMapping(elements=gdict['horizontal']['layer'], dtype=object)
            pin_vlayer = laygo2.object.grid.CircularMapping(elements=gdict['vertical']['pin_layer'], dtype=object)
            pin_hlayer = laygo2.object.grid.CircularMapping(elements=gdict['horizontal']['pin_layer'], dtype=object)
            xcolor = laygo2.object.grid.CircularMapping(elements=gdict['vertical']['xcolor'], dtype=object)
            ycolor = laygo2.object.grid.CircularMapping(elements=gdict['horizontal']['ycolor'], dtype=object)
            primary_grid = gdict['primary_grid']
            # Create the via map defined by the yaml file.
            vmap_original = gdict['via']['map']  # viamap defined in the yaml file.
            vmap_mapped = list()  # map template objects to the via map.
            for vmap_org_row in vmap_original:
                vmap_mapped_row = []
                for vmap_org_elem in vmap_org_row:
                    vmap_mapped_row.append(templates[vmap_org_elem])
                vmap_mapped.append(vmap_mapped_row)
            viamap = laygo2.object.grid.CircularMappingArray(elements=vmap_mapped, dtype=object)
            g = laygo2.object.grid.RoutingGrid(name=gn, vgrid=gv, hgrid=gh,
                                               vwidth=vwidth, hwidth=hwidth,
                                               vextension=vextension, hextension=hextension,
                                               vlayer=vlayer, hlayer=hlayer,
                                               pin_vlayer=pin_vlayer, pin_hlayer=pin_hlayer,
                                               viamap=viamap, primary_grid=primary_grid,
                                               xcolor=xcolor, ycolor=ycolor,
                                               vextension0=vextension0, hextension0=hextension0)
            glib.append(g)
    return glib


# Tests
if __name__ == '__main__':
    # Create grids.
    print("Load templates")
    import laygo2_tech_templates
    templates = laygo2_tech_templates.load_templates()
    print("Create grids")
    grids = load_grids(templates=templates)
    for gn, g in grids.items():
        print(g)
