import subprocess

def convert_audio(input_file, output_file):
    """
    Convert audio file to desired format using ffmpeg.
    
    Parameters:
    - input_file (str): Path to the input audio file.
    - output_file (str): Path to the output audio file.
    """
    command = ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', output_file, '-y']
    subprocess.run(command, check=True)