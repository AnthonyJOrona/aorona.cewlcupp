"""
CeWL (5.4.9) + CUPP (0.0+20190501)
Homepage: -
GitHub: -
Type: IMAGE-BASED
Version: v1.4.0
"""
from levrt import Cr, annot, ctx, remote, File
from levrt.annot.cats import Attck

# https://stackoverflow.com/questions/58751357/python-script-pexpect-hangs-on-child-wait
# https://stackoverflow.com/questions/26081820/regular-expression-to-extract-whole-sentences-with-matching-word

@annot.meta(
    desc="Dictionary: cupp -w <file>",
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
    """
    @remote
    def entry():
        import pexpect, logging, traceback
        cewl_file = '/cewl_file'
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
        except Exception as e:
            ctx.set(msg=f"Error running cewl: {e} {traceback.print_exc()}")
    return Cr("", entry=entry())

@annot.meta(
    desc="Dictionary: cupp -w <file>",
    params=[
        annot.Param("depth", "depth to spider"),
        annot.Param("min_length", "minimum word length"),
        annot.Param("offsite", "allow spider to visit other sites"),
        annot.Param("url", "url to spider"),
        annot.Param("concatenate", "concatenate all words from wordlist"),
        annot.Param("special_chars", "add special chars at the end of words"),
        annot.Param("random_nums", "some random numbers at the end of words"),
        annot.Param("leet", " Leet mode"),
    ],
    cats=[Attck.PrivilegeEscalation, Attck.CredentialAccess, Attck.LateralMovement],
)


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
        annot.Param("childs_birthday", "Password Creator's Child's Birthday")
        annot.Param("pets_name", "Password Creator's Pet's Name"),
        annot.Param("company", "Password Creator's Company"),
        annot.Param("keywords", "Add words related to the Password Creator?")
        annot.Param("related_words", "Words related to the Password Creator"),
        annot.Param("special_chars", "Add special chars at the end of words"),
        annot.Param("random_nums", "some random numbers at the end of words"),
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
    keywords: bool = False,
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
    @remote
    def entry():
        import pexpect, logging, json
        try:
            logging.basicConfig()
            logger = logging.getLogger("lev")
            logger.setLevel(logging.DEBUG)

            logger.debug('Spawning CUPP..')
            cupp_child = pexpect.spawn('cupp -i')
            logger.debug('CUPP spawned')

            logger.debug('First Name')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])Name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(first_name)
            logger.debug('First Name Added')

            logger.debug('Last Name')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])Surname(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(surname)
            logger.debug('Last Name Added')

            logger.debug('Nickname')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])Nickname(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(nickname)
            logger.debug('Nickname Added')

            logger.debug('Birthday')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])DDMMYYYY(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(birthday)
            logger.debug('Birthday Added')

            logger.debug('Partner\'s Name')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])Name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(partners_name)
            logger.debug('Partner\'s First Name Added')

            logger.debug('Partner\'s Nickname')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])nickname(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(partners_nickname)
            logger.debug('Partner\'s Nickname Added')

            logger.debug('Partner\'s Birthday')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])DDMMYYYY(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(partners_birthday)
            logger.debug('Partner\'s Birthday Added')

            logger.debug('Child\'s Name')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(childs_name)
            logger.debug('Child\'s Name Added')

            logger.debug('Child\'s Nickname')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])nickname(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(childs_nickname)
            logger.debug('Child\'s Nickname Added')

            logger.debug('Child\'s Birthday')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])DDMMYYYY(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(childs_birthday)
            logger.debug('Child\'s Birthday Added')

            logger.debug('Pet\'s Name')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(pets_name)
            logger.debug('Pet\'s Name Added')

            logger.debug('Company')
            cupp_child.expect(["[^.?!]*(?<=[.?\s!])name(?=[\s.?!])[^.?!]*[.?!]", pexpect.EOF])
            cupp_child.sendline(company)
            logger.debug('Company Added')

            logger.debug('Keywords')
            cupp_child.expect("> Do you want to add some key words about the victim? Y/[N]:")
            cupp_child.sendline("Y" if keywords else "N")
            logger.debug('Keywords')

            logger.debug('Keywords List')
            cupp_child.expect("> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed:")
            cupp_child.sendline(related_words)
            logger.debug('Keywords List')

            # Other Options. 

            logger.debug('before special_chars')
            cupp_child.expect("> Do you want to add special chars at the end of words? Y/[N]:")
            cupp_child.sendline("Y" if special_chars else "N")
            logger.debug('after special_chars')

            logger.debug('before random_nums')
            cupp_child.expect("> Do you want to add some random numbers at the end of words? Y/[N]:")
            cupp_child.sendline("Y" if random_nums else "N")
            logger.debug('after random_nums')

            logger.debug('before leet')
            cupp_child.expect("> Leet mode? (i.e. leet = 1337) Y/[N]:")
            cupp_child.sendline("Y" if leet else "N")
            logger.debug('after leet')

            logger.debug('before hyperspeed')
            cupp_child.expect("> Hyperspeed Print? (Y/n) :")
            cupp_child.sendline("N")
            logger.debug('after hyperspeed')

            # TODO: Add names of program

            with open('target.txt', 'r') as f:
                lines = f.readlines()
                wordlist = [line.rstrip() for line in lines]
            
            wordlist_json = json.dumps(wordlist)

            ctx.set(wordlist=wordlist_jsons)
            ctx.set(msg="Success")
        except:
            ctx.set(msg="Fail")
    return Cr("", entry=entry())

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
    @remote
    def entry():
        import pexpect, logging, traceback
        cewl_file = "/cewl_file"
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
            ctx.set(msg=f"Error running Wordlist: {e} {traceback.print_exc()}")
    return Cr("", entry=entry())

__lev__ = annot.meta(
    [cewl, cupp_interactive, cewlcupp],
    desc = "CeWL (5.4.9) + CUPP (0.0+20190501)",
    cats = {
        Attck: [
            Attck.PrivilegeEscalation,
            Attck.CredentialAccess,
            Attck.LateralMovement
        ]
    }
)
