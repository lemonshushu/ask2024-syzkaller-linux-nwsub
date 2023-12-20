# Data Repository for Fuzzing Research
## Currently Running Instance
https://syzkaller.lemonshushu.me
- HTTP 502 에러가 뜨면 현재 fuzzing중이 아니라는 의미임 (혹은 fuzzing중에 다운됨)

## Files Explained
### `configs/`
Fuzzing에 실제로 사용한 configuration 파일들. 각각에 대한 간략한 설명은 다음과 같다:
- [Network Config](configs/config_network.json)
    - Enabled syscalls : `socket$inet_tcp`, `bind$inet`, `listen`, `syz_emit_ethernet`, `syz_extract_tcp_res$synack`, `accept$inet`
    - Coverage filter : `net/ipv4/*`, `net/core/*`, `net/socket.c`
- [Default Config](configs/config_default.json)
    - Enabled syscalls : All
    - Coverage filter : `net/ipv4/*`, `net/core/*`, `net/socket.c`
- [Route + Netfilter Config](configs/config_route.json)
    - Enabled syscalls : All
    - Coverage filter : `net/ipv4/route.c`, `net/ipv4/ip_forward.c`, `net/ipv4/fib_*`, `net/ipv4/netfilter/*`, `net/ipv4/netfilter.c`, `net/ipv4/netlink.c`, `net/netfilter/*`, `net/netlink/*`
    - 현재로서는 약 3일정도만 연속으로 fuzzing을 진행한 상태. 추후 더 이어서 진행하여 데이터 추가 예정

### `coverage/`
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

### `bachelor_paper/`

학사논문 관련 자료들을 포함함 (참고용)