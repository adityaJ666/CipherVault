// =====================================================
// CIPHERVAULT WEB
// Client-side AES-256-GCM Encryption
// =====================================================


// =====================================================
// NAVIGATION
// =====================================================

const navItems =
    document.querySelectorAll(".nav-item");

const pages = {
    dashboard:
        document.getElementById("dashboardPage"),

    text:
        document.getElementById("textPage"),

    file:
        document.getElementById("filePage")
};


function showPage(pageName) {

    Object.values(pages).forEach(
        page => page.classList.remove("active-page")
    );

    if (pages[pageName]) {
        pages[pageName].classList.add("active-page");
    }

    navItems.forEach(item => {

        item.classList.toggle(
            "active",
            item.dataset.page === pageName
        );

    });

    window.scrollTo(0, 0);
}


navItems.forEach(item => {

    item.addEventListener(
        "click",
        () => showPage(item.dataset.page)
    );

});


document.querySelectorAll(".quick-action")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => showPage(button.dataset.page)
        );

    });


// =====================================================
// COMMON CRYPTO FUNCTIONS
// =====================================================


function textToBytes(text) {

    return new TextEncoder().encode(text);
}


function bytesToText(bytes) {

    return new TextDecoder().decode(bytes);
}


function bytesToBase64(bytes) {

    let binary = "";

    const chunkSize = 0x8000;

    for (
        let i = 0;
        i < bytes.length;
        i += chunkSize
    ) {

        const chunk =
            bytes.subarray(
                i,
                Math.min(
                    i + chunkSize,
                    bytes.length
                )
            );

        binary += String.fromCharCode(...chunk);
    }

    return btoa(binary);
}


function base64ToBytes(base64) {

    const binary = atob(base64);

    const bytes =
        new Uint8Array(binary.length);

    for (
        let i = 0;
        i < binary.length;
        i++
    ) {

        bytes[i] =
            binary.charCodeAt(i);
    }

    return bytes;
}


async function deriveKey(password, salt) {

    const passwordBytes =
        textToBytes(password);


    const keyMaterial =
        await crypto.subtle.importKey(
            "raw",
            passwordBytes,
            "PBKDF2",
            false,
            ["deriveKey"]
        );


    return crypto.subtle.deriveKey(

        {
            name: "PBKDF2",
            salt: salt,
            iterations: 600000,
            hash: "SHA-256"
        },

        keyMaterial,

        {
            name: "AES-GCM",
            length: 256
        },

        false,

        [
            "encrypt",
            "decrypt"
        ]
    );
}


// =====================================================
// TEXT ENCRYPTION
// =====================================================


const textInput =
    document.getElementById("textInput");

const passwordInput =
    document.getElementById("password");

const output =
    document.getElementById("output");

const encryptBtn =
    document.getElementById("encryptBtn");

const decryptBtn =
    document.getElementById("decryptBtn");

const clearBtn =
    document.getElementById("clearBtn");

const togglePassword =
    document.getElementById("togglePassword");

const copyBtn =
    document.getElementById("copyBtn");

const characterCount =
    document.getElementById("characterCount");

const passwordStatus =
    document.getElementById("passwordStatus");

const strengthText =
    document.getElementById("strengthText");

const strengthBars =
    document.querySelectorAll(".strength-bar");

const statusMessage =
    document.getElementById("statusMessage");


function showTextStatus(message, type) {

    statusMessage.textContent = message;

    statusMessage.className =
        "status-message " + type;
}


function hideTextStatus() {

    statusMessage.textContent = "";

    statusMessage.className =
        "status-message hidden";
}


