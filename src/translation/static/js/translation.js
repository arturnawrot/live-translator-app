var audio = new Audio();
const sampleAudio = "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xP2CBlxtEyCAdgDGjCKkAImoi7oDIwfynkEKScZKcrw52jj7cpSs5/PTM3VyaHIdCtbZIsJNhR4VImAmaJW7//tq+q+/7PR/Zd/+9QCBSwGhvWV7yIi3v+x4Mp04hwnhsBUb1qv/+yDE9IAFsIUTIIB0ALoP4mQQDoDxQY1MKOEDHtEBUMhuqnf9HV6+ZjVLsK6NE39v7v4oCOvqA9J2311viiTlgDrDQq0H3zY0XHoOMtaGQfJoYdiqWi0XS9Rg4e/Zd/p/+X6e5H9kXR+xagYV1Mnelq/+g0hTEqEAGFBy2DGDiojc//sgxP0ACFgBEMAAAADXACJkAAAAtw8XXM2F6B71N73cXcLFjNhNR1QVevQzS44qv//1It6G7dYtJxsokF/qdnAxNJsLl28pNXyVkcHGHIQwIzg4sAAINDgoPMHPofEyjaHhcokewXKE0ss/IVjy6rqdzPIX7K/r87/4ygABKq5hP//7MMT3Agg8ZRMgBGSA/IBiJAAAAJRqIUMnAoI1C55dCDbAxpHAUoZUBD1agfTdrlK2JEgQQ2dG+7/StdM6uATkzT9F//33fT9RfVBl/9f/mhO9pQ1oQQausIpEJRK3DEUMEa3LFGB4NwE50YeJDT0XKXFnvFyRE4DI5ml2pPro8d7//6qPWN7a6gD1aoHIcvXUgoshsku2w+Tpe//7IMT6AAewXxDABGtA8BQiZBAOgPVpHmUhiNVTcgjmQotq9STbBYjvcZSGhgDXd/f37EqmPuj920fO+72qvhP2+smFQFnNndha3+cCyVmRwMOWEFBAGQ82j3HmRxBEIgKJwv1AyBRxIXEp42gXeExWLHXf265S2pApuTekd16aakz/+yDE84AG/HEQwIBSQNoAIlgAAABBTUUzLjEwMKqqqqqqqqqqqqqqqqqqQSVCAFT2afFm9DPA28tqFwVKyKP9TZmLP0f9f/6//7Kv//9n/VVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//swxPKCBzwDEsAAAAEOjiJoAIy4VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//swxPcDB1QDEyAAAAD+kGJIEA6AVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//sgxP0CB+iFEMCEaUD4AGHIAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/7EMTpA8SsAxDAAAAAAAA/wAAABFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV";
var soundsToBePlayed = [];
var ws = null;
var stream = null;
var micstatus = false;
var processor = null;
var source = null;

const stopButton = document.getElementById('stop');
const startButton = document.getElementById('start');
const offOnMark = document.getElementById('offOnMark');

// Translated Text TextArea
const area = document.getElementById('translationTextArea');


if(typeof FRONTEND_COMMUNICATION_PROTOCOL === 'undefined') {
    const FRONTEND_COMMUNICATION_PROTOCOL = "websocket";
}

if(typeof SHARE_CODE === 'undefined') {
    const SHARE_CODE = null;
}

function isLocal() {
    const hosts = ['localhost', '127.0.0.1', '192.168.'];
    const windowHostname = window.location.hostname;

    for (const host of hosts) {
        if (windowHostname === host || windowHostname.startsWith(host) || windowHostname.includes(host)) {
            return true;
        }
    }

    return false;
}

function openWs()
{
    let url;

    if (isLocal()) {
        url = 'ws://' + window.location.hostname + ':' + window.location.port + '/translate';
    } else {
        url = 'wss://' + window.location.hostname + ':' + window.location.port + '/translate';
    }
    
    ws = new WebSocket(url);

    ws.addEventListener('open', function(event) {
        console.log(event);
    });

    ws.addEventListener('error', function(event) {
        console.log(event);
    });

    ws.addEventListener('message', function(event) {

        document.dispatchEvent(new CustomEvent('translationResultReceived', {
            detail: { res: JSON.parse(event.data) }
        }));

    });
}

