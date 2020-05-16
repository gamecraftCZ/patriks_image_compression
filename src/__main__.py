import wx

from MainGui import MainGui


def main():
    app = wx.App()
    gui = MainGui()
    app.MainLoop()


if __name__ == '__main__':
    main()
