import { useState } from "react"
import axios from "axios"

function App() {
  const [repoUrl, setRepoUrl] = useState("")
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState([])
  const [lastRepoTopic, setLastRepoTopic] = useState("")

  const [repoStatus, setRepoStatus] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [isTyping, setIsTyping] = useState(false)

  const handleAnalyze = async () => {
    if (!repoUrl.trim()) {
      setRepoStatus("Please enter a GitHub repository URL.")
      return
    }

    try {
      setIsAnalyzing(true)
      setRepoStatus("Analyzing repository...")

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze-repo",
        {
          repo_url: repoUrl
        }
      )

      setRepoStatus(response.data.message)
    } catch (error) {
      console.error(error)
      setRepoStatus("Failed to analyze repository ❌")
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleSend = async () => {
    if (!message.trim()) return

    const currentMessage = message

    const userMessage = {
      role: "user",
      text: currentMessage
    }

    setMessages((prev) => [...prev, userMessage])
    setMessage("")
    setIsTyping(true)

    try {
      const response = await axios.post(
  "http://127.0.0.1:8000/chat",
  {
    message: currentMessage,
    messages: messages.map((m) => m.text),
    last_repo_topic: lastRepoTopic
  },
  {
    responseType: "text"
  }
)

const aiMessage = {
  role: "assistant",
  text: response.data
}

      setMessages((prev) => [...prev, aiMessage])
      setLastRepoTopic(response.data.last_repo_topic)
    } catch (error) {
      console.error(error)

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Something went wrong while contacting the backend."
        }
      ])
    } finally {
      setIsTyping(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend()
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="max-w-5xl mx-auto">

        <div className="mb-10">
          <h1 className="text-5xl font-bold text-slate-900">
            RepoMind
          </h1>

          <p className="text-slate-600 mt-3 text-lg">
            Your AI-powered repository assistant
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">
            Connect Repository
          </h2>

          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Paste GitHub repository URL..."
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              className="flex-1 px-4 py-3 rounded-xl border border-slate-300 outline-none focus:ring-2 focus:ring-slate-300"
            />

            <button
              onClick={handleAnalyze}
              className="px-6 py-3 rounded-xl bg-slate-900 text-white font-medium hover:bg-slate-800 transition"
            >
              {isAnalyzing ? "Analyzing..." : "Analyze"}
            </button>
          </div>

          {repoStatus && (
            <p className="mt-4 text-sm text-slate-600">
              {repoStatus}
            </p>
          )}
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 h-[650px] flex flex-col">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">
            Chat with RepoMind
          </h2>

          <div className="flex-1 bg-slate-50 rounded-xl p-4 border border-slate-200 overflow-y-auto space-y-4">
            {messages.length === 0 ? (
              <p className="text-slate-500">
                Ask something about your repository...
              </p>
            ) : (
              messages.map((msg, index) => (
                <div
                    key={index}
                    className={`p-4 rounded-2xl max-w-[80%] whitespace-pre-wrap break-words leading-relaxed ${
                      msg.role === "user"
                        ? "ml-auto bg-slate-900 text-white"
                        : "bg-white border border-slate-200 shadow-sm"
                    }`}
                  >
                    {msg.text}
                  </div>
              ))
            )}

            {isTyping && (
              <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-2xl max-w-[200px]">
                RepoMind is typing...
              </div>
            )}
          </div>

          <div className="mt-4 flex gap-4">
            <input
              type="text"
              placeholder="Ask something about the repository..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1 px-4 py-3 rounded-xl border border-slate-300 outline-none focus:ring-2 focus:ring-slate-300"
            />

            <button
              onClick={handleSend}
              className="px-6 py-3 rounded-xl bg-slate-900 text-white font-medium hover:bg-slate-800 transition"
            >
              Send
            </button>
          </div>
        </div>

      </div>
    </div>
  )
}

export default App