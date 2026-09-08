"""Verify the package checker against isolated valid and invalid packages."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_REL = Path("plugins/lazyest-qa/skills/lazyest-qa")


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "package"
        shutil.copytree(ROOT, self.root,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "dist"))
        self.skill = self.root / SKILL_REL

    def validate(self):
        return subprocess.run([sys.executable, str(self.root / "scripts/validate.py")],
                              cwd=self.root, capture_output=True, text=True, timeout=15)

    def assert_rejected(self, expected):
        result = self.validate()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(expected, result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def set_frontmatter(self, content):
        path = self.skill / "SKILL.md"
        _, _, body = path.read_text(encoding="utf-8").split("---", 2)
        path.write_text(f"---\n{content}\n---{body}", encoding="utf-8")

    def test_current_package_is_valid(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_malformed_skill_yaml_is_rejected(self):
        self.set_frontmatter("name: lazyest-qa\ndescription: valid text\nmetadata: [unclosed")
        self.assert_rejected("Invalid YAML in SKILL.md frontmatter")

    def test_skill_required_values_are_nonempty_strings(self):
        for description in ("[]", "false", "null", "42", "'   '"):
            with self.subTest(description=description):
                self.set_frontmatter(f"name: lazyest-qa\ndescription: {description}")
                self.assert_rejected("SKILL.md.description must be a nonempty string")

    def test_skill_name_type_and_identity_are_checked(self):
        for name in ("[]", "another-skill"):
            with self.subTest(name=name):
                self.set_frontmatter(f"name: {name}\ndescription: Valid description")
                self.assert_rejected("Skill name must match its directory")

    def test_nonmapping_yaml_is_rejected(self):
        self.set_frontmatter("- name: lazyest-qa\n- description: Valid description")
        self.assert_rejected("SKILL.md frontmatter must contain a YAML mapping")

    def test_malformed_ui_yaml_is_rejected(self):
        (self.skill / "agents/openai.yaml").write_text("interface: [unclosed\n", encoding="utf-8")
        self.assert_rejected("Invalid YAML in agents/openai.yaml")

    def test_missing_and_incorrect_ui_field_types_are_rejected(self):
        path = self.skill / "agents/openai.yaml"
        valid = path.read_text(encoding="utf-8")
        for field in ("display_name", "short_description", "default_prompt"):
            original = next(line for line in valid.splitlines(True)
                            if line.startswith(f"  {field}:"))
            for replacement in ("", f"  {field}: []\n", f"  {field}: false\n"):
                with self.subTest(field=field, replacement=replacement):
                    path.write_text(valid.replace(original, replacement), encoding="utf-8")
                    self.assert_rejected(f"interface.{field} must be a nonempty string")

    def test_incorrect_interface_type_is_rejected(self):
        (self.skill / "agents/openai.yaml").write_text("interface: []\n", encoding="utf-8")
        self.assert_rejected("interface must be a mapping")

    def test_unreferenced_reference_count_is_not_an_acceptance_gate(self):
        (self.skill / "references/another-topic.md").write_text("Additional local topic.\n",
                                                                 encoding="utf-8")
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_link_target_is_rejected(self):
        with (self.skill / "SKILL.md").open("a", encoding="utf-8") as document:
            document.write("\n[Needed guide](references/missing-guide.md)\n")
        self.assert_rejected("Broken link:")


if __name__ == "__main__":
    unittest.main()
