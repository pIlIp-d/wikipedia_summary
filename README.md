# wikipedia_summary
Little script that summarizes wikipedia articles using simple nltk techniques

# Installation

## Clone Repo
```bash
git clone https://github.com/pIlIp-d/wikipedia_summary
cd wikipedia_summary
```

## Install Python Packages
```bash
pip install -r requirements.txt
```

# Usage

Put the wikipedia title you want to summarize in the string at the bottom. (where "Rick Astley" is)
Run the programm and you get the summarized parts in `output.json`. 
```bash
python wikipedia_summary.py
```

Formatted like this:
```json
[
{
  "heading": "some fitting heading",
  "body": "summarized content of the paragraph"
},
...
]
```
