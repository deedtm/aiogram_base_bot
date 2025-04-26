from dataclasses import dataclass


@dataclass()
class ExtendedCallback:
    data: str
    button_text: str
    prefix: str = ""

    def prefix_text(self, prefix: str = "") -> str:
        if not prefix:
            prefix = self.prefix
        return (prefix + " " + self.button_text).strip()

    def text_from_data(self) -> str:
        d = self.data
        self.button_text = (
            d.split(":", 1)[1].replace("_", " ").replace(":", " ").title()
        )
        return self.button_text
