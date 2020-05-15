import React, { useEffect, useState } from 'react';

function App() {
  const [currentMessage, setMessage] = useState("Hello from client");

  useEffect(() => {
    fetch("/message").then(res => res.json()).then(msg => setMessage(msg.message));
  })

  return (
    <div className="App">
        <p>
          {currentMessage}
        </p>
    </div>
  );
}

export default App;
