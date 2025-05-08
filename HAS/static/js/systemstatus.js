const socket = io('/systemstatus');

socket.on('connect', () => {
    console.log('Connected to /systemstatus');
});

socket.on('backendData', (data) => {
    console.log('Received from server:', data);

    // PROCESS DATA HERE

});
