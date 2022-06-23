import levrt
from lev.aorona.cewlcupp import CeWLCUPP

async def main():
    print("""
    ----------------------
    Testing CeWL + CUPP
    ----------------------
    """)
    doc = await CeWLCUPP.Wordlist(
        url = 'https://levi.zone/',
        depth = 1,
        min_length = 5,
        offsite = False,
        word_list = None,
        concatenate = False,
        special_chars = False,
        random_nums = False,
        leet = False,
    )

if __name__ == "__main__":
    levrt.run(main())
