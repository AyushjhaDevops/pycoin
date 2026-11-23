
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [status, setStatus] = useState("Checking backend...");

  useEffect(() => {
    let active = true;

    fetch("http://127.0.0.1:8000/api/v1/health")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend unavailable");
        }

        return response.json();
      })
      .then((data) => {
        if (active) {
          setStatus(data.data.status);
        }
      })
      .catch(() => {
        if (active) {
          setStatus("Backend offline");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <main className="app">
      <section className="hero">
        <div className="coin-symbol">P</div>

        <p className="eyebrow">DECENTRALIZED DIGITAL CURRENCY</p>

        <h1>Welcome to PyCoin</h1>

        <p className="description">
          An educational cryptocurrency built with Python.
          Explore blockchain technology, cryptography and
          decentralized networking.
        </p>

        <div className="status">
          <span className="status-dot" />
          Backend: {status}
        </div>

        <div className="project-info">
          <div>
            <span>Coin</span>
            <strong>PyCoin</strong>
          </div>

          <div>
            <span>Symbol</span>
            <strong>PYC</strong>
          </div>

          <div>
            <span>Consensus</span>
            <strong>Proof of Work</strong>
          </div>

          <div>
            <span>Language</span>
            <strong>Python</strong>
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;
