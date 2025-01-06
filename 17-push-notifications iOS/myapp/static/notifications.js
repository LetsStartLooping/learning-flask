// Check Permission for Notifications
function checkNotificationPermission() {

    // Check Permission Status
    if (Notification.permission === "granted") {
        console.log("Notification permission is granted.");
        // You can set up notifications here
    } else if (Notification.permission === "denied") {
        console.log("Notification permission is denied.");
        // The user has denied notification permission
    } else {
        console.log("Notification permission is not decided yet.");
        if (isSafariBrowser()) {
            // Show the button to ask for permission
            var button = document.getElementById("notification_permission");
            button.style.display = 'block';
            button.addEventListener("click", () => {
                registerServiceWorker();
            });
        } else {
            registerServiceWorker();
        }
    }
}

// Register Service Worker and Subscribe to Push Notifications
function registerServiceWorker() {

    // Check if already registered for the Service Worker
    navigator.serviceWorker.getRegistration(sw_path).then(function (registration) {
        if (registration) {
            console.log(`Service Worker already registered for scope: ${sw_path}`, registration);
            // Wait for active state if necessary
            waitForServiceWorkerActivation(registration).then(() => {
                subscribeUserToPushNotifications(registration);
            });
        } else {
            console.log(`No Service Worker registered for scope: ${sw_path}`);
            // Register Service Worker
            navigator.serviceWorker.register(sw_path)
                .then(function (registration) {
                    console.log('Service Worker registered:', registration);
                    // Subscribe to Push Notification
                    // Wait for active state if necessary
                    waitForServiceWorkerActivation(registration).then(() => {
                        subscribeUserToPushNotifications(registration);
                    });
                })
                .catch(function (error) {
                    console.error('Service Worker registration failed:', error);
                });
        }
    }).catch(function (error) {
        console.error(`Error checking Service Worker for scope: ${sw_path}`, error);
    });
}


        // Hide Request to Subscription button - Safari Only
        // document.getElementById(permission_element_id).style.display = 'none'

// Subscribe to Push Notifications
async function subscribeUserToPushNotifications(registration) {
    try {
        // Subscribe to notifications
        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(publicVapidKey) // Public VAPID Key passed from Flask App
        });

        console.log(JSON.stringify(subscription));

        const dataToSend = {
            ...subscription.toJSON(),
            // Add additional fields to JSON
            // user_id: user_id
        }

        // Send subscription information back to the flask app (server)
        await fetch('/subscribe', {
            method: 'POST',
            body: JSON.stringify(dataToSend),
            headers: {
                'content-type': 'application/json'
            }
        });

        console.log('User subscribed to notifications!!!!');

        // Hide Request to Subscription button - Safari Only
        document.getElementById("notification_permission").style.display = 'none'

        return subscription;
    } catch (error) {
        console.error('Subscription failed:', error);
        throw error; // Re-throw the error for handling elsewhere if needed
    }
}

// Base64 to Unit8 Conversion
function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}


function waitForServiceWorkerActivation(registration) {
    return new Promise((resolve) => {
        if (registration.active) {
            // Service Worker is already active
            resolve();
        } else if (registration.installing) {
            // Wait for the 'statechange' event
            registration.installing.addEventListener('statechange', function () {
                if (registration.active) {
                    resolve();
                }
            });
        } else if (registration.waiting) {
            // Waiting state indicates it's ready to activate
            registration.waiting.addEventListener('statechange', function () {
                if (registration.active) {
                    resolve();
                }
            });
        }
    });
}

function isSafariBrowser() {
    var userAgent = navigator.userAgent.toLowerCase();

    // Safari's user agent string contains 'safari' and not 'chrome' or 'chromium'
    var isSafari = userAgent.includes('safari') && !userAgent.includes('chrome') && !userAgent.includes('chromium');

    return isSafari;
}