import wx
from controller import Controller
from view import MainFrame
import gettext
import os.path
import argparse
import sys
import os
import imp
from settings import DefaultSettings
import model.modeltest as mt

def parse_args():
    parser = argparse.ArgumentParser(
        description='Small desktop application to store and view results for Luftgewehr shooting.')
    parser.add_argument('--perftest', dest='perftest', action='store_true',
                   default=False,
                   help='Populate the model with performance data.')

    return parser.parse_args()

def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
    if "linux" in sys.platform or "darwin" in sys.platform:
        return os.path.dirname(__file__)
    print sys.executable, sys.argv
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])


def main():
    args = parse_args()
    gettext.install("schiessdb") # replace with the appropriate catalog name
    app = wx.App()
    if args.perftest:
        settings = DefaultSettings()
        settings.store_dir = "perfdata"
        model = settings.model(settings)
        model.load()
        t = mt.populate_model(model)
        print "Took ", t, " seconds to perform population test."
    else:
        model = None
    frame = MainFrame(Controller(model=model), None, wx.ID_ANY, "")
    _icon = wx.EmptyIcon()
    iconpath = os.path.join(get_main_dir(), "resources/logo.bmp")
    _icon.CopyFromBitmap(wx.Bitmap(iconpath, wx.BITMAP_TYPE_ANY))
    frame.SetIcon(_icon)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()