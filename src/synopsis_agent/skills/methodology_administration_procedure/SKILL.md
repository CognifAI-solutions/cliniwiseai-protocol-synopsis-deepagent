---
name: methodology_administration_procedure
description: Provides instructions to generate Methodology and Investigational Product Administration Procedure sections in the protocol synopsis. Use the study title, drug/device name provided by sponsor, reference drug or device name.
---

# Generate Methodology, Investigational Product Administration Procedure sections

## Reference File directories:
Use the files in the following directories when required. Use the filesystem tool 'ls' to list the files in each directory
 - **Drugs' Label Information**: /synopsis/labels/
 - **Existing study protocols**: /synopsis/existing_protocols/ 

## Methodology:

This section will include Visit wise details as several paragraphs:

- Screening duration, washout or stabilization duration (if applicable)
- Tests to be conducted at screening (will include common safety tests like laboratory examinations- haematology, biochemistry etc and diagnostic tests for the indication as per inclusion criteria and as given in the label).
- The day of randomization and housing if required will be mentioned along with treatment period and how long the treatment period will last.
- Details of total PK samples will be included if applicable (the number of PK samples to be withdrawn will be decided upon PK data from literatures/ label/ Pharmacology review)
- Brief details of dosing at clinical facility and at home will be mentioned.
- EOS day and safety follow up day will be mentioned with window period.

## Investigational Product Administration Procedure:

The adminisitration procedure should be generated for both the following:
- **Test Product (T)**
- **Reference Product (T)**

If the drug is a generic product, use the label information available for the drug.
Refer the existing protocols to generate the administration procedure.

If the above to information do not exist, add the following generic message to this sections.
```
To be provided by the sponsor
```
