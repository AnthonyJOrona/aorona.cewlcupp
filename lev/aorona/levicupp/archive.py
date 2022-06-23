# @annot.meta(
#     desc="Dictionary: cupp -l",
#     params=[],
#     cats=[Attck.PrivilegeEscalation, Attck.CredentialAccess, Attck.LateralMovement],
# )
# def Funet() -> Cr:
#     """
#         -l Download huge wordlists from repository
#     """
#     @remote
#     def entry():
#         import sys, subprocess, logging, os, json
#         try:
#             logger = init_logger(logging)
#             subprocess.run('cupp -l')
#             # write_output_file()
#             ctx.set(msg="generated x")
#         except:
#             ctx.set(msg="Fail")
#     return Cr("2746dc3d57b0", entry=entry())

# @annot.meta(
#     desc="Dictionary: cupp -a",
#     params=[],
#     cats=[Attck.PrivilegeEscalation, Attck.CredentialAccess, Attck.LateralMovement],
# )
# def Alecto() -> Cr:
#     """
#         -a Parse default usernames and passwords directly from Alecto DB.  Project Alecto uses
#         purified databases of Phenoelit and CIRT which where merged and enhanced.
#     """
#     @remote
#     def entry():
#         import sys, subprocess, logging, os, json
#         try:
#             logger = init_logger(logging)
#             subprocess.run('cupp -a')
#             # write_output_file()
#             ctx.set(msg="generated x")
#         except:
#             ctx.set(msg="Fail")
#     return Cr("2746dc3d57b0", entry=entry())

# @annot.meta(
#     desc="Dictionary: cupp -w <file>",
#     params=[annot.Param("filepath", "absolute path")],
#     cats=[Attck.PrivilegeEscalation, Attck.CredentialAccess, Attck.LateralMovement],
# )
# def Raw(argv:list[str]) -> Cr:
#     """
#     """
#     @remote
#     def entry(argv):
#         import sys, subprocess, logging, os, json
#         try:
#             logger = init_logger(logging)
#             subprocess.run(['/usr/bin/cupp', *argv], text=True)
#             # write_output_file()
#             ctx.set(msg="generated x")
#         except:
#             ctx.set(msg="Fail")
#     return Cr("2746dc3d57b0", entry=entry())

# __lev__ = annot.meta(
#     [Dictionary, Funet, Alecto, Raw],
#     desc = "CUPP - Common User Passwords Profiler",
#     cats = {
#         Attck: [
#             Attck.PrivilegeEscalation,
#             Attck.CredentialAccess,
#             Attck.LateralMovement
#         ]
#     }
# )
