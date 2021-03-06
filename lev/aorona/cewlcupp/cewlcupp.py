"""
CeWL (5.4.9) + CUPP (0.0+20190501)
Homepage: -
GitHub: -
Type: IMAGE-BASED
Version: v1.0.4
"""

import levrt
from levrt import Cr, annot, ctx, remote
from levrt.annot.cats import Attck

# https://stackoverflow.com/questions/58751357/python-script-pexpect-hangs-on-child-wait
# https://stackoverflow.com/questions/26081820/regular-expression-to-extract-whole-sentences-with-matching-word

@annot.meta(
    desc="Run CeWL against a url",
    params=[
        annot.Param("depth", "depth to spider"),
        annot.Param("min_length", "minimum word length"),
        annot.Param("offsite", "allow spider to visit other sites"),
        annot.Param("url", "url to spider"),
    ],
    cats=[
        Attck.PrivilegeEscalation,
        Attck.CredentialAccess,
        Attck.LateralMovement
    ],
)
async def Cewl(
    url: str =  '',
    depth: int = 1,
    min_length: int = 3,
    offsite: bool = False,
) -> Cr:
    """
        Cewl
    """
    @levrt.remote
    def entry():
        import pexpect, logging, traceback, json
        cewl_file = 'cewl_file'
        try:
            logging.basicConfig()
            logger = logging.getLogger("lev")
            logger.setLevel(logging.DEBUG)
            # 1) run CeWL
            logger.debug('Running CeWL..')
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
            logger.debug('CeWL completed..')
            with open(cewl_file, 'r') as f:
                lines = f.readlines()
            wordlist = json.dumps([line.rstrip() for line in lines])
            ctx.set(wordlist=wordlist)
        except Exception as e:
            ctx.set(msg=f"Error running cewl: {e} {traceback.print_exc()}")
    return Cr("5991d9084fbd", entry=entry())

@annot.meta(
    desc="User Profiling : cupp -i",
    params=[
        annot.Param("first_name", "(Required, default='User') Password Creator's First Name"),
        annot.Param("surname", "Password Creator's Surname"),
        annot.Param("nickname", "Password Creator's Nickname"),
        annot.Param("birtday", "(Required, default=00000000) Password Creator's Birthday (DDMMYYYY)"),
        annot.Param("partners_name", "Password Creator's Partner's Name"),
        annot.Param("partners_nickname", "Password Creator's Partner's Nickname"),
        annot.Param("partners_birthday", "Password Creator's Partner's Birthday (DDMMYYYY)"),
        annot.Param("childs_name", "Password Creator's Child's Name"),
        annot.Param("childs_nickname", "Password Creator's Child's Nickname"),
        annot.Param("childs_birthday", "Password Creator's Child's Birthday"),
        annot.Param("pets_name", "Password Creator's Pet's Name"),
        annot.Param("company", "Password Creator's Company"),
        annot.Param("related_words", "Words related to the Password Creator"),
        annot.Param("special_chars", "Add special chars at the end of words"),
        annot.Param("random_nums", "Some random numbers at the end of words"),
        annot.Param("leet", " Leet mode")
    ],
    cats=[
        Attck.PrivilegeEscalation,
        Attck.CredentialAccess,
        Attck.LateralMovement
    ],
)

