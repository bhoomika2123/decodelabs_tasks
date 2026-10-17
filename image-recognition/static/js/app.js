(() => {
  const form = document.getElementById("recognition-form");
  if (!form) return;

  const input = document.getElementById("image");
  const preview = document.getElementById("preview");
  const status = document.getElementById("status");
  const results = document.getElementById("results");
  const reset = document.getElementById("reset");
  const threshold = document.getElementById("threshold");

  if (threshold) threshold.addEventListener("input", () => {
    document.getElementById("threshold-value").textContent =
      `${Math.round(Number(threshold.value) * 100)}%`;
  });

  input.addEventListener("change", () => {
    results.classList.add("d-none");
    status.textContent = "";
    const file = input.files[0];
    if (!file) {
      preview.classList.add("d-none");
      preview.removeAttribute("src");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      input.value = "";
      status.textContent = "Image must be 10 MB or smaller.";
      status.className = "mt-3 status-error";
      return;
    }
    preview.src = URL.createObjectURL(file);
    preview.classList.remove("d-none");
  });

  reset.addEventListener("click", () => {
    form.reset();
    preview.classList.add("d-none");
    preview.removeAttribute("src");
    results.classList.add("d-none");
    status.textContent = "";
    status.className = "mt-3";
    const annotated = document.getElementById("annotated");
    if (annotated) annotated.removeAttribute("src");
    const detections = document.getElementById("detections");
    if (detections) detections.innerHTML = "";
    if (threshold) document.getElementById("threshold-value").textContent = "80%";
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!input.files[0]) return;
    const submit = form.querySelector('button[type="submit"]');
    submit.disabled = true;
    submit.textContent = "Processing…";
    status.className = "mt-3 text-secondary";
    status.textContent = "Processing image locally…";
    results.classList.add("d-none");

    try {
      const response = await fetch(form.dataset.endpoint, {
        method: "POST",
        body: new FormData(form)
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.message || "Processing failed.");

      status.className = "mt-3 status-success";
      status.textContent = data.message;
      results.classList.remove("d-none");
      document.getElementById("annotated").src = data.annotated_image;
      document.getElementById("count").textContent = data.count;

      const holder = document.getElementById("detections");
      if (!data.detections.length) {
        holder.innerHTML = "<p class='text-secondary mt-3'>No detections passed this threshold.</p>";
      } else {
        const table = document.createElement("table");
        table.className = "table mt-3";
        table.innerHTML = "<thead><tr><th>Object</th><th>Confidence</th><th>Bounding box (x, y, w, h)</th></tr></thead>";
        const tbody = document.createElement("tbody");
        data.detections.forEach(d => {
          const tr = document.createElement("tr");
          const box = d.box;
          [d.label, `${(d.confidence * 100).toFixed(1)}%`,
            `${box.x}, ${box.y}, ${box.width}, ${box.height}`].forEach(value => {
              const td = document.createElement("td");
              td.textContent = value;
              tr.appendChild(td);
            });
          tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        holder.replaceChildren(table);
      }
    } catch (error) {
      status.className = "mt-3 status-error";
      status.textContent = error.message;
    } finally {
      submit.disabled = false;
      submit.textContent = "Detect Objects";
    }
  });
})();
