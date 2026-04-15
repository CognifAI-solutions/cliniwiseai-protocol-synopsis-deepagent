---
name: inclusion_exclusion_criteria
description: Provides instructions to generate Inclusion and Exclusion criteria sections in the protocol synopsis. Use the study title, drug/device name provided by sponsor, reference drug or device name.
---

# Generate Inclusion, Exclusion Criteria:

## Reference File directories.

Use the files in the following directories when required. Use the filesystem tool 'ls' to list the files in each directory

- **Drugs' Label Information**: /synopsis/labels/
- **Existing study protocols**: /synopsis/existing_protocols/

## Instructions(STRICT):

- Use the 'ls' filesystem tool to list all the files in the above directories.
- Read the contents of the each file.
- Use the information from the files to generate the Inclusion and Exclusion criteria
- You MUST analyse the following sections in the label information for extracting relevant information.
  - **Warnings and precautions**
  - **Indications and usage**
  - **Adverse Reactions**
  - **Drug Interactions**
  - **Use in Specific Populations**
  - **Medication Guide**
- You MUST analyse the following sections in the existing protocol synopsis for extracting relevant information.
  - **Inclusion Criteria**
  - **Exclusion Criteria**
- After gathering the required information from the above sections in labels and existing protocols,
use the following tools if required, to find more information if required.
    **internet_search**: Search the internet for additional information.
    **extract_webpage**: Extract webpage contents of the website url.
- The inclusion criteria and exclusion criteria should not be numbered list with proper line breaks in markdown format.

## Inclusion Criteria:

Inclusion criteria are characteristics that define the population under study, e.g., those criteria that every potential participant must satisfy, to qualify for study entry. Provide a statement that individuals must meet all of the inclusion criteria in order to be eligible to participate in the study and then list each criterion. Women and members of minority groups must be included in accordance with the NIH Policy on Inclusion of Women and Minorities as Participants In Research Involving Human Subjects.

Some criteria to consider for inclusion are: provision of appropriate consent and assent, willingness and ability to participate in study procedures, age range, health status, specific clinical diagnosis or symptoms, background medical treatment, laboratory ranges, and use of appropriate contraception. Additional criteria should be included as appropriate for the study design and risk.

### Inclusion Criteria Example Template

Analyse the following example template. The Inclusion criteria generated must closely follow this template.

```
Example text provided as a guide, customize as needed:

[In order to be eligible to participate in this study, an individual must meet all of the following criteria:
    1. Provision of signed and dated informed consent form
    2. Stated willingness to comply with all study procedures and availability for the duration of the study
    3. Male or female, aged <specify range>
    4. In good general health as evidenced by medical history or diagnosed with <specify condition/disease> or exhibiting <specify clinical signs or symptoms or physical/oral examination findings>
    5. <Specify laboratory test> results between <specify range>
    6. Ability to take oral medication and be willing to adhere to the <study intervention> regimen
    7. For females of reproductive potential: use of highly effective contraception for at least 1 month prior to screening and agreement to use such a method during study participation and for an additional <specify duration> weeks after the end of <study intervention> administration
    8. For males of reproductive potential: use of condoms or other methods to ensure effective contraception with partner
    9. Agreement to adhere to Lifestyle Considerations (see section 5.3) throughout study duration]
```

### Inclusion Criteria Example:

The inclusion criteria MUST be similar in format and in details to the below example.

