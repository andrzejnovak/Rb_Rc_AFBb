# BibTeX Validation Report
**Doc 4a, Iteration 2** | Session: `ada_4351`  
**Date:** 2026-04-02 | **Validator:** BibTeX Validator

---

## Executive Summary

**Classification: A** — All checks PASS. Analysis note bibliography is complete and correct.

| Aspect | Result | Evidence |
|--------|--------|----------|
| Cite key resolution | ✓ PASS | 12 cited keys; all 12 in references.bib |
| Required fields | ✓ PASS | All entries have author, title, year |
| LaTeX in titles | ✓ PASS | No raw LaTeX commands found |
| Duplicates | ✓ PASS | No duplicate titles |
| INSPIRE/arXiv IDs | ✓ PASS | All IDs correctly formatted |
| Unused entries | ⚠ NOTED | 3 unused (valid in context) |

---

## Detailed Validation

### 1. Cite Key Resolution

**Cited keys found in ANALYSIS_NOTE_doc4a_v2.tex:**
```
ALEPH:AFBb
ALEPH:Rb:1996
ALEPH:Rb:precise
ALEPH:Rc
ALEPH:VDET
ALEPH:opendata
ALEPH:sigma_had
DELPHI:Rb
LEP:EWWG:2005
LEP:HF:2001
LEP:gcc
PDG:2024
```

**Result:** ✓ All 12 keys found in references.bib  
**Unresolved citations:** 0  
**Status:** PASS

---

### 2. Required Fields Completeness

All 15 entries in references.bib contain required fields:

| Key | Type | Author | Title | Year | Status |
|-----|------|--------|-------|------|--------|
| ALEPH:Rb:1996 | article | ✓ | ✓ | 1997 | ✓ |
| ALEPH:Rb:precise | article | ✓ | ✓ | 1998 | ✓ |
| ALEPH:AFBb | article | ✓ | ✓ | 1998 | ✓ |
| ALEPH:Rc | article | ✓ | ✓ | 2000 | ✓ |
| ALEPH:VDET | article | ✓ | ✓ | 1995 | ✓ |
| ALEPH:gbb | article | ✓ | ✓ | 1998 | ✓ |
| ALEPH:sigma_had | article | ✓ | ✓ | 1997 | ✓ |
| ALEPH:opendata | misc | ✓ | ✓ | 2024 | ✓ |
| DELPHI:Rb | article | ✓ | ✓ | 2000 | ✓ |
| DELPHI:AFBb | article | ✓ | ✓ | 1999 | ✓ |
| DELPHI:AFBb:2 | article | ✓ | ✓ | 1999 | ✓ |
| LEP:EWWG:2005 | article | ✓ | ✓ | 2006 | ✓ |
| LEP:HF:2001 | article | ✓ | ✓ | 2001 | ✓ |
| LEP:gcc | article | ✓ | ✓ | 2003 | ✓ |
| PDG:2024 | article | ✓ | ✓ | 2024 | ✓ |

**Result:** ✓ 100% complete  
**Missing fields:** 0  
**Status:** PASS

---

### 3. LaTeX in Titles

All titles use plain text with no raw LaTeX commands:

- Titles correctly use ASCII: `b-bbar`, `R(b)`, `A(b,FB)`, `R(0,b)`, etc.
- No `\mathrm{}`, `\alpha`, `\beta`, or other command sequences
- Mathematical notation handled with plain text (subscripts as text)
- Special characters (slashes, parentheses): properly escaped in BibTeX format

**Result:** ✓ No problematic LaTeX found  
**Examples of correct notation:**
```
✓ "A precise measurement of Gamma(Z to b-bbar) / Gamma(Z to hadrons)"
✓ "An upgraded measurement of A(b,FB) from the charge asymmetry..."
✓ "Measurement of A(0,b,FB) using jet charge measurements in Z decays"
```

**Status:** PASS

---

### 4. Duplicate Detection

Title uniqueness check across all 15 entries:

**Result:** ✓ No duplicates found  
**Duplicate titles:** 0  
**Status:** PASS

---

### 5. INSPIRE and arXiv ID Validation

**INSPIRE IDs (format: 6-7 digit numbers in range ~300K–2M):**