async function encryptText() {

    const text =
        textInput.value;

    const password =
        passwordInput.value;


    if (!text.trim()) {

        showTextStatus(
            "Please enter some text to encrypt.",
            "error"
        );

        return;
    }


    if (!password) {

        showTextStatus(
            "Please enter an encryption password.",
            "error"
        );

        return;
    }


    try {

        encryptBtn.disabled = true;

        encryptBtn.textContent =
            "Encrypting...";


        const salt =
            crypto.getRandomValues(
                new Uint8Array(16)
            );


        const nonce =
            crypto.getRandomValues(
                new Uint8Array(12)
            );


        const key =
            await deriveKey(
                password,
                salt
            );


        const encrypted =
            await crypto.subtle.encrypt(

                {
                    name: "AES-GCM",
                    iv: nonce
                },

                key,

                textToBytes(text)
            );


        const packageData =
            new Uint8Array(
                16 +
                12 +
                encrypted.byteLength
            );


        packageData.set(
            salt,
            0
        );


        packageData.set(
            nonce,
            16
        );


        packageData.set(
            new Uint8Array(encrypted),
            28
        );


        output.value =
            bytesToBase64(packageData);


        showTextStatus(
            "Text encrypted successfully.",
            "success"
        );


    } catch (error) {

        console.error(error);

        showTextStatus(
            "Encryption failed.",
            "error"
        );

    } finally {

        encryptBtn.disabled = false;

        encryptBtn.innerHTML =
            "🔒 Encrypt";
    }
}


async function decryptText() {

    const encryptedText =
        textInput.value.trim();

    const password =
        passwordInput.value;


    if (!encryptedText) {

        showTextStatus(
            "Please enter encrypted data.",
            "error"
        );

        return;
    }


    if (!password) {

        showTextStatus(
            "Please enter your password.",
            "error"
        );

        return;
    }


    try {

        decryptBtn.disabled = true;

        decryptBtn.textContent =
            "Decrypting...";


        const packageData =
            base64ToBytes(
                encryptedText
            );


        if (packageData.length < 29) {
            throw new Error(
                "Invalid encrypted data."
            );
        }


        const salt =
            packageData.slice(
                0,
                16
            );


        const nonce =
            packageData.slice(
                16,
                28
            );


        const encrypted =
            packageData.slice(
                28
            );


        const key =
            await deriveKey(
                password,
                salt
            );


        const decrypted =
            await crypto.subtle.decrypt(

                {
                    name: "AES-GCM",
                    iv: nonce
                },

                key,

                encrypted
            );


        output.value =
            bytesToText(
                new Uint8Array(decrypted)
            );


        showTextStatus(
            "Text decrypted successfully.",
            "success"
        );


    } catch (error) {

        console.error(error);

        output.value = "";

        showTextStatus(
            "Incorrect password or corrupted encrypted data.",
            "error"
        );

    } finally {

        decryptBtn.disabled = false;

        decryptBtn.innerHTML =
            "🔓 Decrypt";
    }
}


// =====================================================
// TEXT PASSWORD
// =====================================================


togglePassword.addEventListener(
    "click",
    () => {

        if (
            passwordInput.type === "password"
        ) {

            passwordInput.type =
                "text";

            togglePassword.textContent =
                "Hide";

        } else {

            passwordInput.type =
                "password";

            togglePassword.textContent =
                "Show";
        }
    }
);


function calculatePasswordStrength(password) {

    let score = 0;


    if (password.length >= 8)
        score++;


    if (password.length >= 12)
        score++;


    if (/[A-Z]/.test(password))
        score++;


    if (
        /[0-9]/.test(password) &&
        /[^A-Za-z0-9]/.test(password)
    )
        score++;


    return score;
}


function updatePasswordStrength() {

    const password =
        passwordInput.value;


    passwordStatus.textContent =
        password
            ? "Set"
            : "Not set";


    strengthBars.forEach(
        bar =>
            bar.style.background =
                "#30363d"
    );


    if (!password) {

        strengthText.textContent =
            "Password strength";

        return;
    }


    const score =
        calculatePasswordStrength(
            password
        );


    if (score === 1) {

        strengthText.textContent =
            "Weak";

        strengthBars[0].style.background =
            "#f85149";

    } else if (score === 2) {

        strengthText.textContent =
            "Fair";

        strengthBars[0].style.background =
            "#d29922";

        strengthBars[1].style.background =
            "#d29922";

    } else if (score === 3) {

        strengthText.textContent =
            "Good";

        for (
            let i = 0;
            i < 3;
            i++
        ) {

            strengthBars[i].style.background =
                "#58a6ff";
        }

    } else {

        strengthText.textContent =
            "Strong";

        strengthBars.forEach(
            bar =>
                bar.style.background =
                    "#3fb950"
        );
    }
}


