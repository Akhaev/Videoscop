document.addEventListener('DOMContentLoaded', () => {
  const removeVideoBtn = document.getElementById('remove-video');
  const videoUploader = document.getElementById('video-uploader');
  const uploadedVideo = document.getElementById('uploaded-video');
  const customUploadBtn = document.querySelector('.custom-file-upload');
  const startTraining = document.getElementById('start-training');

  videoUploader?.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file && uploadedVideo) {
      uploadedVideo.src = URL.createObjectURL(file);
      uploadedVideo.style.display = 'block';
      uploadedVideo.play();
      removeVideoBtn.style.display = 'block';
      customUploadBtn.style.display = 'none';
    }
  });

  removeVideoBtn?.addEventListener('click', () => {
    if (uploadedVideo) {
      uploadedVideo.pause();
      uploadedVideo.src = '';
      uploadedVideo.style.display = 'none';
    }
    videoUploader.value = '';
    removeVideoBtn.style.display = 'none';
    customUploadBtn.style.display = 'flex';
  });

  startTraining?.addEventListener('click', () => {
    if (videoUploader) {
      videoUploader.style.display = 'none';
    }
  });

  // Тепловая карта
  const canvas = document.getElementById('heatMap');
  const ctx = canvas?.getContext('2d');
  if (canvas && ctx) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let recording = false;
    const points = [];

    const startButton = document.getElementById('start-training');
    const stopButton = document.getElementById('stop-recording');
    const finishButton = document.getElementById('finish-recording');
    const recordingButton = document.getElementById('recording-button');

    startButton?.addEventListener('click', () => {
      recording = true;
      points.length = 0;
      startButton.disabled = true;
      stopButton.disabled = false;
      finishButton.disabled = false;
      drawHeatMap();
    });

    stopButton?.addEventListener('click', () => {
      recording = false;
      startButton.disabled = false;
      stopButton.disabled = true;
    });

    finishButton?.addEventListener('click', () => {
      recording = false;
      startButton.disabled = false;
      stopButton.disabled = true;
      finishButton.disabled = true;
      if (recordingButton) recordingButton.style.display = 'none';
    });
  }
});

