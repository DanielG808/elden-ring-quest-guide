import { useState } from "react";
import viteLogo from "/vite.svg";
import "./index.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank"></a>
      </div>
      <h1 className="text-3xl text-red-500 font-bold underline">Elden Ring Quest Tracker</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="text-bold">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;