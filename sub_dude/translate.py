import re
from itertools import chain
from typing import List, Dict

import openai

from sub_dude.srt_parse import srt_parse, concatenate_srt_list, replace_translation


def split_into_chunks(lst, chunk_size, overlap):
    """Split a list into overlapping chunks"""
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size - overlap)]


def join_overlapping_chunks(chunks, overlap):
    """Join overlapping chunks"""
    # Check if the overlap is larger than the chunk size
    if overlap > len(chunks[0]):
        raise ValueError("Overlap size cannot be larger than chunk size")
    remaining_chunks = [chunk[overlap:] for chunk in chunks[1:]]
    return list(chain.from_iterable(chunks[0:1] + remaining_chunks))


def translate_srt(
    srt_file,
    *,
    target_language="Polish",
    extra_prompt_instruction="",
    model="gpt-3.5-turbo",
    temperature=0.1,
    chunk_size=10,
    overlap=3,
    overlap_mode="lines",
    callback=None,
):
    """Translate an SRT file

    Translation happens in overlapping chunks of `chunk_size` lines,
    with `overlap` lines of overlap. This helps maintain consistent
    translation.
    """
    str_list = srt_parse(srt_file)

    srt_chunks = split_into_chunks(str_list, chunk_size, overlap if overlap_mode == "lines" else 0)

    messages = []
    translated_chunks = []
    for i, chunk in enumerate(srt_chunks):
        chunk_str = concatenate_srt_list(chunk)
        messages += translation_message(
            chunk_str,
            target_language=target_language,
            extra_prompt_instruction=extra_prompt_instruction,
        )

        response = translate_chunk(
            messages[-1:] if overlap_mode == "lines" else messages[-overlap:],
            target_language=target_language,
            model=model,
            temperature=temperature,
            callback=callback,
        )
        translated_chunk_str = find_translated_text(response)
        translated_list = re.split(r"\n\n", translated_chunk_str)
        translated_chunks += [replace_translation(chunk, translated_list)]

        if overlap_mode == "messages":
            messages += [
                {
                    "role": "assistant",
                    "content": response,
                }
            ]

    return join_overlapping_chunks(translated_chunks, overlap if overlap_mode == "lines" else 0)


def find_translated_text(translated_text):
    """Find the translated text in the response"""
    match = re.search(r"'''\n?(.*?)'''", translated_text, re.DOTALL)
    if match:
        return match.group(1)
    return translated_text


def translate_chunk(messages, *, model, temperature, target_language, callback=None):
    """Translate a chunk of text"""

    print(messages)
    messages = translation_messages(messages, target_language=target_language)

    full_response = ""
    for response in openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=True,
    ):
        response = response.choices[0].delta.get("content", "")
        full_response += response
        if callback:
            callback(response)

    return full_response


def translation_message(text_chunk, *, target_language, extra_prompt_instruction):
    """Construct the translation message"""
    return [
        {
            "role": "user",
            "content": f"""
'''
{text_chunk}
'''
Please translate above text to {target_language}. 
Please maintain the exact text structure (lines of text, empty lines, line breaks, etc.) and do not add or remove any text.
Enclose whole translation inside triple single quotes ('''). 
{extra_prompt_instruction}
""",
        }
    ]


def translation_messages(messages: List[Dict[str, str]], *, target_language: str):
    """Construct the translation messages"""
    return [
        {
            "role": "system",
            "content": f"""You are a world class professional translator specialized in translating to {target_language}.""",
        }
    ] + messages


"""
0: As most creators know, creating videos can be a super lengthy and frustrating process.
1: But what if I told you with the help of AI, you can convert text to video in only one minute
2: by generating an automatic script and instantly turning it into a full-blown video
3: in just a couple of clicks. Let's get straight in. So first thing we want to do is write a script,
4: um, generate a script. We'll be using VEED's free AI Video Script Generator in which we can simply
5: write out the idea we have for our video, select the tone of voice and format specifics, and let
6: the AI Generator do its thing. In just a few moments you will have an amazing and suitable
7: video script you can use for your videos. So now we have our video script and the next thing we'll
8: be doing is heading to VEED's built-in video editor. Of course we can record the video ourselves but
9: that would take time and we don't want to do that. Instead what we'll do is copy the text of the
10: generated script, head over to the text-to-speech menu in the editor, and we're going to paste our
11: script text into the text-to-speech text box. Select a language and AI voice by choice and
12: when you're satisfied add the text-to-speech audio to your project. So now you've got your audio.
13: Dolphins are some of the most fascinating creatures in the ocean. Now let's quickly turn
14: it into subtitles. Under the subtitles tab in the menu you can make this happen automatically.
15: The subtitles will come out accurately and fully synced with the audio yet fully editable through
16: the text boxes and timeline menu if you would like to make certain adjustments. Additionally
17: under the styles tab you can fully customize the design of your subtitles. You can choose a
18: subtitle preset but you can also change the font, the size, colors, add effects, or even one-click
19: subtitle animations to really make your subtitles stand out. Finally to bring your video to life

0: Jak większość twórców wie, tworzenie filmów może być bardzo długim i frustrującym procesem.
1: Ale co byś powiedział, gdybym powiedział Ci, że dzięki pomocy sztucznej inteligencji możesz przekształcić tekst w film w zaledwie jedną minutę?
2: generując automatyczny scenariusz i natychmiast zamieniając go w pełnoprawny film
3: w zaledwie kilka kliknięć. Zaczynajmy od razu. Pierwszą rzeczą, którą chcemy zrobić, jest napisanie scenariusza,
4: eh, wygenerowanie scenariusza. Będziemy korzystać z darmowego generatora scenariuszy wideo AI VEED, w którym po prostu możemy
5: opisać pomysł, jaki mamy na nasz film, wybrać ton głosu i szczegóły formatowania, a następnie
6: pozwolić generatorowi AI zrobić swoje. W zaledwie kilka chwil będziesz miał niesamowity i odpowiedni
7: scenariusz wideo, który możesz wykorzystać do swoich filmów. Teraz mamy nasz scenariusz wideo, a następną rzeczą, którą
8: zrobimy, jest przejście do wbudowanego edytora wideo VEED. Oczywiście możemy sami nagrać film, ale
9: to zajęłoby czas, którego nie chcemy tracić. Zamiast tego skopiujemy tekst
10: wygenerowanego scenariusza, przejdziemy do menu przekształcania tekstu na mowę w edytorze i wkleimy nasz
"""
