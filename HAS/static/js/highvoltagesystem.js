// Access the container element (the 'leftSide' div or the 'body' if you prefer)
const leftSide = document.querySelector('.leftSide');

// Retrieve the dynamic data from the data attributes
const hvOn = leftSide.dataset.hvOn === "true";
const targetFrequency = parseFloat(leftSide.dataset.targetFrequency);
const targetPwm = parseFloat(leftSide.dataset.targetPwm);
const automatic = leftSide.dataset.automatic === "true";
const handBetrieb = leftSide.dataset.mainSwitchState === "manual";
const isOff = leftSide.dataset.mainSwitchState === "off";

ToggleHv(hvOn);
document.getElementById("sollPwm").value = targetPwm;
document.getElementById("sollFrequency").value = targetFrequency;
ToggleAutomatic(automatic);
ToggleControlStatus(handBetrieb, isOff);

// Define the global JavaScript variable
const host = window.location.hostname; // Gets the host (IP or domain name)
// Construct the iframe URL
const iframeSrcTemp1 = `http://${host}:3000/d-solo/Highvoltagesystem?orgId=1&panelId=1`;
const iframeSrcTemp2 = `http://${host}:3000/d-solo/Highvoltagesystem?orgId=1&panelId=2`;
const iframeSrcPressure = `http://${host}:3000/d-solo/Highvoltagesystem?orgId=1&panelId=3`;

const socket = io('/highvoltagesystem');

socket.on('connect', () => {
    console.log('Connected to /highvoltagesystem');
});

socket.on('backendData', (data) => {
  console.log('Received from server:', data);

  // PROCESS DATA HERE
  ToggleHv(data.highVoltageState.hvOn);
  document.getElementById("sollPwm").value = data.highVoltageState.targetPwm;
  document.getElementById("actualDutyCycle").innerText = data.actualDutyCycle.value;
  document.getElementById("sollFrequency").value = data.highVoltageState.targetFrequency;
  document.getElementById("actualFrequency").innerText = data.actualFrequency.value;
  ToggleAutomatic(data.highVoltageState.automatic);
  var isHandBetrieb = data.mainSwitchState.state === "manual";
  var isOff = data.mainSwitchState.state === "off";
  ToggleControlStatus(isHandBetrieb, isOff);
});

var callbackFunction = null;
var currentModal = null;

// Dynamically set the iframe src using the variable
document.getElementById("grafana-temp1").src = iframeSrcTemp1;
document.getElementById("grafana-temp2").src = iframeSrcTemp2;
document.getElementById("grafana-pressure").src = iframeSrcPressure;

document.getElementById("sollFrequency").addEventListener("keypress", function(event) {
  // Check if the Enter key (keyCode 13) is pressed
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent form submission (if inside a form)
    showModal(setTargetFrequency); // Show the confirmation modal
  }
});

document.getElementById("sollPwm").addEventListener("keypress", function(event) {
  // Check if the Enter key (keyCode 13) is pressed
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent form submission (if inside a form)
    showModal(setTargetPwm); // Show the confirmation modal
  }
});

async function setTargetFrequency() {
  try {
    const targetFrequency = document.getElementById("sollFrequency");

    const response = await fetch(`/highvoltagesystem/setTargetFrequency?targetFrequency=${targetFrequency.value}`);
    
    if (response.status !== 200) {
      console.log("Failed to set frequency");
      targetFrequency.value = '';
      return;
    }

    console.log("Set frequency successfully");
  }
  catch (error) {
    console.error("Failed to set frequency:", error);
  }
}

async function setTargetPwm() {
  try {
    const targetPwm = document.getElementById("sollPwm");

    const response = await fetch(`/highvoltagesystem/setTargetPwm?targetPwm=${targetPwm.value}`);
    
    if (response.status !== 200) {
      console.log("Failed to set pwm");
      targetPwm.value = '';
      return;
    }

    console.log("Set pwm successfully");
  }
  catch (error) {
    console.error("Failed to set pwm:", error);
  }
}

function ModeManual(){
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const frequencySoll = document.getElementById("sollFrequency");
  const pwmSoll = document.getElementById("sollPwm");
  const buttonTurnOn = document.getElementById("turnOn");
  const buttonTurnOff = document.getElementById("turnOff");
  buttonStart.disabled = true;
  buttonStop.disabled = true;
  frequencySoll.disabled = false;
  pwmSoll.disabled = false;
  buttonTurnOn.disabled = false;
  buttonTurnOff.disabled = false;
}

