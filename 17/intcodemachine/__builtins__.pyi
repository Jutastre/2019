
def reset() -> None : ...
def select_machine(machine_id:int) -> None : ...
def set_debug(debug_level:int) -> None : ...
def set_debug_global(debug_level:int) -> None : ...
def status() -> tuple[int,str] : ...
def feed(program:list[int]) -> None : ...
def execute() -> None : ...
def read() -> list[int] : ...
def output() -> int : ...
def input(number:int) -> None : ...
