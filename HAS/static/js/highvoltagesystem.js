    function getAllUsers() {
        fetch(`/highvoltagesystem/get`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('getAllUsersResult').innerText = JSON.stringify(data);
            })
            .catch(error => console.error('Error:', error));
    }

    function createUser() {
        const newUserName = document.getElementById('newUserName').value;
        fetch(`/highvoltagesystem/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: newUserName }),
        })
        .then(response => response.json())
        .then(data => console.log('User created:', data))
        .catch(error => console.error('Error:', error));
    }