import React, { useState } from "react";
import styled, { createGlobalStyle } from "styled-components";
import axios from "axios";

const API_URL = "http://localhost:5001";

const GlobalStyle = createGlobalStyle`
  body {
    background: linear-gradient(120deg, #22223b 0%, #4a4e69 100%);
    color: #f2e9e4;
    font-family: 'Inter', sans-serif;
    margin: 0;
    min-height: 100vh;
  }
`;

const Container = styled.div`
  max-width: 600px;
  margin: 48px auto;
  background: rgba(34, 34, 59, 0.95);
  border-radius: 18px;
  box-shadow: 0 8px 32px 0 rgba(44, 44, 84, 0.37);
  padding: 40px 32px 32px 32px;
`;

const Title = styled.h1`
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #c9ada7;
  letter-spacing: 1px;
`;

const Subtitle = styled.h2`
  font-size: 1.1rem;
  font-weight: 400;
  margin-bottom: 32px;
  color: #f2e9e4;
  opacity: 0.8;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  margin-bottom: 18px;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  background: #f2e9e4;
  color: #22223b;
  outline: none;
`;

const Button = styled.button<{ secondary?: boolean }>`
  background: ${({ secondary }) => (secondary ? "#9a8c98" : "#4a4e69")};
  color: #f2e9e4;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 600;
  margin-right: ${({ secondary }) => (secondary ? "0" : "12px")};
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: ${({ secondary }) => (secondary ? "#bfa6a0" : "#22223b")};
  }
`;

const AnswerBox = styled.div`
  background: #f2e9e4;
  color: #22223b;
  border-radius: 8px;
  padding: 18px;
  margin-top: 24px;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(34, 34, 59, 0.08);
`;

const ChunksBox = styled.div`
  margin-top: 18px;
  background: #4a4e69;
  border-radius: 8px;
  padding: 12px;
  color: #f2e9e4;
  font-size: 0.95rem;
  opacity: 0.95;
`;

const ErrorMsg = styled.div`
  color: #ff6f61;
  margin-bottom: 16px;
  font-weight: 500;
`;

function App() {
  const [docUrl, setDocUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [chunks, setChunks] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleIndex = async () => {
    setError("");
    setAnswer("");
    setChunks([]);
    if (!docUrl) {
      setError("Please enter a document URL.");
      return;
    }
    setLoading(true);
    try {
      await axios.post(`${API_URL}/index`, { url: docUrl });
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to index document.");
      setLoading(false);
      return;
    }
    setLoading(false);
  };

  const handleAsk = async () => {
    setError("");
    setAnswer("");
    setChunks([]);
    if (!question) {
      setError("Please enter a question.");
      return;
    }
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/ask`, { question });
      setAnswer(res.data.answer);
      setChunks(res.data.chunks);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to get answer.");
    }
    setLoading(false);
  };

  const handleClear = async () => {
    setError("");
    setAnswer("");
    setChunks([]);
    setLoading(true);
    try {
      await axios.post(`${API_URL}/clear`);
    } catch (err: any) {
      setError("Failed to clear index.");
    }
    setLoading(false);
  };

  return (
    <>
      <GlobalStyle />
      <Container>
        <Title>LangChain Q&A</Title>
        <Subtitle>
          Upload a document (Google Doc export or PDF URL), ask questions, and get answers powered by AI.
        </Subtitle>
        {error && <ErrorMsg>{error}</ErrorMsg>}
        <Input
          type="text"
          placeholder="Paste document URL (Google Doc export or PDF)..."
          value={docUrl}
          onChange={e => setDocUrl(e.target.value)}
          disabled={loading}
        />
        <Button onClick={handleIndex} disabled={loading || !docUrl}>
          {loading ? "Indexing..." : "Index Document"}
        </Button>
        <Button secondary onClick={handleClear} disabled={loading}>
          Clear Index
        </Button>
        <Input
          type="text"
          placeholder="Ask a question about the document..."
          value={question}
          onChange={e => setQuestion(e.target.value)}
          style={{ marginTop: 24 }}
          disabled={loading}
        />
        <Button onClick={handleAsk} disabled={loading || !question}>
          {loading ? "Thinking..." : "Ask"}
        </Button>
        {answer && (
          <AnswerBox>
            <strong>Answer:</strong>
            <div style={{ marginTop: 8 }}>{answer}</div>
          </AnswerBox>
        )}
        {chunks.length > 0 && (
          <ChunksBox>
            <strong>Relevant Chunks:</strong>
            <ol>
              {chunks.map((chunk, i) => (
                <li key={i} style={{ marginBottom: 8 }}>{chunk}</li>
              ))}
            </ol>
          </ChunksBox>
        )}
      </Container>
    </>
  );
}

export default App;
