from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QLineEdit,
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QStackedWidget,
    QFrame,
)

from PySide6.QtCore import Qt

from core.encryption import (
    encrypt_text,
    decrypt_text,
    encrypt_file,
    decrypt_file,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CipherVault")
        self.setMinimumSize(1050, 700)

        self.selected_file = None

        self.setup_ui()
        self.apply_styles()

    # ==================================================
    # MAIN UI
    # ==================================================

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==================================================
        # SIDEBAR
        # ==================================================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 20)
        sidebar_layout.setSpacing(10)

        logo = QLabel("🔐  CipherVault")
        logo.setObjectName("logo")

        sidebar_layout.addWidget(logo)

        subtitle = QLabel("SECURE DATA PROTECTION")
        subtitle.setObjectName("sidebarSubtitle")

        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(30)

        self.dashboard_button = QPushButton("🏠   Dashboard")
        self.text_button = QPushButton("📝   Text Encryption")
        self.file_button = QPushButton("📁   File Encryption")

        self.dashboard_button.setObjectName("sidebarButton")
        self.text_button.setObjectName("sidebarButton")
        self.file_button.setObjectName("sidebarButton")

        sidebar_layout.addWidget(self.dashboard_button)
        sidebar_layout.addWidget(self.text_button)
        sidebar_layout.addWidget(self.file_button)

        sidebar_layout.addStretch()

        security_label = QLabel("●  SYSTEM SECURE")
        security_label.setObjectName("secureStatus")

        sidebar_layout.addWidget(security_label)

        version_label = QLabel("CipherVault v1.0")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)

        sidebar_layout.addWidget(version_label)

        # ==================================================
        # PAGES
        # ==================================================

        self.pages = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.text_page = self.create_text_page()
        self.file_page = self.create_file_page()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.text_page)
        self.pages.addWidget(self.file_page)

        self.dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.dashboard_page)
        )

        self.text_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.text_page)
        )

        self.file_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.file_page)
        )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

    # ==================================================
    # DASHBOARD
    # ==================================================

    def create_dashboard_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setContentsMargins(45, 40, 45, 40)
        layout.setSpacing(15)

        title = QLabel("Welcome to CipherVault")
        title.setObjectName("pageTitle")

        layout.addWidget(title)

        description = QLabel(
            "A secure desktop application for protecting "
            "your text and files using modern cryptography."
        )

        description.setObjectName("description")
        description.setWordWrap(True)

        layout.addWidget(description)

        layout.addSpacing(30)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        cards = [
            ("🔐", "AES-256-GCM", "Authenticated encryption"),
            ("🔑", "PBKDF2", "Secure password derivation"),
            ("🛡️", "Integrity", "Tamper detection"),
        ]

        for icon, title_text, description_text in cards:

            card = QFrame()
            card.setObjectName("securityCard")

            card_layout = QVBoxLayout(card)

            icon_label = QLabel(icon)
            icon_label.setObjectName("cardIcon")

            card_title = QLabel(title_text)
            card_title.setObjectName("cardTitle")

            card_description = QLabel(description_text)
            card_description.setObjectName("cardDescription")
            card_description.setWordWrap(True)

            card_layout.addWidget(icon_label)
            card_layout.addWidget(card_title)
            card_layout.addWidget(card_description)

            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        layout.addSpacing(25)

        features_title = QLabel("Security Features")
        features_title.setObjectName("sectionTitle")

        layout.addWidget(features_title)

        features = QLabel(
            "✓ AES-256-GCM encryption\n"
            "✓ PBKDF2-HMAC-SHA256 password protection\n"
            "✓ Random salt and nonce for every encryption\n"
            "✓ Text and file encryption\n"
            "✓ Authentication and integrity protection"
        )

        features.setObjectName("featureList")

        layout.addWidget(features)

        layout.addStretch()

        return page

    # ==================================================
    # TEXT PAGE
    # ==================================================

    def create_text_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(45, 40, 45, 40)
        layout.setSpacing(12)

        title = QLabel("Text Encryption")
        title.setObjectName("pageTitle")

        layout.addWidget(title)

        description = QLabel(
            "Encrypt and decrypt sensitive text using AES-256-GCM."
        )

        description.setObjectName("description")

        layout.addWidget(description)

        layout.addSpacing(15)

        input_label = QLabel("TEXT / ENCRYPTED DATA")
        input_label.setObjectName("inputLabel")

        layout.addWidget(input_label)

        self.text_input = QTextEdit()

        self.text_input.setPlaceholderText(
            "Enter your message or encrypted data here..."
        )

        layout.addWidget(self.text_input)

        password_label = QLabel("PASSWORD")
        password_label.setObjectName("inputLabel")

        layout.addWidget(password_label)

        # Secure password field
        self.text_password = QLineEdit()

        self.text_password.setPlaceholderText(
            "Enter encryption password..."
        )

        self.text_password.setEchoMode(
            QLineEdit.Password
        )

        layout.addWidget(self.text_password)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        encrypt_button = QPushButton("🔐  Encrypt")
        decrypt_button = QPushButton("🔓  Decrypt")
        clear_button = QPushButton("Clear")

        encrypt_button.setObjectName("primaryButton")
        decrypt_button.setObjectName("secondaryButton")
        clear_button.setObjectName("clearButton")

        encrypt_button.clicked.connect(
            self.encrypt_text_message
        )

        decrypt_button.clicked.connect(
            self.decrypt_text_message
        )

        clear_button.clicked.connect(
            self.clear_text
        )

        button_layout.addWidget(encrypt_button)
        button_layout.addWidget(decrypt_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        return page

    # ==================================================
    # FILE PAGE
    # ==================================================

    def create_file_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(45, 40, 45, 40)
        layout.setSpacing(15)

        title = QLabel("File Encryption")
        title.setObjectName("pageTitle")

        layout.addWidget(title)

        description = QLabel(
            "Protect files using AES-256-GCM encryption."
        )

        description.setObjectName("description")

        layout.addWidget(description)

        layout.addSpacing(25)

        file_box = QFrame()
        file_box.setObjectName("fileBox")

        file_layout = QVBoxLayout(file_box)
        file_layout.setContentsMargins(30, 30, 30, 30)
        file_layout.setSpacing(15)

        file_icon = QLabel("📁")
        file_icon.setObjectName("largeIcon")
        file_icon.setAlignment(Qt.AlignCenter)

        file_layout.addWidget(file_icon)

        select_button = QPushButton("Select File")

        select_button.setObjectName("primaryButton")

        select_button.clicked.connect(
            self.select_file
        )

        file_layout.addWidget(
            select_button,
            alignment=Qt.AlignCenter
        )

        self.file_label = QLabel(
            "No file selected"
        )

        self.file_label.setObjectName("fileLabel")
        self.file_label.setWordWrap(True)
        self.file_label.setAlignment(Qt.AlignCenter)

        file_layout.addWidget(self.file_label)

        layout.addWidget(file_box)

        layout.addSpacing(15)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        encrypt_file_button = QPushButton(
            "🔐  Encrypt File"
        )

        decrypt_file_button = QPushButton(
            "🔓  Decrypt File"
        )

        encrypt_file_button.setObjectName(
            "primaryButton"
        )

        decrypt_file_button.setObjectName(
            "secondaryButton"
        )

        encrypt_file_button.clicked.connect(
            self.encrypt_selected_file
        )

        decrypt_file_button.clicked.connect(
            self.decrypt_selected_file
        )

        button_layout.addWidget(
            encrypt_file_button
        )

        button_layout.addWidget(
            decrypt_file_button
        )

        layout.addLayout(button_layout)

        layout.addStretch()

        return page

    # ==================================================
    # TEXT ENCRYPTION
    # ==================================================

    def encrypt_text_message(self):

        text = self.text_input.toPlainText()
        password = self.text_password.text()

        if not text:

            QMessageBox.warning(
                self,
                "Missing Text",
                "Please enter some text to encrypt."
            )

            return

        if not password:

            QMessageBox.warning(
                self,
                "Missing Password",
                "Please enter a password."
            )

            return

        try:

            encrypted = encrypt_text(
                text,
                password
            )

            self.text_input.setPlainText(
                encrypted
            )

            QMessageBox.information(
                self,
                "Encryption Successful",
                "Your text has been encrypted successfully."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Encryption Failed",
                str(e)
            )

    # ==================================================
    # TEXT DECRYPTION
    # ==================================================

    def decrypt_text_message(self):

        encrypted_text = self.text_input.toPlainText()
        password = self.text_password.text()

        if not encrypted_text:

            QMessageBox.warning(
                self,
                "Missing Data",
                "Please enter encrypted text."
            )

            return

        if not password:

            QMessageBox.warning(
                self,
                "Missing Password",
                "Please enter your password."
            )

            return

        try:

            decrypted = decrypt_text(
                encrypted_text,
                password
            )

            self.text_input.setPlainText(
                decrypted
            )

            QMessageBox.information(
                self,
                "Decryption Successful",
                "Your text has been decrypted successfully."
            )

        except Exception:

            QMessageBox.critical(
                self,
                "Decryption Failed",
                "Incorrect password or corrupted encrypted text."
            )

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_text(self):

        self.text_input.clear()
        self.text_password.clear()

    # ==================================================
    # SELECT FILE
    # ==================================================

    def select_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File"
        )

        if file_path:

            self.selected_file = file_path

            self.file_label.setText(
                f"Selected:\n{file_path}"
            )

    # ==================================================
    # ENCRYPT FILE
    # ==================================================

    def encrypt_selected_file(self):

        if not self.selected_file:

            QMessageBox.warning(
                self,
                "No File Selected",
                "Please select a file first."
            )

            return

        password, ok = QInputDialog.getText(
            self,
            "Encrypt File",
            "Enter password:"
        )

        if not ok or not password:

            return

        try:

            input_path = self.selected_file
            output_path = input_path + ".enc"

            encrypt_file(
                input_path,
                output_path,
                password
            )

            QMessageBox.information(
                self,
                "Encryption Successful",
                f"File encrypted successfully!\n\n"
                f"Saved as:\n{output_path}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Encryption Failed",
                str(e)
            )

    # ==================================================
    # DECRYPT FILE
    # ==================================================

    def decrypt_selected_file(self):

        if not self.selected_file:

            QMessageBox.warning(
                self,
                "No File Selected",
                "Please select an encrypted file first."
            )

            return

        password, ok = QInputDialog.getText(
            self,
            "Decrypt File",
            "Enter password:"
        )

        if not ok or not password:

            return

        try:

            input_path = self.selected_file

            if input_path.lower().endswith(".enc"):

                output_path = input_path[:-4]

            else:

                output_path = input_path + ".decrypted"

            decrypt_file(
                input_path,
                output_path,
                password
            )

            QMessageBox.information(
                self,
                "Decryption Successful",
                f"File decrypted successfully!\n\n"
                f"Saved as:\n{output_path}"
            )

        except Exception:

            QMessageBox.critical(
                self,
                "Decryption Failed",
                "Incorrect password or corrupted encrypted file."
            )

    # ==================================================
    # DARK CYBERSECURITY THEME
    # ==================================================

    def apply_styles(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #0b0f14;
            }

            QWidget {
                background-color: #0b0f14;
                color: #e6edf3;
                font-family: Segoe UI;
                font-size: 14px;
            }

            #sidebar {
                background-color: #111820;
                border-right: 1px solid #26313d;
                min-width: 240px;
                max-width: 240px;
            }

            #logo {
                color: #58a6ff;
                font-size: 24px;
                font-weight: bold;
                padding: 5px;
            }

            #sidebarSubtitle {
                color: #6e7681;
                font-size: 10px;
                padding-left: 8px;
            }

            #sidebarButton {
                background-color: transparent;
                color: #8b949e;
                border: none;
                border-radius: 8px;
                padding: 13px;
                text-align: left;
                font-size: 14px;
            }

            #sidebarButton:hover {
                background-color: #1c2631;
                color: #ffffff;
            }

            #secureStatus {
                color: #3fb950;
                font-weight: bold;
                padding: 10px;
            }

            #versionLabel {
                color: #6e7681;
                font-size: 11px;
            }

            #pageTitle {
                color: #ffffff;
                font-size: 30px;
                font-weight: bold;
            }

            #description {
                color: #8b949e;
                font-size: 14px;
            }

            #sectionTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: bold;
            }

            #securityCard {
                background-color: #111820;
                border: 1px solid #26313d;
                border-radius: 12px;
                padding: 10px;
            }

            #cardIcon {
                font-size: 28px;
            }

            #cardTitle {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
            }

            #cardDescription {
                color: #8b949e;
                font-size: 12px;
            }

            #featureList {
                color: #8b949e;
                font-size: 14px;
            }

            #inputLabel {
                color: #8b949e;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
            }

            QTextEdit,
            QLineEdit {
                background-color: #111820;
                color: #e6edf3;
                border: 1px solid #26313d;
                border-radius: 8px;
                padding: 12px;
                selection-background-color: #1f6feb;
            }

            QTextEdit:focus,
            QLineEdit:focus {
                border: 1px solid #58a6ff;
            }

            #fileBox {
                background-color: #111820;
                border: 1px dashed #3b4652;
                border-radius: 12px;
            }

            #largeIcon {
                font-size: 48px;
            }

            #fileLabel {
                color: #8b949e;
                font-size: 13px;
            }

            #primaryButton {
                background-color: #238636;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
            }

            #primaryButton:hover {
                background-color: #2ea043;
            }

            #secondaryButton {
                background-color: #1f6feb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
            }

            #secondaryButton:hover {
                background-color: #388bfd;
            }

            #clearButton {
                background-color: #21262d;
                color: #8b949e;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 12px 20px;
            }

            #clearButton:hover {
                background-color: #30363d;
                color: white;
            }

            QMessageBox,
            QInputDialog {
                background-color: #111820;
            }
            """
        )


# ==================================================
# APPLICATION START
# ==================================================

if __name__ == "__main__":

    app = QApplication([])

    window = MainWindow()

    window.show()

    app.exec()