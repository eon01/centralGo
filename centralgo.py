#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Aymen El Amri(eon01)"
__copyright__ = "Copyright 2014"
__credits__ = ["Aymen El Amri"]
__license__ = "GNU GENERAL PUBLIC LICENSE Version 2"
__version__ = "1.0.1"
__maintainer__ = "Aymen El Amri"
__email__ = "amri.aymen@gmail.com"
__status__ = "Beta"

import sys, time
from core.centralgo import CentralGo
from centralgod import CentralGod

class MyCentralGod(CentralGod):
    def run(self):
        while True:       
            c = CentralGo()
            c.main()
            time.sleep(1)


if __name__ == "__main__":
    daemon = MyCentralGod('/tmp/CGo.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
