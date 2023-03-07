'use strict';

const video = document.getElementById('video');
const snap = document.getElementById("snap");
const canvas = document.getElementById('canvas');
const errorMsgElement = document.querySelector('span#errorMsg');

const constraints = {
    audio: false,
    video: {
    width: 800, height: 600
        },
    Image: {
        width: 800, height: 600
            }
    };

// Acceso a la webcam
async function init() {
try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
    } catch (e) {
    errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
    }
// Correcto!
function handleSuccess(stream) {
    window.stream = stream;
    video.srcObject = stream;
    }
// Load init
init();
// Dibuja la imagen
var context = canvas.getContext('2d');
    snap.addEventListener("click", function() {
    context.drawImage(video, 0, 0, 640, 480);
    const dataURL = canvas.toDataURL();
    document.getElementById("url_image").setAttribute('value', dataURL);
    });

function confirmFunction() {
    if (confirm("¿Deseas enviar la imagen?") == true) {
        document.getElementById("ColorChanger").style.backgroundColor = "green";
    } else {
        document.getElementById("ColorChanger").style.backgroundColor = "#C0C0C0";
    }
}