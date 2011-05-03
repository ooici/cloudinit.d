import cloudinitd
import cloudinitd.nosetests
from cloudinitd.user_api import CloudInitD
import tempfile
import logging

__author__ = 'bresnaha'

import unittest
import os

class SingleVMTests(unittest.TestCase):

    def setUp(self):
        self.plan_basedir = cloudinitd.nosetests.g_plans_dir

    def _get_running_vms(self):

        key = None
        secret = None
        host = None
        port = None
        try:
            key = os.environ['CLOUDBOOT_IAAS_ACCESS_KEY']
            secret = os.environ['CLOUDBOOT_IAAS_SECRET_KEY']
            host = os.environ['CLOUDBOOT_IAAS_HOSTNAME']
            port = os.environ['CLOUDBOOT_IAAS_PORT']
        except:
            pass

        # XXX this test may fail for nimbus
        con = cloudinitd.cb_iaas.iaas_get_con(None, key=key, secret=secret, iaashostname=host, iaasport=port)
        i_list = con.get_all_instances()
        return i_list

    def test_manyservices_one_vm_simple(self):
        self.plan_basedir = cloudinitd.nosetests.g_plans_dir
        dir = tempfile.mkdtemp()
        conf_file = self.plan_basedir + "/singlevmmanyservice/top.conf"
        cb = CloudInitD(dir, conf_file, terminate=False, boot=True, ready=True)
        cb.start()
        cb.block_until_complete(poll_period=1.0)
        cb = CloudInitD(dir, db_name=cb.run_name, terminate=True, boot=False, ready=False)
        cb.shutdown()
        cb.block_until_complete(poll_period=1.0)


    def test_only_one_launched(self):
        ilist_1 = self._get_running_vms()
        count1 = len(ilist_1)
        self.plan_basedir = cloudinitd.nosetests.g_plans_dir
        dir = tempfile.mkdtemp()
        conf_file = self.plan_basedir + "/singlevmmanyservice/top.conf"
        cb = CloudInitD(dir, conf_file, terminate=False, boot=True, ready=True)
        cb.start()
        cb.block_until_complete(poll_period=1.0)

        ilist_2 = self._get_running_vms()
        count2 = len(ilist_2)

        self.assertEqual(count1, count2 - 1, "there should be exactly 1 more VM in count 2: %d %d" % (count1, count2))

        cb = CloudInitD(dir, db_name=cb.run_name, terminate=True, boot=False, ready=False)
        cb.shutdown()
        cb.block_until_complete(poll_period=1.0)


if __name__ == '__main__':
    unittest.main()