---
name: background_information
description: Provides instructions to generate the Background Information section of the clinical trial protocol for the sponsor drug.
---

# Generate Background Information Section.

The Background Information section should be created using the drug label information for the sponsor drug. The label information can be found in the 
filesystem in the below path:
- **Drugs' Label Information**: /synopsis/labels/<drug_name>.md
The Background Information section comprises of the following main sections.

- Drug Description.
- Clinical Pharmacology.

## Drug Description

This section should describe the investigational product which is the sponsor's drug.

**Investigation Product**: <Sponsor Drug name>
**Drug Description**:
  Derive the drug description from the drug label file saved in the file system.
  It should include the chemical name, molecular structure, emperical molecular formula, Inactive and active ingredients. Add necessary images from the label information file.

## Clinical Pharmacology:

This section contains many nested subsections that are as below. Use the drug label information to generate the following sections. You should only use the information from the source files. Do not invent or assume anything. If you do not find the information needed, leave the sections empty.
Recursively search the label information file, until you find the information in the label information file.
If no information is found, leave the section empty. Do not add numbering to the subsections. The main subsections should be in bold and underlined. The nested subsections should be in bold.

- Mechanism of Action and Pharmacodynamics
- Pharmacokinetics
    - Absorption
    - Distribution
    - Biotransformation
    - Elimination
- Indications and usage (Copy the Indication and Usage from the label from the 'HIGHLIGHTS OF PRESCRIBING INFORMATION' section)
- Dosage and administration
    - Patient Selection
    - Recommended Dosing
    - Dose Adjustments for Adverse Reactions
    - Dose adjustments for Co-administration with CYP3A Inhibitors
    - Special populations
- Contraindications
- Warnings and precautions
- Adverse reactions(Should start with a write up of the adverse reactions. Create a Tabulated list of adverse reactions. The columns should be MedDRA System Organ Class, Frequency of All CTCAE grades, Frequency of CTCAE grade 3 and above). Use the **internet_search** to get additional information.
- Drug interactions
    - Pharmacodynamic interactions
    - Pharmacokinetic interactions

