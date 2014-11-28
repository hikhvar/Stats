import wx
from controller import Controller
from view import MainFrame
import gettext

def main():
    gettext.install("schiessdb") # replace with the appropriate catalog name
    app = wx.App()
    frame = MainFrame(Controller(), None, wx.ID_ANY, "")
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()