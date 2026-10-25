
import json
import unittest

from io import BytesIO
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from scripts.xivapi_probe import (
    build_action_url,
    fetch_action,
    summarize_action,
)


class TestXIVAPIProbe(unittest.TestCase):

    def test_build_action_url(self):
        """패치와 필드가 요청 URL에 올바르게 포함되는지 검사"""

        url = build_action_url(75, "7.1")
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        self.assertEqual(
            parsed.path,
            "/api/sheet/Action/75"
        )
        self.assertEqual(params["version"], ["7.1"])
        self.assertEqual(params["language"], ["en"])
        self.assertEqual(
            params["transient"],
            ["Description"]
        )

    @patch("scripts.xivapi_probe.urlopen")
    def test_fetch_action(self, mock_urlopen):
        """가짜 API 응답을 정상적으로 읽는지 검사"""

        sample_response = {
            "row_id": 75,
            "fields": {
                "Name": "True Thrust",
                "ClassJobLevel": 1,
                "Recast100ms": 25,
            },
            "transient": {
                "Description": "Test description"
            },
        }

        mock_urlopen.return_value = BytesIO(
            json.dumps(sample_response).encode("utf-8")
        )

        result = fetch_action(75)

        self.assertEqual(result["row_id"], 75)
        self.assertEqual(
            result["fields"]["Name"],
            "True Thrust"
        )

    def test_summarize_action(self):
        """주요 필드와 재사용 시간 단위 변환 검사"""

        sample_response = {
            "row_id": 75,
            "fields": {
                "Name": "True Thrust",
                "ClassJobLevel": 1,
                "Recast100ms": 25,
            },
            "transient": {
                "Description": "Test description"
            },
        }

        result = summarize_action(sample_response)

        self.assertEqual(result["action_id"], 75)
        self.assertEqual(result["required_level"], 1)
        self.assertEqual(result["recast_seconds"], 2.5)
        self.assertEqual(
            result["description"],
            "Test description"
        )


if __name__ == "__main__":
    unittest.main()
