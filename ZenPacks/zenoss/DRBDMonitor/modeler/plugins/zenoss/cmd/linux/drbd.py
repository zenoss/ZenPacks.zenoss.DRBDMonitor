##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """
Read DRBD block devices
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class drbd(CommandPlugin):
    """
    Read drbd block devices
    """
    command   =  """gawk '/^ *resource / { res=$2 }
                             /^ *device/ { dev=gensub(";+$", "", "g", $2);
                                           if (res)
                                               devs[dev]=res;
                                         }
                                         { for (dev in devs) {
                                               if ($1 == dev) {
                                                   printf("%s,%s,%s\\n", dev, devs[dev], $2);
                                                   mounts[dev]=0;
                                               }
                                           }
                                         }
                                     END { for (dev in devs)
                                               if (!(dev in mounts))
                                                   printf("%s,%s,\\n", dev, devs[dev]);
                                         }' /etc/drbd.conf /proc/mounts"""
    compname  = "hw"
    relname   = "harddisks"
    modname   = "ZenPacks.zenoss.DRBDMonitor.DRBDHardDisk"
    #drbdregex = re.compile("^ *([0-9]+):([^ \t]+)\s+(\w+)\s+(\w+)/(\w+)\s+(\w+)/(\w+)")

#    deviceProperties = \
#                CommandPlugin.deviceProperties + ('zDRBDConfPath',)

    def process(self, device, results, log):
        log.info('Collecting DRBD hard disks for device %s' % device.id)
        rm = self.relMap()

        for disk in results.strip().split("\n"):
            try:
                id, desc, mount = disk.strip().split(",")
                if id.startswith("/dev/"): id = id[5:]
                number = int(re.findall("([0-9]+)$", id)[0])

                om = self.objectMap()
                om.id = self.prepId(id)
                om.description = desc
                om.mount = mount
                om.number = number
                rm.append(om)
            except ValueError:
                continue

        return rm
