# Aiogram Base Bot

This repository contains a template for Telegram bots built with aiogram 3.20.0post0, providing a structured foundation for your bot development.

## Getting Started

1. Create a `.env` file in the root directory
2. Add your bot token: `BOT_TOKEN=your_telegram_bot_token_here`

## Template System Overview

The template uses a dynamic initialization system that converts JSON template files into Python dataclasses for easier usage in your code.

### Initialization Process

On each code execution:

- JSON template files from the `templates/` directory are processed
- Corresponding Python dataclasses are generated in the `templates/enums/` directory
- These classes become immediately available for import

> [!IMPORTANT]
> The `templates/enums/` directory is generated automatically on first execution and is not included in the source code.

### Creating Custom Templates

**Template File Format:**
```json
{
    "attribute_name": "attribute_value",
    "nested_attribute": {
        "inner_attribute_name": "inner_attribute_value"
    }
}
```

**To create a custom template:**

1. Create a `your_template_name.json` file in the `templates/` directory
2. Register your template in `templates/__init__.py`

Your template will be converted to a dataclass in `templates/enums/your_template_name.py` with class name `YourTemplateName`.

> [!NOTE]
> Nested dictionaries are automatically converted to separate dataclasses in `templates/enums/mod_your_template_name/attribute_name.py` and accessible as attributes of the parent class.

> [!TIP]
> Templates are processed before other code executes, so you can safely import your template classes at the top of your files.
