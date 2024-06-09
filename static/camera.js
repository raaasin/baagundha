let video = document.getElementById('camera');
let canvas = document.createElement('canvas');
let captureButton = document.getElementById('capture-button');
let captureOptions = document.getElementById('capture-options');
let imageInput = document.getElementById('image-data');
let stream;

navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function (err) {
        console.error("Error accessing camera: " + err);
    });

function capture() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    let context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    let dataURL = canvas.toDataURL('image/png');
    imageInput.value = dataURL;
    video.pause();
    captureButton.style.display = 'none';
    captureOptions.style.display = 'block';
}

function retry() {
    video.play();
    captureButton.style.display = 'block';
    captureOptions.style.display = 'none';
}
