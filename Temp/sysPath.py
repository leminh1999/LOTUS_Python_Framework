from __future__ import print_function # only when showing how this works

import os, sys
_i = os.path.dirname(os.path.abspath(__file__))
if _i not in sys.path:
    print('inserting {!r} into sys.path'.format(_i))
    sys.path.insert(0, _i)
else:
    print('{!r} is already in sys.path'.format(_i))
del _i # clean up global name space

