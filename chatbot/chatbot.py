import json
import nltk
import re
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

nltk.download('stopwords')

def preprocess_text(text, stop_words):
    text = text.lower()
    text = text.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u')
    text = text.replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

class LibraryChatbot:
    def __init__(self, faq_file):
        self.stop_words = set(stopwords.words('turkish'))
        with open(faq_file, 'r', encoding='utf-8') as f:
            self.faqs = json.load(f)
        self.questions = []
        self.answers = []
        for faq in self.faqs:
            if isinstance(faq['question'], list):
                self.questions.extend(faq['question'])
                self.answers.extend([faq['answer']] * len(faq['question']))
            else:
                self.questions.append(faq['question'])
                self.answers.append(faq['answer'])
        self.processed_questions = [
            preprocess_text(q, self.stop_words) for q in self.questions
        ]
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.processed_questions)

    def get_response(self, user_query):
        processed_query = preprocess_text(user_query, self.stop_words)
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.question_vectors)[0]
        best_match_index = similarities.argmax()
        if similarities[best_match_index] > 0.3:
            return self.answers[best_match_index]
        else:
            return "Üzgünüm, bu konuda size yardımcı olamıyorum. Lütfen farklı bir şekilde ifade eder misiniz?"

class ChatbotWindow(QMainWindow):
    def __init__(self, chatbot):
        super().__init__()
        self.chatbot = chatbot
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Kütüphane Chatbot')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f7f9fc;")
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.header_label = QLabel("Kütüphane Chatbot")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        self.header_label.setStyleSheet("color: #333;")

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont('Segoe UI', 11))
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                margin: 10px 0;
            }
        """)
        self.chat_area.setTextInteractionFlags(Qt.TextSelectableByMouse)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Mesajınızı yazın...")
        self.input_field.setFont(QFont('Segoe UI', 11))
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: #ffffff;
            }
        """)

        self.send_button = QPushButton('Gönder')
        self.send_button.setFont(QFont('Segoe UI', 11))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004785;
            }
        """)

        layout.addWidget(self.header_label)
        layout.addWidget(self.chat_area)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)

        self.add_bot_message("Kütüphane Chatbot'una Hoş Geldiniz! Size nasıl yardımcı olabilirim?")

    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.add_user_message(user_message)
            response = self.chatbot.get_response(user_message)
            self.add_bot_message(response)
            self.input_field.clear()

    def add_user_message(self, message):
        self.chat_area.append(f"""
            <div style="text-align: right; margin: 10px 0;">
                <span style="
                    background-color: #0078d4; 
                    color: white; 
                    padding: 12px 16px; 
                    border-radius: 12px; 
                    display: inline-block; 
                    margin: 5px; 
                    max-width: 70%;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 20px;
                    line-height: 1.5;
                    word-wrap: break-word;
                ">{message}</span>
            </div>
        """)

    def add_bot_message(self, message):
        self.chat_area.append(f"""
            <div style="text-align: left; margin: 10px 0;">
                <span style="
                    background-color: #e9ecef; 
                    color: black; 
                    padding: 12px 16px; 
                    border-radius: 12px; 
                    display: inline-block; 
                    margin: 5px; 
                    max-width: 70%;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 20px;
                    line-height: 1.5;
                    word-wrap: break-word;
                ">{message}</span>
            </div>
        """)

def run_app(chatbot):
    app = QApplication(sys.argv)
    window = ChatbotWindow(chatbot)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    chatbot = LibraryChatbot('library_faqs.json')
    run_app(chatbot)