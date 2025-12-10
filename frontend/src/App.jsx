import { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) return;
    setLoading(true);
    const form = new FormData();
    form.append("file", file);
    
    try {
      const res = await axios.post("/analyze", form, {
  headers: { "Content-Type": "multipart/form-data" }
});
      setResult(res.data);
    } catch (e) { alert("Error: " + e.message); }
    setLoading(false);
  };

  return (
    <div style={{padding: "40px", fontFamily: "Arial", maxWidth: "1000px", margin: "0 auto"}}>
      <h1 style={{textAlign: "center", color: "#d32f2f"}}>Skin Cancer Detection</h1>
      <div style={{textAlign: "center", margin: "30px"}}>
        <input type="file" accept="image/*" onChange={e => setFile(e.target.files[0])} />
        <br /><br />
        <button onClick={upload} disabled={loading} style={{
          padding: "12px 30px", fontSize: "18px", background: "#d32f2f", color: "white", border: "none", borderRadius: "8px"
        }}>
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </div>

      {result && (
        <div style={{background: "#f0f0f0", padding: "30px", borderRadius: "15px"}}>
          <h2>Result</h2>
          <p><strong>Prediction:</strong> <span style={{fontSize: "24px", color: result.cancer ? "red" : "green"}}>
            {result.cancer ? "CANCER DETECTED" : "NO CANCER"}
          </span></p>
          <p><strong>Confidence:</strong> {result.confidence}%</p>
          <p><strong>Risk Level:</strong> {result.risk}</p>
          <p><strong>ABCD Score:</strong> {result.abcd_score}</p>

          <div style={{display: "flex", gap: "20px", flexWrap: "wrap", marginTop: "20px"}}>
            <img src={result.urls.original} alt="Original" style={{maxWidth: "400px", borderRadius: "10px"}} />
            <img src={result.urls.highlighted} alt="Highlighted" style={{maxWidth: "400px", borderRadius: "10px"}} />
          </div>

          <div style={{marginTop: "30px", textAlign: "center"}}>
            <a href={result.urls.report} download target="_blank"
               style={{padding: "15px 40px", background: "#1b5e20", color: "white", textDecoration: "none", borderRadius: "10px", fontSize: "18px"}}>
               Download Full Report (PDF)
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;