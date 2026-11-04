import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const initialMessage = {
  role: "assistant",
  text: "Hello! I’m ready to answer questions about your knowledge base. Upload a document to get started.",
};

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

async function errorMessage(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") return body.detail;
    if (body.detail) return JSON.stringify(body.detail);
  } catch {
    return `Request failed (${response.status})`;
  }
  return `Request failed (${response.status})`;
}

function Icon({ name }) {
  const paths = {
    home: <><path d="m3 11 9-7 9 7v9h-6v-6H9v6H3v-9Z" /></>,
    file: <><path d="M6 3.5h8l4 4v13H6a2 2 0 0 1-2-2v-13a2 2 0 0 1 2-2Z" /><path d="M14 3.5v5h5M8 13h8M8 16.5h6" /></>,
    chat: <><path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5H5l-1-4v-3.5a7.5 7.5 0 1 1 16 0Z" /><path d="M8 11h8M8 14.5h5" /></>,
    upload: <><path d="M12 16V4m-4 4 4-4 4 4" /><path d="M5 14v5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-5" /></>,
    send: <><path d="m21 3-7.5 18-3.6-7.9L2 9.5 21 3Z" /><path d="M21 3 9.9 13.1" /></>,
    sparkle: <><path d="M12 3.5 14.5 9l5.5 2-5.5 2.5-2.5 5.5-2.5-5.5L4 11l5.5-2 2.5-5.5Z" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>,
  };

  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  );
}

