class Restore:

    def __init__(self, caller_class):
        # Undo / Redo Stack
        self.undo_stack = []
        self.redo_stack = []

        # Window Class
        self.window_class = caller_class


    # Undo Button의 동작
    # 현재 상태를 redo stack에 push 후, undo stack에서 pop하여 현재 상태로 만듦
    def undo(self):
        self.redo_stack.append(self.window_class.image_value)
        self.window_class.image_value = self.undo_stack.pop()
        self.window_class.image_area.setPixmap(self.window_class.image_value)
        self.undo_redo_validation()


    # Redo Button의 동작
    def redo(self):
        self.undo_stack.append(self.window_class.image_value)
        self.window_class.image_value = self.redo_stack.pop()
        self.window_class.image_area.setPixmap(self.window_class.image_value)
        self.undo_redo_validation()


    # Process 수행 시 stack의 관리
    # 수정 전 Pixmap을 Undo Stack에 넣음, redo stack 초기화
    def process_stack_management(self):
        self.undo_stack.append(self.window_class.image_value)
        self.redo_stack.clear()

    # Import 수행 시 stack의 관리
    # undo, redo stack 초기화
    def import_stack_management(self):
        self.undo_stack.clear()
        self.redo_stack.clear()

    # Undo / Redo Button 활성화 여부 결정
    def undo_redo_validation(self):
        if len(self.undo_stack) >= 1:
            self.window_class.undo_button.setEnabled(True)
        else:
            self.window_class.undo_button.setEnabled(False)

        if len(self.redo_stack) >= 1:
            self.window_class.redo_button.setEnabled(True)
        else:
            self.window_class.redo_button.setEnabled(False)