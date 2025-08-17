document.addEventListener("DOMContentLoaded", () => {
  const apiBase = "http://127.0.0.1:8000";
  const summaryText = document.getElementById("summaryText");
  const pdfPreview = document.getElementById("pdfPreview");
  const historyList = document.getElementById("historyList");

  async function renderHistory() {
    try {
      const res = await fetch(`${apiBase}/history`);
      let history = await res.json();

      history = history.reverse();

      historyList.innerHTML = history.length
        ? history
            .map(
              (item) =>
                `<li class="list-group-item"><strong>${item.original_filename}</strong><br>${item.summary}</li>`
            )
            .join("")
        : '<li class="list-group-item text-muted">No previous summaries yet</li>';
    } catch {
      historyList.innerHTML =
        '<li class="list-group-item text-danger">Failed to load history</li>';
    }
  }

  renderHistory();

  document.getElementById("pdfForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const file = document.getElementById("pdfFile").files[0];
    if (!file) return alert("Please select a PDF file.");

    const formData = new FormData();
    formData.append("file", file);

    summaryText.innerText = "Loading...";
    pdfPreview.innerText = "Loading...";

    try {
      const res = await fetch(`${apiBase}/upload-pdf`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      summaryText.innerText = data.summary || "No summary yet";
      pdfPreview.innerText = data.pdf_text_preview || "No preview yet";

      renderHistory();
    } catch {
      summaryText.innerText = "Error generating summary";
      pdfPreview.innerText = "";
      alert("Error uploading PDF.");
    }
  });
});
