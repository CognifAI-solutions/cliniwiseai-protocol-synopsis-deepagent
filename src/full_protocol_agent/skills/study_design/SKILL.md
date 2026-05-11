---
name: study_design
description: Provides instructions to generate the Study Design section of the clinical trial protocol for the sponsor drug.
---

# Generating Study Design.
A Brief Study Design is generated in the protocol synopsis file available in the file system
- **Protocol Synopsis**: /synopsis/protocol_synopsis.md

Expand on the study design found in the protocol synopsis.
The Study Design should also include Randomization and Blinding section.

### Generating Images

1. Use the **generate_image** tool to create flow diagrams if required.
2. Save the generated image to the filesystem at path /protocol/images.
3. Refer the images in valid markdown format in the Study Design section.

## Generating Randomization And Blinding
Generate two subsections from the Study Design
- Randomization
- Blinding