function ModeAutomatic(){
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const frequencySoll = document.getElementById("sollFrequency");
  const pwmSoll = document.getElementById("sollPwm");
  const buttonTurnOn = document.getElementById("turnOn");
  const buttonTurnOff = document.getElementById("turnOff");
  buttonStart.disabled = false;
  buttonStop.disabled = false;
  frequencySoll.disabled = true;
  pwmSoll.disabled = true;
  buttonTurnOn.disabled = true;
  buttonTurnOff.disabled = true;
}

async function TurnOnHighVoltage() {
  try {
    const response = await fetch('/highvoltagesystem/StartHighVoltage');

    if (response.status !== 200) {
      console.log("Failed to start hv");
      return;
    }

    console.log("started hv");
    ToggleHv(true);
  }
  catch (error) {
    console.error("Error starting hv:", error);
  }
}

async function TurnOffHighVoltage(){
  try {
    const response = await fetch('/highvoltagesystem/StopHighVoltage');

    if (response.status !== 200) {
      console.log("Failed to stopp hv");
      return;
    }

    console.log("stopped hv");
    ToggleHv(false);
  }
  catch (error) {
    console.error("Error stopping hv:", error);
  }
}

function ToggleHv(isOn) {
  const buttonTurnOn = document.getElementById("turnOn");
  const buttonTurnOff = document.getElementById("turnOff");

  if (isOn) {
    console.log("turned on HighVoltageSystem");
    buttonTurnOn.checked = true;
    buttonTurnOff.checked = false;
    return;
  }

  console.log("turned off HighVoltageSystem");
  buttonTurnOn.checked = false;
  buttonTurnOff.checked = true;
}

async function StartAutomatic() {
  try {
    const response = await fetch('/highvoltagesystem/StartAutomatic');

    if (response.status !== 200) {
      console.log("Failed to start automatic");
      return;
    }

    ToggleAutomatic(true);
  }
  catch (error) {
    console.error("Error starting automatic:", error);
  }
}

async function StopAutomatic(){
  try {
    const response = await fetch('/highvoltagesystem/StopAutomatic');

    if (response.status !== 200) {
      console.log("Failed to stop automatic");
      return;
    }

    ToggleAutomatic(false);
  }
  catch (error) {
    console.error("Error stopping automatic:", error);
  }
}

function ToggleAutomatic(isAutomatic) {
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  
  if (isAutomatic) {
    console.log("started automatic");
    buttonStart.checked = true;
    buttonStop.checked = false;
    return;
  }

  console.log("stopped automatic");
  buttonStart.checked = false;
  buttonStop.checked = true;
}

function ToggleControlStatus(isHandBetrieb, isOff) {
  const hvOn = document.getElementById("turnOn");
  const hvOff = document.getElementById("turnOff");
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const sollFrequency = document.getElementById("sollFrequency");
  const sollPwm = document.getElementById("sollPwm");
  const buttonAutomatic = document.getElementById("Automatic");
  const buttonManual = document.getElementById("Manual");

  if (isOff) {
    document.getElementById('offStatusBanner').style.display = 'block';
    document.getElementById('controlStatusBanner').style.display = 'none';
    hvOn.disabled = true;
    hvOff.disabled = true;
    buttonStart.disabled = true;
    buttonStop.disabled = true;
    sollFrequency.disabled = true;
    sollPwm.disabled = true;
    buttonAutomatic.disabled = true;
    buttonManual.disabled = true;
    return;
  }

  if (isHandBetrieb) {
    document.getElementById('controlStatusBanner').style.display = 'block'; 
    document.getElementById('offStatusBanner').style.display = 'none';
    hvOn.disabled = true;
    hvOff.disabled = true;
    buttonStart.disabled = true;
    buttonStop.disabled = true;
    sollFrequency.disabled = true;
    sollPwm.disabled = true;
    buttonAutomatic.disabled = true;
    buttonManual.disabled = true;
    return;
  }
  
  document.getElementById('controlStatusBanner').style.display = 'none';
  document.getElementById('offStatusBanner').style.display = 'none';

  if (buttonAutomatic.checked) {
    buttonStart.disabled = false;
    buttonStop.disabled = false;
    buttonAutomatic.disabled = false;
    buttonManual.disabled = false;
    return;
  }

  hvOn.disabled = false;
  hvOff.disabled = false;
  sollFrequency.disabled = false;
  sollPwm.disabled = false;
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