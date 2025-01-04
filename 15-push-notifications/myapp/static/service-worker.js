// Regsiter Service Worker in the Browser
self.addEventListener('push', event => {
    // JSON string passed along with the Notification
    // This JSON structure will mainly contain a 'title' and 'body' of the message.
    const data = event.data.json();  
    console.log(data)

    const options = {
        body: data.body, // Body of the Notification Message
        icon: '/icon.png'  // Add your icon here, or dynamically use data.icon if available
    };

    event.waitUntil(
        // Display Notification - Title and Options
        self.registration.showNotification(data.title, options)
    );
});
