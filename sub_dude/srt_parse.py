import re
from copy import deepcopy
from typing import Dict, List

from sub_dude.text_parse import word_wrap


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


def srt_parse(srt_text: str) -> List[Dict[str, str]]:
    """Parse a srt file

    Parse srt file and return a list of dicts containing the timecode
    and text of each subtitle.
    """

    # split by subtitle blocks
    blocks = re.split(r"\n\n", srt_text)

    # parse blocks using a list comprehension, filtering out None results
    subtitles = [sub for block in blocks if (sub := parse_block(block)) is not None]

    return subtitles


def srt_dump(*, srt_list, srt_filename):
    """Dump subtitles to a srt file"""
    with open(srt_filename, "w") as file:
        for index, subtitle in enumerate(srt_list, start=1):
            file.write(
                f"""{index}\n{subtitle["start_time"]} --> {subtitle["end_time"]}\n{subtitle["text"]}\n\n"""
            )
        file.write("\n")


def concatenate_srt_list(srt_list):
    """Concatenate a list of srt dicts into a single srt string"""
    return "\n\n".join([f"{i}: {sub['text']}" for i, sub in enumerate(srt_list)])


def replace_translation(srt_list: List[Dict[str, str]], new_texts: List[str]):
    """Replace text in a list of srt dicts"""

    srt_list = deepcopy(srt_list)
    for text in new_texts:
        number, text = re.findall(r"(\d+):\s*(.*)", text)[0]
        number = int(number)
        srt_list[number]["text"] = word_wrap(text)

    return srt_list