passwordInput.addEventListener(
    "input",
    updatePasswordStrength
);


textInput.addEventListener(
    "input",
    () => {

        const count =
            textInput.value.length;


        characterCount.textContent =
            count +
            (
                count === 1
                    ? " character"
                    : " characters"
            );
    }
);


copyBtn.addEventListener(
    "click",
    async () => {

        if (!output.value) {

            showTextStatus(
                "There is no result to copy.",
                "error"
            );

            return;
        }


        try {

            await navigator.clipboard.writeText(
                output.value
            );


            copyBtn.textContent =
                "✓ Copied";


            showTextStatus(
                "Result copied to clipboard.",
                "success"
            );


            setTimeout(
                () =>
                    copyBtn.textContent =
                        "📋 Copy",
                1500
            );


        } catch (error) {

            showTextStatus(
                "Unable to copy the result.",
                "error"
            );
        }
    }
);


clearBtn.addEventListener(
    "click",
    () => {

        textInput.value = "";

        passwordInput.value = "";

        output.value = "";

        characterCount.textContent =
            "0 characters";

        passwordStatus.textContent =
            "Not set";

        strengthText.textContent =
            "Password strength";


        strengthBars.forEach(
            bar =>
                bar.style.background =
                    "#30363d"
        );


        togglePassword.textContent =
            "Show";

        passwordInput.type =
            "password";


        hideTextStatus();
    }
);


encryptBtn.addEventListener(
    "click",
    encryptText
);


decryptBtn.addEventListener(
    "click",
    decryptText
);


// =====================================================
// FILE ENCRYPTION
// =====================================================


const fileInput =
    document.getElementById("fileInput");

const fileDropArea =
    document.getElementById("fileDropArea");

const selectedFile =
    document.getElementById("selectedFile");

const fileName =
    document.getElementById("fileName");

const fileSize =
    document.getElementById("fileSize");

const removeFileBtn =
    document.getElementById("removeFileBtn");

const filePassword =
    document.getElementById("filePassword");

const toggleFilePassword =
    document.getElementById("toggleFilePassword");

const filePasswordStatus =
    document.getElementById("filePasswordStatus");

const fileStrengthText =
    document.getElementById("fileStrengthText");

const fileStrengthBars =
    document.querySelectorAll(
        ".file-strength-bar"
    );

const encryptFileBtn =
    document.getElementById(
        "encryptFileBtn"
    );

const decryptFileBtn =
    document.getElementById(
        "decryptFileBtn"
    );

const fileStatusMessage =
    document.getElementById(
        "fileStatusMessage"
    );


let selectedFileObject = null;


function showFileStatus(message, type) {

    fileStatusMessage.textContent =
        message;

    fileStatusMessage.className =
        "status-message " + type;
}


function clearFileStatus() {

    fileStatusMessage.textContent =
        "";

    fileStatusMessage.className =
        "status-message hidden";
}


function formatFileSize(bytes) {

    if (bytes < 1024) {
        return bytes + " B";
    }

    if (bytes < 1024 * 1024) {
        return (
            (bytes / 1024).toFixed(2) +
            " KB"
        );
    }

    if (bytes < 1024 * 1024 * 1024) {
        return (
            (bytes / (1024 * 1024)).toFixed(2) +
            " MB"
        );
    }

    return (
        (bytes / (1024 * 1024 * 1024)).toFixed(2) +
        " GB"
    );
}


