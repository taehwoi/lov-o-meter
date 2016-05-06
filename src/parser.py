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
    # to avoid error when ran as a thread
    jpype.attachThreadToJVM()
    while not que.empty():
        idx, time, user, contents = que.get()
        result[idx] = (time, user, nl_parser.pos(contents))
    return


def parse(fp):
    chat_len, chat_que = lexer.lex(fp)
    print(chat_len)
    ret = [0] * chat_len
    pool = [Thread(target=tagging, args=(ret, chat_que))
            for _ in range(THREAD_CNT)]
    for t in pool:
        t.daemon = True
        t.start()
    for t in pool:
        t.join()
    return ret
