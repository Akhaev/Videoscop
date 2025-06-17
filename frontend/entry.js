document.addEventListener('DOMContentLoaded', () => {
  console.log(localStorage.getItem('videoscop_token'));

  const recording = document.querySelector('#recording');
  const pauseIcon = document.querySelector('.pause-icon');
  const letterO = document.getElementById('letter-o');
  const startRecordingButton = document.querySelector('.start-recording');
  const pauseRecordingButton = document.getElementById('stop-recording');
  const finishRecordingButton = document.getElementById('finish-recording');
  const recordingButton = document.getElementById('recording-button');
  const nameVideo = document.querySelector('.name-for-video');
  const main = document.querySelector('.main');
  const videoNameInp = document.getElementById('video-name-input');
  const addVideoBtn = document.querySelector('#add-video');
  const loading = document.querySelector('.loading')
  const header = document.querySelector('header')

  let mediaRecorder;
  let recordedChunks = [];
  let isRecording = false;
  let isPaused = false;
  let startTime;
  let videoBlob = null;

  nameVideo.style.display = 'none';
  main.style.opacity = '1';

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

        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start(100);

      startTime = Date.now();
      isRecording = true;

      setTimeout(() => {
        letterO.style.display = 'none';
        recording.style.display = 'inline-block';
      }, 2000);

      pauseRecordingButton.disabled = false;
      finishRecordingButton.disabled = false;
      startRecordingButton.disabled = true;
    } catch (error) {
      console.error('Ошибка в startRecording:', error);
      pauseRecordingButton.disabled = true;
      finishRecordingButton.disabled = true;
      startRecordingButton.disabled = false;
    }
  };

  startRecordingButton.addEventListener('click', startRecording);

  pauseRecordingButton.addEventListener('click', () => {
    if (mediaRecorder && isRecording) {
      if (isPaused) {
        mediaRecorder.resume();
        recording.style.display = 'inline-block';
        pauseIcon.style.display = 'none';
      } else {
        mediaRecorder.pause();
        recording.style.display = 'none';
        pauseIcon.style.display = 'inline-block';
      }
      isPaused = !isPaused;
    }
  });

  finishRecordingButton.addEventListener('click', () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      isRecording = false;
      isPaused = false;

      letterO.style.display = 'block';
      recording.style.display = 'none';
      pauseIcon.style.display = 'none';

      startRecordingButton.disabled = false;
      pauseRecordingButton.disabled = true;
      finishRecordingButton.disabled = true;
    }
  });

  addVideoBtn.addEventListener('click', async () => {
    const videoName = videoNameInp.value.trim();

    if (!videoName || videoName.length < 3) {
      alert('Please enter a valid video name (at least 3 characters)');
      return;
    }

    if (!videoBlob) {
      alert('No recording available to upload');
      return;
    }

    try {
      console.log('Preparing to upload video...');

      const reader = new FileReader();

      reader.onloadend = async () => {
        const base64data = reader.result.split(',')[1];
        const durationSeconds = Math.floor((Date.now() - startTime) / 1000);
        const sizeMB = Math.round(videoBlob.size / (1024 * 1024));

        const payload = {
          name: videoName,
          length_seconds: Math.min(durationSeconds, 3600),
          size: Math.max(1, Math.min(sizeMB, 1000)),
          video_base64: base64data,
        };

        
        const response = await fetch('http://217.114.10.197:8000/users/me/videos', { 
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('videoscop_token') || sessionStorage.getItem('videoscop_token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        }).then(loading.style.display = 'block', main.style.opacity = '.2', header.style.opacity = '.2');

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || data.detail || `Failed to upload video metadata: ${response.status}`);
        }

        const result = data;
        localStorage.setItem('video', JSON.stringify(result));

        const uploadUrl = result.upload_link;

        if (!uploadUrl || typeof uploadUrl !== 'string') {
          throw new Error('No valid upload URL provided in response');
        }

        console.log('Uploading video to:', uploadUrl);
        const uploadResponse = await fetch(uploadUrl, {
          method: 'PUT',
          headers: {
            'Content-Type': 'video/webm',
          },
          body: videoBlob,
        }).then(loading.style.display = 'none', main.style.opacity = '1', header.style.opacity = '1');

        const responseText = await uploadResponse.text();

        if (!uploadResponse.ok) {
          throw new Error(`Failed to upload video to storage: ${responseText}`);
        }

        nameVideo.style.display = 'none';
        main.style.opacity = '1';
        videoNameInp.value = '';
        videoBlob = null;
      };

      reader.onerror = () => {
        throw new Error('Failed to read video file');
      };

      reader.readAsDataURL(videoBlob);
    } catch (error) {
      console.error('Error uploading video:', error);
      alert(`Upload failed: ${error.message}`);
    }

    nameVideo.style.display = 'none';
    main.style.opacity = '1';
  });

  videoNameInp.addEventListener('input', () => {
    addVideoBtn.disabled = !videoNameInp.value.trim();
  });
  addVideoBtn.disabled = true;
});



