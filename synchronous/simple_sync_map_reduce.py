from typing import Dict, Iterable, Callable


lines = [

    "A long time ago",
    "long ago so long",
    "ago that no one",
    "can remember and no",
    "tree can remember and",
    "no rock can remember",
    "so long ago that",
    "there were no people",
    "and there were no",
    "trees and the rocks",
    "had not been made"
]

def map_text_to_frequency(text: str) -> Dict[str, int]:
    mapped = {}
    words = text.split(' ')
    for word in words:
        mapped[word] = mapped.get(word, 0) + 1
    return mapped
  

def reduce(func: Callable, sequence: Iterable):
    """
    could use functools.reduce instead
    """
    iterator = iter(sequence)
    final = next(iterator)
    for item in iterator:
        final = func(final, item)
    return final  
  

def merge_dicts(a: Dict[str, int], b: Dict[str, int]) -> Dict[str, int]:
    final = a.copy()      # dont modify the original
    for key in b:
        final[key] = final.get(key, 0) + b[key]
    return final  
  
  
frequencies = [map_text_to_frequency(line) for line in lines]
result = reduce(merge_dicts, frequencies)
print(result)  
  
  
  
  
