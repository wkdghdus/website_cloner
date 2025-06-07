"use client";

import { useState } from "react";
import { useEffect } from "react";



export default function Home() {
  const [url, setUrl] = useState("");
  const [html, setHtml] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.title = "Orchids Website Cloner";
  }, []);

  const handleSubmit = async () => {
    setLoading(true);
    setHtml("");

    try {
      const res = await fetch("http://localhost:8000/clone", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!res.ok) {
        const err = await res.json();
        const message = err?.detail?.includes("Cannot navigate to invalid URL")
          ? "Please enter a valid URL (e.g. https://example.com)"
          : "An error occurred while cloning the website.";
        throw new Error(message);
      } 

      const data = await res.json();
      setHtml(data.generated_html);
    } catch (error: any) {
      alert("Cloning failed: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (

      <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="w-full max-w-3xl bg-white rounded-2xl shadow-xl p-8 space-y-6">
          <h1 className="text-3xl font-bold text-gray-800">🌐 Website Cloner</h1>

          <input
            type="text"
            placeholder="Enter a public website URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full px-4 py-3 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 
            placeholder-gray-600 placeholder-opacity-100 text-gray-900 font-medium"
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className={`w-full py-3 rounded-md text-white transition ${
              loading
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Cloning..." : "Clone Website"}
          </button>

          {loading && (
            <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
              <svg
                className="animate-spin h-5 w-5 text-blue-600"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v8H4z"
                />
              </svg>
              <span>Cloning in progress...</span>
            </div>
          )}

          {html && (
            <>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <h2 className="text-xl font-semibold text-gray-700">🔍 Preview</h2>
                  <button
                    onClick={() => {
                      const blob = new Blob([html], { type: "text/html" });
                      const url = URL.createObjectURL(blob);
                      window.open(url, "_blank");
                      setTimeout(() => URL.revokeObjectURL(url), 10000); // Cleanup
                    }}
                    className="text-sm text-blue-500 hover:underline"
                  >
                    Open in new tab ↗
                  </button>
                </div>

                <div className="h-[500px] border rounded-md overflow-hidden">
                  <iframe className="w-full h-full" srcDoc={html} />
                </div>
              </div>

              <div>
                <h2 className="text-xl font-semibold text-gray-700 mt-6 mb-2">
                  🧾 HTML Output
                </h2>

                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-500">Click to copy HTML</span>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(html);
                      alert("Copied to clipboard!");
                    }}
                    className="text-sm text-blue-500 hover:underline"
                  >
                    📋 Copy
                  </button>
                </div>

                <pre className="bg-gray-800 text-white text-sm p-4 rounded-md overflow-auto max-h-[400px] whitespace-pre-wrap">
                  {html}
                </pre>
              </div>

            </>
          )}
        </div>
      </main>
  );
}
