const API = "http://127.0.0.1:8000";

function addMessage(text, type) {
  const chatBox = document.getElementById("chatBox");

  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  msg.innerText = text;

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function uploadFile() {
  const file = document.getElementById("fileInput").files[0];

  if (!file) {
    alert("Select a file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API}/upload`, {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  document.getElementById("uploadStatus").innerText = data.message;
}

async function askQuestion() {
  const input = document.getElementById("question");
  const question = input.value;

  if (!question) return;

  addMessage(question, "user");

  const loading = document.createElement("div");
  loading.className = "message bot";
  loading.innerText = "Typing...";
  document.getElementById("chatBox").appendChild(loading);

  input.value = "";

  try {
    const res = await fetch(`${API}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();

    loading.remove();
    addMessage(data.answer, "bot");
  } catch (err) {
    loading.remove();
    addMessage("Error: server issue", "bot");
  }
}

document.getElementById("question").addEventListener("keypress", function (e) {
  if (e.key === "Enter") askQuestion();
});
