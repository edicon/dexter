# 포크 유지보수 및 원본 동기화 가이드 (Fork Maintenance & Upstream Sync Guide)

이 문서는 Dexter 프로젝트의 포크(Fork) 버전을 관리하고, 원본 저장소(Upstream)의 업데이트를 반영하면서 호환성을 유지하는 방법을 설명합니다.

## 1. 프로젝트 구조 및 호환성 전략

이 포크는 원본과의 충돌을 최소화하기 위해 다음과 같은 전략을 사용합니다:

### 독립적인 모듈 구조
- **`src/dexter/tools/crypto/`**: 암호화폐 관련 모든 코드는 이 새로운 디렉토리에 격리되어 있습니다.
- **`src/dexter/tools/finance/`**: 원본의 금융 도구 코드는 수정하지 않고 그대로 둡니다.

### 충돌 가능성이 있는 파일
유일하게 원본과 공유하며 수정된 파일은 다음과 같습니다:
- **`src/dexter/tools/__init__.py`**: 새로운 Crypto 도구를 등록하기 위해 수정되었습니다.

---

## 2. 원본 업데이트 동기화 (Syncing with Upstream)

원본 저장소에 업데이트가 있을 때, 이를 안전하게 반영하는 절차입니다.

### 1단계: 원본 저장소 연결 (최초 1회)
아직 원본 저장소를 `upstream`으로 등록하지 않았다면 등록합니다.
```bash
git remote add upstream [원본_저장소_URL]
```

### 2단계: 최신 변경사항 가져오기
```bash
git fetch upstream
```

### 3단계: 병합 (Merge) 또는 리베이스 (Rebase)
현재 브랜치(예: `main`)에 원본의 변경사항을 병합합니다.
```bash
git checkout main
git merge upstream/main
```

### 4단계: 충돌 해결 (Conflict Resolution)
대부분의 파일은 자동으로 병합되지만, **`src/dexter/tools/__init__.py`**에서 충돌이 발생할 수 있습니다.

**충돌 발생 시 해결 방법:**
1. 충돌이 발생한 파일을 엽니다.
2. `HEAD` (현재 포크의 변경사항)와 `upstream/main` (원본의 변경사항) 사이의 차이를 확인합니다.
3. **목표**: 원본에서 추가된 도구들을 유지하면서, 우리가 추가한 `crypto` 도구들도 목록에 남아있게 해야 합니다.
4. `TOOLS` 리스트에 `get_crypto_price_snapshot`, `get_crypto_prices`가 포함되도록 코드를 수정합니다.

**예시:**
```python
# 충돌 해결 후 모습
TOOLS: list[Callable[..., any]] = [
    # ... 원본의 기존 도구들 ...
    # ... 원본에서 새로 추가된 도구들 ...

    # [Fork 추가] Crypto 도구
    get_crypto_price_snapshot,
    get_crypto_prices,
]
```

5. 수정 후 커밋합니다.
```bash
git add src/dexter/tools/__init__.py
git commit -m "Merge upstream changes and resolve conflicts in tools registration"
```

---

## 3. 새로운 기능 추가 시 주의사항

- **새로운 파일 생성 권장**: 기존 파일을 수정하기보다 새로운 파일이나 폴더를 만드는 것이 좋습니다.
- **`__init__.py` 수정 최소화**: 도구 등록 등 꼭 필요한 경우에만 공용 파일을 수정하고, 수정 내용을 명확히 주석으로 표시하세요.
