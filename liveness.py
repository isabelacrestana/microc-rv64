"""Parte a implementar pelo grupo. Consulte ENUNCIADO.pdf."""
from backend_api import REGISTERS, CFG, BasicBlock, Liveness, InstructionLiveness
import ir

def solve_liveness(cfg):

    use_per_block = {}
    def_per_block = {}
    live_in = {block.start: set() for block in cfg.blocks.values()}
    live_out = {block.start: set() for block in cfg.blocks.values()}

    for block_id, block in cfg.blocks.items():
        use_b = set()
        def_b = set()

        for i in range(block.start, block.stop):
            instruction = cfg.function.instructions[i]
            use_b |= ir.uses(instruction) - def_b
            def_b |= ir.defs(instruction)

        use_per_block[block_id] = use_b
        def_per_block[block_id] = def_b

    changed = True

    while (changed):
        changed = False

        for block_id, block in block.sucessors:

            new_out = set()

            for successor_id in block.sucessors:
                new_out = new_out | live_in[successor_id]

            new_in = use_per_block[block_id] | (new_out - def_per_block[block_id])

            if new_out != live_out[block_id] or new_in != live_in[block_id]:
                live_out[block_id] = new_out
                live_in[block_id] = new_in
                changed = True

    return Liveness(live_in=live_in, live_out=live_out)




def solve_instruction_liveness(cfg, liveness):
    """Retorne os conjuntos antes e depois de cada instrução."""
    live_before = {}
    live_after = {}

    for block_id, block in cfg.blocks.items():
        current_alive = liveness.live_out[block.start]

        for i in reversed(block.start, block.stop):
            instruction = cfg.function.instructions[i]
            live_after[i] = set(current_alive)
            live_before[i] = ir.uses(instruction) | (live_after[i] - ir.defs(instruction))
            current_alive = live_before[i]

    return InstructionLiveness(before=live_before, after=live_after)
