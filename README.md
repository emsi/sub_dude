# sub_dude

sub_dude is a tool to create and translate subtitles.

1. Create a file `openai_api_key.txt` with your OpenAI API key
2. RUN:
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. streamlit run sub_dude/webui/app.py --browser.gatherUsageStats false
```
3. To render final video with subtitles you need to instal `ffmpeg` package
