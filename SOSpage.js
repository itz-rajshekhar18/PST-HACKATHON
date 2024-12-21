
  document.getElementById('SOSButton').addEventListener('click', async () => {
    if (navigator.geolocation) {
      document.getElementById('geoStatus').textContent = 'Attempting to fetch location...';

      navigator.geolocation.getCurrentPosition(async (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById('geoStatus').textContent = `Location accuracy is high (Lat: ${latitude}, Long: ${longitude})`;

        // Send data to the Flask backend
        try {
          const numMessages = 5; // Send 5 messages for testing

          const response = await fetch('http://127.0.0.1:5000/sos-alert', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              latitude: latitude,
              longitude: longitude,
              timestamp: new Date().toISOString(),
              num_messages: numMessages
            })
          });

          if (response.ok) {
            const result = await response.json();
            alert(result.message);  // Show success message
          } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);  // Show error message
          }
        } catch (err) {
          console.error('Error sending SOS alert:', err);
          alert('Failed to send SOS alert. Please try again.');
        }
      }, (error) => {
        document.getElementById('geoStatus').textContent = `Error: ${error.message}`;
      });
    } else {
      document.getElementById('geoStatus').textContent = 'Geolocation is not supported by your browser.';
    }
  });
