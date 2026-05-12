import Upload from "./components/Upload";
import "./app.css";

function App() {
  return (
    <div className="page">
      <div className="app-container wave">
        <h1 className="title delay-1">AKRITI</h1>

        <p className="subtitle delay-2">
          AI-native Business Intelligence Platform
        </p>


        <div className="delay-4">
          <Upload />
        </div>

        <p className="hint delay-5">
          Upload your data & view your insights
        </p>
      </div>
    </div>
  );
}

export default App;
