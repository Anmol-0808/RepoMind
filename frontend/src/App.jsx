import { useState } from "react"
import axios from "axios"

function App() {
  const [repoUrl, setRepoUrl] = useState("")
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState([])
  const [lastRepoTopic, setLastRepoTopic] = useState("")

  const handleAnalyze = () => {
    if (!repoUrl.trim()) return
    console.log("Selected Repo:", repoUrl)
  }

  const handleSend = async () => {
    if (!message.trim()) return

    const userMessage = {
      role: "user",
      text: message
    }

    setMessages((prev) => [...prev, userMessage])

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message,
          messages: messages.map((m) => m.text),
          last_repo_topic: lastRepoTopic
        }
      )

      const aiMessage = {
        role: "assistant",
        text: response.data.response
      }

      setMessages((prev) => [...prev, aiMessage])
      setLastRepoTopic(response.data.last_repo_topic)
      setMessage("")
    } catch (error) {
      console.error(error)
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
              Analyze
            </button>
          </div>
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
                  className={`p-4 rounded-xl max-w-[80%] ${
                    msg.role === "user"
                      ? "ml-auto bg-slate-900 text-white"
                      : "bg-white border border-slate-200"
                  }`}
                >
                  {msg.text}
                </div>
              ))
            )}
          </div>

          <div className="mt-4 flex gap-4">
            <input
              type="text"
              placeholder="Ask something about the repository..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
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