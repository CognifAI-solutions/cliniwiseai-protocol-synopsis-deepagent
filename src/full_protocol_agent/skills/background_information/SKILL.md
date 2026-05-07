---
name: background
description: Provides instructions to generate the Background Information section of the clinical trial protocol for the sponsor drug.
---

# Generate Background Information Section.

The background section should be created using the drug label information for the sponsor drug.

The Background Information section comprises of the following main sections.

- Drug Description.
- Clinical Pharmacology.

## Drug Description

This section should describe the investigational product which is the sponsor's drug.

**Investigation Product**: <Sponsor Drug name>
**Drug Description**:
  Derive the drug description from the drug label file saved in the file system.
  It should include the chemical name, molecular structure, emperical molecular formula, Inactive and active ingredients. Add images if needed from the label file.

## Clinical Pharmacology:

This section contains many nested subsections that are as below. Use the drug label information and existing protocol files to generate the following sections. You should only use the information from the source files. Do not invent or assume anything. If you do not find the information needed, leave the sections empty.

- Mechanism of Action and Pharmacodynamics
- Pharmacokinetics
- Absorption
- Distribution
- Biotransformation
- Elimination
- Indications and usage
- Dosage and administration
    - Patient Selection
    - Recommended Dosing
    - Dose Adjustments for Adverse Reactions
    - Dose adjustments for Co-administration with CYP3A Inhibitors
    - Special populations
- Contraindications
- Warnings and precautions
- Adverse reactions
- Drug interactions
    - Pharmacodynamic interactions
    - Pharmacokinetic interactions