function App() {
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([initialMessage]);
  const [question, setQuestion] = useState("");
  const [queuedFiles, setQueuedFiles] = useState([]);
  const [autoIndex, setAutoIndex] = useState(true);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [activeUploadName, setActiveUploadName] = useState("");
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");
  const [connection, setConnection] = useState("Connecting");
  const [activeSection, setActiveSection] = useState("home");
  const [assistantWidth, setAssistantWidth] = useState(() => Math.round(window.innerWidth * 0.41));
  const fileInput = useRef(null);
  const chatEnd = useRef(null);
  const resizeStart = useRef(null);
  const maxAssistantWidth = Math.max(
    320,
    window.innerWidth - window.innerWidth * 0.22 - 320,
  );

  function resizeAssistant(event) {
    if (!resizeStart.current) return;
    const minWidth = 320;
    setAssistantWidth(
      Math.min(
        maxAssistantWidth,
        Math.max(minWidth, resizeStart.current.width + resizeStart.current.x - event.clientX),
      ),
    );
  }

  async function loadDocuments({ clearError = true } = {}) {
    setLoadingDocuments(true);
    try {
      const response = await fetch("/documents");
      if (!response.ok) throw new Error(await errorMessage(response));
      const body = await response.json();
      setDocuments(body.documents);
      setConnection("RAG active");
      if (clearError) setError("");
    } catch (loadError) {
      setConnection("Connection issue");
      setError(loadError.message || "Could not load documents.");
    } finally {
      setLoadingDocuments(false);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  useEffect(() => {
    chatEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, asking]);

  function chooseFiles(fileList) {
    const files = Array.from(fileList);
    const pdfs = files.filter((file) => file.name.toLowerCase().endsWith(".pdf"));
    const invalidCount = files.length - pdfs.length;
    const oversized = pdfs.filter((file) => file.size > 20 * 1024 * 1024);
    const allowed = pdfs.filter((file) => file.size <= 20 * 1024 * 1024);
    if (invalidCount > 0) setError("Only PDF files are supported.");
    else if (oversized.length > 0) setError(`${oversized.map((file) => file.name).join(", ")} exceeds the 20 MB limit.`);
    else setError("");

    if (autoIndex && allowed.length > 0) {
      void uploadFiles(allowed);
    } else {
      setQueuedFiles((current) => [...current, ...allowed]);
    }
  }

  async function uploadFiles(files) {
    if (uploading || files.length === 0) return;
    setUploading(true);
    const failures = [];

    for (const file of files) {
      setActiveUploadName(file.name);
      const form = new FormData();
      form.append("file", file);
      try {
        const response = await fetch("/ingest", { method: "POST", body: form });
        if (!response.ok) throw new Error(await errorMessage(response));
        const result = await response.json();
        setQueuedFiles((current) => current.filter((queued) => queued !== file));
        setError(`${result.filename} added · ${result.chunks_added} text chunks indexed.`);
      } catch (uploadError) {
        failures.push(`${file.name}: ${uploadError.message}`);
      }
    }

    if (failures.length > 0) setError(failures.join(" · "));
    setActiveUploadName("");
    setUploading(false);
    await loadDocuments({ clearError: false });
  }

  async function askQuestion(event) {
    event.preventDefault();
    const prompt = question.trim();
    if (!prompt || asking) return;
    setMessages((current) => [...current, { role: "user", text: prompt }]);
    setQuestion("");
    setAsking(true);

    try {
      const response = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: prompt }),
      });
      if (!response.ok) throw new Error(await errorMessage(response));
      const result = await response.json();
      setMessages((current) => [
        ...current,
        { role: "assistant", text: result.answer, sources: result.sources },
      ]);
    } catch (queryError) {
      setMessages((current) => [
        ...current,
        { role: "assistant", text: `I couldn’t answer that just now. ${queryError.message}` },
      ]);
    } finally {
      setAsking(false);
    }
  }

  function startNewChat() {
    setMessages([initialMessage]);
    setQuestion("");
    setActiveSection("chat");
  }

  const indexedCount = documents.filter((document) => document.indexed).length;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="window-dots" aria-hidden="true"><i /><i /><i /></div>
        <div className="workspace-profile">
          <div className="profile-avatar">KB</div>
          <div><strong>My workspace</strong><span>Personal library</span></div>
        </div>
        <nav className="side-nav" aria-label="Main navigation">
          <div className="nav-caption">Workspace</div>
          <button className={activeSection === "home" ? "nav-link active" : "nav-link"} onClick={() => setActiveSection("home")}>
            <Icon name="home" />Home
          </button>
          <button className={activeSection === "documents" ? "nav-link active" : "nav-link"} onClick={() => setActiveSection("documents")}>
            <Icon name="file" />Documents<span className="nav-count">{documents.length}</span>
          </button>
          <button className={activeSection === "chat" ? "nav-link active" : "nav-link"} onClick={() => setActiveSection("chat")}>
            <Icon name="chat" />AI Assistant
          </button>
        </nav>
        <div className="sidebar-footer">
          <div className="profile-avatar small">KB</div>
          <div><strong>Knowledge Base</strong><span>{documents.length} {documents.length === 1 ? "document" : "documents"}</span></div>
        </div>
      </aside>

      <main className="library-pane">
        <section className="upload-section" aria-labelledby="upload-title">
          <div className="section-title" id="upload-title">Upload Knowledge</div>
          <button
            className={uploading ? "drop-zone uploading" : "drop-zone"}
            type="button"
            aria-busy={uploading}
            onClick={() => fileInput.current?.click()}
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => {
              event.preventDefault();
              chooseFiles(event.dataTransfer.files);
            }}
          >
            <span className="upload-icon"><Icon name="upload" /></span>
            <strong>{uploading ? `Uploading ${activeUploadName}` : "Click to upload or drag and drop"}</strong>
            <span>{uploading ? "Please wait while your file is indexed" : "PDF files only · up to 20 MB each"}</span>
          </button>
          <input
            ref={fileInput}
            className="file-input"
            type="file"
            accept=".pdf,application/pdf"
            multiple
            onChange={(event) => {
              chooseFiles(event.target.files);
              event.target.value = "";
            }}
          />
          {uploading && (
            <div className="upload-progress" role="status" aria-live="polite">
              <span className="upload-spinner" aria-hidden="true" />
              <span className="upload-progress-copy">
                <strong>Uploading and indexing</strong>
                <span>{activeUploadName}</span>
              </span>
              <span className="upload-progress-track" aria-hidden="true">
                <span />
              </span>
            </div>
          )}
        </section>

        <div className="library-toolbar">
          <div className="breadcrumb">Home <span>›</span> <strong>Knowledge Base</strong></div>
          <div className="toolbar-actions">
            <label className="auto-index">
              <span>Auto-index</span>
              <input type="checkbox" checked={autoIndex} onChange={(event) => {
                const enabled = event.target.checked;
                setAutoIndex(enabled);
                if (enabled && queuedFiles.length > 0) void uploadFiles(queuedFiles);
              }} />
            </label>
            <button className="icon-button" type="button" aria-label="Refresh documents" onClick={loadDocuments}><span>↻</span></button>
            <button className="add-button" type="button" onClick={() => fileInput.current?.click()}><Icon name="plus" />Add New</button>
          </div>
        </div>

        {queuedFiles.length > 0 && (
          <div className="queued-files">
            <span>{queuedFiles.map((file) => file.name).join(", ")}</span>
            <button type="button" disabled={uploading} onClick={() => void uploadFiles(queuedFiles)}>
              {uploading ? "Uploading…" : `Index ${queuedFiles.length} ${queuedFiles.length === 1 ? "file" : "files"}`}
            </button>
          </div>
        )}
        {error && <div className={connection === "Connection issue" ? "notice error" : "notice"} role="status">{error}</div>}

        <div className="document-heading">
          <span>File name</span><span>Status</span><span>Size</span><span />
        </div>
        <section className="document-list" aria-label="Knowledge base documents" aria-live="polite">
          {loadingDocuments && documents.length === 0 && <div className="empty-state">Loading your documents…</div>}
          {!loadingDocuments && documents.length === 0 && <div className="empty-state">Your library is waiting. Upload a PDF to get started.</div>}
          {documents.map((document) => (
            <article className="document-row" key={document.name}>
              <div className="file-mark"><Icon name="file" /></div>
              <div className="document-name" title={document.name}>{document.name}</div>
              <span className={document.indexed ? "status-badge indexed" : "status-badge"}>{document.indexed ? "Indexed" : "Not indexed"}</span>
              <span className="document-size">{document.size_bytes == null ? "—" : formatBytes(document.size_bytes)}</span>
            </article>
          ))}
        </section>
      </main>

      <section
        className="assistant-pane"
        aria-label="AI Assistant"
        style={{ "--assistant-width": `${assistantWidth}px` }}
      >
        <button
          className="assistant-resize-handle"
          type="button"
          role="separator"
          aria-label="Resize chat panel"
          aria-orientation="vertical"
          aria-valuenow={assistantWidth}
          aria-valuemin={320}
          aria-valuemax={maxAssistantWidth}
          onKeyDown={(event) => {
            if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
            event.preventDefault();
            const change = event.key === "ArrowLeft" ? 24 : -24;
            setAssistantWidth((width) => Math.min(maxAssistantWidth, Math.max(320, width + change)));
          }}
          onPointerDown={(event) => {
            resizeStart.current = { x: event.clientX, width: assistantWidth };
            event.currentTarget.setPointerCapture(event.pointerId);
          }}
          onPointerMove={resizeAssistant}
          onPointerUp={() => {
            resizeStart.current = null;
          }}
          onPointerCancel={() => {
            resizeStart.current = null;
          }}
        />
        <header className="assistant-header">
          <div className="assistant-heading">
            <span className="assistant-avatar"><Icon name="sparkle" /></span>
            <div><strong>AI Assistant</strong><span className={connection === "Connection issue" ? "connection offline" : "connection"}>{connection}</span></div>
          </div>
          <button className="icon-button" type="button" aria-label="New chat" onClick={startNewChat}><Icon name="plus" /></button>
        </header>
        <div className="chat-messages">
          {messages.map((message, index) => (
            <article className={`chat-message ${message.role}`} key={`${index}-${message.text.slice(0, 20)}`}>
              <span className="message-avatar"><Icon name={message.role === "assistant" ? "sparkle" : "home"} /></span>
              <div className="message-content">
                <span className="message-author">{message.role === "assistant" ? "AI Assistant" : "You"}</span>
                <div className="message-bubble">{message.text}</div>
                {message.sources?.length > 0 && (
                  <div className="source-list">
                    {message.sources.map((source, sourceIndex) => (
                      <span className="source-chip" key={`${source.source}-${source.page}-${sourceIndex}`}>{source.source} · p. {source.page}</span>
                    ))}
                  </div>
                )}
              </div>
            </article>
          ))}
          {asking && <div className="thinking" role="status">Thinking…</div>}
          <div ref={chatEnd} />
        </div>
        <form className="chat-composer" onSubmit={askQuestion}>
          <textarea
            rows="1"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                event.currentTarget.form.requestSubmit();
              }
            }}
            placeholder="Ask a question about your documents…"
            aria-label="Ask a question about your documents"
          />
          <button className="send-button" type="submit" disabled={!question.trim() || asking} aria-label="Send question"><Icon name="send" /></button>
        </form>
        <p className="disclaimer">AI can make mistakes. Verify important information.</p>
      </section>

    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
