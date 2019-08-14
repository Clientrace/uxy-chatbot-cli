"""
Authored by Kim Clarence Penaflor
08/14//2019
version 0.0.2
Documented via reST

Project uxy cli setup command manager module
"""
import os
import hashlib


class ChangeControl:


  verbosity = False

  def __init__(self, path, config):
    """
    """
    self.path = path
    self.config = config
    self.verbosity = config['verbosity']

  @classmethod
  def _log(cls, msg):
    """
    Log System Process
    :param msg: string msg to log
    :type msg: string
    """
    if( cls.verbosity ):
      print('[Change Control]: ' + msg)

  @staticmethod
  def _get_checksum(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
      for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


  def generate_filechecksums(self):
    """
    Generate checksums for all the file in path
    """
    ChangeControl._log('Generating file checksums...')
    fileChecksums = {}
    for root, dirs, files in os.walk(self.path):
      for file in files:
        fDir = os.path.join(root, file)
        fileChecksums[fDir] = ChangeControl._get_checksum(fDir)

    return fileChecksums

  def compare_diff(self,path, oldFileChecksums):
    newChecksums = {}
    curChecksums = ChangeControl.generate_filechecksums(self)
    filesDiff = {}
    for filedir in curChecksums:
      if( filedir not in oldFileChecksums ):
        ChangeControl._log('+ New File Detected ['+filedir+']')
        filesDiff[filedir] = 'created'
        newChecksums[filedir] = ChangeControl._get_checksum(filedir)
      else:
        if( curChecksums[filedir] != oldFileChecksums[filedir] ):
          ChangeControl._log('+ File Modified ['+filedir+']')

        newChecksums[filedir] = ChangeControl._get_checksum(filedir)
        curChecksums.pop(filedir)





