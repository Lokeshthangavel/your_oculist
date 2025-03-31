document.addEventListener('DOMContentLoaded', function () {
    const snellenForm = document.getElementById('snellen-form');
    const duochromeForm = document.getElementById('duochrome-form');
    const rightEye = document.getElementById('right-eye');
    const leftEye = document.getElementById('left-eye');
    const duochrome = document.getElementById('duochrome');
    const nextButton = document.querySelector('#snellen-form .btn-primary');
    const submitButton = document.querySelector('#duochrome-form .btn-primary');
    const resultSection = document.getElementById('result-section');
    
    // Function to show the next test section
    function showDuochromeTest() {
        document.getElementById('snellen-test').classList.remove('active');
        document.getElementById('duochrome-test').classList.add('active');

        // Pass values to hidden inputs
        document.getElementById('hidden-right-eye').value = rightEye.value;
        document.getElementById('hidden-left-eye').value = leftEye.value;
    }

    // Function to show result section
    function showResults() {
        document.getElementById('duochrome-test').classList.remove('active');
        resultSection.classList.add('active');
        
        // Display results dynamically
        document.getElementById('result-right-eye').textContent = rightEye.value;
        document.getElementById('result-left-eye').textContent = leftEye.value;
        document.getElementById('result-duochrome').textContent = duochrome.value;
    }

    // Function to create or show an error message
    function createErrorMessage(element, message) {
        let errorSpan = element.nextElementSibling;
        if (!errorSpan || !errorSpan.classList.contains('error-message')) {
            errorSpan = document.createElement('span');
            errorSpan.classList.add('error-message');
            element.parentNode.insertBefore(errorSpan, element.nextSibling);
        }
        errorSpan.textContent = message;
        errorSpan.style.display = 'block';
        element.classList.add('input-error');
    }

    // Function to remove an error message
    function removeErrorMessage(element) {
        let errorSpan = element.nextElementSibling;
        if (errorSpan && errorSpan.classList.contains('error-message')) {
            errorSpan.style.display = 'none';
        }
        element.classList.remove('input-error');
    }

    // Function to validate inputs
    function validateInputs(inputs) {
        let isValid = true;
        inputs.forEach(input => {
            if (!input.value) {
                createErrorMessage(input, `Please select a value.`);
                isValid = false;
            } else {
                removeErrorMessage(input);
            }
        });
        return isValid;
    }

    // Snellen test validation and navigation
    nextButton.addEventListener('click', function (event) {
        if (validateInputs([rightEye, leftEye])) {
            showDuochromeTest();
        }
    });

    // Duochrome test validation before submission
    duochromeForm.addEventListener('submit', function (event) {
        if (!validateInputs([duochrome])) {
            event.preventDefault();
        } else {
            showResults();
            event.preventDefault(); // Prevent actual form submission for demo
        }
    });
});
