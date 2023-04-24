import fitz
import imagehash
import io
from PIL import Image


def get_blocks_from_pdf(filename: str, page_number: int = None):
    doc = fitz.open(filename)
    page_blocks = {}
    for page in doc:
        if page_number and page_number != page.number + 1:
            continue
        page_text = page.get_text("dict")
        page_blocks[page.number + 1] = page_text["blocks"]
    if page_number and page_number not in page_blocks.keys():
        raise KeyError(f"Page number {page_number} not found in the PDF document")
    return page_blocks


def get_texts_from_pdf(filename: str, page_number: int = None):
    blocks = get_blocks_from_pdf(filename=filename, page_number=page_number)
    page_text_blocks = {}
    for blocks_page_number, page_blocks in blocks.items():
        if page_number and page_number != blocks_page_number:
            continue
        text_blocks = []
        for block in page_blocks:
            if block["type"] == 0:
                text_blocks.append(get_text_from_block(block))
        page_text_blocks[blocks_page_number] = text_blocks
    return page_text_blocks


def return_checkboxes(
    filename: str = None, blocks: dict = None, checkbox_texts: list = []
):
    if filename:
        blocks = get_blocks_from_pdf(filename)
    if not blocks:
        raise ValueError("Either filename or blocks must be provided")
    checkboxes = {}
    for _, page_blocks in blocks.items():
        for block in page_blocks:
            block_text = get_text_from_block(block)
            if block_text and block_text in checkbox_texts:
                img_number = block["number"] - 1
                previous_block = page_blocks[img_number]
                if previous_block["type"] == 1:
                    checkboxes[img_number] = {
                        "image": previous_block,
                        "text": block_text,
                        "checked": None,
                    }
    return checkboxes


def get_text_from_block(block):
    if block["type"] != 0:
        return None
    text = ""
    for line in block["lines"]:
        for span in line["spans"]:
            text += span["text"]
    return text


def get_status_of_checkboxes(checkboxes, reference_checked_image):
    hash0 = imagehash.average_hash(Image.open(reference_checked_image))
    cutoff = 5  # maximum bits that could be different between the hashes.
    for checkbox_number, checkbox in checkboxes.items():
        hash1 = imagehash.average_hash(
            Image.open(io.BytesIO(checkbox["image"]["image"]))
        )
        if hash0 - hash1 < cutoff:
            checkboxes[checkbox_number]["checked"] = True
        else:
            checkboxes[checkbox_number]["checked"] = False
    return checkboxes


if __name__ == "__main__":
    filenames = ["resources\\1_Blaa_blaa_2.PDF", "resources\\1_Blaa_blaa_3.PDF"]
    checkbox_texts = [
        "DNA Palvelutasot (Laitteiden valvontajärjestelmä)",
        "Liittymien hallinta ja raportointi (Sähköiset itsepalvelukanavat)",
    ]
    reference_checkbox_checked_image = "resources/checkbox_checked.png"
    for filename in filenames:
        print(f"Checking checkboxes in {filename}")
        checkboxes = return_checkboxes(filename=filename, checkbox_texts=checkbox_texts)
        checkboxes = get_status_of_checkboxes(
            checkboxes, reference_checkbox_checked_image
        )
        for key, val in checkboxes.items():
            print(
                f"\tCheckbox: '{val['text']}' is {'checked' if val['checked'] else 'not checked'}"
            )
