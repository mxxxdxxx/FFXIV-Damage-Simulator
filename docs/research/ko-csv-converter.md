
## 실제 CSV 변환 검증 결과

### 원본 데이터

- 검증일: 2026-10-26
- 한국 클라이언트 패치: 7.57
- 게임 데이터 버전: 2026.10.06.0000.0000
- 원본 저장소: https://github.com/Ra-Workspace/ffxiv-datamining-ko
- 원본 브랜치: master
- 원본 파일: csv/Action.csv
- 원본 커밋: 7a82b4b468a09a364b2c603447b2db0bed8a8a06
- SHA256: D4ABB59678F8624378ED896F8BC20BBA03621EA0BC41527EE1F67AB27F6DB192

### CSV 구조

- Action ID 열: key
- 한국어 이름 열: 0
- 필드 설명 행(#) 및 자료형 행(int32) 제외
- 빈 이름, 잘못된 ID, 중복 ID 검사

### 변환 결과

- Action ID 및 한국어 이름 45,519개 추출
- Action ID 75: 직선 찌르기
- Action ID 78: 사선 찌르기
- 생성 파일: backend/data/localization/generated/ko_7.57.json
- 기존 JSON 덮어쓰기 방지 확인
- 신규 테스트 5개 포함 전체 단위 테스트 26개 통과

### 데이터 관리

- 원본 CSV와 generated JSON은 Git에 포함하지 않는다.
- 생성된 JSON은 기존 한국어 매핑 JSON과 동일한 구조를 사용한다.
- 이번 Issue에서는 기존 skill_localization.py의 조회 경로를 변경하지 않는다.
- 한국어 CSV의 일부 일본어 및 내부 기술명은 원본 그대로 보존한다.
- 실제 플레이어 기술 필터링과 미번역 이름 검증은 후속 작업에서 처리한다.

