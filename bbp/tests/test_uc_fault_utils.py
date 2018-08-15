#! /usr/bin/env python
"""
Copyright 2010-2018 University Of Southern California

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import division, print_function

# Import Python modules
import os
import filecmp
import unittest

# Import Broadband modules
import seqnum
import bband_utils

from install_cfg import InstallCfg
import uc_fault_utils

class TestUCFaultUtils(unittest.TestCase):
    """
    Acceptance Test for jbsim.py
    """

    def setUp(self):
        self.install = InstallCfg()
        self.r_srcfile = "test_wh_ucsb.src"
        self.r_faultfile = "ffsp.inp"
        self.r_velmodel = "labasin.vel"
        self.vmodel_name = "LABasin863"
        self.sim_id = int(seqnum.get_seq_num())
        cmd = "mkdir -p %s/%d" % (self.install.A_IN_DATA_DIR, self.sim_id)
        bband_utils.runprog(cmd)
        cmd = "mkdir -p %s/%d" % (self.install.A_TMP_DATA_DIR, self.sim_id)
        bband_utils.runprog(cmd)
        cmd = "mkdir -p %s/%d" % (self.install.A_OUT_DATA_DIR, self.sim_id)
        bband_utils.runprog(cmd)
        cmd = "mkdir -p %s/%d" % (self.install.A_OUT_LOG_DIR, self.sim_id)
        bband_utils.runprog(cmd)
        cmd = "cp %s/ucsb/%s %s/%d/." % (self.install.A_TEST_REF_DIR,
                                         self.r_srcfile,
                                         self.install.A_IN_DATA_DIR,
                                         self.sim_id)
        bband_utils.runprog(cmd)

    def test_uc_fault_utils(self):
        """
        Test UCSB fault utilities
        """
        indir = os.path.join(self.install.A_IN_DATA_DIR, str(self.sim_id))
        tmpdir = os.path.join(self.install.A_TMP_DATA_DIR, str(self.sim_id))
        a_src_file = os.path.join(indir, self.r_srcfile)
        a_ffsp_inp = os.path.join(tmpdir, self.r_faultfile)

        # Create ffsp.inp file
        uc_fault_utils.uc_create_ffsp_inp(a_ffsp_inp, a_src_file,
                                          self.vmodel_name)
        ref_file = os.path.join(self.install.A_TEST_REF_DIR,
                                "ucsb", self.r_faultfile)
        self.failIf(filecmp.cmp(ref_file, a_ffsp_inp) == False,
                    "output fault file does not match reference fault file")

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestUCFaultUtils)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
