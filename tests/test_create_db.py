from anagram.create_db import set_names, process_word

def test_names():
    fname = 'words.txt'
    db_name, outfile = set_names(fname)

    assert db_name == 'words.db'
    assert outfile == 'words.json'


def test_anagram():
    word = 'anagram'
    assert ''.join(sorted(word)) == 'aaagmnr'


def test_process_word():
    word = 'stop'

    size, anagram, de, le = process_word(word)

    assert size == '4'
    assert anagram == ''.join(sorted(word))
    assert de == {'size': 4, 'anagram': 'opst'}
    assert le == {'word': 'stop', 'size': '4', 'anagram': 'opst'}

def test_list():
    l_e = list()

    word = 'stop'
    size, anagram, de, le = process_word(word)
    l_e.append(le)

    word = 'helping'
    size, anagram, de, le = process_word(word)
    l_e.append(le)

    assert l_e[0] == {'word': 'stop', 'size': '4', 'anagram': 'opst'}
    assert l_e[1] == {'word': 'helping', 'size': '7', 'anagram': 'eghilnp'}

def test_dict():
    d_e = dict()

    word = 'stop'
    size, anagram, de, le = process_word(word)
    d_e[word] = de

    word = 'helping'
    size, anagram, de, le = process_word(word)
    d_e[word] = de

    assert d_e == {'stop': {'size': 4, 'anagram': 'opst'},
                   'helping': {'size': 7, 'anagram': 'eghilnp'}}
