import React, { useState } from 'react';
import styles from './ChatWindow.module.css'; 

export default function ChatWindow() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Welcome to the Physical AI Assistant. Ask me anything about the course!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages([...messages, userMsg]);
    setLoading(true);
    const currentInput = input;
    setInput('');

    try {
      // NOTE: We use localhost for the demo because GitHub Pages (HTTPS) 
      // blocks requests to localhost (HTTP). 
      // For the video, record on http://localhost:3000
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            text: currentInput,
            selected_text: "" // We will add selection logic later
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'bot', content: data.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: "Error: Is the backend running? (Check console)" }]);
    }
    setLoading(false);
  };

  return (
    <div className="chat-widget">
      {!isOpen && (
        <button className="chat-button" onClick={() => setIsOpen(true)}>
          🤖 AI Chat
        </button>
      )}

      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <span>Physical AI Bot</span>
            <button onClick={() => setIsOpen(false)}>✖</button>
          </div>
          
          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                {m.content}
              </div>
            ))}
            {loading && <div className="message bot">Thinking...</div>}
          </div>

          <div className="chat-input">
            <input 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask about ROS 2..."
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}

      <style>{`
        .chat-widget { position: fixed; bottom: 20px; right: 20px; z-index: 9999; font-family: sans-serif; }
        .chat-button { background: #25c2a0; color: white; border: none; padding: 15px 25px; border-radius: 30px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
        .chat-window { width: 350px; height: 500px; background: white; border-radius: 12px; display: flex; flex-direction: column; box-shadow: 0 5px 20px rgba(0,0,0,0.3); border: 1px solid #ddd; }
        .chat-header { background: #1b1b1d; color: white; padding: 15px; border-radius: 12px 12px 0 0; display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
        .chat-header button { background: none; border: none; color: white; cursor: pointer; font-size: 16px; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background: #f9f9f9; }
        .message { max-width: 80%; padding: 10px; border-radius: 8px; font-size: 14px; line-height: 1.4; }
        .message.system { align-self: center; background: #e0e0e0; font-style: italic; font-size: 12px; }
        .message.user { align-self: flex-end; background: #25c2a0; color: white; }
        .message.bot { align-self: flex-start; background: #e9ecef; color: black; }
        .chat-input { padding: 10px; border-top: 1px solid #eee; display: flex; gap: 10px; background: white; border-radius: 0 0 12px 12px; }
        .chat-input input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; outline: none; }
        .chat-input button { background: #25c2a0; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }
      `}</style>
    </div>
  );
}