# Lazyest-qa

ISTQB의 테스트 체계를 참고한 범용 QA 스킬입니다. 프로젝트의 요구사항과 위험도를 파악하고 필요한 검사를 설계·실행하며, 결함과 미검증 범위를 근거로 설명합니다.

[English](README.md)

## Claude Code 설치

Claude Code 안에서 실행합니다.

```text
/plugin marketplace add lazyest-hyun/lazyest-qa
/plugin install lazyest-qa@lazyest-qa
```

설치 후 다음처럼 사용합니다.

```text
/lazyest-qa:lazyest-qa 이번 변경과 관련 흐름을 QA해줘. 기존 도구로 실제 테스트하고 결함과 미검증 범위를 알려줘.
```

앞의 이름은 플러그인, 뒤의 이름은 스킬입니다. 활성화를 요청하면 `/reload-plugins`를 실행하거나 새 세션을 시작합니다.

## Codex 설치

플러그인을 지원하는 Codex CLI에서 실행합니다.

```sh
codex plugin marketplace add lazyest-hyun/lazyest-qa
codex plugin add lazyest-qa@lazyest-qa
```

Codex에서 플러그인 스킬은 `lazyest-qa:lazyest-qa`로 등록됩니다. 단독 설치의 이름은 `lazyest-qa`입니다.

새 작업에서 스킬 선택 메뉴의 **Lazyest-qa**를 선택하거나 다음처럼 요청합니다.

```text
Lazyest-qa 스킬로 이번 변경을 QA해줘. 기존 프로젝트의 도구로 실행하고 결과와 남은 위험을 알려줘.
```

플러그인 명령을 지원하지 않으면 Codex에 직접 스킬 설치를 요청할 수 있습니다.

```text
$skill-installer 다음 GitHub 경로의 스킬을 설치해줘.
https://github.com/lazyest-hyun/lazyest-qa/tree/main/plugins/lazyest-qa/skills/lazyest-qa
```

단독 설치 후에는 `$lazyest-qa`로 호출합니다. 중복 표시를 피하려면 플러그인과 단독 설치 중 하나를 사용하세요. 기존 단독 설치본이 있으면 그대로 사용하거나 설치 방식을 바꾸면서 교체를 요청하면 됩니다.

## 사용 예시

```text
Lazyest-qa로 이 요구사항의 테스트 계획과 구체적인 케이스만 만들어줘.
경계값, 권한 조합과 상태 전이를 검토하고 미정인 정책은 따로 표시해줘.
```

```text
Lazyest-qa로 이 버그가 수정됐는지 확인하고 관련 회귀 테스트도 해줘.
제품 코드는 수정하지 마.
```

```text
Lazyest-qa로 이 AI 서비스의 출시 증거를 검토해줘.
실제 평가 결과, 불충분한 근거와 미검증 항목을 구분하고 배포는 하지 마.
```

## 범위와 동작

웹, 모바일, 데스크톱, CLI, API, 분산 처리, 데이터, 마이그레이션, 성능, 복구, 접근성, 사용성, 보안 관련 QA와 AI 평가를 다룹니다. 동등 분할, 경계값, 결정 테이블, 상태 전이 등의 기법을 위험과 요구사항에 맞춰 선택합니다.

계획만 요청하면 실행하지 않고, 실행 요청에서는 사용 가능한 도구로 실제 검사를 수행합니다. 미실행·차단·불확실한 결과를 통과로 처리하지 않습니다. 권한이나 실제 기기가 필요한 검사는 해당 환경이 없으면 남은 범위로 표시합니다.

제품과 기존 테스트를 먼저 읽고 짧은 공통 지침으로 진행합니다. 참조 문서는 해결되지 않은 구체적인 질문이 생길 때 해당 부분만 읽습니다. 전용 실행기, MCP 서버, 계정이나 유료 서비스는 필수가 아닙니다. 지침은 영어이며 결과는 요청자의 언어를 따릅니다.

출력이 짧으면 기존 테스트 명령을 직접 사용합니다. 긴 로그를 다룰 때 선택적으로 쓰는 `scripts/run_check.py`는 각 실행의 전체 로그를 별도 파일로 보존하고 실제 종료 코드·경과 시간·마지막 일부만 출력합니다. 종료 코드 0을 QA 통과로 해석하지 않습니다. 이 도구만 Python 3.9 이상이 필요하며, Windows의 자식 프로세스 정리는 아직 실행 검증하지 않았습니다.

패키지 유지보수 검증에는 개발용 PyYAML이 필요합니다. 저장소에서 `python3 -m pip install -r requirements-dev.txt` 후 `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`를 실행합니다. 스킬 설치·일반 사용에는 이 개발 의존성이 필요하지 않습니다.

공식 ISTQB 제공물이나 인증 교육 자료가 아니며 모든 결함의 발견을 보장하지 않습니다. [참고 자료](plugins/lazyest-qa/skills/lazyest-qa/references/sources.md)와 [검증 범위](docs/validation.md)를 확인할 수 있습니다.

[공개 QA 환경 구축 안내](benchmarks/public-qa/README.md)로 Tornado의 실제 과거 결함 3개를 재현할 수 있습니다. 고정된 원본·수정본에서 같은 회귀 검사의 실패→통과를 먼저 확인하고, 참가자 코드와 채점 자료를 분리합니다. BugsInPy에서 선택한 소규모 환경이며 전체 벤치마크 점수나 스킬의 필수 의존성이 아닙니다.

업데이트와 유지보수 방법은 [영문 안내](README.md#updates)에 있습니다. 직접 작성한 패키지 내용에는 [MIT 라이선스](LICENSE)가 적용되고, 참고한 외부 자료의 권리와 상표는 각 권리자에게 있습니다.
