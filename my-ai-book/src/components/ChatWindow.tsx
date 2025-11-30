import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown'; // <--- NEW IMPORT

// Define the shape of a message for TypeScript
interface Message {
  role: 'system' | 'user' | 'bot';
  content: string;
}

export default function ChatWindow() {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'system', content: 'Welcome to the Physical AI Assistant. Ask me anything about the course!' }
  ]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  // --- Original English text storage ---
  const [originalContent, setOriginalContent] = useState<string>('');

  useEffect(() => {
    if (isOpen && !originalContent) {
        const contentDiv = document.querySelector('article div.markdown') as HTMLElement;
        if (contentDiv) {
            setOriginalContent(contentDiv.innerHTML);
        }
    }
  }, [isOpen]);

  const resetToEnglish = () => {
    const contentDiv = document.querySelector('article div.markdown') as HTMLElement;
    if (contentDiv && originalContent) {
        contentDiv.innerHTML = originalContent;
        contentDiv.setAttribute('dir', 'ltr'); // Force Left-to-Right
        setMessages(prev => [...prev, { role: 'bot', content: "Restored original English text." }]);
    }
  };

  const personalizePage = async (level: string) => {
    setMessages(prev => [...prev, { role: 'bot', content: `Rewriting page to be ${level}...` }]);
    const contentDiv = document.querySelector('article div.markdown') as HTMLElement;
    if (!contentDiv) return;

    const sourceText = originalContent ? new DOMParser().parseFromString(originalContent, 'text/html').body.innerText : contentDiv.innerText;

    try {
      const response = await fetch('http://127.0.0.1:8000/personalize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: sourceText, level: level })
      });
      const data = await response.json();
      
      // FIX: Direct HTML injection (Backend now sends HTML)
      contentDiv.innerHTML = data.personalized_text;
      contentDiv.setAttribute('dir', 'ltr'); // English is LTR

      setMessages(prev => [...prev, { role: 'bot', content: "Page Updated!" }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: "Error: Backend not reachable." }]);
    }
  };

  const translatePage = async () => {
    setMessages(prev => [...prev, { role: 'bot', content: "Translating page to Urdu... Please wait." }]);
    const contentDiv = document.querySelector('article div.markdown') as HTMLElement;
    if (!contentDiv) return;

    const sourceText = originalContent ? new DOMParser().parseFromString(originalContent, 'text/html').body.innerText : contentDiv.innerText;

    try {
      const response = await fetch('http://127.0.0.1:8000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: sourceText })
      });
      const data = await response.json();
      
      // FIX: Direct HTML injection (Backend now sends HTML)
      contentDiv.innerHTML = data.translated_text;
      contentDiv.setAttribute('dir', 'rtl'); // Urdu is Right-to-Left

      setMessages(prev => [...prev, { role: 'bot', content: "Translation Complete!" }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: "Error: Backend not reachable." }]);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    const currentInput = input;
    setInput('');

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: currentInput })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'bot', content: data.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: "Error: Is the backend running?" }]);
    }
    setLoading(false);
  };

  return (
    <div className="chat-widget">
      {!isOpen && (
        <button className="chat-button" onClick={() => setIsOpen(true)}>🤖 AI Chat</button>
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
                {m.role === 'bot' ? (
                    <ReactMarkdown
                        components={{
                            // Custom renderer for code blocks to handle Urdu/RTL issues
                            code({node, inline, className, children, ...props}: any) {
                                const match = /language-(\w+)/.exec(className || '');
                                return !inline ? (
                                    <div style={{
                                        direction: 'ltr', // FORCE Left-to-Right for code
                                        textAlign: 'left', 
                                        background: '#282c34', 
                                        color: '#abb2bf', 
                                        padding: '10px', 
                                        borderRadius: '5px', 
                                        overflowX: 'auto',
                                        margin: '10px 0'
                                    }}>
                                        <code className={className} {...props}>
                                            {children}
                                        </code>
                                    </div>
                                ) : (
                                    <code style={{
                                        background: '#e0e0e0', 
                                        padding: '2px 4px', 
                                        borderRadius: '4px',
                                        fontFamily: 'monospace'
                                    }} {...props}>
                                        {children}
                                    </code>
                                )
                            }
                        }}
                    >
                        {m.content}
                    </ReactMarkdown>
                ) : (
                    m.content
                )}
              </div>
            ))}
            {loading && <div className="message bot">Thinking...</div>}
          </div>

          <div className="chat-input-container">
            <div className="action-buttons">
                <button onClick={resetToEnglish} style={{backgroundColor: '#95a5a6'}}>Eng</button>
                <button onClick={translatePage} style={{backgroundColor: '#e67e22'}}>Urdu</button>
                <button onClick={() => personalizePage('simple')} style={{backgroundColor: '#3498db'}}>Simple</button>
                <button onClick={() => personalizePage('advanced')} style={{backgroundColor: '#9b59b6'}}>Deep</button>
            </div>
            <div className="input-row">
                <input 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Ask about ROS 2..."
                />
                <button onClick={sendMessage} className="send-btn">Send</button>
            </div>
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
        .message.system { align-self: center; background: #e0e0e0; font-style: italic; font-size: 12px; color: #555; }
        .message.user { align-self: flex-end; background: #25c2a0; color: white; }
        .message.bot { align-self: flex-start; background: #e9ecef; color: black; }
        
        /* Removed old styles that conflicted with the new markdown renderer */
        .message.bot p { margin: 0 0 10px 0; }
        .message.bot strong { font-weight: bold; color: #2c3e50; }
        .message.bot ul { padding-left: 20px; margin: 5px 0; }

        .chat-input-container { padding: 10px; border-top: 1px solid #eee; background: white; border-radius: 0 0 12px 12px; display: flex; flex-direction: column; gap: 8px; }
        .action-buttons { display: flex; gap: 5px; justify-content: space-between; }
        .action-buttons button { flex: 1; color: white; border: none; padding: 6px; border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: bold; }
        .input-row { display: flex; gap: 5px; }
        .input-row input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; outline: none; }
        .send-btn { background: #25c2a0; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; }
      `}</style>
    </div>
  );
}