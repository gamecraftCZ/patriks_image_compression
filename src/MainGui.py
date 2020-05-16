import wx


class MyFileDropTarget(wx.FileDropTarget):
    onDrop = None

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def BindOnDrop(self, handler):
        self.onDrop = handler

    def OnDropFiles(self, x, y, filenames):
        if self.onDrop:
            self.onDrop(filenames[0])
        return True


class Title(wx.StaticText):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetFont(titleFont)


class MainGui(wx.Frame):
    selectedFileToCompress: str = None
    selectedBlobToDecompress: str = None
    selectedPcfToDecompress: str = None

    def __init__(self, ):
        super().__init__(parent=None, title="PIC - Patrikovo komprese obrázků", size=(400, 620))
        self._setup_gui()
        self.Show()

    def _setup_gui(self):
        self.panel = wx.Panel(self, size=(400, 600))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.__setupCompressMenu()
        self.sizer.Add(wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL, size=(5000, 2)), 0, wx.ALL, 5)
        self.__setupDecompressMenu()

    def __setupCompressMenu(self):
        text = Title(self.panel, label="Komprimovat")
        self.sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        #######################################################
        self.compress_drop = wx.StaticText(self.panel, -1, "Přetáhni soubor ke kopresi nebo vyber kliknutím",
                                           size=(5000, 200),
                                           style=wx.ST_NO_AUTORESIZE | wx.BORDER_SIMPLE)
        self.compress_drop.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
        self.compress_drop.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        dropTarget = MyFileDropTarget(self.panel)
        self.compress_drop.SetDropTarget(dropTarget)
        dropTarget.BindOnDrop(self.selectFileToCompress)

        self.compress_drop.Bind(wx.EVT_LEFT_DOWN, self.selectFileToCompress)

        self.sizer.Add(self.compress_drop, 0, wx.ALL, 5)
        #######################################################
        self.compressButton = wx.Button(self.panel, label="Začít")
        self.compressButton.Disable()
        self.sizer.Add(self.compressButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)

    def __setupDecompressMenu(self):
        text = Title(self.panel, label="Dekomprimovat")
        self.sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        #######################################################
        dropPanel = wx.Panel(self.panel)
        dropSizer = wx.BoxSizer(wx.HORIZONTAL)
        dropPanel.SetSizer(dropSizer)
        self.sizer.Add(dropPanel, 0, wx.ALL | wx.EXPAND, 5)
        #######################################################
        self.decompress_drop_blob = wx.StaticText(dropPanel, -1,
                                                  "Přetáhni soubor .blob k dekompresi nebo vyber kliknutím",
                                                  size=(180, 200),
                                                  style=wx.ST_NO_AUTORESIZE | wx.BORDER_SIMPLE)
        self.decompress_drop_blob.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
        self.decompress_drop_blob.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        BlobDropTarget = MyFileDropTarget(dropPanel)
        self.decompress_drop_blob.SetDropTarget(BlobDropTarget)
        BlobDropTarget.BindOnDrop(self.selectBlobToDecompress)

        self.decompress_drop_blob.Bind(wx.EVT_LEFT_DOWN, self.selectBlobToDecompress)

        dropSizer.Add(self.decompress_drop_blob, 0, wx.ALL, 5)
        #######################################################
        self.decompress_drop_pcf = wx.StaticText(dropPanel, -1,
                                                 "Přetáhni soubor .pcf k dekompresi nebo vyber kliknutím",
                                                 size=(180, 200),
                                                 style=wx.ST_NO_AUTORESIZE | wx.BORDER_SIMPLE)
        self.decompress_drop_pcf.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
        self.decompress_drop_pcf.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        pcfDropTarget = MyFileDropTarget(dropPanel)
        self.decompress_drop_pcf.SetDropTarget(pcfDropTarget)
        pcfDropTarget.BindOnDrop(self.selectPcfToDecompress)

        self.decompress_drop_pcf.Bind(wx.EVT_LEFT_DOWN, self.selectPcfToDecompress)

        dropSizer.Add(self.decompress_drop_pcf, 0, wx.ALL, 5)
        #######################################################
        self.decompressButton = wx.Button(self.panel, label="Začít")
        self.decompressButton.Disable()
        self.sizer.Add(self.decompressButton, 0, wx.ALL | wx.ALIGN_CENTER, 5)

    def selectFileToCompress(self, filepath: str = None):
        if not filepath or type(filepath) != str:
            dlg = wx.FileDialog(self, message="Zvol obrázek ke kompresi")
            if dlg.ShowModal() == wx.ID_OK:
                filepath = dlg.GetPath()
            else:
                return

        self.selectedFileToCompress = filepath
        self.compress_drop.SetLabelText('Zvolil jsi soubor: {}'.format(filepath.split("\\")[-1]))
        self.compressButton.Enable()

    def selectBlobToDecompress(self, filepath: str = None):
        if not filepath or type(filepath) != str:
            dlg = wx.FileDialog(self, message="Zvol .blob část obrázku k dekompresi")
            if dlg.ShowModal() == wx.ID_OK:
                filepath = dlg.GetPath()
            else:
                return

        self.selectedBlobToDecompress = filepath
        self.decompress_drop_blob.SetLabelText('Zvolil jsi blob soubor: {}'.format(filepath.split("\\")[-1]))
        if self.selectedFileToCompress:
            self.decompressButton.Enable()

    def selectPcfToDecompress(self, filepath: str = None):
        if not filepath or type(filepath) != str:
            dlg = wx.FileDialog(self, message="Zvol .pcf část obrázku k dekompresi")
            if dlg.ShowModal() == wx.ID_OK:
                filepath = dlg.GetPath()
            else:
                return

        self.selectedPcfToDecompress = filepath
        self.decompress_drop_pcf.SetLabelText('Zvolil jsi blob soubor: {}'.format(filepath.split("\\")[-1]))
        if self.selectedBlobToDecompress:
            self.decompressButton.Enable()
