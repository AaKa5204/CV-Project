import subprocess
def get_volume():
    result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], capture_output=True, text=True)
    volume_line = result.stdout.split('\n')[0]
    volume = int(volume_line.split('/')[1].strip().replace('%', ''))
    return volume

def set_volume(volume):
    if volume > 100:
        volume = 100
    subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{volume}%'], check=True)


