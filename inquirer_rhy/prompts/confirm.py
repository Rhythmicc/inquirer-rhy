# -*- coding: utf-8 -*-
"""
confirm type question
"""
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession

from .common import default_style


def question(message, **kwargs):
    # TODO need ENTER confirmation
    default = kwargs.pop('default', True)

    # TODO style defaults on detail level
    style = kwargs.pop('style', default_style)
    status = {'answer': None}

    qmark = kwargs.pop('qmark', '?')

    def get_prompt_tokens():
        tokens = []

        tokens.append(('class:questionmark', qmark))
        tokens.append(('class:question', ' %s' % (message + ' ' if message else '')))
        if isinstance(status['answer'], bool):
            tokens.append(
                ('class:answer', ' Yes' if status['answer'] else ' No'))
        else:
            if default:
                instruction = ' (Y/n)'
            else:
                instruction = ' (y/N)'
            tokens.append(('class:instruction', instruction))
        return tokens

    # key bindings
    kb = KeyBindings()

    @kb.add('c-q', eager=True)
    @kb.add('c-c', eager=True)
    def _(event):
        event.app.exit(result=None)
        #raise KeyboardInterrupt()

    @kb.add('n')
    @kb.add('N')
    def key_n(event):
        status['answer'] = False
        event.app.exit(result=False)

    @kb.add('y')
    @kb.add('Y')
    def key_y(event):
        status['answer'] = True
        event.app.exit(result=True)

    @kb.add('enter', eager=True)
    def set_answer(event):
        status['answer'] = default
        event.app.exit(result=default)

    return PromptSession(
        message=get_prompt_tokens,
        key_bindings=kb,
        mouse_support=False,
        style=style,
        erase_when_done=False,
    )
