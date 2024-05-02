from pyteal import *
import os

"""Basic Counter Application"""

def approval_program():
    handle_creation = Seq(
        App.globalPut(Bytes("Count1"), Int(0)),
        App.globalPut(Bytes("Count2"), Int(0)),
        App.globalPut(Bytes("Count3"), Int(0)),
        App.globalPut(Bytes("Count4"), Int(0)),
        Return(Int(1))
    )

    scratchCount = ScratchVar(TealType.uint64)

    addC1 = Seq(
        scratchCount.store(App.globalGet(Bytes("Count1"))),
        App.globalPut(Bytes("Count1"), scratchCount.load() + Int(1)),
        Return(Int(1))
    )

    addC2 = Seq(
        scratchCount.store(App.globalGet(Bytes("Count2"))),
        App.globalPut(Bytes("Count2"), scratchCount.load() + Int(1)),
        Return(Int(1))
    )

    addC3 = Seq(
        scratchCount.store(App.globalGet(Bytes("Count3"))),
        App.globalPut(Bytes("Count3"), scratchCount.load() + Int(1)),
        Return(Int(1))
    )

    addC4 = Seq(
        scratchCount.store(App.globalGet(Bytes("Count4"))),
        App.globalPut(Bytes("Count4"), scratchCount.load() + Int(1)),
        Return(Int(1))
    )

    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)),
        Cond(
            [Txn.application_args[0] == Bytes("AddC1"), addC1],
            [Txn.application_args[0] == Bytes("AddC2"), addC2],
            [Txn.application_args[0] == Bytes("AddC3"), addC3],
            [Txn.application_args[0] == Bytes("AddC4"), addC4],
        )
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation], 
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(0))], 
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(0))], 
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(Int(0))],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(0))],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=5)

def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)

if __name__ == "__main__":
    path = "./contracts/artifacts"
    with open(os.path.join(path, "counter_approval.teal"), 'w') as f:
        f.write(approval_program())
    with open(os.path.join(path, "counter_clear.teal"), 'w') as f:
        f.write(clear_state_program())
