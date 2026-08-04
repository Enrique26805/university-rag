import { useState } from 'react'

function SourcesPanel({ sources }) {
  const [expanded, setExpanded] = useState(true)

  if (!sources || sources.length === 0) {
    return null
  }

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <button
        type="button"
        onClick={() => setExpanded((prev) => !prev)}
        className="w-full flex items-center justify-between px-4 py-2 bg-gray-50 hover:bg-gray-100 text-sm font-medium text-gray-700"
      >
        <span>Sources ({sources.length})</span>
        <span className="text-gray-400">{expanded ? '−' : '+'}</span>
      </button>

      {expanded && (
        <ul className="divide-y divide-gray-100">
          {sources.map((source, index) => (
            <li
              key={`${source.document}-${index}`}
              className="flex items-center justify-between px-4 py-2 text-sm text-gray-600"
            >
              <span className="truncate">{source.document}</span>
              <span className="ml-3 shrink-0 text-xs text-gray-400">
                {source.score.toFixed(3)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default SourcesPanel
