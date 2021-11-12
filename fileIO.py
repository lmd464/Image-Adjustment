from PyQt5.QtWidgets import QFileDialog, QMessageBox

class FileIO:

    def __init__(self, caller_class):
        # 원본 이미지 경로
        self.filepath = ""

        # Window Class
        self.window_class = caller_class


    # Import Button의 동작
    # 파일을 탐색기로 열어서 이미지 표시, 창 크기 조절
    def file_open(self):

        # 탐색기 열어, 파일 경로 가져옴 : 이미지 파일만
        filter = "Images (*.bmp *.gif *.jpg *.jpeg *.png)"
        self.filepath = QFileDialog.getOpenFileName(self.window_class, 'Open File', filter=filter)[0]
        print(self.filepath)

        # Label에 표시할 이미지 불러옴
        self.window_class.image_value.load(self.filepath)

        # import 후처리
        self.__import_postprocess()


    # Export Button의 동작
    # 이미지 원본과 같은 폴더에 _modified 붙여 저장
    def file_save(self):
        save_file_name = self.filepath.split(".")[-2] + "_modified"
        save_file_type = self.filepath.split(".")[-1]
        save_file_path = save_file_name + "." + save_file_type
        print(save_file_path)
        save_var = self.window_class.image_area.pixmap()
        save_var.save(save_file_path)

        # 저장 완료 메시지 팝업
        msg = QMessageBox()
        msg.setWindowTitle("Save Complete!")
        msg.setText(save_file_path)
        msg.exec_()


    # Import 직후, 창 / 버튼 / Stack 관련 후처리
    def __import_postprocess(self):

        # 이미지 크기에 맞춰, 전체 창 너비 / 높이 조절
        # image width + 40 / image height + 140
        # 버튼의 총 크기보다 창 크기가 작을 경우, 버튼 크기를 우선으로 함 (총 370 + padding 80 = 450)
        image_width, image_height = self.window_class.image_value.width(), self.window_class.image_value.height()
        self.window_class.resize(max(image_width + 40, 450), image_height + 140)

        # 변화된 창 크기에 맞춰 버튼들 재배치
        self.window_class.import_button.move(20, 20)
        self.window_class.export_button.move(130, 20)
        self.window_class.undo_button.move(20, self.window_class.height() - 50)
        self.window_class.redo_button.move(130, self.window_class.height() - 50)
        self.window_class.process_combo.move(self.window_class.width() - 210, self.window_class.height() - 50)

        # 이미지 크기만큼 Label 크기 조절 후 이미지 표시
        self.window_class.image_area.resize(image_width, image_height)
        self.window_class.image_area.setPixmap(self.window_class.image_value)

        # Process 콤보상자 / Export 버튼 활성화
        self.window_class.process_combo.setEnabled(True)
        self.window_class.export_button.setEnabled(True)

        # Undo / Redo Stack 초기화
        self.window_class.restore.import_stack_management()
        self.window_class.restore.undo_redo_validation()

        # image 픽셀 수가 1200 * 800 이상일 경우, 시간이 오래 걸릴 수 있음을 팝업으로 알림
        if image_height * image_width >= 1200 * 800:
            msg = QMessageBox()
            msg.setWindowTitle("Image size is Big")
            msg.setText("It may take a while to process")
            msg.exec_()



