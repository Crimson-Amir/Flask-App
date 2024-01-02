function fetchConfigInformation() {
    // Get the configuration from the textarea
    const config = document.getElementById('configTextarea').value;

    // TODO: Implement logic to fetch information based on the entered configuration
    // For demonstration purposes, we'll display a placeholder volume information
    const volumeInfo = "Volume: 100GB";

    // Display the information in the info section
    document.getElementById('volumeInfo').innerText = volumeInfo;
}

function toggleAdminMessage() {
    const adminMessageSection = document.getElementById('adminMessageSection');
    adminMessageSection.classList.toggle('hidden');
}

function sendAdminMessage() {
    // Get the message from the textarea
    const adminMessage = document.getElementById('adminMessage').value;

    // TODO: Implement logic to send the message to the admin
    // For demonstration purposes, we'll log the message to the console
    console.log("Message to admin:", adminMessage);

    // Optionally, you can clear the textarea after sending the message
    document.getElementById('adminMessage').value = "";
}
