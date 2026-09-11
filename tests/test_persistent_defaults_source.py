from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS_RPY = ROOT / "Monika After Story" / "game" / "definitions.rpy"


class PersistentDefaultsSourceTests(unittest.TestCase):

    def test_ever_won_persistent_data_is_coerced_to_defaultdict(self):
        source = DEFINITIONS_RPY.read_text(encoding="utf-8")

        default_index = source.index(
            "default persistent._mas_ever_won = collections.defaultdict(bool)"
        )
        fix_index = source.index(
            "        persistent._mas_ever_won = collections.defaultdict(",
            default_index + 1
        )
        deprecated_comment_index = source.index(
            "# TODO: Delete this as depricated",
            fix_index
        )
        fix_block = source[default_index:deprecated_comment_index]

        self.assertGreater(fix_index, default_index)
        self.assertIn("persistent._mas_ever_won.default_factory is not bool", source)
        self.assertIn("dict(persistent._mas_ever_won)", fix_block)


if __name__ == "__main__":
    unittest.main()
