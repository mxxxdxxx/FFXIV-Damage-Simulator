
import unittest

from fastapi.testclient import TestClient

from main import app


class TestSkillsAPI(unittest.TestCase):
    """
    직업별 기술 조회 API 테스트.
    """

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_drg_skills(self):
        """용기사 레벨 100 데이터 정상 조회"""

        response = self.client.get(
            "/api/skills/DRG",
            params={
                "level": 100,
                "patch": "7.10"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["job"], "DRG")
        self.assertEqual(data["level"], 100)
        self.assertEqual(data["patch"], "7.10")
        self.assertEqual(len(data["skills"]), 3)

    def test_lowercase_job(self):
        """소문자 직업 코드 요청"""

        response = self.client.get(
            "/api/skills/drg",
            params={
                "level": 100,
                "patch": "7.10"
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_patch(self):
        """없는 패치 데이터 요청"""

        response = self.client.get(
            "/api/skills/DRG",
            params={
                "level": 100,
                "patch": "0.00"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_invalid_job(self):
        """데이터가 없는 직업 요청"""

        response = self.client.get(
            "/api/skills/ABC",
            params={
                "level": 100,
                "patch": "7.10"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_missing_level(self):
        """필수 레벨 파라미터 누락"""

        response = self.client.get(
            "/api/skills/DRG",
            params={
                "patch": "7.10"
            }
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