function selectFile(file) {

    if (!file) {
        return;
    }


    selectedFileObject = file;


    fileName.textContent =
        file.name;


    fileSize.textContent =
        formatFileSize(file.size);


    selectedFile.classList.remove(
        "hidden"
    );


    clearFileStatus();
}


fileInput.addEventListener(
    "change",
    event => {

        const file =
            event.target.files[0];

        selectFile(file);
    }
);


removeFileBtn.addEventListener(
    "click",
    () => {

        selectedFileObject = null;

        fileInput.value = "";

        selectedFile.classList.add(
            "hidden"
        );

        clearFileStatus();
    }
);


// Drag and drop
fileDropArea.addEventListener(
    "dragover",
    event => {

        event.preventDefault();

        fileDropArea.classList.add(
            "dragover"
        );
    }
);


fileDropArea.addEventListener(
    "dragleave",
    () => {

        fileDropArea.classList.remove(
            "dragover"
        );
    }
);


fileDropArea.addEventListener(
    "drop",
    event => {

        event.preventDefault();

        fileDropArea.classList.remove(
            "dragover"
        );


        const file =
            event.dataTransfer.files[0];

        selectFile(file);
    }
);


// =====================================================
// FILE PASSWORD
// =====================================================


toggleFilePassword.addEventListener(
    "click",
    () => {

        if (
            filePassword.type === "password"
        ) {

            filePassword.type =
                "text";

            toggleFilePassword.textContent =
                "Hide";

        } else {

            filePassword.type =
                "password";

            toggleFilePassword.textContent =
                "Show";
        }
    }
);


function updateFilePasswordStrength() {

    const password =
        filePassword.value;


    filePasswordStatus.textContent =
        password
            ? "Set"
            : "Not set";


    fileStrengthBars.forEach(
        bar =>
            bar.style.background =
                "#30363d"
    );


    if (!password) {

        fileStrengthText.textContent =
            "Password strength";

        return;
    }


    const score =
        calculatePasswordStrength(
            password
        );


    if (score === 1) {

        fileStrengthText.textContent =
            "Weak";

        fileStrengthBars[0].style.background =
            "#f85149";

    } else if (score === 2) {

        fileStrengthText.textContent =
            "Fair";

        fileStrengthBars[0].style.background =
            "#d29922";

        fileStrengthBars[1].style.background =
            "#d29922";

    } else if (score === 3) {

        fileStrengthText.textContent =
            "Good";

        for (
            let i = 0;
            i < 3;
            i++
        ) {

            fileStrengthBars[i].style.background =
                "#58a6ff";
        }

    } else {

        fileStrengthText.textContent =
            "Strong";

        fileStrengthBars.forEach(
            bar =>
                bar.style.background =
                    "#3fb950"
        );
    }
}


filePassword.addEventListener(
    "input",
    updateFilePasswordStrength
);


// =====================================================
// FILE ENCRYPTION FORMAT
// =====================================================

/*
    CipherVault encrypted file:

    8 bytes   = magic header
    1 byte    = version
    16 bytes  = salt
    12 bytes  = nonce
    remaining = ciphertext + GCM authentication tag

    This gives us a simple versioned file format.
*/


const MAGIC =
    new TextEncoder().encode(
        "CVLTFILE"
    );

const VERSION = 1;


function createFilePackage(
    salt,
    nonce,
    encrypted
) {

    const packageData =
        new Uint8Array(
            8 +
            1 +
            16 +
            12 +
            encrypted.byteLength
        );


    packageData.set(
        MAGIC,
        0
    );


    packageData[8] =
        VERSION;


    packageData.set(
        salt,
        9
    );


    packageData.set(
        nonce,
        25
    );


    packageData.set(
        new Uint8Array(encrypted),
        37
    );


    return packageData;
}


function isValidFilePackage(data) {

    if (data.length < 54) {
        return false;
    }


    for (
        let i = 0;
        i < MAGIC.length;
        i++
    ) {

        if (data[i] !== MAGIC[i]) {
            return false;
        }
    }


    return data[8] === VERSION;
}


// =====================================================
// DOWNLOAD FILE
// =====================================================


