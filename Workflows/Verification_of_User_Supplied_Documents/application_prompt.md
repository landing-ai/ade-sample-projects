Purpose:
The app needs to demonstrate the user workflow and the speed of processing for a quick verification check on user supplied documents.
The app should have 2 split sides. The left side can be what the user sees and the right side can show the code running and internal logic.


Functionallity:

Left side user-experience:
0. User is asked to enter 3 values: borrower_name, borrower_ssn, loan_application_date
1. User will be prompted to upload a specific type of document - DOC1 - that must have certain characteristics. 
2. LandingAi's Agentic Document Extraction (ADE) is use to parse the document and extract a small number of key value pairs.
3. Business rules are applied to the extracted values. If the DOC1 passes, the user is asked to upload the next document - DOC2 - and the process repeats. If DOC1 does not pass, the user is asked to try again.

Right side processing view:
1. Reports the time stamp when the user upload is complete
2. Reports the time stamp when ADE Parse is complete
3. Reports the time stamp when ADE Extract is complete
4. Prints the extracted key value pairs to screen
5. Prints the business rule checks to screen
6. Prints whether the document passes of fails to screen

DOC1 - W2 form
The application should ask for a W2 form as DOC1.
The extraction schema should include w2_employee_name, w2_employee_ssn, w2_tax_year
The business logic has 3 parts. All 3 parts must be true for the document to pass.
A. Does the extracted w2_employee_name match with the entered value borrower_name?
B. Does the extracted w2_employee_ssn match with the entered value borrower_ssn?
C. Is the W-2 within the last 2 years? If the current month of the year is greater than January, W-2 for previous year and the year before previous year is acceptable. If the current month of the year is January, W-2 for previous year, or two years prior is considered valid and acceptable.

DOC2 - Paystub
The application should ask for a Paystub form as DOC2.
The extraction schema should include paystub_employee_name, paystub_employee_ssn, paystub_paydate
The business logic has 3 parts. All 3 parts must be true for the document to pass.
A. Does the extracted paystub__employee_name match with the entered value borrower_name?
B. Does the extracted paystub__employee_ssn match with the entered value borrower_ssn?
C. Is the paystub_paydate within 30 days from the loan_application_date?



Questions:
Tech stack
  1. What framework do you prefer — Streamlit (fastest to build, easy to run locally), or a web app with Flask/FastAPI + HTML/JS (more
   polished, harder to share)? Or something else?

  Matching & validation logic
  2. For name matching (borrower_name vs. extracted name): exact match, case-insensitive, or fuzzy/partial? Names on documents often
  have middle names, suffixes, or formatting differences.
  3. For SSN matching: should the app normalize formats first (e.g., treat 123-45-6789 and 123456789 as equal)?
  4. If ADE fails to extract a field (returns null or empty), should that count as an automatic fail, or show a specific "could not
  extract" error?

  UX flow
  5. After DOC2 passes, what happens? A final success/congratulations screen? Or is there a DOC3+ in the future?
  6. Should the SSN input be masked (password field) for privacy, and should it be redacted in the right-side processing view?
  7. Should the right-side processing view update in real time as each step completes, or display all at once after processing
  finishes?

  API
  8. For extraction, are you using the Landing.AI ADE extract endpoint (similar to how classify.py uses the classify endpoint)? Do you
   have a preferred way to call it — via the landingai-ade Python package we just installed, or raw HTTP like in classify.py?

  Presentation
  9. Any branding requirements — Landing.AI logo, specific colors?
  10. Is this running locally only, or does it need to be shareable/deployable (e.g., a public URL)?

 1. Can Streamlit handle the side-by-side I asked for?                                                                               
  2. Exact match, case-insensitive. John McCay matches John Mccay but does not match John McCay Jr. or John Mc Cay                    
  3. SSN normalization is fine                                                                                                        
  4. Return null/empty. Proceed with business logic checks on other fields. If other fields pass, consider the document as a pass.    
  Add the document to a list for manual review.                                                                                       
  5. Success screen with summary metrics. Show extracted fields. Show time to parse each DOC, time to extract each DOC, total time    
  for DOC1, total time for DOC2                                                                                                       
  6. No. demo system with fake data                                                                                                   
  7. real-time                                                                                                                        
  8. Call the REST API using https://docs.landing.ai/api-reference/tools/ade-parse and                                                
  https://docs.landing.ai/api-reference/tools/ade-extract                                                                             
  9. Use the branding at @"Landing AI Brand Guidelines 2026 V1.html" which I just added                                               
  10. Local only 