import pyautogui
import mouse
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import pytube
import webbrowser


class QRCodeCapture:
    def __init__(self):
        self.played = {}

    def getPoint(self):
        while True:
            if mouse.is_pressed(button='left'):
                x, y = pyautogui.position()
                return (x, y)


    def getCapturePoint(self, center):
        range = 120
        center_x, center_y = center
        LTx = center_x - range // 2
        LTy = center_y - range // 2
        return (LTx, LTy, range, range)


    def capture(self,):
        img = pyautogui.screenshot(region=self.getCapturePoint(self.getPoint()))
        img = cv2.cvtColor(np.array(img), cv2.IMREAD_GRAYSCALE)
        return img


    def download_mp3(self,link):
        yt = pytube.YouTube(link)
        filename = yt.title.replace('"', '').replace("?", "").replace(" ", "_") + ".mp3"
        yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first().download(
            filename=filename)
        return filename

    def run(self):
        while True:
            try:
                img = self.capture()
                value = decode(img)
                url = value[0].data.decode('utf-8')
                print('GOt URL from QR code :', url)
                if not url in self.played:
                    filename = self.download_mp3(url)
                    self.played[url] = filename
                    print('Downloaded file from : ', url)
                else:
                    filename = self.played[url]

                webbrowser.open(filename)
                print('Playing file : ', filename)

            except Exception as e:
                print(e)

if __name__ == '__main__':
    qrcode = QRCodeCapture()
    qrcode.run()
