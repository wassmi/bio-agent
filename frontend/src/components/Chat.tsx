import { useState } from 'react'
import '../styles/Chat.css'

interface Message {
    text: string
    isUser: boolean
}

export const Chat = () => {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        
        // Add user message
        setMessages(prev => [...prev, { text: input, isUser: true }])
        
        // Get response from BioAgent
        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input }),
            })
            const data = await response.json()
            setMessages(prev => [...prev, { text: data.response, isUser: false }])
        } catch (error) {
            console.error('Error:', error)
        }
        
        setInput('')
    }

    return (
        <div className="chat-container">
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.isUser ? 'user' : 'agent'}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button type="submit">Send</button>
            </form>
        </div>
    )
}