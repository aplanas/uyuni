# -*- coding: utf-8 -*-
#
# Copyright (c) 2008--2010 Red Hat, Inc.
# Copyright (c) 2010-2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
# 
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation. 
#
import os
import re
import shutil
import subprocess
import sys
import xml.etree.cElementTree as etree

import urlgrabber
from urlgrabber.grabber import URLGrabber, URLGrabError, default_grabber
from rpmUtils.transaction import initReadOnlyTransaction
import yum
from yum import misc, Errors
from yum.update_md import UpdateMetadata
from yum.i18n import to_unicode

from spacewalk.common import rhnLog
from spacewalk.satellite_tools.reposync import ContentPackage, ChannelException, ChannelTimeoutException

CACHE_DIR = '/var/cache/rhn/reposync/'
class YumWarnings:
    def write(self, s):
        pass
    def disable(self):
        self.saved_stdout = sys.stdout
        sys.stdout = self
    def restore(self):
        sys.stdout = self.saved_stdout

class ContentSource:
    def __init__(self, url, name, insecure=False, quiet=False, interactive=True,
                 proxy=None, proxy_user=None, proxy_pass=None):
        self.url = url
        self.name = name
        self.insecure = insecure
        self.quiet = quiet
        self.interactive = interactive
        self.proxy = proxy
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self._clean_cache(CACHE_DIR + name)

        repo = yum.yumRepo.YumRepository(self.name)
        self.repo = repo
        self.setup_repo(repo)
        self.sack = None
        self.setup_repo(repo)

    def setup_repo(self, repo):
        """Fetch repository metadata"""
        repo.proxy = self.proxy
        repo.proxy_username = self.proxy_user
        repo.proxy_password = self.proxy_pass
        repo.cache = 0
        repo.metadata_expire = 0
        repo.mirrorlist = self.url
        repo.baseurl = [self.url]
        repo.basecachedir = CACHE_DIR
        if self.insecure:
            repo.repo_gpgcheck = False
        else:
            repo.repo_gpgcheck = True
        warnings = YumWarnings()
        warnings.disable()
        repo.baseurlSetup()
        warnings.restore()
        for burl in repo.baseurl:
            repo.gpgkey = [burl + '/repodata/repomd.xml.key']
 
        repo.setup(False, None, gpg_import_func=self.getKeyForRepo,
                   confirm_func=self.askImportKey)
        self.initgpgdir( repo.gpgdir )
        sack = repo.getPackageSack()

        try:
            sack.populate(repo, 'metadata', None, 0)
        except Errors.RepoError,e :
            if "No more mirrors" in str(e):
                reqFile = re.search('failure:\s+(.+)\s+from',
                                    str(e)).groups()[0]
                raise ChannelTimeoutException("Retrieving '%s' failed: File not found in repository '%s'" % (reqFile, repo))
            else:
                raise
        self.sack = sack

    def list_packages(self):
        """ list packages"""
        list = self.sack.returnPackages()
        to_return = []
        for pack in list:
            if pack.arch == 'src':
                continue
            new_pack = ContentPackage()
            new_pack.setNVREA(pack.name, pack.version, pack.release, 
                              pack.epoch, pack.arch)
            new_pack.unique_id = pack
            for cs in pack.checksums:
                new_pack.checksums[cs[0]] = cs[1]
            to_return.append(new_pack)
        return to_return

    def get_package(self, package):
        """ get package """
        check = (self.verify_pkg, (package.unique_id ,1), {})
        return self.repo.getPackage(package.unique_id, checkfunc=check)

    def verify_pkg(self, fo, pkg, fail):
        return pkg.verifyLocalPkg()

    def _clean_cache(self, directory):
        shutil.rmtree(directory, True)

    def get_updates(self):
        if 'updateinfo' in self.repo.repoXML.repoData:
            um = UpdateMetadata()
            try:
                um.add(self.repo, all=True)
            except Errors.NoMoreMirrorsRepoError:
                raise ChannelTimeoutException('Retrieving updateinfo failed: File not found')
            return ('updateinfo', um.notices)

        elif 'patches' in self.repo.repoXML.repoData:
            patches_path = self.repo.retrieveMD('patches')
            os.mkdir(os.path.join(self.repo.cachedir, 'patches'))

            # parse the patches.xml file and download every patch-xxx.xml file
            notices = []
            for patch in etree.parse(patches_path).getroot():
                (checksum_elem, location_elem) = patch
                relative = location_elem.get('href')
                checksum_type = checksum_elem.get('type')
                checksum = checksum_elem.text
                filename = os.path.join(self.repo.cachedir, 'patches',
                                        os.path.basename(relative))
                try:
                    self.repo.grab.urlgrab(misc.to_utf8(relative),
                                           filename,
                                           checkfunc=(self.patches_checksum_func,
                                                      (checksum_type, checksum),
                                                      {}))
                except URLGrabError, e:
                    self.error_msg("Failed to download %s. [Errno %i] %s" %
                                   (relative, e.errno, e.strerror))
                    continue

                try:
                    notices.append(etree.parse(filename).getroot())
                except SyntaxError, e:
                    self.error_msg("Could not parse %s. "
                                   "The file is not a valid XML document. %s" %
                                   (filename, e.msg))
                    continue

            return ('patches', notices)
        else:
            return ('', [])

    def patches_checksum_func(self, callback_obj, checksum_type, checksum):
        """Simple function to checksum patches for urlgrabber

        """
        import types
        # this is ugly code copy&pasted from yumRepo.YumRepository._checkMD
        if type(callback_obj) == types.InstanceType: # urlgrabber check
            filename = callback_obj.filename
        else:
            filename = callback_obj

        local_checksum = self.repo._checksum(checksum_type, filename)

        if local_checksum == checksum:
            return 1
        else:
            raise URLGrabError(-1, 'Metadata file does not match checksum')
          

    def getKeyForRepo(self, repo, callback=None):
        """
        Retrieve a key for a repository If needed, prompt for if the key should
        be imported using callback

        @param repo: Repository object to retrieve the key of.
        @param callback: Callback function to use for asking for verification
                          of a key. Takes a dictionary of key info.
        """
        keyurls = []
        if self.interactive:
            keyurls = repo.gpgkey
        key_installed = False
        for keyurl in keyurls:
            keys = self._retrievePublicKey(keyurl, repo)
            for info in keys:
                # Check if key is already installed
                if info['keyid'] in misc.return_keyids_from_pubring(repo.gpgdir):
                    continue

                # Try installing/updating GPG key
                rc = False
                if callback:
                    rc = callback({'repo':repo, 'userid':info['userid'],
                                   'hexkeyid':info['hexkeyid'], 'keyurl':keyurl,
                                   'fingerprint':info['fingerprint'],
                                   'timestamp':info['timestamp']})


                if not rc:
                    raise ChannelException, "GPG key(0x%s '%s') for repo %s rejected" % (info['hexkeyid'],info['userid'],repo)

                # Import the key
                result = misc.import_key_to_pubring(info['raw_key'], info['hexkeyid'], gpgdir=repo.gpgdir)
                if not result:
                    raise ChannelException, 'Key import failed'
                result = self.import_key_to_rpmdb(info['raw_key'], info['hexkeyid'], gpgdir=repo.gpgdir)
                if not result:
                    raise ChannelException, 'Key import failed'

                key_installed = True

        if not key_installed:
            raise ChannelException, 'The GPG keys listed for the "%s" repository are ' \
                                    'already installed but they are not correct.\n' \
                                    'Check that the correct key URLs are configured for ' \
                                    'this repository.' % (repo)


    def _retrievePublicKey(self, keyurl, repo=None):
        """
        Retrieve a key file
        @param keyurl: url to the key to retrieve
        Returns a list of dicts with all the keyinfo
        """
        key_installed = False

        # Go get the GPG key from the given URL
        try:
            url = misc.to_utf8(keyurl)
            if repo is None:
                rawkey = urlgrabber.urlread(url, limit=9999)
            else:
                #  If we have a repo. use the proxy etc. configuration for it.
                # In theory we have a global proxy config. too, but meh...
                # external callers should just update.
                ug = URLGrabber(bandwidth = repo.bandwidth,
                                retry = repo.retries,
                                throttle = repo.throttle,
                                progress_obj = repo.callback,
                                proxies=repo.proxy_dict)
                ug.opts.user_agent = default_grabber.opts.user_agent
                rawkey = ug.urlread(url, text=repo.id + "/gpgkey")

        except urlgrabber.grabber.URLGrabError, e:
            raise ChannelException('GPG key retrieval failed: ' +
                                    to_unicode(str(e)))
        # Parse the key
        keys_info = misc.getgpgkeyinfo(rawkey, multiple=True)
        keys = []
        for keyinfo in keys_info:
            thiskey = {}
            for info in ('keyid', 'timestamp', 'userid',
                         'fingerprint', 'raw_key'):
                if not keyinfo.has_key(info):
                    raise ChannelException, \
                      'GPG key parsing failed: key does not have value %s' % info
                thiskey[info] = keyinfo[info]
            thiskey['keyid'] = str("%16x" % (thiskey['keyid'] & 0xffffffffffffffffL)).upper()
            thiskey['hexkeyid'] = misc.keyIdToRPMVer(keyinfo['keyid']).upper()
            keys.append(thiskey)

        return keys

    def askImportKey(self, d ):
        if self.interactive:
          print 'Do you want to import the GPG key 0x%s "%s" from %s? [y/n]:' % (d['hexkeyid'], to_unicode(d['userid']), d['keyurl'],)
          yn = sys.stdin.readline()
          yn = yn.strip()

          if yn in ['y', 'Y', 'j', 'J']:
            return True

        return False

    def initgpgdir(self, gpgdir):
      if not os.path.exists(gpgdir):
        os.makedirs(gpgdir)

      ts = initReadOnlyTransaction("/")
      for hdr in ts.dbMatch('name', 'gpg-pubkey'):
        if hdr['description'] != "":
          misc.import_key_to_pubring(hdr['description'], hdr['version'], gpgdir=gpgdir)

    def import_key_to_rpmdb(self, raw, keyid, gpgdir):
      if not os.path.exists(gpgdir):
        os.makedirs(gpgdir)
      tmpfile = os.path.join(gpgdir, keyid)
      fp = open(tmpfile, 'w')
      fp.write(raw)
      fp.close()
      cmd = ['/bin/rpm', '--import', tmpfile]
      p = subprocess.Popen(cmd)
      sts = os.waitpid(p.pid, 0)[1]
      os.remove(tmpfile)
      if sts == 0:
        return True
      return False

    def error_msg(self, message):
        rhnLog.log_clean(0, message)
        if not self.quiet:
            sys.stderr.write(str(message) + "\n")
