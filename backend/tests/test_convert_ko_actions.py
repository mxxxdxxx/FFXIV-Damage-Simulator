
import json
import tempfile
import unittest

from pathlib import Path

from scripts.convert_ko_actions import (
    read_action_names,
    build_mapping,
    save_mapping,
)


class TestKOActionConverter(unittest.TestCase):

    def setUp(self):
        # 테스트 전용 임시 폴더 생성
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)

    def make_csv(self, text: str) -> Path:
        # UTF-8 BOM 테스트를 위해 utf-8-sig 사용
        path = self.root / "Action.csv"

        path.write_text(
            text,
            encoding="utf-8-sig"
        )

        return path

    def test_read_names_and_skip_blank(self):
        """정상 기술명 추출 및 빈 이름 제외"""

        csv_path = self.make_csv(
            "key,Name,Other\n"
            "#,str,int\n"
            "75,직선 찌르기,1\n"
            "78,사선 찌르기,4\n"
            "99,,2\n"
        )

        result = read_action_names(csv_path)

        self.assertEqual(
            result,
            {
                "75": "직선 찌르기",
                "78": "사선 찌르기",
            }
        )

    def test_custom_columns(self):
        """CSV 열 이름을 직접 지정하는 기능"""

        csv_path = self.make_csv(
            "#,0,1\n"
            "75,직선 찌르기,x\n"
        )

        result = read_action_names(
            csv_path,
            id_column="#",
            name_column="0"
        )

        self.assertEqual(
            result["75"],
            "직선 찌르기"
        )

    def test_duplicate_conflicting_id(self):
        """서로 다른 이름이 중복된 ID 감지"""

        csv_path = self.make_csv(
            "key,Name\n"
            "75,직선 찌르기\n"
            "75,다른 기술명\n"
        )

        with self.assertRaises(ValueError):
            read_action_names(csv_path)

    def test_invalid_id(self):
        """숫자가 아닌 Action ID 감지"""

        csv_path = self.make_csv(
            "key,Name\n"
            "abc,테스트\n"
        )

        with self.assertRaises(ValueError):
            read_action_names(csv_path)

    def test_json_and_no_overwrite(self):
        """JSON 생성 및 기존 파일 보호"""

        data = build_mapping(
            {"75": "직선 찌르기"},
            patch="7.57",
            source_ref="test-ref"
        )

        output = (
            self.root
            / "generated"
            / "ko_7.57.json"
        )

        save_mapping(output, data)

        saved = json.loads(
            output.read_text(encoding="utf-8")
        )

        self.assertEqual(
            saved["names"]["75"],
            "직선 찌르기"
        )

        self.assertEqual(
            saved["source_ref"],
            "test-ref"
        )

        # 이미 있는 파일은 덮어쓰지 않아야 함
        with self.assertRaises(FileExistsError):
            save_mapping(output, data)


if __name__ == "__main__":
    unittest.main()
