// Define the global JavaScript variable
const host = window.location.hostname; // Gets the host (IP or domain name)
// Construct the iframe URL
const iframeSrcTemp1 = `http://${host}:3000/d-solo/Vacuumsystem?orgId=1&panelId=1`;
const iframeSrcTemp2 = `http://${host}:3000/d-solo/Vacuumsystem?orgId=1&panelId=2`;
const iframeSrcPressure = `http://${host}:3000/d-solo/Vacuumsystem?orgId=1&panelId=3`;

const socket = io('/vacuumsystem');

socket.on('connect', () => {
    console.log('Connected to /vacuumsystem');
});

socket.on('backendData', (data) => {
    console.log('Received from server:', data);

    // PROCESS DATA HERE

});

var callbackFunction = null;
var currentModal = null;

// Dynamically set the iframe src using the variable
document.getElementById("grafana-temp1").src = iframeSrcTemp1;
document.getElementById("grafana-temp2").src = iframeSrcTemp2;
document.getElementById("grafana-pressure").src = iframeSrcPressure;

function ModeManual(){
  const pumpOn = document.getElementById("On");
  const pumpOff = document.getElementById("Off");
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const sollInput = document.getElementById("sollInput");
  pumpOn.disabled = false;
  pumpOff.disabled = false;
  buttonStart.disabled = true;
  buttonStop.disabled = true;
  sollInput.disabled = false;
}

function ModeAutomatic(){
  const pumpOn = document.getElementById("On");
  const pumpOff = document.getElementById("Off");
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const sollInput = document.getElementById("sollInput");
  pumpOn.disabled = true;
  pumpOff.disabled = true;
  buttonStart.disabled = false;
  buttonStop.disabled = false;
  sollInput.disabled = true;
}

function SwitchPumpOn(){
  console.log("pump turned on");
  const buttonOn = document.getElementById("On");
  const buttonOff = document.getElementById("Off");
  buttonOn.checked = true;
  buttonOff.checked = false;
}

function SwitchPumpOff(){
  console.log("pump turned off");
  const buttonOn = document.getElementById("On");
  const buttonOff = document.getElementById("Off");
  buttonOn.checked = false;
  buttonOff.checked = true;
}

function StartAutomatic(){
  console.log("started automatic");
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  buttonStart.checked = true;
  buttonStop.checked = false;
}

function StopAutomatic(){
  console.log("stopped automatic");
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  buttonStart.checked = false;
  buttonStop.checked = true;
}

function showModal(callBack){
  callbackFunction = callBack;
  currentModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
  currentModal.show();
}

function CloseModal(execute){
  if (execute){
    callbackFunction();
  }
  currentModal.hide();
}