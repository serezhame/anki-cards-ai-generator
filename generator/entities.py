from dataclasses import dataclass


@dataclass(frozen=True)
class WordWithContext:
    word: str
    context: str

    def __post_init__(self):
        if self.word is None or self.context is None:
            raise ValueError("Attributes cannot be None")
        if self.word == "":
            raise ValueError("Word cannot be empty")


@dataclass(frozen=True)
class CardRawData:
    word: str
    card_text: str
    card_text_path: str
    image_prompt: str
    image_url: str
    image_path: str

    def __post_init__(self):
        if self.word is None or self.card_text is None or self.card_text_path is None or self.image_url is None or self.image_path is None:
            raise ValueError("Attributes cannot be None")
        if self.word == "":
            raise ValueError("Word cannot be empty")
        if self.card_text == "":
            raise ValueError("Card text cannot be empty")
        if self.image_url == "":
            raise ValueError("Image URL cannot be empty")
        if self.card_text_path == "" or self.image_path == "":
            raise ValueError("Paths cannot be empty")