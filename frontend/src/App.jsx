import { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [preview, setPreview] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);

  const handleUpload = (e) => {
    const f = e.target.files[0];
    if (f) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setReport(null);
    }
  };

    const analyze = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('/analyze', formData);
      setReport(res.data);
    } catch (err) {
      alert('Network Error: ' + err.message);
    }
    setLoading(false);
  };

  const downloadPDF = () => {
    const printContent = document.getElementById('report').innerHTML;
    const original = document.body.innerHTML;
    document.body.innerHTML = printContent;
    window.print();
    document.body.innerHTML = original;
  };

  if (loading) {
    return <div style={{textAlign: 'center', padding: '100px', fontSize: '30px'}}>Analyzing your skin...</div>;
  }

  return (
    <div style={{background: 'linear-gradient(135deg, #e3f2fd, #bbdefb)', minHeight: '100vh', padding: '20px', textAlign: 'center'}}>
      <h1 style={{color: '#0066ff', fontSize: '48px', marginBottom: '10px'}}>AI Skin Cancer Scanner</h1>
      <p style={{fontSize: '26px', color: '#555', marginBottom: '40px'}}>Instant ABCD Report Generator</p>
      <div style={{background: '#fff3e0', padding: '20px', borderRadius: '20px', margin: '40px auto', maxWidth: '800px', border: '3px solid #ff9800', color: '#d84315', fontWeight: 'bold'}}>
        ⚠️ NOT a medical diagnosis — consult a doctor
      </div>

      {!preview ? (
        <div style={{background: 'white', padding: '50px', borderRadius: '30px', margin: '30px auto', maxWidth: '800px', boxShadow: '0 20px 50px rgba(0,0,0,0.15)'}}>
          <h2 style={{fontSize: '40px', marginBottom: '30px'}}>Upload Skin Photo</h2>
          <label style={{display: 'block'}}>
            <input type="file" accept="image/*" capture="environment" onChange={handleUpload} style={{display: 'none'}} />
            <button style={{padding: '20px 60px', fontSize: '24px', background: '#0066ff', color: 'white', border: 'none', borderRadius: '20px', cursor: 'pointer', margin: '15px'}}>📷 Take Photo</button>
          </label>
          <p style={{margin: '40px', fontSize: '22px', color: '#777'}}>or</p>
          <label>
            <input type="file" accept="image/*" onChange={handleUpload} style={{display: 'none'}} />
            <div style={{border: '5px dashed #999', padding: '80px', borderRadius: '25px', cursor: 'pointer', display: 'inline-block'}}>
              <p style={{fontSize: '28px'}}>Upload from Gallery</p>
            </div>
          </label>
        </div>
      ) : (
        <div>
          <div style={{background: 'white', padding: '50px', borderRadius: '30px', margin: '30px auto', maxWidth: '800px', boxShadow: '0 20px 50px rgba(0,0,0,0.15)'}}>
            <img src={preview} alt="Skin preview" style={{maxWidth: '100%', maxHeight: '500px', border: '10px solid #0066ff', borderRadius: '25px', margin: '30px 0'}} />
            <button onClick={analyze} style={{padding: '20px 60px', fontSize: '24px', background: '#00c853', color: 'white', border: 'none', borderRadius: '20px', cursor: 'pointer'}}>Generate ABCD Report</button>
          </div>

          {report && (
            <div id="report" style={{background: 'white', padding: '50px', borderRadius: '30px', margin: '30px auto', maxWidth: '800px', boxShadow: '0 20px 50px rgba(0,0,0,0.15)'}}>
              <h2 style={{fontSize: '44px', color: '#0066ff', marginBottom: '50px'}}>Your ABCD Report</h2>
              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', margin: '50px 0'}}>
                {Object.entries(report).map(([key, value]) => (
                  <div key={key} style={{background: '#f0f8ff', padding: '30px', borderRadius: '20px', borderLeft: '8px solid #0066ff'}}>
                    <div style={{fontSize: '20px', color: '#333'}}>{key}</div>
                    <p style={{fontSize: '32px', fontWeight: 'bold', color: '#0066ff', marginTop: '10px'}}>{value}</p>
                  </div>
                ))}
              </div>
              <div style={{background: '#ffebee', padding: '40px', borderRadius: '20px', color: '#c62828', fontSize: '32px', fontWeight: 'bold', margin: '40px 0'}}>
                {report["Risk Level"]} — Urgent consultation recommended
              </div>
              <button onClick={downloadPDF} style={{padding: '25px 80px', fontSize: '28px', background: '#0066ff', color: 'white', border: 'none', borderRadius: '20px', cursor: 'pointer'}}>
                📄 Download PDF Report
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;