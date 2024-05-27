(function () {
        'use strict'
        var forms = document.querySelectorAll('.needs-validation')

        Array.prototype.slice.call(forms)
            .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }

                    form.classList.add('was-validated')
                }, false)
            })
    })()

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
}