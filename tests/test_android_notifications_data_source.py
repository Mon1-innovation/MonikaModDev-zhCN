from pathlib import Path
import ast
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "Monika After Story" / "game"
DATA_FILE = GAME_DIR / "zz_android_notifications.rpy"


def extract_init_python_block(source, label):
    lines = source.splitlines()
    start = next(
        index
        for index, line in enumerate(lines)
        if line.startswith(label)
    ) + 1
    end = next(
        index
        for index, line in enumerate(lines[start:], start)
        if line.startswith("init ")
    )
    return lines[start:end]


class AndroidNotificationsDataSourceTests(unittest.TestCase):

    def test_notification_data_block_is_valid_python(self):
        source = DATA_FILE.read_text(encoding="utf-8")
        block_lines = extract_init_python_block(
            source,
            "init -10 python in mas_android_notifs:"
        )

        for line in block_lines:
            if line:
                self.assertTrue(
                    line.startswith("    "),
                    "Unindented line in init python block: {!r}".format(line)
                )

        ast.parse(textwrap.dedent("\n".join(block_lines)))

    def test_notification_data_uses_expected_category_keys(self):
        source = DATA_FILE.read_text(encoding="utf-8")
        block = textwrap.dedent("\n".join(extract_init_python_block(
            source,
            "init -10 python in mas_android_notifs:"
        )))
        module = ast.parse(block)
        data_assign = next(
            node for node in ast.walk(module)
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "data" for target in node.targets)
        )
        data = ast.literal_eval(data_assign.value)

        expected_categories = {
            "school",
            "work",
            "sleep",
            "shopping",
            "chores",
            "workout",
            "play_game",
            "friends",
            "morning_food",
            "noon_food",
            "evening_food",
            "generic_quit",
            "farewell_general",
            "calendar_event",
        }

        for affection in ("normal", "happy", "affectionate", "enamored", "love"):
            categories = set(data[affection])
            self.assertTrue(expected_categories.issubset(categories), affection)
            self.assertNotIn("normal", categories)


if __name__ == "__main__":
    unittest.main()
