// =======================
//  SUMMARY HANDLING
// =======================

const notesInput = document.getElementById("notesInput");
const summaryOutput = document.getElementById("summaryOutput");
const summariseBtn = document.getElementById("summariseBtn");
const copyBtn = document.getElementById("copyBtn");
const downloadBtn = document.getElementById("downloadBtn");
const summaryTypeSelect = document.getElementById("summaryType");
const spinnerOverlay = document.getElementById("spinnerOverlay");

// =======================
//  COPY / DOWNLOAD HELPERS
// =======================

// Copy text to clipboard
copyBtn.addEventListener("click", () => {
    if (!summaryOutput.value) return alert("No summary to copy.");
    summaryOutput.select();
    navigator.clipboard.writeText(summaryOutput.value)
        .then(() => alert("Summary copied!"))
        .catch(err => console.error(err));
});

// Download text as .txt
downloadBtn.addEventListener("click", () => {
    if (!summaryOutput.value) return alert("No summary to download.");
    const blob = new Blob([summaryOutput.value], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "AI_Summary.txt";
    a.click();
    URL.revokeObjectURL(url);
});

// =======================
//  SUMMARISE LOGIC
// =======================
summariseBtn.addEventListener("click", async () => {
    const notes = notesInput.value.trim();
    if (!notes) {
        alert("Please enter clinician notes.");
        return;
    }

    spinnerOverlay.style.display = "flex";

    const summaryType = summaryTypeSelect.value;
    const endpoint = summaryType === "patient"
        ? "http://127.0.0.1:5000/api/patient-summary"
        : "http://127.0.0.1:5000/api/clinical-summary";

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ notes })
        });

        const data = await response.json();

        if (!response.ok) {
            summaryOutput.value = "";
            alert(data.error || "Failed to generate summary.");
            return;
        }

        // Get proper key
        let summaryText = data.summary || data.patient_summary || "";

        // ===============================
        //  NEW FORMATTING RULES
        // ===============================
        const lines = summaryText.split(/\r?\n/);

        const formatted = lines.map(line => {
            const trimmed = line.trim();

            // Keep bold headers EXACTLY as they are
            if (/^\*\*.+\*\*:?$/.test(trimmed)) {
                return trimmed; // Already a bold section heading
            }

            // Lines starting with '+' keep them
            if (trimmed.startsWith("+")) return trimmed;

            // Lines starting with '*' keep them
            if (trimmed.startsWith("*")) return trimmed;

            // Otherwise: make into a bullet
            return `* ${trimmed}`;

        }).join("\n");

        summaryOutput.value = formatted;

    } catch (err) {
        console.error(err);
        summaryOutput.value = "";
        alert("Unable to contact server. Make sure Flask is running.");
    } finally {
        spinnerOverlay.style.display = "none";
    }
});
