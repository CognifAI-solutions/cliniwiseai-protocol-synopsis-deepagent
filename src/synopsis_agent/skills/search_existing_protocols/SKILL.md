---
name: search_existing_protocols
description: Provides steps to search existing protocols submitted for the reference drug or device. Use when the user asks to retrieve existing protocols for the reference drug or device.
---

# Searching for existing protocols.

# Searching:
Use the **extract_webpage** tool for searching the list of protocols.
This will be the base URL that you will use to get a list of protocols from clinicaltrials.gov
**Base URL**:  https://clinicaltrials.gov/search?
**Query Parameters**:
  - **term**: additional terms provided by the user or the study type provided by the user(e.g. Bioequivalence, Pharmacokinetics)
  - **intr**: the reference drug name provided by the user (e.g. Lynparza, Keytruda)
  - **aggFilters**: use `docs:prot` to filter for protocol documents only. Append phase filters as needed (e.g. `docs:prot,phase:0 1 2`)
  Use the below key value pairs as reference for phase filters. The default MUST be Phase 1.
      Early Phase 1 - 0
      Phase 1 - 1
      Phase 2 - 2
      Phase 3 - 3
      Phase 4 - 4
      Not applicable - 5 

  - **viewType**: always set to `Card`
**Example Complete URL**:
https://clinicaltrials.gov/search?term=Bioequivalence&intr=Lynparza&aggFilters=docs:prot,phase:0%201%202&viewType=Card

---

# Extraction:
Once you have constructed the URL, use it to fetch the search results page.
Use the **extract_webpage_and_save** to extract the protocol and save it to the file system.
- Extract all protocol links from the search results. Each result card contains a link to an individual study page in the format: `https://clinicaltrials.gov/study<NCT ID>`
- Collect all `NCT` identifiers listed on the results page.

---


