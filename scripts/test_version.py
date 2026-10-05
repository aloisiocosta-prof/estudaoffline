import unittest
from next_version import next_version
class VersionTests(unittest.TestCase):
 def test_feature(self):self.assertEqual(next_version('v0.1.0',['feat: backup']),'0.2.0')
 def test_fix(self):self.assertEqual(next_version('v0.1.0',['fix: cache']),'0.1.1')
 def test_breaking(self):self.assertEqual(next_version('v0.1.0',['feat!: schema']),'1.0.0')
 def test_none(self):self.assertIsNone(next_version('v0.1.0',['docs: update']))
if __name__=='__main__':unittest.main()
