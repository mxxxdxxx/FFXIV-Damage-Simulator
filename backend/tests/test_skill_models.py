
import unittest

from pydantic import ValidationError

from skill_models import (
    Skill,
    SkillDataset,
    ResourceChange,
    BuffEffect,
)


class TestSkillModels(unittest.TestCase):

    def test_gcd_skill(self):
        """GCD 기술 생성 테스트"""

        skill = Skill(
            id="test_gcd",
            name="테스트 GCD",
            gcd_type="GCD",
            required_level=1,
            potency=300,
            base_recast_seconds=2.5,
        )

        self.assertEqual(skill.gcd_type, "GCD")
        self.assertEqual(skill.potency, 300)

    def test_ogcd_skill(self):
        """oGCD 기술 생성 테스트"""

        skill = Skill(
            id="test_ogcd",
            name="테스트 oGCD",
            gcd_type="oGCD",
            required_level=30,
            potency=250,
            cooldown_seconds=30,
        )

        self.assertEqual(skill.gcd_type, "oGCD")
        self.assertEqual(skill.cooldown_seconds, 30)

    def test_resource_change(self):
        """자원 획득 및 소비 데이터 테스트"""

        skill = Skill(
            id="test_resource",
            name="테스트 자원 기술",
            gcd_type="oGCD",
            required_level=50,
            resource_requirements={
                "job_gauge": 50
            },
            resource_changes=[
                ResourceChange(
                    resource_key="job_gauge",
                    amount=-50
                ),
                ResourceChange(
                    resource_key="job_gauge",
                    amount=10,
                    trigger="on_hit"
                ),
            ],
        )

        self.assertEqual(
            skill.resource_changes[0].amount,
            -50
        )

        self.assertEqual(
            skill.resource_changes[1].amount,
            10
        )

    def test_buff_effect(self):
        """버프 효과 생성 테스트"""

        buff = BuffEffect(
            duration_seconds=20,
            target="party",
            crit_rate_bonus=0.10
        )

        self.assertEqual(buff.duration_seconds, 20)
        self.assertEqual(buff.crit_rate_bonus, 0.10)

    def test_invalid_potency(self):
        """음수 위력 입력 방지 테스트"""

        with self.assertRaises(ValidationError):
            Skill(
                id="invalid_skill",
                name="잘못된 기술",
                gcd_type="GCD",
                required_level=1,
                potency=-100
            )

    def test_dataset(self):
        """직업별 기술 데이터셋 테스트"""

        dataset = SkillDataset(
            job="DRG",
            level=100,
            patch="7.10",
            source="prototype",
            skills=[
                Skill(
                    id="test_skill",
                    name="테스트 기술",
                    gcd_type="GCD",
                    required_level=1,
                    potency=300
                )
            ]
        )

        self.assertEqual(dataset.job, "DRG")
        self.assertEqual(dataset.patch, "7.10")
        self.assertEqual(len(dataset.skills), 1)


if __name__ == "__main__":
    unittest.main()
