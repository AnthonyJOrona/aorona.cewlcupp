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

@annot.meta(
    desc="Dictionary: cupp -w <file>",
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
async def Wordlist(
    url: str =  '',
    depth: int = 1,
    min_length: int = 3,
    offsite: bool = False,
    word_list: File = None,
    concatenate: bool = False,
    special_chars: bool = False,
    random_nums: bool = False,
    leet: bool = False,
) -> Cr:
    """
        input: url
        * Use CeWL to generate a word list
        * If desired, add additional word list
        * Then, use CUPP to profile combined word list
    """
    @remote
    def entry():
        import pexpect, logging
        cewl_file = 'cewl_file'
        try:
            logging.basicConfig()
            logger = logging.getLogger("lev")
            logger.setLevel(logging.DEBUG)
            options_str = f'-k -m{min_length} -d{depth} -w {cewl_file}' 
            if offsite:
                options_str = f'{options_str} -o'

            logger.debug('Formatted CeWL options string')
            cewl_child = pexpect.spawn(f'cewl {options_str} {url}')
            logger.debug('Running cewl..')
            while True:
                try:
                    cewl_child.read_nonblocking()
                except Exception:
                    break
            if cewl_child.isalive():
                cewl_child.wait()
            logger.debug('CeWL completed..')

            logger.debug('Spawning CUPP..')
            cupp_child = pexpect.spawn(f'cupp -w {cewl_file}')
            logger.debug('CUPP spawned')

            logger.debug('before concatenate')
            cupp_child.expect("> Do you want to concatenate all words from wordlist? Y/[N]:")
            cupp_child.sendline("Y" if concatenate else "N")
            logger.debug('concatenated')

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
            ctx.set(msg="Success")
        except:
            ctx.set(msg="Fail")
    return Cr("6043f89f3f29", entry=entry(), files={"/word_list": word_list})

__lev__ = annot.meta(
    [Wordlist],
    desc = "CeWL (5.4.9) + CUPP (0.0+20190501)",
    cats = {
        Attck: [
            Attck.PrivilegeEscalation,
            Attck.CredentialAccess,
            Attck.LateralMovement
        ]
    }
)
