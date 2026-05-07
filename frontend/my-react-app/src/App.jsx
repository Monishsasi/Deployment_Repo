import { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const VITE_SERVER_URL = import.meta.env.VITE_SERVER_URL;

  const [resume, setResume] = useState(null);
  const [TextJD, setTextJD] = useState("");
  const [FileJD, setFileJD] = useState(null);
  const [toggleInputMethod, setToggleInputMethod] = useState(false);
  const [fileInput, setFileInput] = useState("TextUpload");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleToggleInputMethod() {
    setToggleInputMethod((prev) => !prev);
    setFileInput((prev) =>
      prev === "TextUpload" ? "FileUpload" : "TextUpload",
    );
  }

  const handleAnalyze = async () => {
    try {
      const formData = new FormData();

      if (!resume) {
        alert("Upload resume");
        return;
      }

      formData.append("resume", resume);

      if (fileInput === "TextUpload") {
        if (!TextJD.trim()) {
          alert("Enter job description");
          return;
        }
        formData.append("jd_text", TextJD);
      } else {
        if (!FileJD) {
          alert("Upload JD file");
          return;
        }
        formData.append("jd_file", FileJD);
      }

      setLoading(true); // start loading

      const response = await axios.post(
        `${VITE_SERVER_URL}/analyze-resume/`,  // http://localhost:5173
        formData,
        {
          timeout: 120000,
        },
      );

      console.log(VITE_SERVER_URL);

      console.log(response.data);
      setResult(response.data);
    } catch (err) {
      console.error(err.response?.data || err);
    } finally {
      setLoading(false); // stop loading
    }
  };

  return (
    <>
      <div className="body">
        <div className="header">
          <div className="HeaderSubtitle">AI Powered</div>

          <div className="HeaderName">
            <h1>AI Resume Analyzer</h1>
          </div>

          <div className="Slogans">
            <p>Empowering your job search with AI</p>
            <p>Get insights and improve your resume</p>
          </div>

          {/* <p>Upload your resume and get feedback</p>
          <p>Fix errors, improve keywords, and boost your chances of landing the job!</p> */}
        </div>

        <div className="UploadSection">
          <div className="FileUploadBox">
            <div className="ResumeUpload">
              <p>Upload your resume</p>
              <input
                type="file"
                accept=".pdf, .doc, .docx, .jpg, .jpeg, .png, .webp"
                onChange={(e) => {
                  setResume(e.target.files[0]);
                }}
              />
            </div>

            <div className="JobDescriptionUpload">
              <p>Upload job description</p>
              {fileInput === "TextUpload" && (
                <div className="TextUpload">
                  <textarea
                    value={TextJD}
                    placeholder="Paste job description here..."
                    onChange={(e) => setTextJD(e.target.value)}
                  />
                </div>
              )}
              {fileInput === "FileUpload" && (
                <div className="FileUpload">
                  <input
                    type="file"
                    accept=".pdf, .doc, .docx, .jpg, .jpeg, .png, .webp"
                    onChange={(e) => setFileJD(e.target.files[0])}
                  />
                </div>
              )}
              <button className="toggle" onClick={handleToggleInputMethod}>
                {toggleInputMethod
                  ? "Switch to Text Input"
                  : "Switch to File Upload"}
              </button>
            </div>
          </div>
        </div>

        <button
          className="AnalyzeButton"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        {loading && (
          <div className="LoaderOverlay">
            <div className="Loader"></div>
            <p>Analyzing your resume...</p>
          </div>
        )}

        {result?.status === "success" && result?.data && (
          <div className="ResultSection">
            {/* Score */}
            <div className="ScoreCard">
              <h2>{result.data.score?.overall ?? "N/A"}% Match</h2>
              <p>{result.data.score?.interpretation}</p>
            </div>

            {/* Strengths &  Missing */}
            <div className="GridSection">
              <div className="Card">
                <h3> Strengths</h3>
                <div className="Chips">
                  {result.data.matched?.length ? (
                    result.data.matched.map((skill, i) => (
                      <span key={i} className="chip green">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No strengths found</p>
                  )}
                </div>
              </div>

              <div className="Card">
                <h3> Missing Skills</h3>
                <div className="Chips">
                  {result.data.missing?.length ? (
                    result.data.missing.map((skill, i) => (
                      <span key={i} className="chip red">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No missing skills 🎉</p>
                  )}
                </div>
              </div>
            </div>

            {/* AI Explanation */}
            <div className="Card">
              <h3>🧠 AI Analysis</h3>
              <pre>{result.data.explanation || "No analysis available"}</pre>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