async def Cupp_User_Profile(
    first_name: str = "User",
    surname: str = "\n",
    nickname: str = "\n",
    birthday: str="00000000",
    partners_name: str = "\n",
    partners_nickname: str = "\n",
    partners_birthday: str ="\n",
    childs_name: str = "\n",
    childs_nickname: str = "\n",
    childs_birthday = "\n", 
    pets_name: str = "\n",
    company: str = "\n",
    related_words: str = "\n",
    concatenate: bool = False,
    special_chars: bool = False,
    random_nums: bool = False,
    leet: bool = False,
) -> Cr:
    """
    Use this tool to profile users.
    ```
    await Cupp_User_Profiling(...)
    ```
    """
    @levrt.remote
    def entry():
        import pexpect, logging, json, traceback
        def expect_str(child, search_str, desc, user_input, logger):
            logger.debug(f'{desc} before')
            child.expect([f"[^.?!]*(?<=[.?\s!]){search_str}(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            child.sendline(user_input)
            logger.debug(f'{desc} after')
        try:
            logging.basicConfig()
            logger = logging.getLogger("lev")
            logger.setLevel(logging.DEBUG)
            logger.debug('Spawning CUPP..')
            cupp_child = pexpect.spawn('cupp -i')
            logger.debug('CUPP spawned')
            expect_str(cupp_child, 'Name', 'First Name', first_name, logger)
            expect_str(cupp_child, 'Surname', 'Last Name', surname, logger)
            expect_str(cupp_child, 'Nickname', 'Nickname', nickname, logger)
            expect_str(cupp_child, 'DDMMYYYY', 'Birthdate', birthday, logger)
            expect_str(cupp_child, 'name', 'Partner\'s Name', partners_name, logger)
            expect_str(cupp_child, 'nickname', 'Partner\'s Nickname', partners_nickname, logger)
            expect_str(cupp_child, 'DDMMYYYY', 'Partner\'s birthdate', partners_birthday, logger)
            expect_str(cupp_child, 'name', 'Child\'s Name', childs_name, logger)
            expect_str(cupp_child, 'nickname', 'Child\'s Nickname', childs_nickname, logger)
            expect_str(cupp_child, 'DDMMYYYY', 'Child\'s Birthday', childs_birthday, logger)
            expect_str(cupp_child, 'name', 'Pet\'s Name', pets_name, logger)
            expect_str(cupp_child, 'name', 'Company Name', company, logger)
            expect_str(cupp_child, 'key words', 'Keywords', "Y", logger)
            expect_str(cupp_child, 'enter the words', 'Keywords List', related_words, logger)
            expect_str(cupp_child, 'concatenate', 'concatenate', "Y" if concatenate else "N", logger)
            expect_str(cupp_child, 'special chars', 'special_chars', "Y" if special_chars else "N", logger)
            expect_str(cupp_child, 'random numbers', 'random_nums', "Y" if random_nums else "N", logger)
            expect_str(cupp_child, 'Leet mode', 'leet', "Y" if leet else "N", logger)
            with open(f'{first_name}.txt', 'r') as f:
                lines = f.readlines()
            wordlist = json.dumps([line.rstrip() for line in lines])
            ctx.set(wordlist=wordlist)
            ctx.set(msg="Success")
        except Exception as e:
            ctx.set(msg=f"Error running Cupp_User_Profile: {e} {traceback.print_exc()}")
    return Cr("5991d9084fbd", entry=entry())

@annot.meta(
    desc="CewL + CUPP",
    params=[
        annot.Param("depth", "depth to spider"),
        annot.Param("min_length", "minimum word length"),
        annot.Param("offsite", "allow spider to visit other sites"),
        annot.Param("url", "url to spider"),
        annot.Param("word_list", "word list"),
        annot.Param("concatenate", "concatenate all words from wordlist"),
        annot.Param("special_chars", "add special chars at the end of words"),
        annot.Param("random_nums", "some random numbers at the end of words"),
        annot.Param("leet", " Leet mode"),
    ],
    cats=[Attck.PrivilegeEscalation, Attck.CredentialAccess, Attck.LateralMovement],
)
async def CewlCupp(
    url: str =  '',
    depth: int = 1,
    min_length: int = 3,
    offsite: bool = False,
    concatenate: bool = False,
    special_chars: bool = False,
    random_nums: bool = False,
    leet: bool = False,
) -> Cr:
    """
    CewlCupp
    """
    @remote
    def entry():
        import pexpect, logging, traceback, json
        def expect_str(child, search_str, desc, user_input, logger):
            logger.debug(f'{desc} before')
            child.expect([f"[^.?!]*(?<=[.?\s!]){search_str}(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            child.sendline(user_input)
            logger.debug(f'{desc} after')
        cewl_file = "cewl_file"
        try:
            logging.basicConfig()
            logger = logging.getLogger("lev")
            logger.setLevel(logging.DEBUG)
            # 1) run CeWL
            logger.debug('Running CeWL..')
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
            logger.debug('CeWL completed..')
            # 2) Run CUPP
            logger.debug('Running CUPP..')
            cupp_child = pexpect.spawn(f'cupp -w {cewl_file}')
            expect_str(cupp_child, 'concatenate', 'concatenate', "Y" if concatenate else "N", logger)
            expect_str(cupp_child, 'special', 'special_chars', "Y" if special_chars else "N", logger)
            expect_str(cupp_child, 'random', 'random', "Y" if random_nums else "N", logger)
            expect_str(cupp_child, 'Leet', 'Leet', "Y" if leet else "N", logger)
            ctx.set(msg="Success")
            with open(f'{cewl_file}.cupp.txt', 'r') as f:
                lines = f.readlines()
            wordlist = json.dumps([line.rstrip() for line in lines])
            ctx.set(wordlist=wordlist)
        except Exception as e:
            ctx.set(msg=f"Error running CewlCupp: {e} {traceback.print_exc()}")
    return Cr("5991d9084fbd", entry=entry())

__lev__ = annot.meta(
    [Cewl, Cupp_User_Profile],
    desc = "CeWL (5.4.9) + CUPP (0.0+20190501)",
    cats = {
        Attck: [
            Attck.PrivilegeEscalation,
            Attck.CredentialAccess,
            Attck.LateralMovement
        ]
    }
)