function addTranslatedText(text)
{    
    var tmpCopy = area.innerText;

    area.innerText = "";

    area.innerText =  text + "\n" + tmpCopy;
}

document.addEventListener('translationResultReceived', function(e) {
    document.getElementById('status').innerHTML = 'Response received';

    document.getElementById('status').innerHTML = '';

    res = e.detail.res;

    console.log('Received translated message:', res);

    if(res.status != 'success') {
        return;
    }

    soundsToBePlayed.push(res.translation_result['translatedAudio']);

    addTranslatedText(res.translation_result['translatedText'])
});

function ajaxRequest(data)
{
    data.csrfmiddlewaretoken = document.getElementsByName('csrf-token')[0].getAttribute('content');
    
    $.ajax({
        type: "POST",
        url: "/translate",
        data: data,
        success: function(response) {
            document.dispatchEvent(new CustomEvent('translationResultReceived', {
                detail: { res: response }
            }));
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log(xhr.responseText);
        }
    });
}

function websocketRequest(data) {
    const base64Message = JSON.stringify(data);
    // Check if WebSocket connection is already open before sending data
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(base64Message);
        console.log('Data sent');
    } else {
        ws.onopen = () => {
            ws.send(base64Message);
            console.log('Data sent');
        };
    }
}

document.addEventListener('audioClipCaptured', function(e) {
    document.getElementById('status').innerHTML = 'Sending...'

    const audioBase64 = e.detail.base64;
    const id = e.detail.id;

    const target_lang = document.getElementById('translateToInput').value;
    const source_lang = document.getElementById('translateFromInput').value;

    var message = {
        base64: audioBase64,
        target_lang: target_lang,
        source_lang: source_lang
    };

    if(SHARE_CODE != null) {
        message.share_code = SHARE_CODE;
    }

    console.log('Received Base64 audio', id);

    switch(FRONTEND_COMMUNICATION_PROTOCOL) {
        case 'ajax':
            ajaxRequest(message);
            break;
        case 'websocket':
            if(ws === null) {
                openWs();
            }
            else if(ws.readyState === WebSocket.CLOSING || ws.readyState === WebSocket.CLOSED) {
                openWs();
            }

            websocketRequest(message);
            break;
        default:
            alert('Frontend communication protocol not properly configured')
    }
});

async function play() {
    if(micstatus == false) return;

    console.log('play');
    console.log(soundsToBePlayed);
    
    audio.addEventListener('ended', play, false);

    if(soundsToBePlayed.length > 0) {
        audio.src = "data:audio/mpeg;base64," + soundsToBePlayed.pop()
    } else {
        audio.src = "data:audio/mpeg;base64," + sampleAudio;
    }

    audio.play();
}

const rmsThresholdSlider = document.getElementById('rmsThreshold');
const rmsThresholdValueDisplay = document.getElementById('rmsThresholdValue');
const audioClipsList = document.getElementById('audioClips');

var idCounter = 0;

let rmsThreshold = parseInt(rmsThresholdSlider.value);
let mediaRecorder;
let isUserSpeaking = false;
let audioChunks = []; // Moved audioChunks to be accessible by both startRecording and stopRecording
const audioBase64Array = [];

rmsThresholdSlider.oninput = () => {
    rmsThresholdValueDisplay.textContent = rmsThresholdSlider.value;
    rmsThreshold = parseInt(rmsThresholdSlider.value);
};

const getMicrophoneAccess = async () => {
    if(micstatus == false) return;

    stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    document.dispatchEvent(new CustomEvent("RecordingStarted", { detail: { stream } }));

    processAudioStream(stream);
};

startButton.addEventListener('click', async function(event) {
    if(translationState['currentTranslateTo'] === translationState['currentTranslateFrom']) {
        alert('You cannot have 2 same languages set in both "Translate From" and "Translate To".');
        return;
    }
    
    micstatus = true;

    audio = new Audio();

    await play();
    await getMicrophoneAccess();
});