| Entry | ID | Format | Range | Status |
|-------|-----|--------|-------|--------|
| ALEPH:AFBb | 433746 | ✓ | ✓ | ✓ |
| ALEPH:Rb:precise | 433306 | ✓ | ✓ | ✓ |
| ALEPH:Rc | 483143 | ✓ | ✓ | ✓ |
| ALEPH:VDET | 537303 | ✓ | ✓ | ✓ |
| ALEPH:gbb | 484192 | ✓ | ✓ | ✓ |
| ALEPH:sigma_had | 367499 | ✓ | ✓ | ✓ |
| DELPHI:AFBb | 1660289 | ✓ | ✓ | ✓ |
| DELPHI:AFBb:2 | 1661115 | ✓ | ✓ | ✓ |
| DELPHI:Rb | 1661836 | ✓ | ✓ | ✓ |
| LEP:HF:2001 | 416138 | ✓ | ✓ | ✓ |

**Result:** ✓ All 10 INSPIRE IDs correctly formatted  
**Status:** PASS

---

**arXiv IDs (format: `hep-ex/YYMMNNN` or new format `YYMM.NNNNN`):**

| Entry | arXiv ID | Format | Year Check | Status |
|-------|----------|--------|-----------|--------|
| ALEPH:Rb:1996 | hep-ex/9609005 | ✓ | 1996→1997 ✓ | ✓ |
| ALEPH:gbb | hep-ex/9811047 | ✓ | 1998→1998 ✓ | ✓ |
| LEP:EWWG:2005 | hep-ex/0509008 | ✓ | 2005→2006 ✓ | ✓ |
| LEP:HF:2001 | hep-ex/0112021 | ✓ | 2001→2001 ✓ | ✓ |
| LEP:gcc | hep-ex/0302003 | ✓ | 2003→2003 ✓ | ✓ |

**Result:** ✓ All 5 arXiv IDs correctly formatted  
**Consistency:** arXiv submission year ≤ declared publication year ✓ (all entries pass)  
**Status:** PASS

---

### 6. Unused Entries Audit

Three entries in references.bib are not cited in ANALYSIS_NOTE_doc4a_v2.tex:

| Key | Entry Type | Status | Justification |
|-----|------------|--------|-------------|
| ALEPH:gbb | article | Prepared | Potential citation for closure discussion; not yet needed in v2 |
| DELPHI:AFBb | article | Prepared | Reference analysis; cited in strategy, not in v2 prose |
| DELPHI:AFBb:2 | article | Prepared | Alternative DELPHI measurement; backup reference |

**Assessment:** ⚠ NOTED  
**Severity:** Not an error. These are legitimate forward-references for completeness. They may be cited in Doc 4b/4c or in related analyses. Recommend:
1. Leave in place (no harm; helps documentation)
2. OR add a note in STRATEGY.md if these are intentionally being omitted from v2

**Status:** ACCEPTABLE WITH NOTATION

---

## Summary Table

| Check | Total | Pass | Fail | Warn | Notes |
|-------|-------|------|------|------|-------|
| Cite keys in .tex | 12 | 12 | 0 | 0 | All resolve ✓ |
| Entries in .bib | 15 | 15 | 0 | 0 | Complete ✓ |
| Required fields | 15 | 15 | 0 | 0 | 100% complete ✓ |
| LaTeX in titles | 15 | 15 | 0 | 0 | No raw commands ✓ |
| Duplicates | 15 | 15 | 0 | 0 | None ✓ |
| INSPIRE IDs | 10 | 10 | 0 | 0 | All valid ✓ |
| arXiv IDs | 5 | 5 | 0 | 0 | All valid ✓ |
| Unused entries | 3 | — | — | 3 | Noted, acceptable |

---

## Classification

**CATEGORY A: All critical checks PASS**

The bibliography is complete, consistent, and ready for compilation. No blocking issues. The three unused entries are acceptable and may be cited in future document iterations.

---

## Recommendation

**Proceed to review.** The BibTeX infrastructure is sound.

If desired, optionally add a comment to `STRATEGY.md` explaining why ALEPH:gbb, DELPHI:AFBb, and DELPHI:AFBb:2 are prepared but not yet cited (e.g., "Held for comparison section in Doc 4c").

---

**Validator:** ada_4351  
**Timestamp:** 2026-04-02T00:00:00Z  
**Files checked:**
- `/analyses/Rb_Rc_AFBb/references.bib` (15 entries)
- `/analyses/Rb_Rc_AFBb/analysis_note/ANALYSIS_NOTE_doc4a_v2.tex` (12 cited keys)
