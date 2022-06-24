import pexpect, logging, asyncio, sys, traceback

async def cewl(
    url: str =  '',
    depth: int = 1,
    min_length: int = 3,
    offsite: bool = False,
):
    cewl_file = '/cewl_file'
    try:
        options_str = f'-k -m{min_length} -d{depth} -w {cewl_file}' 
        if offsite:
            options_str = f'{options_str} -o'
        cewl_child = pexpect.spawn(f'cewl {options_str} {url}')
        while True:
            try:
                cewl_child.read_nonblocking()
            except Exception:
                break
        if cewl_child.isalive():
            cewl_child.wait()
    except Exception as e:
        print("Error running cewl: {e} {traceback.print_exc()}")

async def cupp_interactive(
    first_name: str = '',
    last_name: str = '',
    nickname: str = '',
    birthdate: str = '',
    partner: str = '',
    partner_nickname: str = '',
    partner_birthdate: str = '',
    child_name: str = '',
    child_nickname: str = '',
    child_birthdate: str = '',
    pet_name: str = '',
    keywords: str = '',
    company_name: str = '',
    concatenate: bool = False,
    special_chars: bool = False,
    random_nums: bool = False,
    leet: bool = False,
):
    try:
        logging.basicConfig()
        logger = logging.getLogger("lev")
        logger.setLevel(logging.DEBUG)
        cupp_child = pexpect.spawn(f'cupp -i')

        # First Name
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])Name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Surname
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])Surname(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Birthdate
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])DDMMYYYY(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Partner's name
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Partner's nickname
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])birthdate(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Partner's birthdate
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Child's name
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])nickname(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Child's nickname
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])DDMMYYYY(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Child's birthdate
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Pet's name
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])

        # Company name
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])


        cupp_child.expect(["[^.?!]*(?<=[.?\s!])concatenate(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if concatenate else "N")
        cupp_child.expect([">[^.?!]*(?<=[.?\s!])special(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if special_chars else "N")
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])random(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if random_nums else "N")
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])Leet(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if leet else "N")
    except Exception as e:
        print("Error running cupp_interactive: {e} {traceback.print_exc()}")

async def cewlcupp(
    url: str =  '',
    depth: int = 1,
    min_length: int = 3,
    offsite: bool = False,
    concatenate: bool = False,
    special_chars: bool = False,
    random_nums: bool = False,
    leet: bool = False,
) :
    cewl_file = '/cewl_file'
    try:
        logging.basicConfig()
        logger = logging.getLogger("lev")
        logger.setLevel(logging.DEBUG)
        # 1) run CeWL
        print('Running CeWL..')
        options_str = f'-k -m{min_length} -d{depth} -w {cewl_file}' 
        if offsite:
            options_str = f'{options_str} -o'
        cewl_child = pexpect.spawn(f'cewl {options_str} {url}')
        while True:
            try:
                cewl_child.read_nonblocking()
            except Exception:
                break
        if cewl_child.isalive():
            cewl_child.wait()
        print('CeWL completed..')
        # 2) Run CUPP
        print('Running CUPP..')
        cupp_child = pexpect.spawn(f'cupp -w {cewl_file}')
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])concatenate(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if concatenate else "N")
        cupp_child.expect([">[^.?!]*(?<=[.?\s!])special(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if special_chars else "N")
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])random(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if random_nums else "N")
        cupp_child.expect(["[^.?!]*(?<=[.?\s!])Leet(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
        cupp_child.sendline("Y" if leet else "N")
        ctx.set(msg="Success")
    except Exception as e:
        print("Error running cewlcupp: {e} {traceback.print_exc()}")

if __name__ == "__main__":
    asyncio.run(cewl(
        url = 'https:levi.zone',
        depth = 1,
        min_length = 3,
        offsite = False,
    ))
    asyncio.run(cupp_interactive(
        concatenate = False,
        special_chars = False,
        random_nums = False,
        leet = False
    ))
    asyncio.run(cewlcupp(
        url = 'https:levi.zone',
        depth = 1,
        min_length = 3,
        offsite = False,
        concatenate = False,
        special_chars = False,
        random_nums = False,
        leet = False
    ))
