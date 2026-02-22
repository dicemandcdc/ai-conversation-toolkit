// ACM-22: Brave Leo Conversation Export Script
// Selectors sourced from ACM-21 DOM analysis + ACM-22 live DOM investigation
// Context: Must be run in 'leo-ai-conversation-entries' DevTools console context

(function exportLeoConversation() {
  const ordered = [];

  // --- Extract all conversation turns in DOM order ---
  const allTurns = document.querySelectorAll('div.lzbMemHg2pzd5OXYhXeIiQ\\=\\=');

  allTurns.forEach((turn, i) => {
    const isLeo = turn.classList.contains('I2XWNKJM-xvcqRdT8CjFGA==');

    if (isLeo) {
      const paras = turn.querySelectorAll('div.b3IH0ax6R\\-OOlUw7Gv4HfA\\=\\= p');
      const text = Array.from(paras).map(p => p.innerText.trim()).join('\n');
      if (text) ordered.push({ role: 'leo', id: null, text });
    } else {
      const textEl = turn.querySelector('div.HIcfvWIoFb2tp4Wu8TLhMQ\\=\\=');
      if (textEl) ordered.push({ role: 'user', id: i, text: textEl.innerText.trim() });
    }
  });

  // --- Build JSON output ---
  const timestamp = new Date().toISOString();
  const filename = `leo-export-${timestamp.replace(/[:.]/g, '-')}.json`;
  const output = {
    exported_at: timestamp,
    source: 'Brave Leo',
    message_count: ordered.length,
    messages: ordered
  };

  const json = JSON.stringify(output, null, 2);

  // --- Console preview ---
  console.log('=== ACM-22 Export Preview ===');
  console.log(`Messages found: ${ordered.length}`);
  console.log(json);

  // --- Manual export instruction ---
  console.log('ACM-22: Right-click the JSON object above → "Copy object"');
  console.log('ACM-22: Then in terminal: cat > ~/Projects/ai-conversation-toolkit/exports/' + filename);
  console.log('ACM-22: Paste JSON, then press Ctrl+D to save.');
})();
