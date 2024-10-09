(1518, 930)
(1553, 804)
(1497, 930)


from util import click

def main():
    def _click(pos):
        click(pos,moveDuration=0.1)
    for i in range(9*14):
        _click((1518, 930))
        _click((1553, 804))
        _click((1497, 930))


import eventloop
eventloop.wrap(main)
