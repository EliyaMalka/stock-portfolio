import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton
)
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt, QThread, Signal, QFile, QTextStream, QTimer

from model.chat_backend import rephrase_question, search_qdrant, generate_answer


class ChatWorker(QThread):
    step_signal = Signal(str)
    result_signal = Signal(str)

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        try:
            self.step_signal.emit("Rephrasing question")
            rephrased = rephrase_question(self.question)

            self.step_signal.emit("Searching in Qdrant")
            context = search_qdrant(rephrased)

            self.step_signal.emit("Generating answer")
            answer = generate_answer(context, rephrased)

            self.result_signal.emit(answer)
        except Exception as e:
            self.result_signal.emit(f"[Error] {str(e)}")


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.load_stylesheet(r"view\chatWindow.qss")
        self.setWindowTitle("AI Chat")
        self.setMinimumSize(600, 400)

        self.layout = QVBoxLayout(self)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter your question...")
        self.layout.addWidget(self.input_line)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_user_input)
        self.layout.addWidget(self.send_button)

        self.worker = None
        self.last_status_position = None
        self.status_base_text = ""
        self.status_dot_count = 0
        self.status_dot_timer = None

    def load_stylesheet(self, path):
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()

    def handle_user_input(self):
        question = self.input_line.text().strip()
        if not question:
            return

        self.chat_display.append(f"\nYou: {question}")
        self.input_line.clear()
        self.send_button.setEnabled(False)

        self.last_status_position = None
        self.worker = ChatWorker(question)
        self.worker.step_signal.connect(self.update_status_line)
        self.worker.result_signal.connect(self.display_answer)
        self.worker.start()

    def update_status_line(self, message):
        self.status_base_text = message.strip(". ")
        self.status_dot_count = 0

        self.append_or_update_status_line(self.status_base_text)

        if self.status_dot_timer:
            self.status_dot_timer.stop()

        self.status_dot_timer = QTimer(self)
        self.status_dot_timer.timeout.connect(self.animate_status_dots)
        self.status_dot_timer.start(500)

    def append_or_update_status_line(self, text):
        cursor = self.chat_display.textCursor()
        if self.last_status_position is None:
            self.chat_display.append(text)
            self.last_status_position = self.chat_display.document().blockCount() - 1
        else:
            block = self.chat_display.document().findBlockByNumber(self.last_status_position)
            cursor.setPosition(block.position())
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.insertText(text)

    def animate_status_dots(self):
        self.status_dot_count = (self.status_dot_count + 1) % 4
        dots = '.' * self.status_dot_count
        animated_text = f"{self.status_base_text}{dots}"
        self.append_or_update_status_line(animated_text)

    def display_answer(self, answer):
        if self.status_dot_timer:
            self.status_dot_timer.stop()
            self.status_dot_timer = None

        if self.last_status_position is not None:
            cursor = self.chat_display.textCursor()
            block = self.chat_display.document().findBlockByNumber(self.last_status_position)
            cursor.setPosition(block.position())
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.insertText(f"AI: {answer}")
        else:
            self.chat_display.append(f"AI: {answer}")

        self.send_button.setEnabled(True)
        self.last_status_position = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
