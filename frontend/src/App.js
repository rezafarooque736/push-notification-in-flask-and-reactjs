import { useEffect } from "react";
import { getToken } from "firebase/messaging";
import "./App.css";
import { messaging } from "./firebase";
import axios from "axios";

function App() {
  async function requestPermission() {
    const permission = await Notification.requestPermission();
    if (permission === "granted") {
      // Generate Token
      const token = await getToken(messaging, {
        vapidKey:
          "BHFnKXbYuc_ao0AybJjlosAYyjnwnERj3OPs9eofrJNTZWGkVcwGDm3qQso0DeCpDBZ-toK9Kd027L3XCMcIToY",
      });
      console.log("Token Gen", token);
      // Send this token  to server ( db)
      await axios.post("/store-tokens", { token });
    } else if (permission === "denied") {
      alert("You denied for the notification");
    }
  }

  useEffect(() => {
    // Req user for notification permission
    requestPermission();
  }, []);

  const sendMultiplePushNotification = async () => {
    await axios.get("/send-notification-to-multiple");
  };

  const sendSinglePushNotification = async () => {
    await axios.get("/send-notification-to-one");
  }

  const buttonStyle = {
    padding: "10px",
    backgroundColor: "#0094de",
    color: "white",
    borderRadius: "10px",
    margin: "10px",
    cursor: "pointer",
    border: "none",
    outline: "none",
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
      }}
    >
      <button onClick={sendSinglePushNotification} style={buttonStyle}>
        send single push notification
      </button>

      <button onClick={sendMultiplePushNotification} style={buttonStyle}>
        send multiple push notification
      </button>
    </div>
  );
}

export default App;
