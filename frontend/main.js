// Use a relative API base by default so the frontend works when served from the same host
const API_BASE = window.API_BASE || "";

async function fetchQuotes(params = {}) {
  const query = new URLSearchParams(params).toString();
  const url = `${API_BASE}/quotes${query ? `?${query}` : ''}`;
  const r = await fetch(url);
  if (!r.ok) throw new Error(`Failed to fetch quotes: ${r.status}`);
  return await r.json();
}

async function createQuote({ text, author, tags }) {
  const r = await fetch(`${API_BASE}/quotes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, author, tags })
  });
  if (!r.ok) throw new Error(`Failed to create quote: ${r.status}`);
  return await r.json();
}

async function deleteQuote(id) {
  const r = await fetch(`${API_BASE}/quotes/${id}`, { method: 'DELETE' });
  return r.ok;
}

async function fetchRandomQuote() {
  const r = await fetch(`${API_BASE}/quotes/random`);
  if (!r.ok) throw new Error(`No random quote: ${r.status}`);
  return await r.json();
}

function renderQuotes(quotes, container) {
  container.innerHTML = "";
  quotes.forEach(q => {
    const li = document.createElement('li');
    const text = document.createElement('span');
    text.textContent = `${q.text} — ${q.author || 'unknown'}`;
    li.appendChild(text);

    if (q.tags && q.tags.length) {
      const tags = document.createElement('small');
      tags.style.marginLeft = '8px';
      tags.textContent = ` [${q.tags.join(', ')}]`;
      li.appendChild(tags);
    }

    // delete button
    const del = document.createElement('button');
    del.textContent = 'Delete';
    del.style.marginLeft = '12px';
    del.addEventListener('click', async () => {
      try {
        del.disabled = true;
        const ok = await deleteQuote(q.id);
        if (ok) {
          const quotes = await fetchQuotes();
          renderQuotes(quotes, container);
        } else {
          alert('Delete failed');
          del.disabled = false;
        }
      } catch (err) {
        alert('Delete failed: ' + err.message);
        del.disabled = false;
      }
    });
    li.appendChild(del);

    container.appendChild(li);
  });
}

if (typeof window !== 'undefined') {
  const ul = document.getElementById('quotes');
  const form = document.getElementById('addForm');
  const status = document.getElementById('status');
  const filterAuthor = document.getElementById('filter-author');
  const filterTag = document.getElementById('filter-tag');
  const filterBtn = document.getElementById('filter-btn');
  const randomBtn = document.getElementById('random-btn');

  async function loadQuotes(params = {}) {
    if (!ul) return;
    status && (status.textContent = 'Loading...');
    // simple retry to mitigate transient network/deploy lag issues
    const attempts = 3;
    for (let i = 1; i <= attempts; i++) {
      try {
        const quotes = await fetchQuotes(params);
        renderQuotes(quotes, ul);
        status && (status.textContent = `Showing ${quotes.length} quotes`);
        return;
      } catch (err) {
        console.error(`loadQuotes attempt ${i} failed`, err);
        if (i === attempts) {
          status && (status.textContent = 'Failed to load quotes: ' + err.message);
          throw err;
        }
        // small wait before retrying
        await new Promise(r => setTimeout(r, 300));
      }
    }
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      submitBtn && (submitBtn.disabled = true);
      const textEl = document.getElementById('text');
      const authorEl = document.getElementById('author');
      const tagsEl = document.getElementById('tags');
      const text = textEl ? textEl.value : '';
      const author = authorEl ? authorEl.value : '';
      const tags = tagsEl ? tagsEl.value.split(',').map(s => s.trim()).filter(Boolean) : [];
      try {
        await createQuote({ text, author, tags });
        status && (status.textContent = 'Quote created');
        form.reset();
        // try to refresh, but do not treat refresh failures as create failures
        try {
          await loadQuotes();
        } catch (err) {
          console.error('Refresh after create failed', err);
          status && (status.textContent = 'Quote created, but refresh failed: ' + err.message);
          // schedule background retry
          setTimeout(() => {
            loadQuotes().catch(err2 => console.error('Background refresh failed', err2));
          }, 1000);
        }
      } catch (err) {
        console.error('Create failed', err);
        status && (status.textContent = 'Create failed: ' + err.message);
      } finally {
        submitBtn && (submitBtn.disabled = false);
      }
    });
  }

  if (filterBtn) {
    filterBtn.addEventListener('click', async (e) => {
      const author = filterAuthor ? filterAuthor.value : '';
      const tag = filterTag ? filterTag.value : '';
      await loadQuotes({ author, tag });
    });
  }

  if (randomBtn) {
    randomBtn.addEventListener('click', async () => {
      try {
        status && (status.textContent = 'Loading random quote...');
        const q = await fetchRandomQuote();
        if (ul) renderQuotes([q], ul);
        status && (status.textContent = 'Random quote');
      } catch (err) {
        status && (status.textContent = 'Random failed: ' + err.message);
      }
    });
  }

  // initial load
  loadQuotes();
}

module.exports = { renderQuotes };
if (typeof window !== 'undefined') {
  const ul = document.getElementById('quotes');
  const form = document.getElementById('addForm');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const text = document.getElementById('text').value;
      const author = document.getElementById('author').value;
      const tags = document.getElementById('tags').value.split(',').map(s => s.trim()).filter(Boolean);
      await createQuote({ text, author, tags });
      if (ul) {
        const quotes = await fetchQuotes();
        renderQuotes(quotes, ul);
      }
      form.reset();
    });
  }

  if (ul) {
    (async () => {
      const quotes = await fetchQuotes();
      renderQuotes(quotes, ul);
    })();
  }
}

module.exports = { renderQuotes };
