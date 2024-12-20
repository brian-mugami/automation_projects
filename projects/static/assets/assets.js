//(function () {
//  "use strict";
//
//  var forms = document.querySelectorAll(".needs-validation");
//
//  Array.prototype.slice.call(forms).forEach(function (form) {
//    form.addEventListener(
//      "submit",
//      function (event) {
//        if (!form.checkValidity()) {
//          event.preventDefault();
//          event.stopPropagation();
//        }
//
//        form.classList.add("was-validated");
//      },
//      false
//    );
//  });
//})();

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("AiParseForm");
  const spinner = document.getElementById("spinner-loader-parse");
  const resultMessage = document.getElementById("resultParseMessage");
  const resultContainer = document.getElementById("wordParseResults");
  const resultButton = document.getElementById("parseButton");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    resultMessage.style.display = "none";
    resultContainer.style.display = "none";
    resultContainer.innerHTML = "";
    spinner.style.display = "block";
    resultButton.disabled = true;

    const formData = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        spinner.style.display = "none";
        resultButton.disabled = false;

        if (data.result) {
          resultMessage.innerText = "Parsing completed successfully!";
          resultMessage.classList.remove("text-danger");
          resultMessage.classList.add("text-success");
          resultMessage.style.display = "block";

          // Dynamically render the result based on its type (e.g., paragraphs, tables)
          resultContainer.innerHTML = formatResult(data.result);
          resultContainer.style.display = "block";
        } else if (data.error) {
          resultMessage.innerText = data.error;
          resultMessage.classList.remove("text-success");
          resultMessage.classList.add("text-danger");
          resultMessage.style.display = "block";
        }
      })
      .catch((error) => {
        spinner.style.display = "none";
        resultButton.disabled = false;
        resultMessage.innerText = "An unexpected error occurred.";
        resultMessage.classList.remove("text-success");
        resultMessage.classList.add("text-danger");
        resultMessage.style.display = "block";
        console.error("Parsing error:", error);
      });
  });

  // Function to format the result based on its structure
  function formatResult(result) {
    // Check if the result is an array (e.g., paragraphs or tables)
    if (Array.isArray(result)) {
      return result.map((item) => {
        // If the item is a string (a paragraph)
        if (typeof item === "string") {
          return `<p>${item}</p>`;
        }
        // If the item is an object (likely a table)
        else if (typeof item === "object" && item !== null) {
          return generateTable(item);
        }
        return "";
      }).join("");
    }
    return `<p>${result}</p>`; // Default case if it's not an array
  }

  // Function to generate a table from the result object
  function generateTable(data) {
    let tableHTML = "<table class='table table-bordered'>";
    // Assuming the data is an array of objects (rows)
    const headers = Object.keys(data[0]);
    tableHTML += "<thead><tr>" + headers.map(header => `<th>${header}</th>`).join("") + "</tr></thead>";

    tableHTML += "<tbody>";
    data.forEach(row => {
      tableHTML += "<tr>" + headers.map(header => `<td>${row[header]}</td>`).join("") + "</tr>";
    });
    tableHTML += "</tbody>";
    tableHTML += "</table>";
    return tableHTML;
  }
});


