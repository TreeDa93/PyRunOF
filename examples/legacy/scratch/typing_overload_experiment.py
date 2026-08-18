from typing import Callable, Generator, overload

@overload
def process(response: None) -> None:
    if isinstance(response, None):
        print('None')
@overload
def process(response: int) -> tuple[int, str]:
    if isinstance(response, int):
        print('int')
@overload
def process(response: str) -> str:
    if isinstance(response, str):
        print('str')

def process(response):
    print(response)

process('str')
