
console.log(localStorage.getItem('videoscop_token'));
const searchInput = document.getElementById('search-input');
const token = localStorage.getItem('videoscop_token');

function debounce(func, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}

async function fetchVideoByName(name) {
  try {
    const response = await fetch(`http://217.114.10.197:8000/users/me/videos/unload_link?name=${encodeURIComponent(name)}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) { 
      throw new Error('Видео не найдено или произошла ошибка при запросе');
    }

    const video = await response.json(); 
    renderSingleVideo(video);
  } catch (err) {
    console.error('Ошибка:', err);
    renderNoResults();
  }
}

function renderSingleVideo(video) {
  const container = document.getElementById('video-list');
  container.innerHTML = '';

  const videoElem = document.createElement('video');
  videoElem.controls = true;
  videoElem.src = video.unload_link;
  videoElem.style.width = '300px';
  videoElem.style.margin = '10px';

  const label = document.createElement('p');
  label.textContent = video.name;

  const wrapper = document.createElement('div');
  wrapper.appendChild(label);
  wrapper.appendChild(videoElem);

videoElem.addEventListener('click', () => {
  console.log('Видео было нажато'); 
  const mainPlayer = document.getElementById('video-player');
  const mainSource = document.getElementById('video-source');

  const extension = video.unload_link.split('.').pop();
  const mimeType = extension === 'mp4' ? 'video/mp4' : 'video/webm';

  mainSource.src = video.unload_link;
  mainSource.type = mimeType;
  mainPlayer.load();
  mainPlayer.play();

  const latestSessions = document.querySelector('.latest-sessions');
  latestSessions.classList.remove('visible');
});


  container.appendChild(wrapper);
}

searchInput.addEventListener('input', debounce(() => {
  const searchValue = searchInput.value.trim();
  const latestSessions = document.querySelector('.latest-sessions');

  if (searchValue) {
    latestSessions.classList.add('visible');
    fetchVideoByName(searchValue);
  } else {
    latestSessions.classList.remove('visible');
    document.getElementById('video-list').innerHTML = '';
  }
}, 500));



function renderNoResults() {
  const container = document.getElementById('video-list');
  container.innerHTML = '<p>Видео не найдено</p>';
}

searchInput.addEventListener('input', debounce(() => {
  const searchValue = searchInput.value.trim();
  if (searchValue) {
    fetchVideoByName(searchValue);
  } else {
    document.getElementById('video-list').innerHTML = '';
  }
}, 500));









// try {
//   const searchRequest = await fetch('http://217.114.10.197:8000/users/me/videos/search', {
//     headers: {
//       'Authorization': `Bearer ${videoscopToken}`,
//       'Content-Type': 'application/json',
//     },
//   })
//   const responseSearch = await searchRequest.json()
//   const findVideo = responseSearch.videos.find(video => video.name === searchInput.value)

//   if (findVideo) {
//     arhiv.innerHTML = `
//       <video controls src=${findVideo.upload_link}></video>
//     `
//   } else {
//     arhiv.innerHTML = `<p>видео не найдено</p>`
//   }
  
// } catch (error){
//   throw new Error('с поиском че то не так')
//   alert('с поиском че то не так')
// }


