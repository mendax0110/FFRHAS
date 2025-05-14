// Access the container element (the 'leftSide' div or the 'body' if you prefer)
const leftSide = document.querySelector('.leftSide');

// Retrieve the dynamic data from the data attributes
const pumpOn = leftSide.dataset.pumpOn === "true";
const targetPressure = parseFloat(leftSide.dataset.targetPressure);
const automatic = leftSide.dataset.automatic === "true";
const handBetrieb = leftSide.dataset.handBetrieb === "true";

TogglePump(pumpOn);
ToggleAutomatic(automatic);
const pressureValue = document.getElementById("sollInput").value = targetPressure;
ToggleControlStatus(handBetrieb);

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

document.getElementById("sollInput").addEventListener("keypress", function(event) {
  // Check if the Enter key (keyCode 13) is pressed
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent form submission (if inside a form)
    showModal(setTargetPressure); // Show the confirmation modal
  }
});

async function setTargetPressure() {
  try {
    const pressureValue = document.getElementById("sollInput");

    const response = await fetch(`/vacuumsystem/setTargetPressure?targetPressure=${pressureValue.value}`);
    
    if (response.status !== 200) {
      console.log("Failed to set pressure");
      pressureValue.value = '';
      return;
    }

    console.log("Set pressure successfully");
  }
  catch (error) {
    console.error("Failed to set pressure:", error);
  }
}

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

async function SwitchPumpOn() {
  try {
    const response = await fetch("/vacuumsystem/pumpOn");

    if (response.status !== 200) {
      console.log("Failed to turn pump on");
      return;
    }

    console.log("pump turned on");
    TogglePump(true);
  }
  catch (error) {
    console.error("Error starting pump:", error);
  }
}

async function SwitchPumpOff() {
  try {
    const response = await fetch("/vacuumsystem/pumpOff");

    if (response.status !== 200) {
      console.log("Failed to turn pump off");
      return;
    }

    console.log("pump turned off");
    TogglePump(false);
  }
  catch (error) {
    console.error("Error stopping pump:", error);
  }
}

function TogglePump(pumpOn) {
  const buttonOn = document.getElementById("On");
  const buttonOff = document.getElementById("Off");
  
  if (pumpOn) {
    buttonOn.checked = true;
    buttonOff.checked = false;
    return;
  }

  buttonOn.checked = false;
  buttonOff.checked = true;  
}

async function StartAutomatic() {
  try {
    const response = await fetch('/vacuumsystem/startAutomatic');
    
    if (response.status !== 200) {
      console.log("Failed to start automatic");
      return;
    }

    console.log("Started automatic");
    ToggleAutomatic(true);
  } catch (error) {
    console.error("Error starting automatic:", error);
  }
}

async function StopAutomatic() {
  try {
    const response = await fetch('/vacuumsystem/stopAutomatic');

    if (response.status !== 200) {
      console.log("Failed to stop automatic");
      return;
    }

    console.log("stopped automatic");
    ToggleAutomatic(false);
  }
  catch (error) {
    console.error("Error stopping automatic:", error);
  }
}

function ToggleAutomatic(isAutomaticMode) {
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const pressureValue = document.getElementById("sollInput");

  if (isAutomaticMode) {
    buttonStart.checked = true;
    buttonStop.checked = false;
    pressureValue.value = '';
    return;
  }

  buttonStart.checked = false;
  buttonStop.checked = true;
}

function ToggleControlStatus(isHandBetrieb) {
  const pumpOn = document.getElementById("On");
  const pumpOff = document.getElementById("Off");
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const sollInput = document.getElementById("sollInput");
  const buttonAutomatic = document.getElementById("Automatic");
  const buttonManual = document.getElementById("Manual");

  if (isHandBetrieb) {
    document.getElementById('controlStatusBanner').style.display = 'block'; 
    pumpOn.disabled = true;
    pumpOff.disabled = true;
    buttonStart.disabled = true;
    buttonStop.disabled = true;
    sollInput.disabled = true;
    buttonAutomatic.disabled = true;
    buttonManual.disabled = true;
    return;
  }
  
  document.getElementById('controlStatusBanner').style.display = 'none';

  if (buttonAutomatic.checked) {
    buttonStart.disabled = false;
    buttonStop.disabled = false;
    buttonAutomatic.disabled = false;
    buttonManual.disabled = false;
    return;
  }

  pumpOn.disabled = false;
  pumpOff.disabled = false;
  sollInput.disabled = false;
  buttonAutomatic.disabled = false;
  buttonManual.disabled = false;
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