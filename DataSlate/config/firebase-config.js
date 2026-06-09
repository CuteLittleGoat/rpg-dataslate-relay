// Plik logiki modułu: konfiguracja, funkcje i obsługa zdarzeń / Module logic file: configuration, functions, and event handling
// config/firebase-config.js
// GLOBALNA konfiguracja Firebase dla GM.html i DataSlate.html
// (nie używamy "export", żeby działało też z firebase-*-compat)

// WAŻNE WDROŻENIE: Każda grupa (każdy serwer) powinna mieć własny projekt Firebase i własny komplet kluczy poniżej.
// IMPORTANT DEPLOYMENT: Each group (each server) should use its own Firebase project and its own full key set below.
window.firebaseConfig = {
  apiKey: "INSERT_YOUR_API_KEY",
  authDomain: "INSERT_YOUR_AUTH_DOMAIN",
  projectId: "INSERT_YOUR_PROJECT_ID",
  storageBucket: "INSERT_YOUR_STORAGE_BUCKET",
  messagingSenderId: "INSERT_YOUR_MESSAGING_SENDER_ID",
  appId: "INSERT_YOUR_APP_ID",
};