```
Patients will be considered eligible for the study based on the following criteria:

    1. Willing and able to provide written informed consent prior to any study-related activities being performed.
    2. Male or female patients aged 18 years and older and having Body mass index (BMI) ≥ 17 calculated as weight in kg/height in m2. 
    3. Patients who requires treatment with the study drug as monotherapy.
    4. Patients with documented advanced (FIGO stages III and IV) BRCA1/2-mutated (germline and/or somatic) high-grade epithelial ovarian, fallopian tube or primary peritoneal cancer who are in response (complete or partial) following completion of first-line platinum-based chemotherapy.
OR
Patients with documented platinum-sensitive relapsed high-grade epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete or partial) to platinum-based chemotherapy should start treatment with Olaparib no later than 8 weeks after completion of their final dose of the platinum-containing regimen.
    5. Able to swallow and retain oral medication.
    6. Eastern Cooperative Oncology Group (ECOG) performance status ≤ 2.
    7. The life expectancy of > 90 days.
    8. Acceptable hematology status:
    a. Hemoglobin ≥ 9 G%
    b. Absolute neutrophil count (ANC) ≥ 1500 cells/µL
    c. Absolute white blood cell (WBC) count ≥ 3000 cells/µL
    d. Platelet count ≥ 1,00,000 cells/µL
    9. Acceptable liver function:
    a. Alanine aminotransferase (ALT) ≤ 2X upper limit of normal (ULN)
    b. Aspartate aminotransferase (AST) ≤ 2X ULN
    c. Bilirubin < 1.5X ULN
    d. Alkaline phosphatase ≤ 2X ULN
Note: For patients with Hepatic or bone metastasis: Alkaline phosphatase < 5X ULN 
    10. Patients with creatinine clearance ≥ 60 mL/minute (using the Cockcroft-Gault Equation).
    11. Female patients of child bearing potential with a negative serum pregnancy test.
    12. Male patients with female partners of reproductive potential must agree to use barrier contraceptives from screening, during study and for at least 03 months after treatment discontinuation.
    13. Women of childbearing potential, (defined as women physiologically capable of becoming pregnant) they must agree to use two effective methods of contraception during study participation and for at least 06 months after the treatment discontinuation.  
Acceptable methods of contraception are:
    a. Intrauterine device (IUD) or intrauterine system (IUD/IUS)
    b. Double barrier method of contraception (Condom and occlusive cap or condom and spermicidal agent)
    c. Male sterilization (at least 6 months prior to the screening, should be the sole male partner for that patient) plus one additional contraception method (hormonal or barrier method)
    d. Female sterilization (surgical bilateral oophorectomy) or tubal ligation within at least 6 weeks prior to study participation
    e. Total abstinence; partial abstinence is not acceptable.
Female patients of non-childbearing potential or female patients who have completed menopause are defined as patients who have 12 consecutive months of spontaneous amenorrhea (not amenorrhea induced by a medical condition or medical therapy) or have bilateral absence of the ovaries.  Female patients of non-childbearing potential are not required to use effective method of contraception during the study.
    14. Female patients must agree to not to breast feed baby while in the study and for 1 month after taking the last dose of IP.
    15. No history of addiction to any recreational drug or drug dependence or alcohol addiction.

```

## Exclusion Criteria:

Exclusion criteria are characteristics that make an individual ineligible for study participation. Provide a statement that all individuals meeting any of the exclusion criteria at baseline will be excluded from study participation and then list each criterion. If specific populations are excluded (e.g., elderly or pediatric populations, women or minorities), provide a clear and compelling rationale and justification, to establish that inclusion is inappropriate with respect to the health of the participants or the purpose of the research. Limited English proficiency cannot be an exclusion criterion.

Some criteria to consider for exclusion are: pre-existing conditions or concurrent diagnoses, concomitant use of other medication(s) or devices, known allergies, other factors that would cause harm or increased risk to the participant or close contacts, or preclude the participant’s full adherence with or completion of the study. Additional criteria should be included as appropriate for the study design and risk.

Include a statement regarding equitable selection or justification for excluding a specific population.

### Exclusion Criteria Example Template

Analyse the following example template. The Inclusion criteria generated must closely follow this template.

```
[An individual who meets any of the following criteria will be excluded from participation in this study:

    1. Current use of < specify disallowed concomitant medications>
    2. Presence of <specific devices (e.g., cardiac pacemaker)>
    3. Pregnancy or lactation
    4. Known allergic reactions to components of the <study intervention>, <specify components/allergens>
    5. Febrile illness within <specify time frame>
    6. Treatment with another investigational drug or other intervention within <specify time frame>
    7. Current smoker or tobacco use within <specify timeframe>
    8. < Specify any condition(s) or diagnosis, both physical or psychological, or physical exam finding that precludes participation>]
```

### Exlusion Criteria Example:


