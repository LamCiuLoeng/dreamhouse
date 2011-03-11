# -*- coding: utf-8 -*-
import traceback
from sys2do.module import *


#===============================================================================
# init the DB
#===============================================================================

def setup_db():
    try:
        metadata.create_all(engine)
    except:
        traceback.print_exc()


if __name__ == "__main__":
    setup_db()
    print "OK"