(function () {
    'use strict';

    var forms = document.querySelectorAll('.needs-validation');

    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    });

})();

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

        // Append 'from_page' and 'to_page' to form data
        formData.append('from_page', fromPage);
        formData.append('to_page', toPage);

        fetch("/reader/read-whole", {
            method: "POST",
            body: formData
        }).then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error("Conversion failed.");
            }
        }).then(blob => {
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = url;
            a.download = "output.xlsx";
            a.click();
            window.URL.revokeObjectURL(url);
        }).catch(error => {
            console.error("Conversion error:", error);
            alert("Conversion failed. Please try again.");
        }).finally(() => {
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
        body: formData
    }).then(response => {
        if (response.ok) {
            var disposition = response.headers.get('Content-Disposition');
            var filename = "initialized.pdf";

            if (disposition) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '');
                }
            }

            return response.blob().then(blob => ({ blob, filename }));
        } else {
            throw new Error("Removal failed.");
        }
    }).then(({ blob, filename }) => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }).catch(error => {
        console.error("Removal Error:", error);
        alert("Removal Failed. Please try again.");
    }).finally(() => {
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
        body: formData
    }).then(response => {
        if (response.ok) {
            var disposition = response.headers.get('Content-Disposition');
            var filename = "initialized.pdf";

            if (disposition) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, ''); // Extract and clean filename
                }
            }

            return response.blob().then(blob => ({ blob, filename }));
        } else {
            throw new Error("Conversion failed.");
        }
    }).then(({ blob, filename }) => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }).catch(error => {
        console.error("Conversion Error:", error);
        alert("Conversion Failed. Please try again.");
    }).finally(() => {
        convertBtn.disabled = false;
        loadingIndicator.style.display = "none";
    });
}

function submitInitialManyImgForm(event) {
    event.preventDefault();
    var form = document.getElementById("initializeManyImgForm");
    var formData = new FormData(form);
    var initialBtn = document.getElementById("initialManyImgBtn");
    var loadingInitIndicator = document.getElementById("loadingInitManyImgIndicator");

    initialBtn.disabled = true;
    loadingInitIndicator.style.display = "block";

    fetch("/initial/initial-many-image", {
        method: "POST",
        body: formData
    }).then(response => {
        if (response.ok) {
            var disposition = response.headers.get('Content-Disposition');
            var filename = "initialized.pdf";

            if (disposition) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, ''); // Extract and clean filename
                }
            }

            return response.blob().then(blob => ({ blob, filename }));
        } else {
            throw new Error("Initialization failed.");
        }
    }).then(({ blob, filename }) => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }).catch(error => {
        console.error("Initialization Error:", error);
        alert("Initialization failed. Please try again.");
    }).finally(() => {
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
        body: formData
    }).then(response => {
        if (response.ok) {
            var disposition = response.headers.get('Content-Disposition');
            var filename = "paginated.pdf";

            if (disposition) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, ''); // Extract and clean filename
                }
            }

            return response.blob().then(blob => ({ blob, filename }));
        } else {
            throw new Error("Pagination failed.");
        }
    }).then(({ blob, filename }) => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }).catch(error => {
        console.error("Initialization Error:", error);
        alert("Initialization failed. Please try again.");
    }).finally(() => {
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
        body: formData
    }).then(response => {
        if (response.ok) {
            var disposition = response.headers.get('Content-Disposition');
            var filename = "initialized.pdf";

            if (disposition) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, ''); // Extract and clean filename
                }
            }

            return response.blob().then(blob => ({ blob, filename }));
        } else {
            throw new Error("Initialization failed.");
        }
    }).then(({ blob, filename }) => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }).catch(error => {
        console.error("Initialization Error:", error);
        alert("Initialization failed. Please try again.");
    }).finally(() => {
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
        body: formData
    }).then(response => {
        if (response.ok) {
            var disposition = response.headers.get('Content-Disposition');
            var filename = "initialized.pdf"; // Default filename

            if (disposition) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, ''); // Extract and clean filename
                }
            }

            return response.blob().then(blob => ({ blob, filename }));
        } else {
            throw new Error("Initialization failed.");
        }
    }).then(({ blob, filename }) => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }).catch(error => {
        console.error("Initialization Error:", error);
        alert("Initialization failed. Please try again.");
    }).finally(() => {
        initialBtn.disabled = false;
        loadingInitIndicator.style.display = "none";
    });
}

function submitMultipleInitialForm(event) {
    event.preventDefault();
    var form = document.getElementById("multipleInitializeForm");
    var formData = new FormData(form);
    var multipleInitialBtn = document.getElementById("multipleInitialBtn");
    var loadingMultipleInitIndicator = document.getElementById("loadingMultipleInitIndicator");
    var initial = document.getElementById("multi_initial").value;
    var size = document.getElementById("multi_size").value;
    var x_axis = document.getElementById("multi_x_axis").value;
    var y_axis = document.getElementById("multi_y_axis").value;
    var font = document.getElementById("multi_font").value;

    multipleInitialBtn.disabled = true;
    loadingMultipleInitIndicator.style.display = "block";

    formData.append('initial', initial);
    formData.append('size', size);
    formData.append('x_axis', x_axis);
    formData.append('y_axis', y_axis);
    formData.append('font', font);

    fetch("/initial/many_doc_initial", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.blob();  // Expect a zip file as a blob
        } else {
            throw new Error("Initialization of multiple documents failed.");
        }
    })
    .then(blob => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "initialized_files.zip";  // Set the name for the downloaded zip file
        a.click();
        window.URL.revokeObjectURL(url);  // Clean up the object URL after download
    })
    .catch(error => {
        console.error("Initialization Error:", error);
        alert("Initialization of multiple documents failed. Please try again.");
    })
    .finally(() => {
        multipleInitialBtn.disabled = false;
        loadingMultipleInitIndicator.style.display = "none";
    });
}