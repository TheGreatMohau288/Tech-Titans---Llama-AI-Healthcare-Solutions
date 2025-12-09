// =======================
//  GET ELEMENTS
// =======================
const notesInput = document.getElementById("notesInput");
const summaryOutput = document.getElementById("summaryOutput");

const summariseBtn = document.getElementById("summariseBtn");
const uploadBtn = document.getElementById("uploadBtn");
const downloadBtn = document.getElementById("downloadBtn");
const copyBtn = document.getElementById("copyBtn");

// =======================
// HANDLE SUMMARISE BUTTON
// =======================

summariseBtn.addEventListener("click", async () => {

    const notes = notesInput.value.trim();

    if (notes === "") {
        alert("Please enter clinician notes before summarising.");
        return;
    }

    // Show loading
    summaryOutput.value = "Summarizing... please wait...";

    try {
        // BACKEND API CALL (Flask + Ollama)
        const response = await fetch("http://127.0.0.1:5000/api/summarize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ notes: notes })
        });

        const data = await response.json();

        summaryOutput.value = data.summary || "No summary was returned.";
    }
    catch (error) {
        summaryOutput.value = "Error contacting server. Make sure Flask is running.";
        console.error(error);
    }
});

// =======================
// UPLOAD FILE
// =======================

uploadBtn.addEventListener("click", () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".txt, .docx, .pdf";

    fileInput.onchange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        // ⚠️ Use correct reader depending on file type
        const fileName = file.name.toLowerCase();

        // 1️⃣ Handle TXT
        if (fileName.endsWith(".txt")) {
            const reader = new FileReader();
            reader.onload = () => {
                notesInput.value = reader.result;
            };
            reader.readAsText(file);
        }

        // 2️⃣ Handle DOCX
        else if (fileName.endsWith(".docx")) {
            const arrayBuffer = await file.arrayBuffer();
            mammoth.extractRawText({ arrayBuffer: arrayBuffer })
                .then(result => {
                    notesInput.value = result.value;
                })
                .catch(err => {
                    alert("Error reading Word document");
                    console.error(err);
                });
        }

        // 3️⃣ Handle PDF
        else if (fileName.endsWith(".pdf")) {
            readPDF(file);
        }
    };

    fileInput.click();
});

// PDF READER FUNCTION
async function readPDF(file) {
    const fileReader = new FileReader();

    fileReader.onload = async function () {
        const typedarray = new Uint8Array(this.result);

        const pdf = await pdfjsLib.getDocument(typedarray).promise;
        let text = "";

        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            const pageText = content.items.map(item => item.str).join(" ");
            text += pageText + "\n\n";
        }

        notesInput.value = text;
    };

    fileReader.readAsArrayBuffer(file);
}

// =======================
//  DOWNLOAD SUMMARY (as TXT)
// =======================

downloadBtn.addEventListener("click", () => {
    const summaryText = summaryOutput.value.trim();

    if (summaryText === "") {
        alert("No summary to download.");
        return;
    }

    const blob = new Blob([summaryText], { type: "text/plain" });
    const link = document.createElement("a");

    link.download = "AI_summary.txt";
    link.href = URL.createObjectURL(blob);
    link.click();
});

// =======================
//  COPY SUMMARY TO CLIPBOARD
// =======================

copyBtn.addEventListener("click", () => {
    const summary = summaryOutput.value.trim();

    if (!summary) {
        alert("No summary to copy.");
        return;
    }

    navigator.clipboard.writeText(summary);
    alert("Summary copied!");
});
