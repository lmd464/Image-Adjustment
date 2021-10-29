import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
import qimage2ndarray

from process import *
import process_restore
import fileIO


# UI파일 연결
form_class = uic.loadUiType("gui.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        ##########################

        # 현재 이미지 정보
        self.image_value = QPixmap()

        # Undo / Redo 정보
        self.restore = process_restore.Restore(caller_class=self)

        # 파일 입출력 정보
        self.file_io = fileIO.FileIO(caller_class=self)

        # UI 설정 : 버튼과 동작 연결
        self.init_UI()



    # GUI와 함수 연결
    def init_UI(self):
        # Undo / Redo / Process / Export 비활성화
        self.undo_button.setEnabled(False)
        self.redo_button.setEnabled(False)
        self.process_combo.setEnabled(False)
        self.export_button.setEnabled(False)

        # Import Button 연결
        self.import_button.clicked.connect(self.file_io.file_open)

        # Export Button 연결
        self.export_button.clicked.connect(self.file_io.file_save)

        # Process Combobox 구성 및 연결
        self.process_combo.addItem('None')
        self.process_combo.addItem('Average Filter')
        self.process_combo.addItem('Sharpening Filter')
        self.process_combo.addItem('Bilateral Filter')
        self.process_combo.addItem('Median Filter')
        self.process_combo.addItem('Histogram Equalization')
        '''
        self.process_combo.addItem('HSV Adjustment')
        '''
        self.process_combo.currentIndexChanged.connect(self.process_select)
        self.process_combo.setCurrentText('None')

        # Undo Button 연결
        self.undo_button.clicked.connect(self.restore.undo)

        # Redo Button 연결
        self.redo_button.clicked.connect(self.restore.redo)



    # Process Combo Box의 동작
    def process_select(self):
        # QPixmap -> QImage -> RGB Swap -> Numpy Array
        src = qimage2ndarray.rgb_view(self.image_value.toImage().rgbSwapped())

        # 선택한 프로세스 수행
        if self.process_combo.currentText() == 'Average Filter':
            self.process_combo.setEnabled(False)
            dst = Process.average_filtering(src)
        elif self.process_combo.currentText() == 'Sharpening Filter':
            self.process_combo.setEnabled(False)
            dst = Process.sharpening_filtering(src)
        elif self.process_combo.currentText() == 'Bilateral Filter':
            self.process_combo.setEnabled(False)

            # Bilateral Filter일 경우, 시간이 오래 걸릴 수 있음을 팝업으로 알림
            msg = QMessageBox()
            msg.setWindowTitle("Bilateral Filtering")
            msg.setText("It may take a while to process")
            msg.exec_()

            dst = Process.bilateral_filtering(src)
        elif self.process_combo.currentText() == 'Median Filter':
            self.process_combo.setEnabled(False)
            dst = Process.median_filtering(src)
        elif self.process_combo.currentText() == 'Histogram Equalization':
            self.process_combo.setEnabled(False)
            dst = Process.equalize_hist(src)
            '''
        elif self.process_combo.currentText() == 'HSV Adjustment':
            self.process_combo.setEnabled(False)
            dst = Process.HSV_Adjustment(src)
            '''
        else:
            dst = src

        self.process_combo.setEnabled(True)

        # 수정 전 Pixmap을 Undo Stack에 넣음, redo stack 초기화
        self.restore.undo_stack.append(self.image_value)
        self.restore.redo_stack = []


        # 수행한 결과를 GUI에 반영
        # BGR2RGB 변환 -> numpy 배열을 QImage로 변환 -> QPixmap으로 변환 후 qPixmapVar(image_value)에 재할당 -> GUI에 표시
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        h, w, c = dst.shape
        qImg = QImage(dst.data, w, h, w*c, QImage.Format_RGB888)
        self.image_value = QPixmap.fromImage(qImg)
        self.image_area.setPixmap(self.image_value)

        self.restore.undo_redo_validation()



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()