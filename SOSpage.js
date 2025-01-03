document.getElementById('sosButton').addEventListener('click', async () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            document.getElementById('geoStatus').textContent = `Location accuracy is high (Lat: ${latitude}, Long: ${longitude})`;

            // Send data to the Flask backend
            try {
                const response = await fetch('http://127.0.0.1:5000/SOSpage', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        latitude: latitude,
                        longitude: longitude,
                        timestamp: new Date().toISOString()
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message); 
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.error}`);
                }
            } catch (err) {
                console.error('Error sending SOS alert:', err);
                alert('Failed to send SOS alert. Please try again.');
            }
        }, (error) => {
            document.getElementById('geoStatus').textContent = 'Unable to fetch location.';
        });
    } else {
        document.getElementById('geoStatus').textContent = 'Geolocation is not supported by your browser.';
    }
});