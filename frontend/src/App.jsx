import { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import SourcesPanel from './components/SourcesPanel'

function App() {
  const [sources, setSources] = useState([])

  return (
    <div className="h-screen bg-gray-50 flex flex-col">
      <header className="border-b border-gray-200 bg-white px-6 py-4">
        <h1 className="text-lg font-semibold text-gray-800">University RAG Assistant</h1>
      </header>

      <main className="flex-1 mx-auto w-full max-w-3xl flex flex-col gap-4 p-4 overflow-hidden">
        <div className="flex-1 bg-white border border-gray-200 rounded-lg overflow-hidden">
          <ChatWindow onNewSources={setSources} />
        </div>

        <SourcesPanel sources={sources} />
      </main>
    </div>
  )
}

export default App
