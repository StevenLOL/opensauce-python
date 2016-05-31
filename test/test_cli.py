import filecmp
import os
from shutil import copytree
from subprocess import Popen, PIPE

from opensauce.__main__ import CLI

from test.support import TestCase, data_file_path

class TestOldCLI(TestCase):

    def test_default_setup(self):
        tmp = self.tmpdir()
        def d(fn):
            return os.path.join(tmp, fn)
        os.mkdir(d('output'))
        copytree('defaults', d('defaults'))
        p = Popen(['python', 'opensauce/process.py',
                        '-i', d('defaults/sounds'),
                        '-o', d('output'),
                        '-s', d('defaults/settings/default.csv'),
                        '-p', d('defaults/parameters/default.csv'),
                        ],
                    stdout=PIPE,
                    )
        # For now, just ignore the output.
        p.stdout.read()
        rc = p.wait()
        self.assertEqual(rc, 0)
        self.assertTrue(filecmp.cmp(d('defaults/sounds/cant_c5_19a.f0'),
                                    data_file_path('cant_c5_19a.f0')))

class TestCLI(TestCase):

    def test_m(self):
        here = os.path.dirname(os.path.dirname(__file__))
        here = here if here else '.'
        p = Popen(['python', '-m', 'opensauce'], cwd=here,
                  stdout=PIPE,
                  stderr=PIPE,
                  universal_newlines=True,
                  )
        out, err = p.communicate()
        self.assertEqual(out, '')
        self.assertIn('too few arguments', err)
        self.assertEqual(p.returncode, 2)

    def test_snackF0(self):
        tmp = self.tmpdir()
        outfile = os.path.join(tmp, 'output.txt')
        CLI(['--measurements', 'snackF0',
             '-o', outfile,
             data_file_path('beijing_f3_50_a.wav')]
            ).process()
        # XXX eventually we should test against the voicesauce data instead,
        # when that is working.
        with open(outfile) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 589)
        self.assertEqual(len([x for x in lines if 'C1' in x]), 101)
        self.assertEqual(len([x for x in lines if 'V1' in x]), 209)
        self.assertEqual(len([x for x in lines if 'C2' in x]), 119)
        self.assertEqual(len([x for x in lines if 'V2' in x]), 159)

    def test_ignore_label(self):
        tmp = self.tmpdir()
        outfile = os.path.join(tmp, 'output.txt')
        CLI(['--measurements', 'snackF0',
             '-o', outfile,
             '--ignore-label', 'C2',
             data_file_path('beijing_f3_50_a.wav')]
            ).process()
        with open(outfile) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 589 - 119)
        self.assertEqual(len([x for x in lines if 'C1' in x]), 101)
        self.assertEqual(len([x for x in lines if 'V1' in x]), 209)
        self.assertEqual(len([x for x in lines if 'C2' in x]), 0)
        self.assertEqual(len([x for x in lines if 'V2' in x]), 159)

    def test_ignore_multiple_labels(self):
        tmp = self.tmpdir()
        outfile = os.path.join(tmp, 'output.txt')
        CLI(['--measurements', 'snackF0',
             '-o', outfile,
             '--ignore-label', 'C2',
             '--ignore-label', 'V1',
             data_file_path('beijing_f3_50_a.wav')]
            ).process()
        with open(outfile) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 589 - 119 - 209)
        self.assertEqual(len([x for x in lines if 'C1' in x]), 101)
        self.assertEqual(len([x for x in lines if 'V1' in x]), 0)
        self.assertEqual(len([x for x in lines if 'C2' in x]), 0)
        self.assertEqual(len([x for x in lines if 'V2' in x]), 159)

    def test_include_empty_lables(self):
        tmp = self.tmpdir()
        outfile = os.path.join(tmp, 'output.txt')
        CLI(['--measurements', 'snackF0',
             '-o', outfile,
             '--include-empty-labels',
             data_file_path('beijing_f3_50_a.wav')]
            ).process()
        with open(outfile) as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 2347)
        self.assertEqual(len([x for x in lines if 'C1' in x]), 101)

    def test_no_textgrid(self):
        tmp = self.tmpdir()
        outfile = os.path.join(tmp, 'output.txt')
        CLI(['--measurements', 'snackF0',
             '-o', outfile,
             '--no-textgrid',
             data_file_path('beijing_f3_50_a.wav')]
            ).process()
        with open(outfile) as f:
            lines = f.readlines()
        # The textgrid output has a repeated frame offset at the end and
        # beginning of each block.  Since there are six blocks (including the
        # ones with blank labels) in this sample, there are five more records
        # in the --include-empty-labels case above than there are here, where
        # we have no repeated frames.
        self.assertEqual(len(lines), 2342)
        self.assertEqual(len([x for x in lines if 'C1' in x]), 0)
        self.assertEqual(len([x for x in lines if 'V1' in x]), 0)
        self.assertEqual(len([x for x in lines if 'C2' in x]), 0)
        self.assertEqual(len([x for x in lines if 'V2' in x]), 0)
