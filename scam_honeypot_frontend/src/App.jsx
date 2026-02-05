import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import './index.css'
import { Send, Shield, Zap, Database, User, Bot } from 'lucide-react'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [intel, setIntel] = useState([])
  const [metadata, setMetadata] = useState({
    scam_detected: false,
    strategy: 'N/A',
    turn: 0
  })

  // Generating a random session ID for this load
  const [conversationId] = useState(() => `session_${Math.random().toString(36).substr(2, 9)}`)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    if (e) e.preventDefault()
    if (!input.trim() || loading) return

    const userMsg = input
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setLoading(true)

    try {
      const res = await axios.post('http://localhost:8000/api/v1/message', {
        conversation_id: conversationId,
        message: userMsg
      })

      const data = res.data

      setMessages(prev => [...prev, { role: 'agent', content: data.agent_reply }])

      if (data.metadata) {
        setMetadata({
          scam_detected: data.metadata.scam_detected,
          strategy: data.metadata.strategy,
          turn: data.metadata.turn,
          reasons: data.metadata.detection_reasons
        })
        if (data.metadata.all_intel) {
          setIntel(data.metadata.all_intel)
        }
      }

    } catch (err) {
      console.error(err)
      setMessages(prev => [...prev, { role: 'system', content: 'Not Accessible: Backend Error' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="chat-section">
        <header style={{ padding: '20px', borderBottom: '1px solid #333', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Shield size={24} color="#646cff" />
          <h2>Agentic Honey-Pot</h2>
          <span style={{ fontSize: '0.8em', color: '#666', marginLeft: 'auto' }}>ID: {conversationId}</span>
        </header>

        <div className="messages">
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', color: '#666', marginTop: '50px' }}>
              <Bot size={48} style={{ opacity: 0.5, marginBottom: '20px' }} />
              <p>Waiting for scammer contact...</p>
              <p style={{ fontSize: '0.8em' }}>Try sending: "You won a lottery, pay tax to UPI"</p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              {msg.role === 'agent' && <span style={{ fontSize: '0.7em', color: '#888', display: 'block', marginBottom: '4px' }}>Agent (Gemini 2.0)</span>}
              {msg.content}
            </div>
          ))}
          {loading && <div className="message agent">...Typing...</div>}
          <div ref={messagesEndRef} />
        </div>

        <form className="input-area" onSubmit={sendMessage}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type a message (act as a scammer)..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input}>
            <Send size={20} />
          </button>
        </form>
      </div>

      <div className="sidebar">
        <h3>Live Intelligence</h3>

        <div className="stat-card">
          <div className="stat-label">Status</div>
          <div className="stat-value" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {metadata.scam_detected ? '🚨 SCAM DETECTED' : '✅ MONITORING'}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Agent Strategy</div>
          <div className="stat-value" style={{ color: '#646cff' }}>{metadata.strategy || 'PASSIVE'}</div>
        </div>

        {intel.length > 0 && (
          <div className="stat-card" style={{ borderColor: '#4dffaa44' }}>
            <div className="stat-label">Extracted Data ({intel.length})</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '8px' }}>
              {intel.map((item, i) => (
                <div key={i} style={{ background: '#111', padding: '8px', borderRadius: '4px', fontSize: '0.85em' }}>
                  <div style={{ color: '#888', fontSize: '0.8em' }}>{item.type}</div>
                  <div style={{ color: '#fff', wordBreak: 'break-all' }}>{item.value}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ marginTop: '20px' }}>
          <div className="stat-label">Turn Count: {metadata.turn}</div>
          {metadata.reasons && (
            <div style={{ marginTop: '10px' }}>
              <div className="stat-label">Detection Signals</div>
              {metadata.reasons.map((r, i) => (
                <span key={i} className="badge scam" style={{ margin: '2px' }}>{r}</span>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default App
