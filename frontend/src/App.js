import { useEffect } from "react";
import { getToken } from "firebase/messaging";
import logo from "./logo.svg";
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

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
