// Validation and UI enhancements
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('vision-form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            const rightEye = document.getElementById('right-eye').value;
            const leftEye = document.getElementById('left-eye').value;
            
            if (!rightEye || !leftEye) {
                event.preventDefault();
                alert('Please select vision values for both eyes.');
            }
        });
    }
});