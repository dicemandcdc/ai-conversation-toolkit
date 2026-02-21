# ACM-21: Brave Leo DOM Structure Analysis

**Ticket:** ACM-21
**Sprint:** Sprint 2
**Status:** Complete
**Date:** 2026-02-21

---

## Summary

DOM inspection of Brave Leo chat interface to identify reliable selectors
for the ACM-22 export script.

---

## Key Findings

### Message Detection

| Message Type | Selector | Distinguishing Factor |
|---|---|---|
| User messages | `div[data-id]` | Has `data-id` attribute (increments) |
| Leo messages | `main > div > div:not([data-id])` | No `data-id` attribute |

### Text Extraction

| Message Type | Text Selector | Container Tag |
|---|---|---|
| User | `div[data-id] p` | p tag |
| Leo | `div:not([data-id]) > div > div` | Nested div |

### Additional Selectors

| Purpose | Selector |
|---|---|
| Leo messages (hash class pattern) | `main div[class*="jqL922FQB"]` |
| User messages (stable) | `main > div > div[data-id]` |
| Leo messages (stable) | `main > div > div:not([data-id])` |

### Example DOM Patterns

User message:
  Element:   div[data-id="1"]
  Class:     lzbMemHg2pzd50XYhXeIlQ==
  Child:     p tag contains user text

Leo message:
  Element:   div (no data-id)
  Class:     jqL922FQB-Xw5iU+V8Sc2A==
  Child:     nested div > div contains Leo text

---

## Shadow DOM

- **Present:** No
- **Implication:** Standard document.querySelector() works directly

## iframe

- **Location:** Main document (no iframe)
- **Implication:** Direct DOM access, no contentDocument needed

---

## Acceptance Criteria

- [x] User message selector identified
- [x] Leo message selector identified
- [x] Text extraction path confirmed for both
- [x] Shadow DOM presence confirmed (none)
- [x] iframe presence confirmed (none)
- [x] Findings documented in markdown

---

## Next Step

ACM-22: Build export script using selectors above.
Branch: feature/ACM-22-export-script
