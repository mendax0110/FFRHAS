    function getAllSensorData() {
        fetch(`/highvoltagesystem/get`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('getAllData').innerText = JSON.stringify(data);
            })
            .catch(error => console.error('Error:', error));
    }

    function createSensorData() {
        const sensorName = document.getElementById('sensorName').value;
        const sensorValue = document.getElementById("sensorValue").value;
        const sensorTimeStamp = document.getElementById("sensorTimestamp").value;
        fetch(`/highvoltagesystem/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: sensorName,
                value: sensorValue,
                time: sensorTimeStamp
             }),
        })
        .then(response => response.json())
        .then(data => console.log('Data created:', data))
        .catch(error => console.error('Error:', error));
    }