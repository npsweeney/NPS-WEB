import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sync_publications as sync


class PublicationSyncTests(unittest.TestCase):
    def test_build_stamp_and_stale_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in sync.INPUTS + sync.OUTPUTS:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"original")
            state = root / "cv/publication-build.json"
            with patch.object(sync, "ROOT", root), patch.object(sync, "STATE", state), patch.object(sync, "build_json") as generate:
                with self.assertRaises(SystemExit):
                    sync.check()
                state.write_text(json.dumps(sync.hashes()))
                sync.check()
                generate.assert_called_once()
                for name in sync.INPUTS + sync.OUTPUTS:
                    with self.subTest(file=name):
                        (root / name).write_bytes(b"changed")
                        with self.assertRaises(SystemExit):
                            sync.check()
                        (root / name).write_bytes(b"original")


if __name__ == "__main__":
    unittest.main()
