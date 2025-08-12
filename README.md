Translate with AI is a Python 3 tool for managing and generating translation files using AI-assisted workflows.

It reads structured JSON files containing LocalDefinition entries, lets you modify translations, and then writes them back in JSON format (with rolling backups) and generates plain-text language files for use in other programs.

## Features
- Maintain translation definitions from a single JSON file.
- Modify translations in Python with built-in helpers (close, synced defaults, etc.).
- Save back to JSON, sorted by language and term.
- Keep history — up to 3 rolling backups of your JSON file.
- Export language-specific .txt files grouped by section for other programs to consume.
- Compatible with AI-assisted translation pipelines.

## Example Input Text
```
#=Common
^@menu.action.start=Start
^@menu.action.auth=Authorize
^@menu.action.deauth=Deauthorize
^@menu.header.store=Store
^@menu.action.restore=Restore Purchases
^@menu.action.unlock=Unlock Premium
^@menu.header.links=Links
^@menu.menu.title=Rotate to Landscape
^@menu.menu.subtitle=Make the image match this:
^@menu.resume=Resume
@com.please.wait.device=Contacting Device....
@com.please.wait.store=Loading store details....
@com.please.wait.dir=Loading directory....
@com.please.wait.loc=Loading locations....
@com.please.wait.folder=Loading folder....
```
### Key Points

`#=` Translations are groupped into sections, this is the start of a new section

`@` A word to translate

`^@` The final product should be "Translation - English"

`!@` Don't translate, just pass along

## What do you need?

For my local environment i've been using Ollama to have API access to the AI.  And the code is setup to use `gpt-oss:20b` which needs about 12 gigs of ram, but has really shined when it comes to translating.

## What is the workflow?

1. In your development tool, have it write out the developer txt file, of all English Strings in a text format.
2. Run the Python conversion tool.
3. The translated text files will be placed into the folder of your choice.
