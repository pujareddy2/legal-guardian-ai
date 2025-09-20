import React, { useState, useEffect, useRef } from 'react';

// --- SVG Icons for a professional look ---
const Icons = {
  upload: ( <svg xmlns="http://www.w.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" /></svg> ),
  party: ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg> ),
  date: ( <svg xmlns="http://www.w.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" /></svg> ),
  law: ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" /><polyline points="14 2 14 8 20 8" /><line x1="12" y1="18" x2="12" y2="12" /><line x1="9" y1="15" x2="15" y2="15" /></svg> ),
  obligation: ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 11 12 14 22 4" /><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" /></svg> ),
  default: ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>),
  summary: ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22a10 10 0 1 1 0-20 10 10 0 0 1 0 20z"/><path d="m12 14-2-2 4-4-2-2"/><path d="m12 18-4-4"/></svg>),
  ask: ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>)
};

const getIconForLabel = (label) => {
    const lowerLabel = label.toLowerCase();
    if (lowerLabel.includes('party')) return Icons.party;
    if (lowerLabel.includes('date')) return Icons.date;
    if (lowerLabel.includes('law')) return Icons.law;
    if (lowerLabel.includes('obligation')) return Icons.obligation;
    return Icons.default;
};

// --- Style Component (to avoid needing a separate .css file) ---
const AppStyles = () => {
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      :root {
        --primary-bg: #0D1B2A; --secondary-bg: #1B263B; --card-bg: #2a3b4f;
        --accent-color: #3ddc84; --text-color: #e0e1dd; --subtle-text: #b0b5bd;
        --glow-color: rgba(61, 220, 132, 0.5);
      }
      body { background-color: var(--primary-bg); color: var(--text-color); font-family: 'Segoe UI', 'Roboto', sans-serif; padding: 40px; transition: background-color 0.3s; }
      .App { text-align: center; } .App-header { max-width: 1200px; margin: 0 auto; }
      .logo-title { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 10px; }
      .logo-title h1 { font-size: 2.5rem; font-weight: 700; color: white; }
      .logo-icon { width: 40px; height: 40px; stroke: var(--accent-color); }
      .subtitle { font-size: 1.2rem; color: var(--subtle-text); margin-bottom: 40px; }
      .upload-box { background-color: var(--secondary-bg); border: 2px dashed #415A77; border-radius: 12px; padding: 40px; cursor: pointer; transition: all 0.3s ease; }
      .upload-box:hover { border-color: var(--accent-color); background-color: var(--card-bg); }
      .upload-box-content { display: flex; flex-direction: column; align-items: center; gap: 15px; }
      .upload-box-content svg { width: 48px; height: 48px; stroke: var(--accent-color); }
      .upload-box-content p { margin: 0; font-weight: 500; }
      .upload-box-content span { font-size: 0.9rem; color: var(--subtle-text); }
      #file-input { display: none; }
      .analyze-button { background-image: linear-gradient(45deg, #3ddc84 0%, #2a9d8f 100%); border: none; padding: 12px 24px; border-radius: 8px; color: white; font-weight: bold; cursor: pointer; transition: all 0.3s ease; margin-top: 20px; box-shadow: 0 4px 15px rgba(61, 220, 132, 0.3); }
      .analyze-button:disabled { background-image: none; background-color: #555; cursor: not-allowed; box-shadow: none; }
      .analyze-button:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(61, 220, 132, 0.4); }
      .analysis-section { margin-top: 50px; text-align: left; }
      .loader { width: 48px; height: 48px; border: 5px solid #FFF; border-bottom-color: var(--accent-color); border-radius: 50%; display: inline-block; box-sizing: border-box; animation: rotation 1s linear infinite; margin: 20px auto; }
      @keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
      .error-message { color: #ff6b6b; font-weight: bold; background-color: var(--card-bg); padding: 20px; border-radius: 12px; }
      .results-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
      .result-card { background-color: var(--card-bg); padding: 20px; border-radius: 12px; border: 1px solid #415A77; transition: all 0.3s ease; opacity: 0; transform: translateY(20px); animation: fadeIn 0.5s forwards; }
      @keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
      .result-card-header { display: flex; align-items: center; gap: 10px; color: var(--accent-color); margin-bottom: 15px; }
      .result-card-header h3 { margin: 0; font-size: 1.1rem; color: #e0e1dd; }
      .result-card-content p, .result-card-content li { font-size: 0.95rem; line-height: 1.6; color: var(--subtle-text); white-space: pre-wrap; }
      .result-card-content ul { padding-left: 20px; margin: 0; }
      .summary-card { grid-column: 1 / -1; } /* Make summary span full width */
      .ask-section { margin-top: 40px; background-color: var(--secondary-bg); padding: 30px; border-radius: 12px; opacity: 0; animation: fadeIn 0.5s 0.5s forwards;}
      .ask-input-group { display: flex; gap: 10px; }
      .ask-input { flex-grow: 1; background-color: var(--card-bg); border: 1px solid #415A77; border-radius: 8px; color: var(--text-color); padding: 12px; font-size: 1rem; }
      .ask-input:focus { outline: none; border-color: var(--accent-color); }
      .ask-button { background-image: linear-gradient(45deg, #3ddc84 0%, #2a9d8f 100%); border: none; padding: 12px 20px; border-radius: 8px; color: white; font-weight: bold; cursor: pointer; transition: all 0.3s ease; }
      .ask-button:hover:not(:disabled) { opacity: 0.9; } .ask-button:disabled { background-image: none; background-color: #555; cursor: not-allowed; }
      .answer-card { margin-top: 20px; }
    `;
    document.head.appendChild(style);
    return () => { document.head.removeChild(style); };
  }, []);
  return null;
};

// --- Main App Component ---
function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  // State for new Gemini features
  const [documentText, setDocumentText] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isAsking, setIsAsking] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setAnalysisResult(null); setError(null); setDocumentText(''); setQuestion(''); setAnswer('');
    }
  };

  const handleBoxClick = () => fileInputRef.current.click();
  
  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setIsLoading(true); setError(null); setAnalysisResult(null); setDocumentText(''); setAnswer('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze-document', { method: 'POST', body: formData });
      const data = await response.json();
      if (data.status === 'SUCCESS') {
        setAnalysisResult(data);
        setDocumentText(data.full_text || '');
      } else {
        setError(data.message || 'An unknown error occurred.');
      }
    } catch (err) {
      setError('Failed to connect to the backend. Is the server running?');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question || !documentText) return;
    setIsAsking(true); setAnswer('');

    try {
        const response = await fetch('http://127.0.0.1:8000/ask-question', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ document_text: documentText, question: question })
        });
        const data = await response.json();
        if (data.status === 'SUCCESS') {
            setAnswer(data.answer);
        } else {
            setAnswer(`Error: ${data.message}`);
        }
    } catch (err) {
        setAnswer('Error: Could not connect to the backend.');
    } finally {
        setIsAsking(false);
    }
  };

  const RenderResults = ({ data }) => (
    <div className="results-grid">
      {data.summary && (
        <div className="result-card summary-card" style={{ animationDelay: `0ms` }}>
          <div className="result-card-header">{Icons.summary}<h3>Plain English Summary</h3></div>
          <div className="result-card-content"><p>{data.summary}</p></div>
        </div>
      )}
      {data.structured_data && Object.keys(data.structured_data).map((key, index) => (
        <div className="result-card" key={key} style={{ animationDelay: `${(index + 1) * 100}ms` }}>
          <div className="result-card-header">{getIconForLabel(key)}<h3>{key.replace(/([A-Z])/g, ' $1').trim()}</h3></div>
          <div className="result-card-content">
            {Array.isArray(data.structured_data[key]) ? (
              <ul>{data.structured_data[key].map((item, i) => <li key={i}>{item}</li>)}</ul>
            ) : (<p>{data.structured_data[key]}</p>)}
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <>
      <AppStyles />
      <div className="App">
        <header className="App-header">
          <div className="logo-title">
             <svg className="logo-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
             <h1>Legal Guardian AI</h1>
          </div>
          <p className="subtitle">Your personal AI-powered legal document analyzer.</p>
          
          <div className="upload-box" onClick={handleBoxClick}>
            <input id="file-input" type="file" onChange={handleFileChange} accept=".pdf" ref={fileInputRef} />
            <div className="upload-box-content">
                {Icons.upload}
                {selectedFile ? <p>{selectedFile.name}</p> : <> <p>Click to upload or drag & drop</p> <span>PDF documents only</span> </> }
            </div>
          </div>

          <button className="analyze-button" onClick={handleAnalyze} disabled={isLoading || !selectedFile}>
            {isLoading ? 'Analyzing...' : 'Analyze Document'}
          </button>
          
          <div className="analysis-section">
            {isLoading && <div className="loader"></div>}
            {error && <p className="error-message">{error}</p>}
            {analysisResult && <RenderResults data={analysisResult} />}
            
            {analysisResult && !isLoading && (
              <div className="ask-section">
                 <div className="result-card-header">{Icons.ask}<h3>Ask Your "What-If" Questions</h3></div>
                 <div className="ask-input-group">
                    <input 
                        type="text"
                        className="ask-input"
                        placeholder="e.g., What happens if I miss a payment?"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                    />
                    <button className="ask-button" onClick={handleAskQuestion} disabled={isAsking || !question}>
                        {isAsking ? '...' : 'Get Answer'}
                    </button>
                 </div>
                 {isAsking && <div className="loader" style={{margin: '20px 0 0 0'}}></div>}
                 {answer && (
                    <div className="result-card answer-card" style={{marginTop: '20px'}}>
                         <div className="result-card-content"><p>{answer}</p></div>
                    </div>
                 )}
              </div>
            )}
          </div>
        </header>
      </div>
    </>
  );
}

export default App;