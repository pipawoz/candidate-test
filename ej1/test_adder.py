from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer, Event, Combine
from cocotb.clock import Clock
from cocotb.result import TestSuccess, TestFailure
from random import getrandbits

from adder import Stream, Adder


async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0


@cocotb.test()
async def test_specifics(dut):

    dut._log.info("Running test_specifics...")

    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    dut._log.info(stream_input_a)

    N = 5
    width_a = len(dut.a__data)
    width_b = len(dut.b__data)
    mask = int('1' * width_a, 2)

    data_a = [0x0A, 0x0A, -0x0A, -0x0A, 0x0A]
    data_b = [0x04, -0x04, 0x04, -0x04, -0x0A]
    expected = [0x0E, 0x06, 0x1A, 0x12, 0x00]

    # for a, b, r in zip(data_a, dgata_b, expected):
    #    dut._log.info("[a]:{:02X}, [b]:{:02X}, [r]:{:02X}".format(a, b, r))

    send_a = cocotb.fork(stream_input_a.send(data_a))
    send_b = cocotb.fork(stream_input_b.send(data_b))
    send_a.join()
    send_b.join()

    received = await stream_output.recv(N)

    for expctd, rcvd in zip(expected, received):
        if expctd != rcvd:
            raise TestFailure("Test failed")

    raise TestSuccess("Test passed")


@cocotb.test()
async def test_random_positive(dut):

    dut._log.info("Running test_random_positive...")

    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    dut._log.info(stream_input_a)

    N = 20
    width_a = len(dut.a__data)
    width_b = len(dut.b__data)
    mask = int('1' * width_a, 2)

    data_a = [getrandbits(width_a) for _ in range(N)]
    data_b = [getrandbits(width_b) for _ in range(N)]

    expected = [(a + b) & mask for a, b in zip(data_a, data_b)]

    # for a, b, r in zip(data_a, data_b, expected):
    #    dut._log.info("[a]:{:02X}, [b]:{:02X}, [r]:{:02X}".format(a, b, r))

    send_a = cocotb.fork(stream_input_a.send(data_a))
    send_b = cocotb.fork(stream_input_b.send(data_b))
    send_a.join()
    send_b.join()

    received = await stream_output.recv(N)

    for expctd, rcvd in zip(expected, received):
        if expctd != rcvd:
            raise TestFailure("Test failed")

    raise TestSuccess("Test passed")


@cocotb.test()
async def test_empty_adder(dut):

    dut._log.info("Running test_empty_adder...")

    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    dut._log.info(stream_input_a)

    N = 20
    width_a = len(dut.a__data)
    width_b = len(dut.b__data)
    mask = int('1' * width_a, 2)

    data_a = [getrandbits(width_a) for _ in range(N)]
    data_b = [0 for _ in range(N)]
    expected = [a & mask for a in data_a]

    # for a, b, r in zip(data_a, data_b, expected):
    #    dut._log.info("[a]:{:02X}, [b]:{:02X}, [r]:{:02X}".format(a, b, r))

    send_a = cocotb.fork(stream_input_a.send(data_a))
    send_b = cocotb.fork(stream_input_b.send(data_b))
    send_a.join()
    send_b.join()

    received = await stream_output.recv(N)

    for expctd, rcvd in zip(expected, received):
        if expctd != rcvd:
            dut._log.info("Expected {} Got {}".format(expctd, rcvd))
            raise TestFailure("Test failed")

    raise TestSuccess("Test passed")


@cocotb.test()
async def test_negatives(dut):

    dut._log.info("Running test_negatives...")

    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    dut._log.info(stream_input_a)

    N = 20
    width_a = len(dut.a__data)
    width_b = len(dut.b__data)
    mask = int('1' * width_a, 2)

    data_a = [-getrandbits(width_a) for _ in range(N)]
    data_b = [-getrandbits(width_b) for _ in range(N)]

    expected = [(a + b) & mask for a, b in zip(data_a, data_b)]

    # for a, b, r in zip(data_a, data_b, expected):
    #    dut._log.info("[a]:{:02X}, [b]:{:02X}, [r]:{:02X}".format(a, b, r))

    send_a = cocotb.fork(stream_input_a.send(data_a))
    send_b = cocotb.fork(stream_input_b.send(data_b))
    send_a.join()
    send_b.join()

    received = await stream_output.recv(N)

    for expctd, rcvd in zip(expected, received):
        if expctd != rcvd:
            dut._log.info("Expected {} Got {}".format(expctd, rcvd))
            raise TestFailure("Test failed")

    raise TestSuccess("Test passed")

if __name__ == '__main__':
    core = Adder(5)
    run(
        core, 'test_adder',
        ports=[
            *list(core.a.fields.values()),
            *list(core.b.fields.values()),
            *list(core.r.fields.values())
        ],
        vcd_file='adder.vcd'
    )
