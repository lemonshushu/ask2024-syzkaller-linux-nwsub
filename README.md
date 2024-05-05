# Data Repository for Fuzzing Research
## Paper Information
To be added
## Disclaimer
본 저장소의 파일들은 학사과정 재학 중에 본 연구를 진행하며 기록용으로 저장했던 것들로, 논문에 나와 있는 모든 실험 결과 데이터가 포함되어 있지 않습니다. <br>
구체적으로는, network config(실험 3-1)의 결과는 raw pc trace, CSV coverage, HTML coverage를 포함하여 모든 데이터가 본 저장소에 포함되어 있으나 default config(실험 3-2)의 결과 데이터는 포함되어 있지 않습니다. <br>
다만 두 실험 모두 실험에 사용한 config file들(`config/` 디렉토리)이 남아 있고, 결과 그래프를 생성하는 데 사용된 파이썬 스크립트 파일들(`scripts/` 디렉토리)이 남아 있으므로 결과 재현이 가능합니다.
## Files Explained
### `configs/`
Fuzzing에 실제로 사용한 configuration 파일들. 각각에 대한 간략한 설명은 다음과 같다:
- [Network Config](configs/config_network.json)
    - 논문의 **"3-1) TCP 및 IPv4 소켓 관련 시스템 콜들만 허용하여 실험"** 에 해당
    - Enabled syscalls : `socket$inet_tcp`, `bind$inet`, `listen`, `syz_emit_ethernet`, `syz_extract_tcp_res$synack`, `accept$inet`
    - Coverage filter : `net/ipv4/*`, `net/core/*`, `net/socket.c`
- [Default Config](configs/config_default.json)
    - 논문의 **"3-2) 2)	모든 시스템 콜들을 허용하여 실험"** 에 해당
    - Enabled syscalls : All
    - Coverage filter : `net/ipv4/*`, `net/core/*`, `net/socket.c`

### `coverage/`
- 주의: [위에서 언급하였던 바와 같이](#disclaimer), network config에 대한 coverage report들(html, raw, csv)만 남아 있고, default config는 최종 생성된 plot만 존재함
#### `html/`
각 configuration으로 수 일간 fuzzing 진행 후 최종 coverage 상태를 나타내는 html coverage report 파일들
#### `raw/`
수 일간 fuzzing을 진행하면서 20분에 한번씩 수집한 raw coverage(i.e., PC trace)
#### `csv/`
위의 각 raw coverage를 가지고 생성한 csv coverage report 파일들
### `plots/`
- csv coverage 데이터를 정리하여 생성한 그래프 파일들
- 그래프 생성에 사용된 스크립트들은 `scripts/` 디렉토리에 있음
### `scripts/`
커버리지 데이터 정리 및 plot 생성에 사용한 파이썬 스크립트 파일들
#### `gen_coverage_csv.py`
- input 디렉토리(디렉토리명: `csv_cover`)에 있는 모든 csv coverage 파일들을 모아 하나로 합쳐, `coverage.csv`로 output함.
- 이때 각 csv 파일명은 `"%Y_%m_%d_%H_%M_%S"` 형태임.
- 최소 시간 파일로부터 120시간 내의 데이터만 가지고 처리하고, 나머지는 무시함.
#### `draw_plots.py`
- `gen_coverage_csv.py`를 통해 생성된 `coverage.csv` 파일을 입력으로 받아, 리눅스 커널 코드의 각 파일 및 함수별 시간에 따른 커버리지 변화 양상을 그래프로 그려 output함.
- 생성된 plot들은 `plots/*/out_120h/` 디렉토리에 있음
#### `draw_plots_aggregated.py`
- Subsystem별 합계 coverage의 변화 양상을 하나의 그래프에 나타내어 파일로 output함.
- 생성된 plot들은 `plots/*/coverage_subsys.png`로 볼 수 있음
