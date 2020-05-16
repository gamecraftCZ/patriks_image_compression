import traceback
from threading import Thread

import wx

from compress import runCompressionRound, saveBlobsInformation, saveJustBlobs
from decompress import loadBlobsInformation, loadBlobsPixels
from image_manipulation import show_image_from_numpy_array, save_image_from_numpy_array
from structure.Blobs import Blobs
from structure.Image import Image
from structure.Vector import Vector2


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
        self.compressButton.Bind(wx.EVT_LEFT_DOWN, self.startCompress)
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
        self.decompressButton.Bind(wx.EVT_LEFT_UP, self.startDecompress)
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
            dlg = wx.FileDialog(self, message="Zvol .blob část obrázku k dekompresi",
                                wildcard="Blob files (*.blob)|*.blob", )
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
            dlg = wx.FileDialog(self, message="Zvol .pcf část obrázku k dekompresi",
                                wildcard="Patriks Compressed Files (*.pcf)|*.pcf")
            if dlg.ShowModal() == wx.ID_OK:
                filepath = dlg.GetPath()
            else:
                return

        self.selectedPcfToDecompress = filepath
        self.decompress_drop_pcf.SetLabelText('Zvolil jsi blob soubor: {}'.format(filepath.split("\\")[-1]))
        if self.selectedBlobToDecompress:
            self.decompressButton.Enable()

    def startCompress(self, event=None):
        try:
            image: Image = Image.fromFile(self.selectedFileToCompress, Vector2(8, 8))
            print(f"blobs size: {image.blobs.size}")
            print(f"blobs count: {image.blobs.getBlobsCount()}")
            if image.blobs.getBlobsCount() > 1024:
                dlg = wx.MessageBox(f"Obrázek je velký, komprese zabere dlouho (cca {image.blobs.getBlobsCount() // 750} minut). Chceš pokračovat?", "Varování",
                                    wx.ICON_WARNING | wx.YES_NO)
                if dlg != wx.YES:
                    return
            print("Starting compression")

            image.showFromBlobs("Tohle budu komprimovat")
            allBlobs = image.getFlattenedBlobsArray()

            dlg = wx.ProgressDialog("Komprimuji", f'',
                                    maximum=len(allBlobs),
                                    parent=self,
                                    style=wx.PD_APP_MODAL | wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME | wx.PD_CAN_ABORT)

            progressObject = {"count": 0, "max": len(allBlobs), "cancel": False}
            Thread(target=runCompressionRound, args=(allBlobs, progressObject)).start()

            while progressObject["count"] < progressObject["max"]:
                wx.MilliSleep(100)
                wx.Yield()
                if dlg.WasCancelled():
                    print("Cancelled")
                    progressObject["cancel"] = True
                    wx.MessageBox("Komprese byla přerušena uživatelem.", "Zrušeno", wx.ICON_INFORMATION)
                    dlg.Update(progressObject["max"])
                    dlg.Destroy()
                    return

                dlg.Update(progressObject["count"])

            print("Compression done")
            dlg.Destroy()
            image.showFromBlobs("Zkomprimovaný obrázek")

            blobSaveDlg = wx.FileDialog(None, "Kam chceš uložit část obrázku .blob ?",
                                        wildcard="Blob files (*.blob)|*.blob",
                                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if blobSaveDlg.ShowModal() != wx.ID_OK:
                wx.MessageBox("Zrušeno uživatelem.", "Zrušeno", wx.ICON_INFORMATION)

            pcfSaveDlg = wx.FileDialog(None, "Kam chceš uložit část obrázku .pcf ?",
                                       wildcard="Patriks Compressed Files (*.pcf)|*.pcf",
                                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if pcfSaveDlg.ShowModal() != wx.ID_OK:
                wx.MessageBox("Zrušeno uživatelem.", "Zrušeno", wx.ICON_INFORMATION)

            saveBlobsInformation(image.blobs, blobSaveDlg.GetPath())
            saveJustBlobs(allBlobs, pcfSaveDlg.GetPath())

            wx.MessageBox("Uloženo.", "Úspěch", wx.ICON_INFORMATION)

        except Exception as e:
            print("Compression error: ", e)
            traceback.print_exc()
            wx.MessageBox("Nepodařilo se zkomprimovat obrázek! Zkuste jiný.", "Chyba", wx.ICON_ERROR)

    def startDecompress(self, event=None):
        try:
            blobs: Blobs = loadBlobsInformation(self.selectedBlobToDecompress)
            loadBlobsPixels(blobs, self.selectedPcfToDecompress)

            imageArray = blobs.toPixels()

            # dlg = wx.ProgressDialog("Komprimuji", f'',
            #                         maximum=len(allBlobs),
            #                         parent=self,
            #                         style=wx.PD_APP_MODAL | wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME | wx.PD_CAN_ABORT)
            #
            # progressObject = {"count": 0, "max": len(allBlobs), "cancel": False}
            # Thread(target=runCompressionRound, args=(allBlobs, progressObject)).start()
            #
            # while progressObject["count"] < progressObject["max"]:
            #     wx.MilliSleep(100)
            #     wx.Yield()
            #     if dlg.WasCancelled():
            #         print("Cancelled")
            #         progressObject["cancel"] = True
            #         wx.MessageBox("Komprese byla přerušena uživatelem.", "Zrušeno", wx.ICON_INFORMATION)
            #         dlg.Update(progressObject["max"])
            #         dlg.Destroy()
            #         return
            #
            #     dlg.Update(progressObject["count"])

            print("Decompression done")
            # dlg.Destroy()
            show_image_from_numpy_array(imageArray, "Dekomprimovaný obrázek")

            saveDlg = wx.FileDialog(None, "Kam chceš uložit dekomprimovaný obrázek?",
                                    wildcard="Patriks Compressed Files (*.jpg)|*.jpg",
                                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if saveDlg.ShowModal() != wx.ID_OK:
                wx.MessageBox("Zrušeno uživatelem.", "Zrušeno", wx.ICON_INFORMATION)
                return

            save_image_from_numpy_array(saveDlg.GetPath(), imageArray)

            wx.MessageBox("Uloženo.", "Úspěch", wx.ICON_INFORMATION)

        except Exception as e:
            print("Compression error: ", e)
            traceback.print_exc()
            wx.MessageBox("Nepodařilo se zkomprimovat obrázek! Zkuste jiný.", "Chyba", wx.ICON_ERROR)
