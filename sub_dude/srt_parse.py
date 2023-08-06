import re
from typing import Dict, List


def parse_block(block):
    """Parse a single subtitle block"""
    # if block consists of just newline we're at the end of the file
    if block == "\n":
        return None
    try:
        index, timecodes, *text = block.split("\n")
        # convert list of text lines back to a single string with newlines
        text = "\n".join(text)

        # parse start and end times
        start_time, end_time = timecodes.split(" --> ")

        return {"text": text, "start_time": start_time, "end_time": end_time}
    except ValueError:
        raise ValueError(f"""Error parsing subtitles. Invalid block "{block}" """)


def srt_parse(srt_file: str) -> List[Dict[str, str]]:
    """Parse a srt file

    Parse srt file and return a list of dicts containing the timecode
    and text of each subtitle.
    """
    with open(srt_file, "r") as file:
        srt_text = file.read()

    # split by subtitle blocks
    blocks = re.split(r"\n\n", srt_text)

    # parse blocks using a list comprehension, filtering out None results
    subtitles = [sub for block in blocks if (sub := parse_block(block)) is not None]

    return subtitles


def concatenate_srt_list(srt_list):
    """Concatenate a list of srt dicts into a single srt string"""
    return "\n\n".join([f"{i}: {sub['text']}" for i, sub in enumerate(srt_list)])


def replace_translation(srt_list: List[Dict[str, str]], new_texts: List[str]):
    """Replace text in a list of srt dicts"""

    srt_list = srt_list.copy()
    for text in new_texts:
        number, text = re.findall(r'(\d+):\s*(.*)', text)[0]
        number = int(number)
        srt_list[number]["text"] = text

    return srt_list

