import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import multiprocessing
import math
from typing import Dict, List

text = """A heavier task could not have been imposed
Than I to speak my griefs unspeakable:
Yet, that the world may witness that my end
Was wrought by nature, not by vile offence,
I'll utter what my sorrows give me leave.
In Syracusa was I born, and wed
Unto a woman, happy but for me,
And by me, had not our hap been bad.
With her I lived in joy; our wealth increased
By prosperous voyages I often made
To Epidamnum; till my factor's death
And the great care of goods at random left
Drew me from kind embracements of my spouse:
From whom my absence was not six months old
Before herself, almost at fainting under
The pleasing punishment that women bear,
Had made provision for her following me
And soon and safe arrived where I was.
There had she not been long, but she became
A joyful mother of two goodly sons;
And, which was strange, the one so like the other,
As could not be distinguish'd but by names.
That very hour, and in the self-same inn,
A meaner woman was delivered
Of such a burden, male twins, both alike:
Those,--for their parents were exceeding poor,--
I bought and brought up to attend my sons.
My wife, not meanly proud of two such boys,
Made daily motions for our home return:
Unwilling I agreed. Alas! too soon,
We came aboard.
A league from Epidamnum had we sail'd,
Before the always wind-obeying deep
Gave any tragic instance of our harm:
But longer did we not retain much hope;
For what obscured light the heavens did grant
Did but convey unto our fearful minds
A doubtful warrant of immediate death;
Which though myself would gladly have embraced,
Yet the incessant weepings of my wife,
Weeping before for what she saw must come,
And piteous plainings of the pretty babes,
That mourn'd for fashion, ignorant what to fear,
Forced me to seek delays for them and me.
And this it was, for other means was none:
The sailors sought for safety by our boat,
And left the ship, then sinking-ripe, to us:
My wife, more careful for the latter-born,
Had fasten'd him unto a small spare mast,
Such as seafaring men provide for storms;
To him one of the other twins was bound,
Whilst I had been like heedful of the other:
The children thus disposed, my wife and I,
Fixing our eyes on whom our care was fix'd,
Fasten'd ourselves at either end the mast;
And floating straight, obedient to the stream,
Was carried towards Corinth, as we thought.
At length the sun, gazing upon the earth,
Dispersed those vapours that offended us;
And by the benefit of his wished light,
The seas wax'd calm, and we discovered
Two ships from far making amain to us,
Of Corinth that, of Epidaurus this:
But ere they came,--O, let me say no more!
Gather the sequel by that went before."""


def get_word_frequencies(line: str) -> Dict[str, int]:
    results = dict()
    for word in line.split(" "):
        results[word] = results.get(word, 0) + 1
    return results


def partition_text(chunk_size: int, input_text: List[str]) -> list[list[str]]:
    groups = []
    for i in range(0, 16):
        group = input_text[i * chunk_size:chunk_size + (i * chunk_size)]
        if len(group) > 0:
            groups.append(group)
    return groups


def clean_line(line: str, chars_to_remove: List[str]) -> str:
    result = line
    for char in chars_to_remove:
        result = result.replace(char, "")
    return result.lower()


def prepare_text() -> List[str]:
    lines = text.split("\n")
    chars_to_remove = [",", ":", ".", ";", "-", "'", "!"]
    cleaned = []
    for line in lines:
        cleaned.append(clean_line(line, chars_to_remove))
    return cleaned


def setup():
    cpu_count = multiprocessing.cpu_count()
    cleaned = prepare_text()
    chunk_size = math.ceil(len(cleaned) / cpu_count)
    groups = partition_text(chunk_size, cleaned)
    return groups


def merge_dicts(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    results = second

    for key, values in first.items():
        results[key] = results.get(key, 0) + first[key]
    return results


async def main():
    groups = setup()

    with ProcessPoolExecutor() as pool:
        loop = asyncio.get_event_loop()

        functions_to_run = []
        for group in groups:
            functions_to_run.append(partial(get_word_frequencies, " ".join(group)))

        result_futures = []

        for func in functions_to_run:
            result_futures.append(loop.run_in_executor(executor=pool, func=func))

        results = await asyncio.gather(*result_futures)

        final_result = functools.reduce(merge_dicts, results)
        print(final_result)


if __name__ == '__main__':
    asyncio.run(main())
