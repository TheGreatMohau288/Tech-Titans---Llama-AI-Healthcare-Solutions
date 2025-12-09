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
// 1️⃣ HANDLE SUMMARISE BUTTON
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
// 2️⃣ UPLOAD TXT FILE
// =======================

uploadBtn.addEventListener("click", () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".txt";

    fileInput.onchange = (event) => {
        const file = event.target.files[0];

        if (!file) return;

        const reader = new FileReader();
        reader.onload = () => {
            notesInput.value = reader.result;
        };

        reader.readAsText(file);
    };

    fileInput.click();
});

// =======================
// 3️⃣ DOWNLOAD SUMMARY (as TXT)
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
// 4️⃣ COPY SUMMARY TO CLIPBOARD
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
