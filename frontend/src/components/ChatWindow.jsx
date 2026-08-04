import { useState } from 'react'
import { askQuestion, ValidationError, BackendUnavailableError } from '../api/client'
import MarkdownAnswer from './MarkdownAnswer'

function ChatWindow({ onNewSources }) {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(event) {
    event.preventDefault()

    const question = input.trim()
    if (!question || loading) {
      return
    }

    setError(null)
    setMessages((prev) => [...prev, { role: 'user', text: question }])
    setInput('')
    setLoading(true)

    try {
      const data = await askQuestion(question)
      setMessages((prev) => [...prev, { role: 'assistant', text: data.answer }])
      onNewSources?.(data.sources)
    } catch (err) {
      if (err instanceof ValidationError) {
        setError({ kind: 'validation', message: err.message })
      } else if (err instanceof BackendUnavailableError) {
        setError({ kind: 'unavailable', message: err.message })
      } else {
        setError({ kind: 'generic', message: 'Something went wrong. Please try again.' })
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-3 p-4">
        {messages.length === 0 && (
          <p className="text-sm text-gray-400 text-center mt-8">
            Ask a question about your course materials to get started.
          </p>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white rounded-br-sm'
                  : 'bg-gray-100 text-gray-800 rounded-bl-sm'
              }`}
            >
              {message.role === 'assistant' ? (
                <MarkdownAnswer answer={message.text} />
              ) : (
                message.text
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] rounded-2xl rounded-bl-sm bg-gray-100 px-4 py-2 text-sm text-gray-400">
              Thinking...
            </div>
          </div>
        )}

        {error && (
          <div className="flex justify-start">
            <div
              className={`max-w-[80%] rounded-2xl rounded-bl-sm px-4 py-2 text-sm ${
                error.kind === 'validation'
                  ? 'bg-yellow-50 text-yellow-800 border border-yellow-200'
                  : 'bg-red-50 text-red-700 border border-red-200'
              }`}
            >
              {error.kind === 'validation' && error.message}
              {error.kind === 'unavailable' &&
                `The backend is unavailable right now: ${error.message}`}
              {error.kind === 'generic' && error.message}
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2 border-t border-gray-200 p-3">
        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
          className="flex-1 rounded-full border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-full bg-blue-600 px-5 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:bg-gray-300"
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatWindow
