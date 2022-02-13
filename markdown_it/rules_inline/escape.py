"""
Process escaped chars and hardbreaks
"""
from .state_inline import StateInline
from ..common.utils import isSpace


ESCAPED = [0 for _ in range(256)]
for ch in "\\!\"#$%&'()*+,./:;<=>?@[]^_`{|}~-":
    ESCAPED[ord(ch)] = 1


def escape(state: StateInline, silent: bool):
    pos = state.pos
    maximum = state.posMax

    if state.src[pos] != "\\":
        return False

    pos += 1

    if pos < maximum:
        ch = state.src[pos]

        if ch < "\u0100" and ESCAPED[ord(ch)] != 0:
            if not silent:
                state.pending += state.src[pos]
            state.pos += 2
            return True

        if ch == "\n":
            if not silent:
                state.push("hardbreak", "br", 0)

            pos += 1
            # skip leading whitespaces from next line
            while pos < maximum:
                ch = state.src[pos]
                if not isSpace(ch):
                    break
                pos += 1

            state.pos = pos
            return True

    if not silent:
        state.pending += "\\"
    state.pos += 1
    return True
