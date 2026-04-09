---
name: samplesize_products_duration
description: Provides instructions to generate Sample Size Justification, Investigational Products, Study Duration sections of the protocol synopsis.Uses the study title, drug/device name provided by sponsor, reference drug or device name.
---

# Generating Sample Size Justification, Investigational Products, Study Duration

## Reference File directories.
Use the files in the following directories when required. Use the filesystem tool 'ls' to list the files in each directory
  - **Drugs' Label Information**: /synopsis/labels/

## Sample Size Justification:

A Generic statement for Sample Size Justification. Use the below example as such

Eg. Considering drop-out and withdrawals, XX patients will be randomized.
Withdrawn and discontinued patients will not be replaced.

## Investigational Products:

- Analyse the drug labels files in /synopsis/labels.
- Generate the following content from the label information.

  **Test Product (T)** : The sponsor provided drug name, dosage and drug format in a single sentence.
  **Reference Product (R)**: The reference drug name provided, dosage, drug format and the Marketing Authorization Holder name or Manufacturer name in a single sentence.

## Study Duration:

It should have two parts. The contents of the section will be the same as the example provided.

- **A table with the one row**. The column names should be.
Column 1 - Total Study Duration.
Column 2 - Approximately 64 days.
Column 3 - Approximately 42 days.

- **A Paragraph**: Total patient study participation duration will depend on the number of days needed to conduct all the screening procedures as well as stabilization period.

