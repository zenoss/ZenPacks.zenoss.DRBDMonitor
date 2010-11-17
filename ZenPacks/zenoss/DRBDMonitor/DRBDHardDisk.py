from copy import deepcopy
from Products.ZenModel.HardDisk import HardDisk

def manage_addDBRDHardDisk(context, id, title = None, REQUEST = None):
    """make a DRBD Hard Disk"""
    hd = DRBDHardDisk(id, title)
    context._setObject(id, hd)
    hd = context._getOb(id)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main') 

class DRBDHardDisk(HardDisk):
    portal_type = meta_type = 'DRBDHardDisk'

    mount = ""
    number = 0

    _properties = HardDisk._properties + (
                 {'id':'mount',  'type':'string', 'mode':'w'},
                 {'id':'number', 'type':'int',    'mode':'w'},
                )
    
    factory_type_information = deepcopy(HardDisk.factory_type_information)
    factory_type_information[0]['id']                   = 'DRBDHardDisk'
    factory_type_information[0]['meta_type']            = 'DRBDHardDisk'
    factory_type_information[0]['description']          = 'DRBD Hard Disk'
    factory_type_information[0]['factory']              = 'manage_addDRBDHardDisk'
    factory_type_information[0]['immediate_view']       = 'viewDRBDHardDisk'
    factory_type_information[0]['actions'][0]['action'] = 'viewDRBDHardDisk'