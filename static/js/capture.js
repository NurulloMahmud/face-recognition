window.addEventListener("load", function(){
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const captureButton = document.getElementById('capture');
    const uploadButton = document.getElementById('upload');
    const imageInput = document.getElementById('imageInput');

    // Initially hide the upload button
    uploadButton.style.display = 'none';

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        });

    captureButton.addEventListener('click', function() {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        video.style.display = 'none';
        canvas.style.display = 'block';
        captureButton.style.display = 'none'; // Hide capture button
        uploadButton.style.display = 'block'; // Show upload button
    });

    uploadButton.addEventListener('click', function() {
        canvas.toBlob(function(blob) {
            const file = new File([blob], "user_image.png", {type: 'image/png'});
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            imageInput.files = dataTransfer.files;

            // Submit the form
            document.getElementById('uploadForm').submit();
        }, 'image/png');
    });
});
