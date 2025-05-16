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

});

var callbackFunction = null;
var currentModal = null;

// Dynamically set the iframe src using the variable
document.getElementById("grafana-temp1").src = iframeSrcTemp1;
document.getElementById("grafana-temp2").src = iframeSrcTemp2;
document.getElementById("grafana-pressure").src = iframeSrcPressure;

function ModeManual(){
  const buttonStart = document.getElementById("start");
  const buttonStop = document.getElementById("stop");
  const frequencySoll = document.getElementById("frequencySoll");
  const pwmSoll = document.getElementById("pwmSoll");
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
  const frequencySoll = document.getElementById("frequencySoll");
  const pwmSoll = document.getElementById("pwmSoll");
  const buttonTurnOn = document.getElementById("turnOn");
  const buttonTurnOff = document.getElementById("turnOff");
  buttonStart.disabled = false;
  buttonStop.disabled = false;
  frequencySoll.disabled = true;
  pwmSoll.disabled = true;
  buttonTurnOn.disabled = true;
  buttonTurnOff.disabled = true;
}

function TurnOnHighVoltage(){
    console.log("turned on HighVoltageSystem");
    const buttonTurnOn = document.getElementById("turnOn");
    const buttonTurnOff = document.getElementById("turnOff");
    buttonTurnOn.checked = true;
    buttonTurnOff.checked = false;
}

function TurnOffHighVoltage(){
    console.log("turned off HighVoltageSystem");
    const buttonTurnOn = document.getElementById("turnOn");
    const buttonTurnOff = document.getElementById("turnOff");
    buttonTurnOn.checked = false;
    buttonTurnOff.checked = true;
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