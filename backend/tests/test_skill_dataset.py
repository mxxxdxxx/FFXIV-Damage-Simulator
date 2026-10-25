import unittest
from pathlib import Path

from skill_models import SkillDataset


class TestSkillDatasetJSON(unittest.TestCase):

    def test_load_drg_dataset(self):
        """용기사 JSON 데이터가 공통 모델에 맞는지 검증"""

        file_path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "skills"
            / "drg_100_prototype.json"
        )

        dataset = SkillDataset.model_validate_json(
            file_path.read_text(encoding="utf-8")
        )

        self.assertEqual(dataset.job, "DRG")
        self.assertEqual(dataset.level, 100)
        self.assertEqual(dataset.patch, "7.10")
        self.assertEqual(len(dataset.skills), 3)

        self.assertEqual(
            dataset.skills[0].resource_changes[0].amount,
            10
        )

        self.assertEqual(
            dataset.skills[1].combo_from,
            "drg_test_gcd_01"
        )

        self.assertEqual(
            dataset.skills[2].buff.target,
            "party"
        )


if __name__ == "__main__":
    unittest.main()