from re import S
import sys
from uuid import SafeUUID
sys.path.append("/var/www/backend")
from pool import tasks

sample_hash = "fbc5ab623d6510e372febc57fe03535b"
tasks.get_IPC2.apply_async([sample_hash])
tasks.get_CellPLoc.apply_async([sample_hash])
tasks.get_JPred.apply_async([sample_hash])
tasks.get_DeepTMHMM.apply_async([sample_hash])
