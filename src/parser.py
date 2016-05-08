import lexer
import jpype
# Kkma is slower, yet more verbose than Mecab.
# If speed becomes the issue, consider changing to Mecab.
from konlpy.tag import Kkma
from threading import Thread
# from konlpy.tag import Mecab
THREAD_CNT = 4

nl_parser = Kkma()


def tagging(result, que):
    """get string from a queue and tags it"""
    # to avoid error when ran as a thread
    jpype.attachThreadToJVM()
    while 1:
        try:
            tok = que.pop()
            result[tok.pos] = (tok.time, tok.user,
                               nl_parser.pos(tok.contents))
        except AttributeError:
            pass
        except IndexError:
            break
    return


def parse(fp):
    """create threads to tag chatlog using a thread-safe queue"""
    chat_len, chat_que = lexer.lex(fp)
    ret = [None] * chat_len
    pool = [Thread(target=tagging, args=(ret, chat_que))
            for _ in range(THREAD_CNT)]
    for t in pool:
        t.daemon = True
        t.start()
    for t in pool:
        t.join()
    # print(ret)
    return ret