document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("AiWordForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const aiButton = document.getElementById("aiButton");
    const spinnerLoader = document.getElementById("spinner-loader-ai");
    const resultMessage = document.getElementById("resultAiMessage");
    const wordDataResults = document.getElementById("wordDataResults");
    const parseLink = document.getElementById("redirect-to-parse");
    const parseLink2 = document.getElementById("redirect-to-parse-2");

    const formData = new FormData(this);
    aiButton.disabled = true;
    resultMessage.style.display = "block";
    resultMessage.innerHTML = "Reading Document...";
    spinnerLoader.style.display = "block";

    fetch("/ai/word", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        spinnerLoader.style.display = "none";
        aiButton.disabled = false;
        if (data.success) {
          parseLink.style.display = "block";
          parseLink2.style.display = "block";
          resultMessage.innerHTML = "Document read successfully!";
          let content = `<h3>Headings</h3><ul>`;
          data.word_data.headings.forEach((h) => {
            content += `<li>${h[1]} (${h[0]})</li>`;
          });
          content += `</ul><h3>Body Text</h3><p>${data.word_data.body.join(
            "<br>"
          )}</p>`;
          content += `<h3>Tables</h3>`;
          data.word_data.tables.forEach((table) => {
            content += `<table border="1">`;
            table.forEach((row) => {
              content += `<tr>${row
                .map((cell) => `<td>${cell}</td>`)
                .join("")}</tr>`;
            });
            content += `</table>`;
          });
          wordDataResults.innerHTML = content;
        } else {
          resultMessage.innerHTML = data.message || "Error reading document.";
          parseLink.style.display = "none";
          parseLink2.style.display = "none";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        resultMessage.innerHTML = "An error occurred during processing.";
        aiButton.disabled = false;
        spinnerLoader.style.display = "none";
        parseLink.style.display = "none";
        parseLink2.style.display = "none";
      });
  });
});
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("wordFileInput")
    .addEventListener("change", function () {
      const translateButton = document.getElementById("translateButton");
      const spinnerLoader = document.getElementById("spinner-loader-detect");
      const resultMessage = document.getElementById("resultMessage");
      const fileInput = this.files[0];
      if (!fileInput) return;

      const formData = new FormData();
      formData.append("word_file", fileInput);
      translateButton.disabled = true;
      resultMessage.innerHTML = "Detecting language...";
      resultMessage.style.display = "block";
      spinnerLoader.style.display = "block";
      fetch("/translate/detect", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.language) {
            resultMessage.innerHTML = `Main Detected Language: ${data.language}`;
            translateButton.disabled = false;
            spinnerLoader.style.display = "none";
          } else {
            resultMessage.innerHTML =
              "No language detected, ensure the document is a word document and is not blank";
            translateButton.disabled = false;
            spinnerLoader.style.display = "none";
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          resultMessage.innerHTML = "An error occurred during detection!";
          translateButton.disabled = true;
        });
    });

  document.getElementById("translateModalForm")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      const modalStatusMessage = document.getElementById("modalStatusMessage");
      const spinner = document.getElementById("spinner-while-translating");
      const messageContainer = document.getElementById("messages");
      messageContainer.innerHTML = "";
      modalStatusMessage.textContent = "Starting translation...";
      modalStatusMessage.style.display = "block";
      spinner.style.display = "block";
      const eventSource = new EventSource("/translate/translate");
      eventSource.onmessage = function (event) {
        const message = event.data;
        const newMessage = document.createElement("p");
        newMessage.textContent = message;
        messageContainer.appendChild(newMessage);
        if (message.startsWith("download_url-")) {
          const downloadUrl = message.replace("download_url-", "").trim();
          eventSource.close();
          spinner.style.display = "none";
          modalStatusMessage.textContent =
            "Translation completed! Downloading file...";
          window.location.href = downloadUrl;
        }
        if (message.includes("Translation completed.")) {
          eventSource.close();
          modalStatusMessage.textContent = "Translation completed!";
          spinner.style.display = "none";
        }
      };

      eventSource.onerror = function (error) {
        console.error("EventSource error:", error);
        modalStatusMessage.textContent = "Error occurred during translation:." + error;
        spinner.style.display = "none";
        eventSource.close();
      };
    });
});

function validateForm() {
  var fromPage = document.getElementById("from_page").value;
  var toPage = document.getElementById("to_page").value;

  if (fromPage || toPage) {
    if (!fromPage || !toPage) {
      alert("Both from_page and to_page must be filled out.");
      return false;
    }
  }
  return true;
}

function submitForm(event) {
  event.preventDefault();
  if (!validateForm()) return;

  var form = document.getElementById("pdfForm");
  var formData = new FormData(form);
  var convertBtn = document.getElementById("convertBtn");
  var loadingIndicator = document.getElementById("loadingIndicator");
  var fromPage = document.getElementById("from_page").value;
  var toPage = document.getElementById("to_page").value;

  convertBtn.disabled = true;
  loadingIndicator.style.display = "block";

  formData.append("from_page", fromPage);
  formData.append("to_page", toPage);

  fetch("/reader/read-whole", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        return response.blob();
      } else {
        throw new Error("Conversion failed.");
      }
    })
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = "output.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Conversion error:", error);
      alert("Conversion failed. Please try again.");
    })
    .finally(() => {
      convertBtn.disabled = false;
      loadingIndicator.style.display = "none";
    });
}

