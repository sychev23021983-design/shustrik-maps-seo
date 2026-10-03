#!/usr/bin/env python3
"""Bounded aggregate-only sampling. No env, request table, paths or credentials."""
import datetime, json, pathlib, subprocess, urllib.error

ROOT = pathlib.Path('/var/log/shustrik-observability')
PHP = '''$c=stream_context_create(['http'=>['timeout'=>3]]);
$s=@file_get_contents('http://127.0.0.1:8099/server-status?auto',false,$c);
if($s===false){echo json_encode(['available'=>false]);exit(0);}
$o=['available'=>true];foreach(explode("\\n",$s) as $l){$a=explode(': ',$l,2);
if(count($a)==2 && in_array($a[0],['BusyWorkers','IdleWorkers','Uptime','ReqPerSec'],true))$o[$a[0]]=$a[1];}
echo json_encode($o);'''

def run(args, timeout):
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if p.returncode: raise RuntimeError('command_failed')
    return p.stdout

def collect():
    now = datetime.datetime.now(datetime.timezone.utc)
    row = {'utc': now.isoformat(), 'status_probe_counts_as_busy_worker': True}
    try:
        row['workers'] = json.loads(run(['docker', 'exec', 'shustrik-maps-wordpress-1', 'php', '-r', PHP], 5))
    except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError):
        row['workers'] = {'available': False, 'probe_error': True}
    try:
        raw = run(['docker', 'stats', '--no-stream', '--format', '{{json .}}',
                   'shustrik-maps-wordpress-1', 'shustrik-maps-db-1'], 5)
        row['containers'] = [{k: json.loads(line).get(k) for k in ['Name','CPUPerc','MemUsage','PIDs']} for line in raw.splitlines()]
    except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError):
        row['containers'] = []; row['stats_error'] = True
    row['load_average'] = pathlib.Path('/proc/loadavg').read_text().split()[:3]
    mem = {}
    for line in pathlib.Path('/proc/meminfo').read_text().splitlines():
        key, value = line.split(':', 1)
        if key in ['MemAvailable','SwapFree','SwapTotal']: mem[key + '_KiB'] = int(value.split()[0])
    row['host_memory'] = mem
    ROOT.mkdir(exist_ok=True)
    # Keep only date-named aggregate JSON files, at most 7 days; no arbitrary paths.
    cutoff = now.date() - datetime.timedelta(days=7)
    for path in ROOT.glob('workers-????-??-??.jsonl'):
        try: day = datetime.date.fromisoformat(path.stem.removeprefix('workers-'))
        except ValueError: continue
        if day < cutoff: path.unlink()
    with (ROOT / ('workers-' + now.date().isoformat() + '.jsonl')).open('a') as f:
        f.write(json.dumps(row, separators=(',', ':')) + '\n')
    return row

if __name__ == '__main__':
    print(json.dumps(collect(), separators=(',', ':')))
