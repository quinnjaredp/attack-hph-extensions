Extending ATT&CK: HPH DICOM PoC

--------------------------------
PACKAGE DESCRIPTION

This is a small, reusable, proof-of-concept uses the Healthcare and Public Health (HPH) sector as an example of how to model sector-specific abuse using tools like ATT&CK Workbench and ATT&CK Navigator.

The package adds a custom HPH sub-technique, along with its related objects, to ATT&CK - and includes a focused Navigator layer with triage notes which link back to the custom Workbench collection.

--------------------------------
USE CASE

CVE-2025-35975 (https://www.cve.org/CVERecord?id=CVE-2025-35975) was published in May of 2025, and addresses a 'code-execution via malformed .dcm' vulnerability in the MicroDicom Viewer application. 

The PoC demonstrates how to represent and operationalize sector-specific risks such as this.

--------------------------------
PACKAGE CONTENTS

Workbench Collection: workbench_hph_dicom.json

  - Sub-Technique: Malicious Healthcare File (QNTK-T1204.121)
	
	- Data Source: Clinical File Telemetry (QNTK-DS1201)

		- Analytic: Analytic 1201 (QNTK-AN1201)
		
		- Log Source: Healthcare File Telemetry (QNTK-LS1201)

		- Asset: Healthcare Imaging Workstation (QNTK-A1201)
		
		- Campaign: Operation Code Blue (QNTK-C1201)
		
		- Group: Wizard Spider (G0102)
		  Note: A hypothetical relationship to QNTK-T1204.121 was added for demonstration.

		- Software: Ryuk (S0446)
		  Note: A hypothetical relationship to QNTK-T1204.121 was added for demonstration.
		
		- Mitigation: Sector-Specific File Normalization (QNTK-M1201)
		
		- Detection: Malicious Healthcare File - Structure Anomaly (QNTK-DET1201)

Navigator Layer: navigator_hph_dicom.json

  - HPH: DICOM Layer with only the QNTK-T1204.121 visible. 
	
	- A default coverage score 10 (i.e., No Coverage) was applied to QNTK-T1204.121. 
		
	- The QNTK-T1204.121 sub-technique includes an example triage checklist and links back to the corresponding Workbench objects. 

--------------------------------
MINIMUM PREREQUISITES

  - ATT&CK Workbench (e.g., Docker)

  - ATT&CK Navigator v5.x

  - ATT&CK Enterprise Dataset (e.g., v17.x available in Workbench/Navigator)

Note: The Navigator layer’s links assume the Workbench UI is at https://localhost/. If your UI differs, update the links after import.

--------------------------------
QUICK START

1. 	Import the provided Workbench collection.

	- Open Workbench → Collections → Imported Collections → Import Collection.

	- Select workbench_hph_dicom.json.

	- Verify you can open:

		- QNTK-T1204.121 under 'T1204: User Execution'

		- QNTK-DS1201 (Data Source)
		
		- QNTK-AN1201 (Analytic)

2. Make Navigator aware of the custom objects.

	- In Navigator: Create New Layer → More options → Create from collection/STIX file, then upload workbench_hph_dicom.json.

		- Domain: enterprise-attack

		- Version: 17.1201 (or any unused number)

	Note: This step lets Navigator resolve the custom QNTK-… objects by name.

3. Load the Navigator layer. 

	- Open Navigator → Open Existing Layer → Load from your computer.

	- Select navigator_hph_dicom.json.
	  
	Note: You should see a minimal layer with User Execution → Malicious Healthcare File highlighted in red and a tooltip containing triage notes that can be pinned.

Optional: Fix link targets if Workbench isn’t at localhost.

In Navigator:

  - Select the sub-technique → Technique Controls → Links (and Layer Controls → Links if used):

	- Change http://localhost to your Workbench URL.

Alternatively, edit the JSON before loading:

   - macOS/Linux: sed -i '' 's#https://localhost/#https://your-host/#g' navigator_hph_dicom.json

   - Windows (PowerShell): (Get-Content navigator_hph_dicom.json) -replace 'https://localhost/','https://your-host/' | Set-Content navigator_hph_dicom.json

--------------------------------
HOW TO

Teach the workflow: Pin the sub-technique tooltip to show the triage checklist to analysts during hunt/IR.

Assess the coverage: Clone the layer, add legend items (e.g., red = triage now, amber = needs engineering, green = covered) and score techniques across the path.

Extend to production: Add your data source names, analytics, and runbooks as Links; copy the comments into your “Master” layer.

--------------------------------
FINE PRINT

This PoC is intentionally narrow, it focuses on a single healthcare-specific execution path to show how sector content hangs together in ATT&CK.

No malware or exploit code is included. If you test parsing/validation behaviors, do so in an isolated lab.

--------------------------------
TROUBLESHOOTING NOTES

Links open with a 404 on mitre.org: That’s expected for custom objects; use the Workbench links in the tooltip/layer.

No red color: Ensure the sub-technique has a score of 10, and that your legend/gradient is configured (i.e., Layer Controls → color/legend).

Missing objects after import: Re-import workbench_hph_dicom.json into Workbench first, then reload the Navigator layer.

--------------------------------
LICENSE

This repository uses **dual licensing**:

- **Content (CTI JSON, layers, docs):** Creative Commons **CC BY 4.0**  
  See `LICENSE-CC-BY-4.0`. You **must** attribute:  
  *“Extending ATT&CK: HPH DICOM PoC by Jared P. Quinn (https://github.com/quinnjaredp)”* and indicate changes.

- **Code/scripts (if present):** **Apache License 2.0**  
  See `LICENSE-APACHE-2.0` and `NOTICE`. You may use, modify, and redistribute (including commercially) with preservation of notices.

Attribution line you can copy:
> Extending ATT&CK: HPH DICOM PoC © Jared P. Quinn — used under CC BY 4.0 / Apache-2.0 (as applicable).

--------------------------------
INTEGRITY CHECK

workbench_hph_dicom.json SHA-256: 707F183C57D362F02A66540F60B2B3D5BD905F6EAD4CCE3E52692D33CF85A92A 

navigator_hph_dicom.json SHA-256: 9806D6285070312400E03407391947770AF16E58BEE2A8D391A66FD644F3BC74

--------------------------------
VERSION HISTORY

- **0.1.0 — 2025-09-12**  
  First public PoC: Workbench collection (`workbench_hph_dicom.json`) and Navigator layer (`navigator_hph_dicom.json`) for CVE-2025-35975; includes sub-technique QNTK-T1204.121, mitigation QNTK-M1201, campaign QNTK-C1201, analytic QNTK-A1201, and links/triage note.

- **0.1.1 — 2025-09-12**  
  File renames, README polish, integrity hashes, license added.
