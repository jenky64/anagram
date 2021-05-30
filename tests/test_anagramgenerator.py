from anagram.anagramgenerator import AnagramGenerator
import pytest

generator = AnagramGenerator()


@pytest.mark.order(1)
def test_initialize_db():
    db_name = 'collins.db'

    generator.initialize_db(db_name=db_name)
    table = generator.database.get_tables()[0]

    assert table == 'words'


@pytest.mark.order(2)
def test_get_stats():
    generator.get_stats()

    assert generator.max_word_length == 15
    assert generator.word_count == 279496


@pytest.mark.order(3)
def test_set_word_set_size_one():
    generator.set_word(word='python')

    assert generator.word == ['h', 'n', 'o', 'p', 't', 'y']
    assert generator.min_size == 2
    assert generator.max_size == 7
    assert generator.size is None


@pytest.mark.order(4)
def test_set_word_set_size_two():
    generator.set_word(word='numbers', min_size=3, max_size=4)

    assert generator.word == ['b', 'e', 'm', 'n', 'r', 's', 'u']
    assert generator.min_size == 3
    assert generator.max_size == 5
    assert generator.size is None


@pytest.mark.order(5)
def test_set_word_set_size_three():
    generator.set_word(word='regis', size=4)

    assert generator.word == ['e', 'g', 'i', 'r', 's']
    assert generator.min_size == 4
    assert generator.max_size == 5
    assert generator.size is None


@pytest.mark.order(6)
def test_generate_anagrams_one():
    generator.set_word('stop')
    generator.generate_anagrams()

    expected = {2: ['op', 'os', 'po', 'so', 'st', 'to'],
                3: ['ops', 'opt', 'pos', 'pot', 'pst', 'sop', 'sot', 'top'],
                4: ['opts', 'post', 'pots', 'spot', 'stop', 'tops']}

    assert generator.anagrams == expected


@pytest.mark.order(7)
def test_generate_anagrams_two():
    generator.set_word('python', min_size=3, max_size=4)
    generator.generate_anagrams()

    expected = {3: ['hon', 'hop', 'hot', 'hoy', 'hyp', 'noh', 'not', 'noy', 'nth', 'ony', 'opt',
                    'pho', 'pht', 'poh', 'pot', 'tho', 'thy', 'ton', 'top', 'toy', 'yon'],
               4: ['hypo', 'phon', 'phot', 'pont', 'pony', 'pyot', 'thon', 'tony',
                   'toph', 'typo', 'yont']}

    assert generator.anagrams == expected


@pytest.mark.order(8)
def test_generate_anagrams_three():
    generator.set_word('development', size=7)
    generator.generate_anagrams()

    expected = {7: ['demeton', 'deplete', 'develop', 'devotee', 'dolente', 'dovelet',
                    'element', 'enmoved', 'envelop', 'evented', 'lemoned', 'leptome',
                    'pentode', 'teendom', 'telemen', 'templed', 'venomed']}


    assert generator.anagrams == expected
