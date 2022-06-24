import json

def newlinestr_to_json(filename: str = ''):
    with open(filename, 'r') as f:
        lines = f.readlines()
        wordlist = [line.rstrip() for line in lines]
    return json.dumps(wordlist)

def expect_str(child, search_str, desc, user_input, logger):
    logger.debug(f'{desc} before')
    child.expect([f"[^.?!]*(?<=[.?\s!]){search_str}(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
    child.sendline(user_input)
    logger.debug(f'{desc} after')