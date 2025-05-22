import subprocess
import asyncio

target = "bypkrpihayqo"

async def test_in(test_input):
    proc = await asyncio.create_subprocess_exec(
        "./constant_folding",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    #proc.stdin.write(test_input)
    stdout, stderr = await proc.communicate(test_input.encode())
    res = stdout.decode().split("processed secret: ")[1].strip()
    print(test_input)
    print(res)

    return res

max_len =12 
def encode_base26(n: int, length: int = 0) -> str:
    if n < 0:
        raise ValueError("Only non-negative integers are allowed")
    if n == 0:
        result = 'a'
    else:
        result = ''
        while n > 0:
            n, r = divmod(n, 26)
            result = chr(ord('a') + r) + result
    # Pad with 'a' to the left
    return result.rjust(length, 'a')


def pad_right(v, pad_to = max_len):
    return v + 'a' * (pad_to - len(v))
def strcmp_delta(v1, v2):
    assert(len(v1) == len(v2))
    ctr = 0
    for i in range(len(v1)):
        if v1[i] == v2[i]:
            ctr += 1
    return ctr


async def main():
    res_str = ""
    for i in range(13):
        found = False
        cur_max = await test_in(pad_right(res_str))
        cur_max_score = strcmp_delta(cur_max, target)
        for j in range(26):
            cur_char = chr(ord('a') + j)
            cur_str = res_str + cur_char
            cur_str = pad_right(cur_str)
            cur_res = await test_in(cur_str)
            score = strcmp_delta(target, cur_res)
            if score > cur_max_score:
                found = True
                res_str += cur_char
                break
        if not found:
            res_str += 'a'
    #for i in range(128):
    #    v = encode_base26(i, 12)
    #    res = await test_in(v)

if __name__ == "__main__":
    asyncio.run(main())