function downloadBlob(
    blob,
    filename
) {

    const url =
        URL.createObjectURL(blob);


    const link =
        document.createElement("a");


    link.href = url;

    link.download = filename;

    document.body.appendChild(link);

    link.click();

    link.remove();


    setTimeout(
        () =>
            URL.revokeObjectURL(url),
        1000
    );
}


// =====================================================
// ENCRYPT FILE
// =====================================================


async function encryptFile() {

    if (!selectedFileObject) {

        showFileStatus(
            "Please select a file first.",
            "error"
        );

        return;
    }


    const password =
        filePassword.value;


    if (!password) {

        showFileStatus(
            "Please enter an encryption password.",
            "error"
        );

        return;
    }


    try {

        encryptFileBtn.disabled = true;

        encryptFileBtn.textContent =
            "Encrypting...";


        const data =
            new Uint8Array(
                await selectedFileObject.arrayBuffer()
            );


        const salt =
            crypto.getRandomValues(
                new Uint8Array(16)
            );


        const nonce =
            crypto.getRandomValues(
                new Uint8Array(12)
            );


        const key =
            await deriveKey(
                password,
                salt
            );


        const encrypted =
            await crypto.subtle.encrypt(

                {
                    name: "AES-GCM",
                    iv: nonce
                },

                key,

                data
            );


        const packageData =
            createFilePackage(
                salt,
                nonce,
                encrypted
            );


        const blob =
            new Blob(
                [packageData],
                {
                    type:
                        "application/octet-stream"
                }
            );


        downloadBlob(
            blob,
            selectedFileObject.name +
            ".cvault"
        );


        showFileStatus(
            "File encrypted successfully. The encrypted file has been downloaded.",
            "success"
        );


    } catch (error) {

        console.error(error);

        showFileStatus(
            "File encryption failed.",
            "error"
        );

    } finally {

        encryptFileBtn.disabled = false;

        encryptFileBtn.textContent =
            "🔒 Encrypt File";
    }
}


// =====================================================
// DECRYPT FILE
// =====================================================


async function decryptFile() {

    if (!selectedFileObject) {

        showFileStatus(
            "Please select an encrypted .cvault file.",
            "error"
        );

        return;
    }


    const password =
        filePassword.value;


    if (!password) {

        showFileStatus(
            "Please enter your password.",
            "error"
        );

        return;
    }


    try {

        decryptFileBtn.disabled = true;

        decryptFileBtn.textContent =
            "Decrypting...";


        const data =
            new Uint8Array(
                await selectedFileObject.arrayBuffer()
            );


        if (!isValidFilePackage(data)) {

            throw new Error(
                "Invalid CipherVault file."
            );
        }


        const salt =
            data.slice(
                9,
                25
            );


        const nonce =
            data.slice(
                25,
                37
            );


        const encrypted =
            data.slice(
                37
            );


        const key =
            await deriveKey(
                password,
                salt
            );


        const decrypted =
            await crypto.subtle.decrypt(

                {
                    name: "AES-GCM",
                    iv: nonce
                },

                key,

                encrypted
            );


        let originalName =
            selectedFileObject.name;


        if (
            originalName.toLowerCase()
                .endsWith(".cvault")
        ) {

            originalName =
                originalName.slice(
                    0,
                    -7
                );
        }


        const blob =
            new Blob(
                [decrypted]
            );


        downloadBlob(
            blob,
            originalName
        );


        showFileStatus(
            "File decrypted successfully. The original file has been downloaded.",
            "success"
        );


    } catch (error) {

        console.error(error);

        showFileStatus(
            "Incorrect password or corrupted/invalid CipherVault file.",
            "error"
        );

    } finally {

        decryptFileBtn.disabled = false;

        decryptFileBtn.textContent =
            "🔓 Decrypt File";
    }
}


encryptFileBtn.addEventListener(
    "click",
    encryptFile
);


decryptFileBtn.addEventListener(
    "click",
    decryptFile
);