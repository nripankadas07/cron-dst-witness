import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    command=shutil.which('cron-dst-witness')
    assert command, 'installed console command missing from PATH'
    data=json.loads((Path(__file__).parent/'example.json').read_text())
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/'snapshot.json';path.write_text(json.dumps(data))
        result_run=subprocess.run([command,str(path)],cwd=d,capture_output=True,text=True)
        assert result_run.returncode == 0, result_run.stderr
        result=json.loads(result_run.stdout)
        assert result['counts']['ambiguous'] == 1; assert [x['utc'] for x in result['anomalies'][0]['witnesses']] == ['2026-11-01T05:30:00+00:00','2026-11-01T06:30:00+00:00']
        path.write_text('{}')
        failed=subprocess.run([command,str(path)],cwd=d,capture_output=True,text=True)
        assert failed.returncode == 2 and failed.stderr.startswith('error:'), failed
    print('installed example and malformed-input failure verified')


if __name__=='__main__':main()
