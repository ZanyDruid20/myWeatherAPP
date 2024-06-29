// Function to get the current location of the user
function getLocation() {
    // Check if geolocation is supported by the browser
    if (navigator.geolocation) {
        // Get the current position and call showPosition if successful
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        // Alert the user if geolocation is not supported
        alert("Geolocation is not supported by this browser.");
    }
}

// Function to handle the position data retrieved by getLocation
function showPosition(position) {
    // Extract latitude and longitude from the position object
    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;

    // Send a POST request to the /weather endpoint with the coordinates
    fetch('/weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // Convert the coordinates to a JSON string for the request body
        body: JSON.stringify({ lat: latitude, lon: longitude })
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data as needed (e.g., display weather info)
        console.log(data);
    })
    .catch(error => {
        // Log any errors that occur during the fetch request
        console.error('Error fetching weather data:', error);
    });
}
