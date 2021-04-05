import wx
import cv2
import os
from datetime import datetime

capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
width, height = (640, 360)
tag = ''


class Imagenes(wx.Frame):

    def __init__(self, parent, title):
        super(Imagenes, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(3, 3)
        self.now = datetime.now()
        self.takeButton = wx.Button(self.panel, size=(60, 60), label="Take!")
        self.panelDeImagen = wx.Panel(self.panel, -1, size=(640, 360))
        self.capture = webcamPanel(self.panelDeImagen, capture)

        self.sizer.Add(self.takeButton, pos=(3, 1), span=(0, 0), flag=wx.BOTTOM | wx.TOP | wx.LEFT | wx.RIGHT, border=15)
        self.sizer.Add(self.panelDeImagen, pos=(0, 0), span=(2, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=15)
        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.take_picture, self.takeButton)

    def take_picture(self, e):
        global height
        global width
        global tag

        self.camera = capture
        self.camera.set(3, width)
        self.camera.set(4, height)

        return_value, image = self.camera.read()

        self.tag = str(self.now.hour) +\
          "_" + str(self.now.minute) + "_" + str(self.now.second) +\
          "_" + str(self.now.day) + "_" + str(self.now.month) + "_" + str(self.now.year) + ".png"

        cv2.imwrite(self.tag, image)


class webcamPanel(wx.Panel):

    def __init__(self, parent, capture, fps=30):
        wx.Panel.__init__(self, parent)
        self.camera = capture
        capture.set(3, 640)
        capture.set(4, 360)
        return_value, frame = self.camera.read()
        height, width = frame.shape[:2]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.SetSize((width, height))
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        self.timer = wx.Timer(self)
        self.timer.Start(int(1000 / fps))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, e):
        return_value, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh(eraseBackground=False)

if __name__ == "__main__":
    app = wx.App()
    Imagenes(None, title='Imagenes').Show()
    app.MainLoop()