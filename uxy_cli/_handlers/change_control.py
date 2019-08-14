"""
Authored by Kim Clarence Penaflor
08/14//2019
version 0.0.2
Documented via reST

Project uxy cli setup command manager module
"""

import os
import json
import hashlib


class ChangeControl:


  verbosity = False

  def __init__(self, path, config):
    """
    Initialize change control files dir
    :param path: source files
    :type path: string
    :param config: application configuration
    :type config: string
    """
    self.path = path
    self.config = config
    ChangeControl.verbosity = config['verbosity']

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

  def compare_diff(self, path, oldFilesChecksums):
    """
    Compare checksums difference
    :param path: Directory path
    :type path: string
    :param oldFilesChecksums: previous files checksums
    :type oldFilesChecksums: string
    :return: new checksums and status if changed
    :rtype: dictionary and boolean
    """

    changeStatus = False
    newChecksums = {}
    curChecksums = ChangeControl.generate_filechecksums(self)
    # New to old comparison
    for filedir in curChecksums:
      if( filedir not in oldFilesChecksums ):
        changeStatus = True
        ChangeControl._log('+ New File Detected '+filedir+'')
        newChecksums[filedir] = ChangeControl._get_checksum(filedir)
      else:
        if( curChecksums[filedir] != oldFilesChecksums[filedir] ):
          changeStatus = True
          ChangeControl._log('+ File Modified '+filedir+'')

        newChecksums[filedir] = ChangeControl._get_checksum(filedir)
        oldFilesChecksums.pop(filedir)

    # Old to new comparison
    for filedir in oldFilesChecksums:
      if( filedir not in curChecksums ):
        changeStatus = True
        ChangeControl._log('- File removed: '+filedir+'')

    return newChecksums, changeStatus






