import React, { useState } from "react";
import axios from "axios";

const Feedback = () => {
  const [form, setForm] = useState({
    rollno: "",
    name: "",
    subject: "Math",
    rating: "",
  });

  const submitFeedback = async () => {
    try {
      await axios.post("https://05cjv9z918.execute-api.eu-north-1.amazonaws.com/studentrating", form);
      alert("Submitted!");
    } catch (err) {
      alert("Submission failed");
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center min-vh-100 bg-light p-4">
      <div className="card shadow-lg p-4 w-100" style={{ maxWidth: "500px" }}>
        <h2 className="text-center mb-4 text-primary">Feedback Form</h2>

        <div className="mb-3">
          <input
            type="text"
            className="form-control"
            placeholder="Roll No"
            value={form.rollno}
            onChange={(e) => setForm({ ...form, rollno: e.target.value })}
          />
        </div>

        <div className="mb-3">
          <input
            type="text"
            className="form-control"
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </div>

        <div className="mb-3">
          <select
            className="form-select"
            value={form.subject}
            onChange={(e) => setForm({ ...form, subject: e.target.value })}
          >
            <option value="Math">Cloud Computing</option>
            <option value="Science">Neural Networks</option>
            <option value="History">Internet Of Things</option>
            <option value="History">Competitive Programming</option>
          </select>
        </div>

        <div className="mb-3">
          <input
            type="number"
            className="form-control"
            placeholder="Rating (1-5)"
            min="1"
            max="5"
            value={form.rating}
            onChange={(e) => setForm({ ...form, rating: e.target.value })}
          />
        </div>

        <button
          onClick={submitFeedback}
          className="btn btn-primary w-100"
        >
          Submit
        </button>
      </div>
    </div>
  );
};

export default Feedback;