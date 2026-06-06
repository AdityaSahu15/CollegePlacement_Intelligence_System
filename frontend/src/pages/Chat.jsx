import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, AlertCircle, Loader2 } from 'lucide-react';
import { api } from '../api';

const suggestedQuestions = [
  "Which companies visited last year?",
  "Which companies allow below 7 CGPA?",
  "Who got into Amazon that I can contact?",
  "What is the selection process for Deloitte?"
];

const Chat = ({ messages, setMessages }) => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (text) => {
    if (!text.trim()) return;
    
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await api.chat(text);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.answer,
        sources: response.sources
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'error',
        content: "Sorry, I encountered an error connecting to the backend. Please ensure the server and Ollama are running."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto max-w-5xl h-[calc(100vh-6rem)] md:h-[calc(100vh-8rem)] flex flex-col mt-20 md:mt-24 mb-4">
      <div className="flex-1 bg-glass rounded-2xl flex flex-col overflow-hidden border border-bg-tertiary shadow-2xl">
        
        {/* Header */}
        <div className="p-4 border-b border-bg-tertiary bg-bg-secondary/50 flex items-center gap-3">
          <Bot className="text-accent-primary" size={24} />
          <div>
            <h2 className="font-semibold text-lg leading-tight">Placement Assistant</h2>
            <p className="text-xs text-text-secondary">Powered by Qwen3-8B</p>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center animate-fade-in">
              <Bot size={64} className="text-accent-primary/20 mb-6" />
              <h3 className="text-2xl font-semibold mb-2">How can I help you prepare?</h3>
              <p className="text-text-secondary mb-8 max-w-md">
                Ask me anything about past company visits, selection processes, or senior experiences.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl">
                {suggestedQuestions.map((q, idx) => (
                  <button 
                    key={idx}
                    onClick={() => handleSend(q)}
                    className="p-4 rounded-xl border border-bg-tertiary bg-bg-primary/50 text-left hover:border-accent-primary hover:bg-accent-primary/5 transition-all text-sm text-text-secondary hover:text-text-primary"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''} animate-fade-in`}>
                <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
                  msg.role === 'user' ? 'bg-accent-primary' : 
                  msg.role === 'error' ? 'bg-danger' : 'bg-bg-tertiary'
                }`}>
                  {msg.role === 'user' ? <User size={20} /> : 
                   msg.role === 'error' ? <AlertCircle size={20} /> : <Bot size={20} />}
                </div>
                <div className={`max-w-[80%] rounded-2xl p-4 ${
                  msg.role === 'user' ? 'bg-accent-primary/20 border border-accent-primary/30 rounded-tr-none' : 
                  msg.role === 'error' ? 'bg-danger/20 border border-danger/30 text-danger rounded-tl-none' : 
                  'bg-bg-secondary border border-bg-tertiary rounded-tl-none'
                }`}>
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="flex gap-4 animate-fade-in">
              <div className="w-10 h-10 rounded-full bg-bg-tertiary flex items-center justify-center shrink-0">
                <Bot size={20} />
              </div>
              <div className="bg-bg-secondary border border-bg-tertiary rounded-2xl rounded-tl-none p-4 flex items-center gap-3">
                <Loader2 className="animate-spin text-accent-primary" size={20} />
                <span className="text-text-secondary text-sm">Searching knowledge base...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-bg-secondary/50 border-t border-bg-tertiary">
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSend(input); }}
            className="flex gap-3"
          >
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about placements..."
              className="input-field flex-1"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              disabled={isLoading || !input.trim()}
              className="btn btn-primary px-6"
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;
