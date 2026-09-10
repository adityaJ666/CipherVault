from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QLineEdit,
    QMessageBox,
)
from PySide6.QtCore import Qt
from core.encryption import encrypt_text, decrypt_text

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("KeyScrambler")
        self.setMinimumSize(1000, 650)

        self.setup_ui()

    def setup_ui(self):

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- SIDEBAR ----------------

        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)

        logo = QLabel("🔐 KeyScrambler")
        logo.setObjectName("logo")

        subtitle = QLabel("Secure Data Protection")
        subtitle.setObjectName("subtitle")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(30)

        dashboard_button = QPushButton("  Dashboard")
        text_button = QPushButton("  Text Encryption")
        file_button = QPushButton("  File Encryption")
        settings_button = QPushButton("  Settings")
        about_button = QPushButton("  About")

        sidebar_layout.addWidget(dashboard_button)
        sidebar_layout.addWidget(text_button)
        sidebar_layout.addWidget(file_button)

        sidebar_layout.addSpacing(15)

        sidebar_layout.addWidget(settings_button)
        sidebar_layout.addWidget(about_button)

        sidebar_layout.addStretch()

        status = QLabel("● System Ready")
        status.setObjectName("status")

        sidebar_layout.addWidget(status)

        # ---------------- CONTENT ----------------

        self.pages = QStackedWidget()

        dashboard_page = self.create_dashboard()
        text_page = self.create_text_page()
        file_page = self.create_file_page()
        settings_page = self.create_simple_page(
            "Settings",
            "Application settings will be available here."
        )
        about_page = self.create_simple_page(
            "About KeyScrambler",
            "A secure text and file protection application."
        )

        self.pages.addWidget(dashboard_page)
        self.pages.addWidget(text_page)
        self.pages.addWidget(file_page)
        self.pages.addWidget(settings_page)
        self.pages.addWidget(about_page)

        dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        text_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        file_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        settings_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        about_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

    # ---------------- DASHBOARD ----------------

    def create_dashboard(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Security Dashboard")
        title.setObjectName("page_title")

        description = QLabel(
            "Welcome to KeyScrambler. Protect your sensitive "
            "information using secure encryption."
        )

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addSpacing(30)

        security = QLabel(
            "🔒  AES-256-GCM\n\n"
            "✓ Authenticated encryption\n"
            "✓ Password-based key derivation\n"
            "✓ Random encryption nonce\n"
            "✓ Integrity protection"
        )

        security.setObjectName("security_card")

        layout.addWidget(security)

        layout.addStretch()

        return page

    # ---------------- TEXT PAGE ----------------

    def create_text_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Text Encryption")
        title.setObjectName("page_title")

        layout.addWidget(title)

        layout.addWidget(QLabel("Enter text"))

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Type your confidential message here..."
        )

        layout.addWidget(self.text_input)

        layout.addWidget(QLabel("Encryption password"))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(
            "Enter a strong password"
        )
        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        encrypt_button = QPushButton("🔒 Encrypt")
        decrypt_button = QPushButton("🔓 Decrypt")
        clear_button = QPushButton("Clear")

        button_layout.addWidget(encrypt_button)
        button_layout.addWidget(decrypt_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        layout.addWidget(QLabel("Result"))

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        layout.addWidget(self.result_output)

        clear_button.clicked.connect(self.clear_text)
        encrypt_button.clicked.connect(self.encrypt_text)
        return page

    # ---------------- FILE PAGE ----------------

    def create_file_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("File Encryption")
        title.setObjectName("page_title")

        layout.addWidget(title)

        description = QLabel(
            "Encrypt and decrypt files securely."
        )

        layout.addWidget(description)

        layout.addSpacing(20)

        select_button = QPushButton("📁 Select File")
        encrypt_button = QPushButton("🔒 Encrypt File")
        decrypt_button = QPushButton("🔓 Decrypt File")

        layout.addWidget(select_button)
        layout.addWidget(encrypt_button)
        layout.addWidget(decrypt_button)

        layout.addStretch()

        return page

    # ---------------- SIMPLE PAGE ----------------

    def create_simple_page(self, title_text, description_text):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel(title_text)
        title.setObjectName("page_title")

        description = QLabel(description_text)

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addStretch()

        return page

    # ---------------- CLEAR ----------------

    def clear_text(self):

        self.text_input.clear()
        self.password_input.clear()
        self.result_output.clear()


    def encrypt_text(self):

        text = self.text_input.toPlainText()
        password = self.password_input.text()

        if not text:
            QMessageBox.warning(self, "Error", "Please enter some text.")
            return

        if not password:
            QMessageBox.warning(self, "Error", "Please enter a password.")
            return

        try:
            encrypted = encrypt_text(text, password)
            self.result_output.setPlainText(encrypted)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Encryption Error",
                str(error)
            )