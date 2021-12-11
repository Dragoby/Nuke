try:
    # Doing an from import * is getting an error here due to QtCharts,  Explicitly importing modules instead.  Updating
    # The list as needed
    from PySide2 import QtGui, QtCore, QtWidgets
except ImportError:
    from PySide import QtCore
    from PySide import *

del globals()['QtGui']
del globals()['QtWidgets']
del globals()['QtCore']

from . import QtGui
from . import QtCore
