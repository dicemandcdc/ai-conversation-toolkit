# ACM-45: DOM Inspection — Leo AI Memories Panel

**Story:** ACM-44 Export Leo AI Memories (8pts, P0, Parent ACM-2)
**Subtask:** ACM-45 DOM Inspection (Spike)
**Sprint:** Sprint 3 (March 18–31, 2026)
**Completed:** 2026-03-18
**Author:** Diceman

---

## Summary

This spike inspected the Brave Browser DOM to identify HTML elements, CSS
selectors, and data attributes that expose the Leo AI Memories panel.
Findings confirm that automated export is feasible and unblocks ACM-46
(MongoDB VM Setup) and ACM-47 (Build export script).

---

## Methodology

Followed the same approach established in ACM-21 (DOM Inspection: Leo AI
Conversation Panel) with no assumptions carried forward. The memories panel
has a significantly different DOM structure than the conversation panel —
most notably, it is deeply nested inside multiple Shadow DOM layers.

**Tools used:** Brave DevTools → Elements tab, Console tab

---

## DOM Structure

The memories panel is accessible via:
`Brave Settings → Customize Leo → Memories`

The panel must be **actively visible** before inspection — memory DOM nodes
are conditionally rendered only when the panel is open.

### Full Shadow DOM Chain
settings-ui                                 → #shadow-root (open)
  settings-main                             → #shadow-root (open)
    settings-brave-leo-assistant-page-index → #shadow-root (open)
      leo-customization-subpage             → #shadow-root (open)
        memory-section                      → #shadow-root (open)
          div.list-container
            div.list
              div.memory                    ← individual memory item
                div.memory-info
                  div.label                 ← memory text content
                div.memory-actions          ← edit / delete buttons

---

## CSS Selectors

| Target | Selector | Notes |
|---|---|---|
| Panel wrapper | settings-section[section="memories"] | Most reliable outer anchor |
| Memory component | memory-section | Custom web component |
| List container | div.list-container | Inside memory-section shadow root |
| List parent | div.list | Direct parent of all memory items |
| Individual item | div.memory | One per memory entry |
| Text content | div.label | Contains full memory string |
| Action buttons | div.memory-actions | Edit and delete controls |

---

## Shadow DOM Findings

**Shadow DOM: CONFIRMED PRESENT**

Five nested shadow roots must be pierced in sequence to reach memory items.
Standard document.querySelector('div.memory') will NOT work from the
top-level document context.

### Validated Console Selector Chain

document.querySelector('settings-ui').shadowRoot
  .querySelector('settings-main').shadowRoot
  .querySelector('settings-brave-leo-assistant-page-index').shadowRoot
  .querySelector('leo-customization-subpage').shadowRoot
  .querySelector('memory-section').shadowRoot
  .querySelectorAll('div.memory')
// Returns: NodeList(66) [div.memory, div.memory, ...]

### Text Extraction (Validated)

document.querySelector('settings-ui').shadowRoot
  .querySelector('settings-main').shadowRoot
  .querySelector('settings-brave-leo-assistant-page-index').shadowRoot
  .querySelector('leo-customization-subpage').shadowRoot
  .querySelector('memory-section').shadowRoot
  .querySelectorAll('div.label')
  .forEach((el, i) => console.log(i, el.textContent.trim()))
// Returns: 67 items, index 0-66, full text content, no truncation

---

## iframe Findings

**iframe: RULED OUT**

No iframe elements found wrapping the memories panel.

---

## Data Attributes

**No data-* attributes found on memory items.**

Memory order is positional (index-based). The export index in ACM-47
must use the DOM node position as the order field. Item at index 0 is a
panel header string and must be filtered out in the export script.

| Field | Source | Notes |
|---|---|---|
| text | div.label → textContent.trim() | Full memory string |
| order | NodeList index | 0-based; index 0 = header, filter out |
| id | None found | Assign UUID at export time in ACM-47 |
| tags | None found | Not present in current DOM |

---

## Comparison to ACM-21 (Conversation Panel)

| Attribute | ACM-21 (Conversation) | ACM-45 (Memories) |
|---|---|---|
| Shadow DOM | None | 5 nested layers |
| iframe | None | None |
| Consistent selectors | Yes | Yes |
| data-id attributes | Present | Not present |
| Order mechanism | data-id attribute | Positional index |
| Export complexity | Low | Medium (shadow piercing required) |

---

## Memory Count

**67 total DOM nodes** returned by querySelectorAll('div.label')

- Index 0: Panel header text — exclude from export
- Index 1-66: Individual memory items — include in export
- **Net exportable memories: 66**

---

## Feasibility Decision

| Outcome | Decision |
|---|---|
| Consistent selectors found | Proceed to ACM-46 and ACM-47 |

Automated export is fully feasible. The Shadow DOM chain is navigable,
all 66 memory items are reachable with consistent selectors, and text
content extracts cleanly. No manual fallback required.

---

## Unblocked Stories

- ACM-46 — MongoDB VM Setup
- ACM-47 — Build export_leo_memories.py export script

---

## Definition of Done

- [x] Leo AI memories panel located and inspected via Brave DevTools
- [x] CSS selectors identified for individual memory items
- [x] Data attributes documented (none found — positional order confirmed)
- [x] Shadow DOM presence confirmed (5 layers, all open)
- [x] iframe presence ruled out
- [x] Findings documented in docs/ACM-45-leo-memories-dom-analysis.md
- [x] Feasibility decision recorded: automated export confirmed

---

## Notes for ACM-47

1. Use the full shadow DOM chain — do not simplify
2. Filter index 0 (header node) before building export array
3. Assign UUID to each memory at export time (no native ID in DOM)
4. Target output: flat JSON array matching brave_leo_export.js format
5. Memories panel must be open and visible when script executes
