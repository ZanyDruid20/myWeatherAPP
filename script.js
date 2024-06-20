function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;

    fetch('/weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ lat: latitude, lon: longitude })
    })
    .then(response => response.json())
    .then(data => {
        // Handle response data as needed
        console.log(data);
    })
    .catch(error => {
        console.error('Error fetching weather data:', error);
    });
}
