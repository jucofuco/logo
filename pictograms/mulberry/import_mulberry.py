"""Copies the Mulberry Symbols we use out of the official zip into pictograms/mulberry/svg/<word id>.svg.

Usage:  python3 pictograms/mulberry/import_mulberry.py <mulberry-symbols.zip>
Download the zip from https://github.com/mulberrysymbols/mulberry-symbols/releases/latest (about 52 MB,
not kept in the repo). Only the symbols listed below are copied, plus LICENSE.txt and VERSION.txt.

Mulberry has no pronouns, conjunctions, prepositions or adjectives of size, and no library, cinema,
museum, hoop, tetris and a few more, so those words have no entry here; the set built by build.py
(svg-mulberry/) takes our own style 2 drawing for them.
"""
import json
import pathlib
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent

# word id (logo/Vocabulary/structure.json) -> Mulberry symbol name (file name in EN-symbols/ without .svg)
MAPPING = {
    # core
    'yes': 'correct', 'no': 'mistake_no_wrong', 'want': 'want_,_to',
    # toys
    'ball': 'ball', 'computer': 'computer_1', 'phone': 'mobile_phone', 'teddy': 'teddy_bear', 'doll': 'doll',
    'blocks': 'bricks', 'cards': 'playing_cards', 'lego': 'lego', 'toyCar': 'car_toy', 'balloon': 'balloon',
    'puzzle': 'jigsaw_puzzle', 'bicycle': 'bicycle',
    # clothes
    'trousers': 'trousers', 'tshirt': 't-shirt', 'shorts': 'shorts', 'shirt': 'shirt', 'socks': 'socks',
    'shoes': 'shoe_-_mans', 'cap': 'cap', 'coat': 'coat', 'underpants': 'pants', 'glasses': 'glasses',
    'sunglasses': 'sunglasses', 'scarf': 'scarf',
    # verbs
    'see': 'look_,_to', 'make': 'make_,_to', 'ask': 'ask_,_to', 'dress': 'get_dressed_,_to', 'drink': 'drink_,_to',
    'eat': 'eat_,_to', 'go': 'go_,_to', 'listen': 'hear_,_to', 'play': 'play_,_to', 'sleep': 'sleep_female_,_to',
    'speak': 'talk_1_,_to', 'cook': 'cook_,_to', 'enter': 'type_,_to', 'stir': 'stir_,_to',
    # food
    'pizza': 'pizza', 'bread': 'bread', 'cheese': 'cheese', 'milk': 'milk', 'cake': 'cake', 'glassOfWater': 'water',
    'butter': 'butter', 'rice': 'rice', 'fruit': 'fruit', 'vegetables': 'vegetables', 'iceCream': 'ice_cream',
    'chocolate': 'chocolate', 'eggs': 'egg', 'soup': 'soup', 'chicken': 'chicken',
    # feelings
    'happy': 'happy_man', 'love': 'heart', 'sad': 'sad_man', 'surprised': 'surprised_man', 'angry': 'angry_man',
    'scared': 'afraid_man', 'hot': 'hot_person',
    # places
    'home': 'house', 'school': 'school', 'shop': 'shop', 'restaurant': 'cafe', 'classroom': 'class_room',
    'clinic': 'surgery_health_centre',
    # people
    'mom': 'mum_parent', 'dad': 'dad_parent', 'brother': 'brother', 'sister': 'sister', 'grandma': 'grandmother',
    'grandpa': 'grandfather', 'teacher': 'teacher_1a',
    # more
    'colors': 'paint_box', 'big': 'large', 'small': 'little', 'on': 'on',
}
MAPPING.update({f'letter.{c.lower()}': c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'})
MAPPING.update({f'number.{i}': n for i, n in enumerate(['Zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'])})


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    z = zipfile.ZipFile(sys.argv[1])
    available = {n[len('EN-symbols/'):-len('.svg')] for n in z.namelist() if n.startswith('EN-symbols/') and n.endswith('.svg')}
    missing = {i: s for i, s in MAPPING.items() if s not in available}
    if missing:
        sys.exit(f'not in the zip: {missing}')
    out = HERE / 'svg'
    out.mkdir(exist_ok=True)
    for old in out.glob('*.svg'):
        old.unlink()
    for word_id, symbol in MAPPING.items():
        (out / f'{word_id}.svg').write_bytes(z.read(f'EN-symbols/{symbol}.svg'))
    for name in ('LICENSE.txt', 'VERSION.txt'):
        (HERE / name).write_bytes(z.read(name))
    (HERE / 'index.json').write_text(json.dumps(sorted(MAPPING)), encoding='utf-8')
    print(f'{len(MAPPING)} symbols copied to {out}')


main()
