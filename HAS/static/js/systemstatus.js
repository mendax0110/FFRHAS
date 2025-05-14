const host = window.location.hostname; // Gets the host (IP or domain name)

// Construct the iframe URL
const iframeSrc = `http://${host}:3000/d-solo/Systemstatus?orgId=1&panelId=1`;

const socket = io('/systemstatus');

socket.on('connect', () => {
    console.log('Connected to /systemstatus');
});

socket.on('backendData', (data) => {
    console.log('Received from server:', data);

    // PROCESS DATA HERE

});

// Dynamically set the iframe src using the variable
document.getElementById("grafana-dashboard").src = iframeSrc;
