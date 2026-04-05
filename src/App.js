import './App.css';
import { useState } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

  const onFileChange = (event) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setResult(null);
    setError('');
  };

  const analyzeDocument = async () => {
    if (!selectedFile) {
      setError('Please select a PDF first.');
      return;
    }

    setIsLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze-document`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      if (!response.ok || data.status !== 'SUCCESS') {
        throw new Error(data.message || 'Failed to analyze document.');
      }

      setResult(data);
    } catch (requestError) {
      setError(requestError.message || 'Could not connect to backend service.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <main className="app-shell">
        <h1>Legal Guardian AI</h1>
        <p className="subtitle">Upload a contract PDF and get an instant plain-English summary.</p>

        <div className="card">
          <label htmlFor="file-input" className="label">Choose PDF document</label>
          <input id="file-input" type="file" accept=".pdf" onChange={onFileChange} />
          {selectedFile && <p className="file-name">Selected: {selectedFile.name}</p>}

          <button className="analyze-btn" onClick={analyzeDocument} disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Analyze Document'}
          </button>

          {error && <p className="error">{error}</p>}
        </div>

        {result && (
          <section className="card results">
            <h2>Summary</h2>
            <p>{result.summary || 'No summary returned.'}</p>

            <h3>Extracted Fields</h3>
            <pre>{JSON.stringify(result.structured_data || {}, null, 2)}</pre>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
