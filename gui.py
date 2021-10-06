import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
import qimage2ndarray

from basic_filtering import *

# UI파일 연결
form_class = uic.loadUiType("gui.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        ##########################
        self.init_UI()

        # 원본 이미지 경로
        self.filepath = ""

        # 현재 이미지 정보
        self.qPixmapVar = QPixmap()

        # Undo / Redo Stack
        self.undo_stack = []
        self.redo_stack = []



    # GUI와 함수 연결
    def init_UI(self):
        # Undo / Redo / Process / Export 비활성화
        self.undo_button.setEnabled(False)
        self.redo_button.setEnabled(False)
        self.process_combo.setEnabled(False)
        self.export_button.setEnabled(False)

        # Import Button 연결
        self.import_button.clicked.connect(self.file_open)

        # Export Button 연결
        self.export_button.clicked.connect(self.file_save)

        # Process Combobox 구성 및 연결
        self.process_combo.addItem('None')
        self.process_combo.addItem('Average Filter')
        self.process_combo.addItem('Sharpening Filter')
        self.process_combo.addItem('Bilateral Filter')
        self.process_combo.addItem('Median Filter')
        self.process_combo.addItem('Histogram Equalization')
        self.process_combo.currentIndexChanged.connect(self.process_select)
        self.process_combo.setCurrentText('None')

        # Undo Button 연결
        self.undo_button.clicked.connect(self.undo)

        # Redo Button 연결
        self.redo_button.clicked.connect(self.redo)



    # Import Button의 동작
    # 파일을 탐색기로 열어서 이미지 표시, 창 크기 조절
    def file_open(self):

        # 탐색기 열어, 파일 경로 가져옴 : 이미지 파일만
        filter = "Images (*.bmp *.gif *.jpg *.jpeg *.png)"
        self.filepath = QFileDialog.getOpenFileName(self, 'Open File', filter=filter)[0]
        print(self.filepath)

        # Label에 표시할 이미지 불러옴
        self.qPixmapVar.load(self.filepath)

        # 이미지 크기에 맞춰, 전체 창 너비 / 높이 조절
        # image width + 40 / image height + 140
        # 버튼의 총 크기보다 창 크기가 작을 경우, 버튼 크기를 우선으로 함 (총 370 + padding 80 = 450)
        image_width, image_height = self.qPixmapVar.width(), self.qPixmapVar.height()
        self.resize(max(image_width + 40, 450), image_height + 140)


        # 변화된 창 크기에 맞춰 버튼들 재배치
        self.import_button.move(20, 20)
        self.export_button.move(130, 20)
        self.undo_button.move(20, self.height()-50)
        self.redo_button.move(130, self.height()-50)
        self.process_combo.move(self.width()-210, self.height()-50)

        # 이미지 크기만큼 Label 크기 조절 후 이미지 표시
        self.image_area.resize(image_width, image_height)
        self.image_area.setPixmap(self.qPixmapVar)

        # Process 콤보상자 / Export 버튼 활성화
        self.process_combo.setEnabled(True)
        self.export_button.setEnabled(True)

        # Undo / Redo Stack 초기화
        self.undo_stack = []
        self.redo_stack = []


    # Export Button의 동작 : 이미지 원본과 같은 폴더에 _modified 붙여 저장
    def file_save(self):
        save_file_name = self.filepath.split(".")[-2] + "_modified"
        save_file_type = self.filepath.split(".")[-1]
        save_file_path = save_file_name + "." + save_file_type
        print(save_file_path)
        save_var = self.image_area.pixmap()
        save_var.save(save_file_path)

        # 저장 완료 메시지 팝업
        msg = QMessageBox()
        msg.setWindowTitle("Save Complete!")
        msg.setText(save_file_path)
        msg.exec_()



    # Process Combo Box의 동작
    def process_select(self):
        # QPixmap -> QImage -> RGB Swap -> Numpy Array
        src = qimage2ndarray.rgb_view(self.qPixmapVar.toImage().rgbSwapped())

        # 선택한 프로세스 수행
        if self.process_combo.currentText() == 'Average Filter':
            dst = average_filtering(src)
        elif self.process_combo.currentText() == 'Sharpening Filter':
            dst = sharpening_filtering(src)
        elif self.process_combo.currentText() == 'Bilateral Filter':
            dst = bilateral_filtering(src)
        elif self.process_combo.currentText() == 'Median Filter':
            dst = median_filtering(src)
        elif self.process_combo.currentText() == 'Histogram Equalization':
            dst = equalize_hist(src)

        # 수정 전 Pixmap을 Undo Stack에 넣음
        self.undo_stack.append(self.qPixmapVar)


        # 수행한 결과를 GUI에 반영
        # BGR2RGB 변환 -> numpy 배열을 QImage로 변환 -> QPixmap으로 변환 후 qPixmapVar에 재할당 -> GUI에 표시
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        h, w, c = dst.shape
        qImg = QImage(dst.data, w, h, w*c, QImage.Format_RGB888)
        self.qPixmapVar = QPixmap.fromImage(qImg)
        self.image_area.setPixmap(self.qPixmapVar)

        self.undo_redo_validation()


    # Undo Button의 동작
    # 현재 상태를 redo stack에 push 후, undo stack에서 pop하여 현재 상태로 만듦
    def undo(self):
        self.redo_stack.append(self.qPixmapVar)
        self.qPixmapVar = self.undo_stack.pop()
        self.image_area.setPixmap(self.qPixmapVar)
        self.undo_redo_validation()


    # Redo Button의 동작
    def redo(self):
        self.undo_stack.append(self.qPixmapVar)
        self.qPixmapVar = self.redo_stack.pop()
        self.image_area.setPixmap(self.qPixmapVar)
        self.undo_redo_validation()


    # Undo / Redo Button 활성화 여부 결정
    def undo_redo_validation(self):
        if len(self.undo_stack) >= 1:
            self.undo_button.setEnabled(True)
        else:
            self.undo_button.setEnabled(False)

        if len(self.redo_stack) >= 1:
            self.redo_button.setEnabled(True)
        else:
            self.redo_button.setEnabled(False)


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()