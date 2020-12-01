#!/usr/bin/env python

import wx
import wx.adv
from wx.lib.wordwrap import wordwrap
from mpl_demo import demo

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show some MathPlotLib Demos within wx", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        # First we create and fill the info object
        demo()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx Embedding MatPlotLib</center></h2>

This function shows some of the features of MatPlotLib running
within the wx framework.

It is almost 100% lifted from the <A href="https://matplotlib.org/gallery/index.html">examples</A>
with the MatPlotLib documentation site.

You will need MatPlotLib installed on your system.
</body></html>
"""


licenseText = "blah " * 250 + "\n\n" +"yadda " * 100


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

