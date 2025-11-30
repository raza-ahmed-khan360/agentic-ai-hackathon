import React, { useState } from 'react';

export default function ChatBot() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input) return;
    
    const newMsg = { role: 'user', content: input };
    setMessages([...messages, newMsg]);
    
    // Call your Python Backend
    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'bot', content: data.answer }]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ position: 'fixed', bottom: 20, right: 20, width: 300, background: 'white', border: '1px solid #ccc', padding: 10 }}>
      <div style={{ height: 200, overflowY: 'scroll' }}>
        {messages.map((m, i) => (
          <div key={i}><strong>{m.role}:</strong> {m.content}</div>
        ))}
      </div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}