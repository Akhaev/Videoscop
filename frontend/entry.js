document.addEventListener('DOMContentLoaded', () => {
  console.log(localStorage.getItem('videoscop_token'));

  const plottingCanvas = document.getElementById("plotting_canvas");
  const webgazerGazeDot = document.getElementById("webgazerGazeDot");
  const main = document.querySelector(".main")
  const modalFade = document.querySelector(".modal");
  const videoUploader = document.getElementById('heatmapUpload');

  let selectedVideoFile = null;

  const restoreCanvas = () => {
    const existingCanvas = document.getElementById('plotting_canvas');
    if (!existingCanvas) {
      const canvas = document.createElement('canvas');
      canvas.id = 'plotting_canvas';
      canvas.width = 500;
      canvas.height = 500;
      canvas.style.cursor = 'crosshair';

      const nav = document.getElementById('webgazerNavbar');
      if (nav) {
        nav.parentNode.insertBefore(canvas, nav);
      } else {
        document.body.appendChild(canvas);
      }
    }
  };

  videoUploader.addEventListener('change', (event) => {
    if (sessionStorage.getItem('video_uploaded') === 'true') {
      alert('Вы уже загрузили видео в этой сессии!');
      videoUploader.value = '';
      const canvas = document.getElementById('plotting_canvas');
      if (canvas) canvas.style.pointerEvents = 'auto';
      return;
    }

    const file = event.target.files[0];
    if (file) {
      selectedVideoFile = file;
      startVideoUpload(); 
    } else {
      selectedVideoFile = null;
      modalFade.style.display = "block";
      restoreCanvas();
    }
  });

  async function startVideoUpload() {
  const loadingEl = document.querySelector('.loading');

  if (loadingEl) loadingEl.style.display = 'block';

  if (main) main.style.opacity = '0.5';

  try {
    if (sessionStorage.getItem('video_uploaded') === 'true') {
      alert('Вы уже загрузили видео в этой сессии!');
      return;
    }

    const videoName = prompt("name video")?.trim();

    if (!videoName || videoName.length < 3) {
      alert('Please enter a valid video name (at least 3 characters)');
      return;
    }

    if (!selectedVideoFile) {
      alert('No video file selected');
      return;
    }

    console.log('Preparing to upload video metadata...');
    const durationSeconds = Math.floor(selectedVideoFile.duration || 0); 
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

    sessionStorage.setItem('video_uploaded', 'true');
    selectedVideoFile = null;
    videoUploader.value = '';
    restoreCanvas();
    alert('Видео успешно загружено!');
  } catch (error) {
    console.error('Error uploading video:', error);
    alert(`Upload failed: ${error.message}`);
  } finally {
    if (loadingEl) loadingEl.style.display = 'none';
    if (main) main.style.opacity = '1';
  }
}
});
