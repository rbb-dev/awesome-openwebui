# Export to Word

Export current conversation from Markdown to Word (.docx) file with proper Chinese and English encoding.

## Features

- **One-Click Export**: Adds an "Export to Word" action button to the chat.
- **Markdown Conversion**: Converts Markdown syntax to Word formatting (headings, bold, italic, code, tables, lists).
- **Multi-language Support**: Properly handles both Chinese and English text without garbled characters.
- **Auto Title Extraction**: Automatically uses the first heading as the filename.

## Supported Markdown Syntax

| Syntax                              | Word Result                    |
| :---------------------------------- | :----------------------------- |
| `# Heading 1` to `###### Heading 6` | Heading levels 1-6             |
| `**bold**` or `__bold__`            | Bold text                      |
| `*italic*` or `_italic_`            | Italic text                    |
| `***bold italic***`                 | Bold + Italic                  |
| `` `inline code` ``                 | Monospace with gray background |
| ` ``` code block ``` `              | Code block with indentation    |
| `[link](url)`                       | Blue underlined link text      |
| `~~strikethrough~~`                 | Strikethrough text             |
| `- item` or `* item`                | Bullet list                    |
| `1. item`                           | Numbered list                  |
| Markdown tables                     | Table with grid                |
| `---` or `***`                      | Horizontal rule                |

## Usage

1. Install the plugin.
2. In any chat, click the "Export to Word" button.
3. The .docx file will be automatically downloaded to your device.

## Font Configuration

- **English Text**: Times New Roman
- **Chinese Text**: SimSun (宋体) for body, SimHei (黑体) for headings
- **Code**: Consolas

## Author

Fu-Jie  
GitHub: [Fu-Jie/awesome-openwebui](https://github.com/Fu-Jie/awesome-openwebui)

## License

MIT License
