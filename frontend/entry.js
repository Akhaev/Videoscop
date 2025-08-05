document.addEventListener('DOMContentLoaded', () => {
  console.log(localStorage.getItem('videoscop_token'));

  const recording = document.querySelector('#recording');
  const pauseIcon = document.querySelector('.pause-icon');
  const letterO = document.getElementById('letter-o');
  const nameVideo = document.querySelector('.name-for-video');
  const plottingCanvas = document.getElementById("plotting_canvas")
  const main = document.querySelector('.main');
  const videoNameInp = document.getElementById('video-name-input');
  const addVideoBtn = document.querySelector('#add-video');
  const loading = document.querySelector('.loading')
  const header = document.querySelector('header')
  const heatmapVideo = document.querySelector("#heatmapVideo")
  const heatmapImage = document.querySelector("#heatmapImage")
  const webgazerGazeDot = document.getElementById("webgazerGazeDot")
  const modalFade = document.querySelector(".modal")
  let mediaRecorder;

  let recordedChunks = [];
  let isRecording = false;
  let isPaused = false;
  let startTime;
  let videoBlob = null;

  // Функция для восстановления canvas
  const restoreCanvas = () => {
    const existingCanvas = document.getElementById('plotting_canvas');
    if (!existingCanvas) {
      const canvas = document.createElement('canvas');
      canvas.id = 'plotting_canvas';
      canvas.width = 500;
      canvas.height = 500;
      canvas.style.cursor = 'crosshair';

      // Вставляем canvas перед nav элементом
      const nav = document.getElementById('webgazerNavbar');
      if (nav) {
        nav.parentNode.insertBefore(canvas, nav);
      } else {
        // Если nav не найден, вставляем в конец body
        document.body.appendChild(canvas);
      }

      // Обновляем глобальную переменную
      plottingCanvas = canvas;
    }
  };



  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: false,
      });

      recordedChunks = [];
      videoBlob = null;

      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        videoBlob = new Blob(recordedChunks, { type: 'video/webm' });

        nameVideo.style.display = 'block';
        main.style.opacity = '.1';
        // main.style.pointerEvents = 'none'; // УДАЛЕНО
      };

      mediaRecorder.start(100);

      startTime = Date.now();
      isRecording = true;

      setTimeout(() => {
        letterO.style.display = 'none';
        recording.style.display = 'inline-block';
      }, 2000);
    } catch (error) {
      console.error('Ошибка в startRecording:', error);
    }
  };



  const videoUploader = document.getElementById('heatmapUpload');
  let selectedVideoFile = null;

  videoUploader.addEventListener('change', (event) => {
    if (sessionStorage.getItem('video_uploaded') === 'true') {
      alert('Вы уже загрузили видео в этой сессии!');
      videoUploader.value = '';
      nameVideo.style.display = 'none';
      main.style.opacity = '1';
      // main.style.pointerEvents = 'auto'; // УДАЛЕНО
      // Восстанавливаем pointer-events для canvas
      const canvas = document.getElementById('plotting_canvas');
      if (canvas) canvas.style.pointerEvents = 'auto';
      return;
    }
    const file = event.target.files[0];
    if (file) {
      selectedVideoFile = file;
      nameVideo.style.display = 'block'; // Показываем блок для названия
      main.style.opacity = '.1';
      webgazerGazeDot.style.opacity = "0";
      modalFade.style.display = "none"

      // Полностью удаляем canvas из DOM чтобы он не блокировал input
      const canvas = document.getElementById('plotting_canvas');
      if (canvas) {
        canvas.remove();
      }

      // Фокусируемся на input после небольшой задержки
      setTimeout(() => {
        videoNameInp.focus();
      }, 100);
    } else {
      selectedVideoFile = null;
      nameVideo.style.display = 'none';
      main.style.opacity = '1';
      modalFade.style.display = "block"
      // Восстанавливаем canvas
      restoreCanvas();
    }

  });
  addVideoBtn.addEventListener('click', async () => {
    nameVideo.style.display = 'none';
    modalFade.style.display = "block"
    webgazerGazeDot.style.opacity = "1";
    main.style.opacity = '1';

    // Восстанавливаем canvas после загрузки
    restoreCanvas();

    if (sessionStorage.getItem('video_uploaded') === 'true') {
      alert('Вы уже загрузили видео в этой сессии!');
      return; // Гарантированный выход до любых сетевых запросов
    }
    const videoName = videoNameInp.value.trim();

    if (!videoName || videoName.length < 3) {
      alert('Please enter a valid video name (at least 3 characters)');
      return;
    }

    if (!selectedVideoFile) {
      alert('No video file selected');
      return;
    }

    try {

      console.log('Preparing to upload video metadata...');
      const durationSeconds = Math.floor(selectedVideoFile.duration || 0); // duration может быть не определён
      const sizeMB = Math.round(selectedVideoFile.size / (1024 * 1024));

      const payload = {
        name: videoName,
        length_seconds: Math.min(durationSeconds, 3600),
        size: Math.max(1, Math.min(sizeMB, 1000)),
      };

      const response = await fetch('http://217.114.10.197:8000/users/me/videos', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('videoscop_token') || sessionStorage.getItem('videoscop_token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.detail || `Failed to upload video metadata: ${response.status}`);
      }

      const uploadUrl = data.upload_link;
      if (!uploadUrl || typeof uploadUrl !== 'string') {
        throw new Error('No valid upload URL provided in response');
      }

      console.log('Uploading video to:', uploadUrl);
      const uploadResponse = await fetch(uploadUrl, {
        method: 'PUT',
        headers: {
          'Content-Type': selectedVideoFile.type || 'video/webm',
        },
        body: selectedVideoFile,
      });

      const responseText = await uploadResponse.text();
      if (!uploadResponse.ok) {
        throw new Error(`Failed to upload video to storage: ${responseText}`);
      }

      nameVideo.style.display = 'none';
      main.style.opacity = '1';
      videoNameInp.value = '';
      selectedVideoFile = null;
      videoUploader.value = '';
      sessionStorage.setItem('video_uploaded', 'true');

      // Восстанавливаем canvas полностью
      restoreCanvas();

      alert('Видео успешно загружено!');
    } catch (error) {
      console.error('Error uploading video:', error);
      alert(`Upload failed: ${error.message}`);
    }
  });

  videoNameInp.addEventListener('input', () => {
    addVideoBtn.disabled = !videoNameInp.value.trim();
  });

  
});




