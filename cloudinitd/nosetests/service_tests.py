import cloudinitd
from cloudinitd.exceptions import ServiceException, APIUsageException
import cloudinitd.nosetests
from cloudinitd.user_api import CloudInitD
import tempfile
import logging

__author__ = 'bresnaha'

import unittest
import os

class ServiceTests(unittest.TestCase):

    def setUp(self):
        self.plan_basedir = cloudinitd.nosetests.g_plans_dir

    def dep_not_found_test(self):
        self.plan_basedir = cloudinitd.nosetests.g_plans_dir
        dir = tempfile.mkdtemp()
        conf_file = self.plan_basedir + "/oneservice/top.conf"
        cb = CloudInitD(dir, conf_file, terminate=False, boot=True, ready=True)
        cb.start()
        ok = False
        try:
            cb.find_dep("notaservice", "whatever")
        except APIUsageException, ex:
            ok = True
        self.assertTrue(ok, "Test should have thrown an exception")
        cb.block_until_complete(poll_period=1.0)

        cb = CloudInitD(dir, db_name=cb.run_name, terminate=True, boot=False, ready=False)
        cb.shutdown()
        cb.block_until_complete(poll_period=1.0)
        fname = cb.get_db_file()
        os.remove(fname)


if __name__ == '__main__':
    unittest.main()