const processAudioStream = (stream) => {
    const audioContext = new AudioContext();
    source = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    processor = audioContext.createScriptProcessor(512, 1, 1);

    source.connect(analyser);
    analyser.connect(processor);
    processor.connect(audioContext.destination);

    analyser.fftSize = 512;
    var dataArray = new Uint8Array(analyser.frequencyBinCount);

    processor.onaudioprocess = () => {
        if(micstatus == false) {
            processor.disconnect();
        }

        analyser.getByteFrequencyData(dataArray);
        let rms = Math.sqrt(dataArray.reduce((sum, value) => sum + value * value, 0) / Math.max(dataArray.length, 50));
        if (rms > rmsThreshold && !isUserSpeaking) {
            isUserSpeaking = true;
            startRecording(stream);
        } else if (rms <= rmsThreshold && isUserSpeaking) {
            isUserSpeaking = false;
            stopRecording();
        }
    };
};

const startRecording = (stream) => {
    audioChunks = []; // Reset audioChunks to empty on start
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
};

const stopRecording = () => {
    mediaRecorder.stop();
    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
        const base64AudioMessage = await blobToBase64(audioBlob);

        if(base64AudioMessage.length < 8000) return;

        audioBase64Array.push({ data: base64AudioMessage, size: base64AudioMessage.length });

        displayAudioClip(base64AudioMessage, audioBlob, idCounter);

        document.dispatchEvent(new CustomEvent('audioClipCaptured', {
            detail: { base64: base64AudioMessage, id: idCounter }
        }));

        idCounter++;
    };
};

const blobToBase64 = (blob) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result.split(',')[1]);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
});

const displayAudioClip = (base64AudioMessage, audioBlob, id) => {
    const audioUrl = URL.createObjectURL(audioBlob);
    const audioElement = document.createElement('audio');
    audioElement.controls = true;
    audioElement.src = audioUrl;

    const listItem = document.createElement('li');
    const base64TextInput = document.createElement('input');
    base64TextInput.type = 'text';
    base64TextInput.value = base64AudioMessage;
    base64TextInput.readOnly = true; // Making the input read-only

    const sizeSpan = document.createElement('span');
    sizeSpan.textContent = ` Size: ${base64AudioMessage.length} bytes`;

    listItem.appendChild(audioElement);
    listItem.appendChild(document.createElement('br'));
    listItem.appendChild(base64TextInput);
    listItem.appendChild(sizeSpan);
    listItem.id = id;
    listItem.className = 'my-8 py-8';
    audioClipsList.prepend(listItem);
};

document.addEventListener("RecordingStarted", (event) => {
    const stream = event.detail.stream;

    startButton.style.display = 'none';
    stopButton.style.display = 'inline-block';

    animateMicIcon(stream);
    offOnMark.style.color = 'green';
    offOnMark.innerText = "ON";
  });
  
  function animateMicIcon(stream) {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const microphone = audioContext.createMediaStreamSource(stream);
    microphone.connect(analyser);
    analyser.fftSize = 512;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
  
    const micIcon = document.querySelector('#mic');
  
    function animate() {
      requestAnimationFrame(animate);
  
      analyser.getByteFrequencyData(dataArray);
  
      let sum = 0;
      for(let i = 0; i < bufferLength; i++) {
        sum += dataArray[i];
      }
      let averageVolume = sum / bufferLength;
  
      const scale = Math.min((1 + averageVolume / 64), 2);
      micIcon.style.transform = `scale(${scale})`;
    }
  
    animate();
  }

stopButton.addEventListener('click', async function(event) {
    if(ws != null) {
        ws.close();
    }

    micstatus = false;

    if (processor) {
        processor.disconnect();
        processor.onaudioprocess = null;
    }

    if (source) {
        source.disconnect();
    }

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }

    processor = null;
    source = null;
    stream = null;

    stopButton.style.display = 'none';
    startButton.style.display = 'inline-block';
    offOnMark.style.color = 'black';
    offOnMark.innerText = "OFF";
});