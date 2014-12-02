import wx
from controller import Controller
from view import MainFrame
import gettext
import os.path

def main():
    gettext.install("schiessdb") # replace with the appropriate catalog name
    app = wx.App()
    frame = MainFrame(Controller(), None, wx.ID_ANY, "")
    _icon = wx.EmptyIcon()
    iconpath = os.path.join(os.path.dirname(__file__), "resources/logo.bmp")
    _icon.CopyFromBitmap(wx.Bitmap(iconpath, wx.BITMAP_TYPE_ANY))
    frame.SetIcon(_icon)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()