function submitWordForm(event) {
  event.preventDefault();
  var form = document.getElementById("wordForm");
  var formData = new FormData(form);
  var convertBtn = document.getElementById("convertWordBtn");
  var loadingIndicator = document.getElementById("loadingWordIndicator");
  convertBtn.disabled = true;
  loadingIndicator.style.display = "block";

  fetch("/reader/remove-word", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        var disposition = response.headers.get("Content-Disposition");
        var filename = "sanitized_word.doc";

        if (disposition) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, "");
          }
        }

        return response.blob().then((blob) => ({ blob, filename }));
      } else {
        throw new Error("Removal failed.");
      }
    })
    .then(({ blob, filename }) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Removal Error:", error);
      alert("Removal Failed. Please try again.");
    })
    .finally(() => {
      convertBtn.disabled = false;
      loadingIndicator.style.display = "none";
    });
}

function submitPagesForm(event) {
  event.preventDefault();
  var form = document.getElementById("pagesForm");
  var formData = new FormData(form);
  var convertBtn = document.getElementById("convertPagesBtn");
  var loadingIndicator = document.getElementById("loadingPagesIndicator");
  convertBtn.disabled = true;
  loadingIndicator.style.display = "block";

  fetch("/reader/remove", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        var disposition = response.headers.get("Content-Disposition");
        var filename = "initialized.pdf";

        if (disposition) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, "");
          }
        }

        return response.blob().then((blob) => ({ blob, filename }));
      } else {
        throw new Error("Removal failed.");
      }
    })
    .then(({ blob, filename }) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Removal Error:", error);
      alert("Removal Failed. Please try again.");
    })
    .finally(() => {
      convertBtn.disabled = false;
      loadingIndicator.style.display = "none";
    });
}

function submitExcelForm(event) {
  event.preventDefault();
  var form = document.getElementById("excelForm");
  var formData = new FormData(form);
  var convertBtn = document.getElementById("convertExcelBtn");
  var loadingIndicator = document.getElementById("loadingExcelIndicator");
  convertBtn.disabled = true;
  loadingIndicator.style.display = "block";

  fetch("/excel/excel-home", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        var disposition = response.headers.get("Content-Disposition");
        var filename = "initialized.pdf";

        if (disposition) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, ""); // Extract and clean filename
          }
        }

        return response.blob().then((blob) => ({ blob, filename }));
      } else {
        throw new Error("Conversion failed.");
      }
    })
    .then(({ blob, filename }) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Conversion Error:", error);
      alert("Conversion Failed. Please try again.");
    })
    .finally(() => {
      convertBtn.disabled = false;
      loadingIndicator.style.display = "none";
    });
}

function submitInitialManyImgForm(event) {
  event.preventDefault();
  var form = document.getElementById("initializeManyImgForm");
  var formData = new FormData(form);
  var initialBtn = document.getElementById("initialManyImgBtn");
  var loadingInitIndicator = document.getElementById(
    "loadingInitManyImgIndicator"
  );

  initialBtn.disabled = true;
  loadingInitIndicator.style.display = "block";

  fetch("/initial/initial-many-image", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        var disposition = response.headers.get("Content-Disposition");
        var filename = "initialized.pdf";

        if (disposition) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, ""); // Extract and clean filename
          }
        }

        return response.blob().then((blob) => ({ blob, filename }));
      } else {
        throw new Error("Initialization failed.");
      }
    })
    .then(({ blob, filename }) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Initialization Error:", error);
      alert("Initialization failed. Please try again.");
    })
    .finally(() => {
      initialBtn.disabled = false;
      loadingInitIndicator.style.display = "none";
    });
}

