const audioPlayer = document.getElementById('audioPlayer');
const playButton = document.getElementById('playButton');
const currentTimeDisplay = document.getElementById('currentTime'); // Display for current time
const totalTimeDisplay = document.getElementById('totalTime'); // Display for total duration
const songNameDisplay = document.getElementById('songName'); // Display for total duration

let isPlaying = false;
let currentSongIndex = -1;
const songCache = {};

playButton.addEventListener('click', () => {
    if (!isPlaying) {
        synchronizeAndPlay();
    } else {
        audioPlayer.pause();
        playButton.textContent = 'Play';
        isPlaying = false;
    }
});


// Update the current time display as the audio plays
audioPlayer.addEventListener('timeupdate', () => {
    currentTimeDisplay.textContent = formatTime(Math.floor(audioPlayer.currentTime));
});

async function synchronizeAndPlay() {
    try {
        const data = await fetchCurrentSongInfo();
        
        if (currentSongIndex !== data.songIndex) {
            currentSongIndex = data.songIndex;
            await loadSong(currentSongIndex);
            totalTimeDisplay.textContent = formatTime(data.totalTime); // Update total time display
            let songName = data.songName.slice(0, -4); // Remove .mp3
            let delimiterIndex = songName.indexOf('_');
            if (delimiterIndex !== -1) {
                songName = songName.slice(0, delimiterIndex);
            }
            songNameDisplay.textContent = songName || 'mystery song';
        }

        audioPlayer.currentTime = data.currentTime;
        await audioPlayer.play();
        playButton.textContent = 'Pause';
        isPlaying = true;

        // Schedule the next song
        setTimeout(() => {
            if (isPlaying) synchronizeAndPlay();
        }, (data.totalTime - data.currentTime) * 1000);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function fetchCurrentSongInfo() {
    const response = await fetch(`/${GENRE}/current_song_info`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

async function loadSong(index) {
    if (!songCache[index]) {
        const response = await fetch(`/${GENRE}/get_song/${index}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        songCache[index] = URL.createObjectURL(blob);
    }
    audioPlayer.src = songCache[index];
}

// Format time from seconds to mm:ss
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}


// Function to send hearbeat to be included in active listener count
function sendHeartbeat() {
    fetch(`/${GENRE}/heartbeat`);
}

// Function to fetch and change active listener counter
async function updateListenerCount() {
    try {
        const response = await fetch(`/${GENRE}/listener_count`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        document.getElementById('listenerCountValue').textContent = data.count;
    } catch (error) {
        console.error('Error updating listener count:', error);
    }
}

// Send heartbeat and update listener count every 30 seconds
setInterval(() => {
    sendHeartbeat();
    setTimeout(() => {}, 1000); // Sleep between requests or else you won't be counted in count first time
    updateListenerCount();
}, 15000);

// Initial update
sendHeartbeat();
updateListenerCount();
