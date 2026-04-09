// export_leo_memories.js
// ACM-47: Export Leo AI Memories from Brave Browser
// Run in DevTools Console while Brave Settings → Customize Leo → Memories is OPEN
// Selectors sourced from ACM-45 DOM analysis

(function exportLeoMemories() {
  // ── Pierce Shadow DOM chain (5 layers) ──────────────────────────────────────
  const shadowChain = document.querySelector('settings-ui')?.shadowRoot
    ?.querySelector('settings-main')?.shadowRoot
    ?.querySelector('settings-brave-leo-assistant-page-index')?.shadowRoot
    ?.querySelector('leo-customization-subpage')?.shadowRoot
    ?.querySelector('memory-section')?.shadowRoot;

  if (!shadowChain) {
    console.error('export_leo_memories.js: Could not reach memory-section shadow root.');
    console.error('Make sure Settings → Customize Leo → Memories panel is open and visible.');
    return;
  }

  // ── Extract memory labels (skip index 0 — panel header) ───────────────────
  const labels = shadowChain.querySelectorAll('div.label');

  if (!labels || labels.length === 0) {
    console.error('export_leo_memories.js: No memory items found.');
    return;
  }

  const memories = [];
  labels.forEach((el, i) => {
    if (i === 0) return; // skip header node per ACM-45
    const text = el.textContent.trim();
    if (text) {
      memories.push({ memory_text: text });
    }
  });

  // ── Build output JSON ──────────────────────────────────────────────────────
  const timestamp = new Date().toISOString();
  const output = {
    exported_at: timestamp,
    source: 'Brave Leo AI',
    memory_count: memories.length,
    memories: memories
  };

  const json = JSON.stringify(output, null, 2);

  // ── Console output ─────────────────────────────────────────────────────────
  console.log('=== export_leo_memories.js Output ===');
  console.log(`Memories found: ${memories.length}`);
  console.log(json);
  console.log('=== Right-click the JSON above → Copy object, then save as raw_export.json ===');
})();