function pagerForm(event) {
  event.preventDefault();
  var form = document.getElementById("pagerForm");
  var formData = new FormData(form);
  var pagerBtn = document.getElementById("pagerBtn");
  var loadingPagerIndicator = document.getElementById("loadingPagerIndicator");

  pagerBtn.disabled = true;
  loadingPagerIndicator.style.display = "block";

  fetch("/pager/page-home", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        var disposition = response.headers.get("Content-Disposition");
        var filename = "paginated.pdf";

        if (disposition) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, ""); // Extract and clean filename
          }
        }

        return response.blob().then((blob) => ({ blob, filename }));
      } else {
        throw new Error("Pagination failed.");
      }
    })
    .then(({ blob, filename }) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Initialization Error:", error);
      alert("Initialization failed. Please try again.");
    })
    .finally(() => {
      pagerBtn.disabled = false;
      loadingPagerIndicator.style.display = "none";
    });
}

function submitInitialImgForm(event) {
  event.preventDefault();
  var form = document.getElementById("initializeImgForm");
  var formData = new FormData(form);
  var initialBtn = document.getElementById("initialImgBtn");
  var loadingInitIndicator = document.getElementById("loadingInitImgIndicator");

  initialBtn.disabled = true;
  loadingInitIndicator.style.display = "block";

  fetch("/initial/initial-image", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        var disposition = response.headers.get("Content-Disposition");
        var filename = "initialized.pdf";

        if (disposition) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, ""); // Extract and clean filename
          }
        }

        return response.blob().then((blob) => ({ blob, filename }));
      } else {
        throw new Error("Initialization failed.");
      }
    })
    .then(({ blob, filename }) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Initialization Error:", error);
      alert("Initialization failed. Please try again.");
    })
    .finally(() => {
      initialImgBtn.disabled = false;
      loadingInitImgIndicator.style.display = "none";
    });
}

function submitInitialForm(event) {
  event.preventDefault();
  var form = document.getElementById("initializeForm");
  var formData = new FormData(form);
  var initialBtn = document.getElementById("initialBtn");
  var loadingInitIndicator = document.getElementById("loadingInitIndicator");

  initialBtn.disabled = true;
  loadingInitIndicator.style.display = "block";

  fetch("/initial/one_doc_initial", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        var disposition = response.headers.get("Content-Disposition");
        var filename = "initialized.pdf"; // Default filename

        if (disposition) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, ""); // Extract and clean filename
          }
        }

        return response.blob().then((blob) => ({ blob, filename }));
      } else {
        throw new Error("Initialization failed.");
      }
    })
    .then(({ blob, filename }) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Initialization Error:", error);
      alert("Initialization failed. Please try again.");
    })
    .finally(() => {
      initialBtn.disabled = false;
      loadingInitIndicator.style.display = "none";
    });
}

function submitMultipleInitialForm(event) {
  event.preventDefault();
  var form = document.getElementById("multipleInitializeForm");
  var formData = new FormData(form);
  var multipleInitialBtn = document.getElementById("multipleInitialBtn");
  var loadingMultipleInitIndicator = document.getElementById(
    "loadingMultipleInitIndicator"
  );
  var initial = document.getElementById("multi_initial").value;
  var size = document.getElementById("multi_size").value;
  var x_axis = document.getElementById("multi_x_axis").value;
  var y_axis = document.getElementById("multi_y_axis").value;
  var font = document.getElementById("multi_font").value;

  multipleInitialBtn.disabled = true;
  loadingMultipleInitIndicator.style.display = "block";

  formData.append("initial", initial);
  formData.append("size", size);
  formData.append("x_axis", x_axis);
  formData.append("y_axis", y_axis);
  formData.append("font", font);

  fetch("/initial/many_doc_initial", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        return response.blob(); // Expect a zip file as a blob
      } else {
        throw new Error("Initialization of multiple documents failed.");
      }
    })
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = "initialized_files.zip"; // Set the name for the downloaded zip file
      a.click();
      window.URL.revokeObjectURL(url); // Clean up the object URL after download
    })
    .catch((error) => {
      console.error("Initialization Error:", error);
      alert("Initialization of multiple documents failed. Please try again.");
    })
    .finally(() => {
      multipleInitialBtn.disabled = false;
      loadingMultipleInitIndicator.style.display = "none";
    });
}
