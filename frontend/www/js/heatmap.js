(function () {
    'use strict';

    const FIXED_WIDTH = 800;
    const FIXED_HEIGHT = 600;
    const MAX_POINTS = 400;
    const TAU = 3;
    const GRID_SIZE = 20;

    const modal = document.getElementById('heatmapModal');
    const saveBtn = document.getElementById('saveHeatmap');
    const replayBtn = document.getElementById('replayHeatmap');
    const stopBtn = document.getElementById('stopReplayHeatmap');
    const uploadInput = document.getElementById('heatmapUpload');

    const img = document.getElementById('heatmapImage');
    const video = document.getElementById('heatmapVideo');
    const canvas = document.getElementById('heatmapCanvas');

    let heat = null;
    let isReplaying = false;
    let replayTimer = null;
    let videoReplayListener = null;

    let gazeGrid = new Map();
    let rawGaze = [];

    const now = () => Date.now();

    function getMediaElement() {
        return (video.src && video.style.display !== 'none') ? video : img;
    }

    function setFixedSize(mediaEl) {
        mediaEl.width = FIXED_WIDTH;
        mediaEl.height = FIXED_HEIGHT;
        canvas.width = FIXED_WIDTH;
        canvas.height = FIXED_HEIGHT;
    }

    let isRedrawScheduled = false;

    function getCurrentHeatmapData() {
        const t = now();
        return Array.from(gazeGrid.values())
            .map(({x, y, duration, timestamp}) => {
                const age = (t - timestamp) / 1000;
                const value = Math.min(duration / 2, 5) * Math.exp(-age / TAU);
                return [x, y, value];
            })
            .filter(([, , value]) => value > 0.01);
    }

    function redraw() {
        if (!heat || isRedrawScheduled) return;
        isRedrawScheduled = true;
        requestAnimationFrame(() => {
            heat.data(getCurrentHeatmapData());
            heat.draw(0.6);
            isRedrawScheduled = false;
        });
    }

    function pushGridPoint(x, y) {
        const gridX = Math.floor(x / GRID_SIZE) * GRID_SIZE + GRID_SIZE / 2;
        const gridY = Math.floor(y / GRID_SIZE) * GRID_SIZE + GRID_SIZE / 2;
        const key = `${gridX},${gridY}`;

        const cell = gazeGrid.get(key) ?? {x: gridX, y: gridY, duration: 0, timestamp: now()};
        cell.duration += 0.1;
        cell.timestamp = now();
        gazeGrid.set(key, cell);

        if (gazeGrid.size > MAX_POINTS) {
            gazeGrid.delete(gazeGrid.keys().next().value);
        }

        redraw();
    }

    function initHeatmap() {
        const media = getMediaElement();
        canvas.classList.remove('ready');
        gazeGrid.clear();

        const setupCanvas = () => {
            setFixedSize(media);

            if (!heat) {
                heat = simpleheat(canvas).radius(30, 25);
                heat.max(5);
                heat.gradient({
                    0.0: 'rgba(0, 0, 255, 0)',
                    0.2: 'blue',
                    0.4: 'lightblue',
                    0.6: 'cyan',
                    0.8: 'orange',
                    1.0: 'red'
                });
            }

            heat.clear().draw(0);
            canvas.classList.add('ready');
        };

        if (media.tagName === 'IMG') {
            (media.complete && media.naturalWidth !== 0)
                ? setupCanvas()
                : media.addEventListener('load', setupCanvas, {once: true});
        } else {
            (media.readyState >= 1)
                ? setupCanvas()
                : media.addEventListener('loadedmetadata', setupCanvas, {once: true});
        }
    }

    let gazeListener = null;

    function startTracking() {
        if (gazeListener) return;
        webgazer.resume();
        gazeListener = (data) => {
            if (!data || isReplaying) return;
            const media = getMediaElement();
            if (media.tagName === 'VIDEO' && media.paused) return;

            const rect = media.getBoundingClientRect();
            const scaleX = FIXED_WIDTH / media.offsetWidth;
            const scaleY = FIXED_HEIGHT / media.offsetHeight;

            const x = (data.x - rect.left) * scaleX;
            const y = (data.y - rect.top) * scaleY;

            if (x < 0 || x > FIXED_WIDTH || y < 0 || y > FIXED_HEIGHT) return;
            pushGridPoint(x, y);

            if (media.tagName === 'VIDEO') {
                rawGaze.push({x, y, t: media.currentTime});
            }
        };
        webgazer.setGazeListener(gazeListener);
    }

    function stopTracking() {
        webgazer.pause();
        if (gazeListener) {
            webgazer.clearGazeListener();
            gazeListener = null;
        }
    }

    uploadInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const url = URL.createObjectURL(file);

        if (file.type.startsWith('image/')) {
            video.pause();
            video.removeAttribute('src');
            video.style.display = 'none';
            img.src = url;
            img.style.display = 'block';
            rawGaze = [];
            initHeatmap();
        } else if (file.type.startsWith('video/')) {
            img.removeAttribute('src');
            img.style.display = 'none';
            video.src = url;
            video.style.display = 'block';
            video.addEventListener('loadedmetadata', () => {
                gazeGrid.clear();
                rawGaze = [];
                heat?.clear().draw(0);
                initHeatmap();
            }, {once: true});
        }
    });

    modal.addEventListener('shown.bs.modal', () => {
        initHeatmap();
        isReplaying = false;
        startTracking();
    });

    modal.addEventListener('hidden.bs.modal', () => {
        if (replayTimer) clearInterval(replayTimer);
        stopVideoReplay();
        isReplaying = false;
        stopBtn.classList.add('d-none');
        replayBtn.disabled = false;
        startTracking();
    });

    saveBtn.addEventListener('click', () => {
        const media = getMediaElement();
        const data = (media.tagName === 'VIDEO') ? rawGaze : Array.from(gazeGrid.values());
        const blob = new Blob([JSON.stringify(data)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = Object.assign(document.createElement('a'), {
            href: url,
            download: media.tagName === 'VIDEO' ? 'heatmap_video_data.json' : 'heatmap_image_data.json'
        });
        a.click();
        URL.revokeObjectURL(url);
    });

    replayBtn.addEventListener('click', () => {
        (getMediaElement().tagName === 'VIDEO') ? handleVideoReplay() : handleImageReplay();
    });

    function handleImageReplay() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = ({target}) => {
            const file = target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = ({target}) => startImageReplay(JSON.parse(target.result || '[]'));
            reader.readAsText(file);
        };
        input.click();
    }

    function startImageReplay(data) {
        if (!data.length) return;
        isReplaying = true;
        replayBtn.disabled = true;
        stopBtn.classList.remove('d-none');
        stopTracking();
        heat?.clear().draw(0);
        gazeGrid.clear();
        let idx = 0;
        replayTimer = setInterval(() => {
            if (idx >= data.length) return stopImageReplay();
            const {x, y} = data[idx++];
            if (x >= 0 && x <= FIXED_WIDTH && y >= 0 && y <= FIXED_HEIGHT) {
                pushGridPoint(x, y);
            }
        }, 50);
    }

    function stopImageReplay() {
        clearInterval(replayTimer);
        isReplaying = false;
        stopBtn.classList.add('d-none');
        replayBtn.disabled = false;
        heat?.clear().draw(0);
        gazeGrid.clear();
        startTracking();
    }

    function handleVideoReplay() {
        const chainLoad = () => {
            if (!video.src) {
                const videoInput = document.createElement('input');
                videoInput.type = 'file';
                videoInput.accept = 'video/*';
                videoInput.onchange = ({target}) => {
                    const file = target.files[0];
                    if (!file) return;
                    video.src = URL.createObjectURL(file);
                    video.style.display = 'block';
                    img.style.display = 'none';
                    video.addEventListener('loadedmetadata', () => {
                        initHeatmap();
                        loadJSONandStart();
                    }, {once: true});
                };
                videoInput.click();
            } else {
                loadJSONandStart();
            }
        };

        const loadJSONandStart = () => {
            const jsonInput = document.createElement('input');
            jsonInput.type = 'file';
            jsonInput.accept = '.json';
            jsonInput.onchange = ({target}) => {
                const file = target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = ({target}) => startVideoReplay(JSON.parse(target.result || '[]'));
                reader.readAsText(file);
            };
            jsonInput.click();
        };

        chainLoad();
    }

    function startVideoReplay(data) {
        if (!data.length) return;
        isReplaying = true;
        replayBtn.disabled = true;
        stopBtn.classList.remove('d-none');
        stopTracking();
        heat?.clear().draw(0);
        gazeGrid.clear();
        data.sort((a, b) => a.t - b.t);
        let idx = 0;
        let lastTime = 0;

        function rebuildUntil(t) {
            heat.clear().draw(0);
            gazeGrid.clear();
            idx = 0;
            while (idx < data.length && data[idx].t <= t) {
                const {x, y} = data[idx++];
                if (x >= 0 && x <= FIXED_WIDTH && y >= 0 && y <= FIXED_HEIGHT) pushGridPoint(x, y);
            }
        }

        rebuildUntil(0);
        video.currentTime = 0;
        video.play();
        videoReplayListener = () => {
            const ct = video.currentTime;
            if (ct < lastTime - 0.05) {
                rebuildUntil(ct);
            }
            while (idx < data.length && data[idx].t <= ct) {
                const {x, y} = data[idx++];
                if (x >= 0 && x <= FIXED_WIDTH && y >= 0 && y <= FIXED_HEIGHT) pushGridPoint(x, y);
            }
            lastTime = ct;
            if (idx >= data.length) stopVideoReplay();
        };
        video.addEventListener('timeupdate', videoReplayListener);
        video.addEventListener('seeked', () => rebuildUntil(video.currentTime));
    }

    function stopVideoReplay() {
        if (videoReplayListener) {
            video.removeEventListener('timeupdate', videoReplayListener);
            videoReplayListener = null;
        }
        if (!isReplaying) return;
        isReplaying = false;
        stopBtn.classList.add('d-none');
        replayBtn.disabled = false;
        video.pause();
        heat?.clear().draw(0);
        gazeGrid.clear();
        startTracking();
    }

    stopBtn.addEventListener('click', () => {
        (getMediaElement().tagName === 'VIDEO') ? stopVideoReplay() : stopImageReplay();
    });
})();
