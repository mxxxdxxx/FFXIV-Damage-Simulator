
import unittest

from skill_models import Skill

from skill_localization import (
    get_korean_skill_name,
    load_korean_skill_names,
)


class TestSkillLocalization(unittest.TestCase):

    def test_true_thrust(self):
        """True Thrust 한국어 명칭 테스트"""

        name = get_korean_skill_name(
            75,
            patch="7.57"
        )

        self.assertEqual(name, "직선 찌르기")

    def test_vorpal_thrust(self):
        """Vorpal Thrust 한국어 명칭 테스트"""

        name = get_korean_skill_name(
            78,
            patch="7.57"
        )

        self.assertEqual(name, "사선 찌르기")

    def test_string_action_id(self):
        """문자열 Action ID 조회 테스트"""

        name = get_korean_skill_name(
            "75",
            patch="7.57"
        )

        self.assertEqual(name, "직선 찌르기")

    def test_unknown_action(self):
        """등록되지 않은 기술 조회 테스트"""

        name = get_korean_skill_name(
            999999,
            patch="7.57"
        )

        self.assertIsNone(name)

    def test_unknown_patch(self):
        """매핑 파일이 없는 패치 조회 테스트"""

        names = load_korean_skill_names("0.00")

        self.assertEqual(names, {})

    def test_skill_with_korean_name(self):
        """Skill 모델의 한국어 이름 저장 테스트"""

        skill = Skill(
            id="75",
            name="True Thrust",
            name_ko=get_korean_skill_name(
                75,
                patch="7.57"
            ),
            gcd_type="GCD",
            required_level=1,
            potency=230,
            base_recast_seconds=2.5
        )

        self.assertEqual(skill.name, "True Thrust")
        self.assertEqual(skill.name_ko, "직선 찌르기")


if __name__ == "__main__":
    unittest.main()
