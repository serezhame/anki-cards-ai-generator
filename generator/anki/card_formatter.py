import os

from . import anki_operations
from ..config import Config
from ..entities import CardRawDataV1


def get_front_html(card_data: CardRawDataV1) -> str:
    formatted_text = card_data.card_text.replace('. ', '.<br>')
    styles = """
    <style>
    .card {
        max-width: 90%; 
        margin: auto; 
        padding: 10px;
    }
    .card-image {
        max-width: 100%; 
        max-height: 450px; 
        height: auto; 
        width: auto; 
        border-radius: 10px;
    }
    
    .card-text {
        font-size: 18px;
        text-align: justify;
        line-height: 1.5;
    }

    .delimiter {
        margin-top: 30px;
        margin-bottom: 30px;
        height: 3px;
        border: none;
        background-color: #ccc;
        display: block;
    }
    </style>
    """

    front_content = f"""
    {styles}
    <div class="card">
        <!-- Image -->
        <img class="card-image" src="{os.path.basename(card_data.image_path)}">

        <!-- Delimiter -->
        <hr class="delimiter">

        <p style='font-family: Verdana, sans-serif; font-size: 20px; text-align: center; margin-bottom: 20px;'>
            {card_data.translation}
        </p>

        <!-- Delimiter -->
        <hr class="delimiter">

        <!-- Text -->
        <p class="card-text">{formatted_text}</p>
    </div>
    """
    return front_content


def get_back_html(card_data: CardRawDataV1) -> str:
    styles = """
    <style>
    .hint {
        font-family: Consolas;
        font-size: 20px;

        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 50px;
        margin-bottom: 10px;
    }

    .dictionary-url {
        color: gray;
        font-weight: bold;
        text-decoration: underline;
    }

    .audio-container {
        text-align: right;
    }
    .audio-button {
        margin-left: 5px;
    }
    </style>
    """

    answer = f"""
    <div style='font-family: Verdana, sans-serif; font-size: 20px; text-align: center; margin-bottom: 20px;'>
        {card_data.word}
    </div>
    """

    # Prepare the container for dictionary link
    back_content = f"""
    {styles}
    {answer}
    <div class='hint'>
    """

    # If there's a dictionary URL, add a link to it
    if card_data.dictionary_url:
        back_content += f"<a class='dictionary-url' href='{card_data.dictionary_url}' target='_blank'>Dictionary</a>"
    else:
        back_content += f"<a class='dictionary-url'></a>"

    # Add audio if it exists
    if card_data.audio_path:
        # audio_text = f"<span class='audio-text'>Audio</span>"
        audio_button = f"<span class='audio-button'>[sound:{os.path.basename(card_data.audio_path)}]</span>"
        back_content += f"<div class='audio-container'>{audio_button}</div>"

    # Close the container
    back_content += """
    </div>
    </div>
    """
    return back_content


def format(card_data: CardRawDataV1, deck_name: str):
    # Ensure sentences end with a new line in HTML and handle text styling
    front_content = get_front_html(card_data)
    back_content = get_back_html(card_data)

    # Construct the note dictionary with HTML content
    return {
        "deckName": deck_name,
        "modelName": Config.CARD_MODEL,
        "fields": {
            "Front": front_content,
            "Back": back_content
        },
        "options": {
            "allowDuplicate": True,
            "duplicateScope": "deck"
        },
        "tags": [anki_operations.word_to_tag(card_data.word), "ai-generated"]
    }
