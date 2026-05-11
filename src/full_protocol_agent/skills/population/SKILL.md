---
name: population
description: Provides instructions to generate the Ppopulation section of the clinical trial protocol for the sponsor drug.
---

# Generating Population section:

The Population section should start with one or two paragraphs of the population involved in the study.

Example:
```
Patients with advanced (FIGO stages III and IV) BRCA1/2-mutated (germline and/or somatic) high-grade epithelial ovarian, fallopian tube or primary peritoneal cancer who are in response (complete or partial) following completion of first-line platinum-based chemotherapy.
OR
Patients with platinum-sensitive relapsed high-grade epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete or partial) to platinum-based chemotherapy should start treatment with Olaparib no later than 8 weeks after completion of their final dose of the platinum-containing regimen.
```

The Population Section will have the following nested subsections.

- Entry Criteria:
  A short write up about the entry criteria.
    - Inclusion Criteria:
       Inclusion Criteria is available in the protocol synopsis in the file system at the below path. Expand on the inclusion criteria from the synopsis.
       **Protocol Synopsis**: /synopsis/protocol_synopsis.md
    - Exclusion Criteria:
        Exclusion Criteria is available in the protocol synopsis in the file system at the below path. Expand on the inclusion criteria from the synopsis.
        **Protocol Synopsis**: /synopsis/protocol_synopsis.md

- Discontinuation Criteria:
  A list of Discontinuation Criteria derived from the inclusion criteria.

- Data collection and follow-up for discontinued patients
  Add the following content as-is.

  ```
  Investigator should try to obtain and document the reason for patient withdrawing consent whenever possible. 
  End of treatment assessment (Section 10.5) shall be performed for all prematurely discontinued patients. For all discontinued patients, data collected till the time of discontinuation shall be reported in eCRF. 
  Safety data shall be collected for all discontinued patients, who are discontinued due to an adverse event (AE) or serious adverse event (SAE). In any case, every effort must be made to undertake protocol-specified safety follow-up procedures. If the patient is discontinued due to an event, he/she should be given an appropriate care under medical supervision until the symptoms of any AE resolve or the patient’s condition becomes stable.
  Lost to follow-up
  For patients whose status is unclear because they fail to appear for study visits without stating an intention to withdraw consent, the site/investigator should demonstrate sufficient efforts by contacting the patient or family or family physician and by documenting in the source documents steps taken to contact the patient, e.g. dates of telephone calls, emails, letters, etc. A patient should not be considered lost to follow-up until sufficient efforts as mentioned above have been completed. Patient status as lost to follow up should be recorded on the appropriate disposition CRF.
  ```

- Replacement of patients
  Add the following content as-is.

```
Replacement of patients will not be allowed post 1st investigational product administration. Withdrawn and discontinued patients will not be replaced.
```
