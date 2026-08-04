import ReactMarkdown from 'react-markdown'

function MarkdownAnswer({ answer }) {
  return (
    <div className="markdown-content text-sm leading-relaxed">
      <ReactMarkdown>{answer}</ReactMarkdown>
    </div>
  )
}

export default MarkdownAnswer
