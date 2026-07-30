I want to build a front-end human-in-the-loop user application which allows users to rapidly compare an original document with the values extracted from that document, make edits if any are required and save the human-reviewed final output. Here are the overall requirements.

Use Agentic Document Extraction from LandingAI to do all of the document processing work. Be sure to use only the v2 stack, which calls the DPT-3 model family. 
You have access to Agentic Document Extraction skills via the plugin named ade-document-processing


1. Top panel where a user 
A. Selects a folder such as input_folders/bill_of_lading
B. Selects a schema to use from schemas folder such as schemas/bill-of-lading-schema.json

C. Presses a button that says "Parse+Extract", which sends the documents using standard tier to parse jobs and extract jobs and saves the results into the corresponding results folder within the selected folder. 
D. Displays a progress bar for Parse completeions and Extraction completions for the count of files in the input folder.

2. A Main panel where a human will review the extracted value versus the original document on e file at a time across all the files in the input folder.

Left side shows the original document with highlighting to allow the human to see the source of the extracted values - line or table cell. Offer 3 different variations of color are formatting for the user to choose from. They can use whatever is easiest in their eyes.

Right side shows each value in the extraction schema with field name, extracted value, and a place to type in an override value. When the user clicks a field name on the right, the exact line or table location is highlighted on the left. Allow the user to navigate using arrows keys to go up and down in the schema.

Minimalist design to make scanning easy. Use the LandingAI brand colors and fonts to make it look like a LandingAI application.


3. Bottom panel with:
A. a button labelled Submit Final for this File. The Final extraction values are a json file based on the Agentic Document Extraction extract file with any human overrides recorded as the correct final values. Saved the final file into the HIL_results folder within the selected folder. In the final ouptut make it clear which values are human overrides.
B. A button labelled Submit Batch whch submits all the human review work for all the files in the folder. This also craetes an extraction error report showing how many human overrides where submitted across all files and the natre of the errors.



