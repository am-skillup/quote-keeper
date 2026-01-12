const API_BASE = window.API_BASE || "http://localhost:8000";

async function fetchQuotes() {
  const r = await fetch(`${API_BASE}/quotes`);
  return await r.json();
}

async function createQuote({ text, author, tags }) {
  const r = await fetch(`${API_BASE}/quotes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, author, tags })
  });
  return await r.json();
}

function renderQuotes(quotes, container) {
  container.innerHTML = "";
  quotes.forEach(q => {
    const li = document.createElement('li');
    li.textContent = `${q.text} — ${q.author || 'unknown'}${q.tags ? ' [' + q.tags.join(', ') + ']' : ''}`;
    container.appendChild(li);
  });
}

if (typeof window !== 'undefined') {
  const ul = document.getElementById('quotes');
  const form = document.getElementById('addForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('text').value;
    const author = document.getElementById('author').value;
    const tags = document.getElementById('tags').value.split(',').map(s => s.trim()).filter(Boolean);
    await createQuote({ text, author, tags });
    const quotes = await fetchQuotes();
    renderQuotes(quotes, ul);
    form.reset();
  });
  (async () => {
    const quotes = await fetchQuotes();
    renderQuotes(quotes, ul);
  })();
}

module.exports = { renderQuotes };
