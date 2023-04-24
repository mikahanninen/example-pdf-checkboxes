*** Settings ***
Library     PDF_extras.py
Library     RPA.PDF
Library     Collections


*** Variables ***
@{PDFS}                         resources\\1_Blaa_blaa_2.PDF
...                             resources\\1_Blaa_blaa_3.PDF
@{CHECKBOX_TEXTS}               DNA Palvelutasot (Laitteiden valvontajärjestelmä)
...                             Liittymien hallinta ja raportointi (Sähköiset itsepalvelukanavat)
${REFERENCE_CHECKED_IMAGE}      resources/checkbox_checked.png


*** Tasks ***
Minimal task
    FOR    ${filename}    IN    @{PDFS}
        Log To Console    Checking checkboxes in ${filename}
        ${checkboxes}=    Return Checkboxes    filename=${filename}    checkbox_texts=${CHECKBOX_TEXTS}
        ${checkboxes}=    Get Status Of Checkboxes    ${checkboxes}    ${REFERENCE_CHECKED_IMAGE}
        FOR    ${key}    ${value}    IN    &{checkboxes}
            Log To Console    \tCheckbox: '${value}[text]' is ${value}[checked]
        END
    END
