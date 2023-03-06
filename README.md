# splitmidikeyboard
Split the midi keyboard for timidity (play two instruments on single keyboard)

This application will allow you to split your midi keyboard into 2 parts and assign a different instrument to play for each part. It also allows you to adjust the transposition for each of the parts.

![Alt text](img/mainwindow.png?raw=true "main window")

## Install dependencies on Debian GNU/Linux:

### Step 1 install dependencies:
Install script dependencies:
```bash
apt install timidity 
pip3 install tkinter mido
```

Install sound font, for example:
fluid-soundfont-gm ~150 mb:
```bash
apt install fluid-soundfont-gm
```
musescore-general-soundfont-lossless ~500mb:
```bash
apt install musescore-general-soundfont-lossless
```

### Step 2 setup timidity:
edit /etc/timidity/timidity.cfg, append or replace if needed:
```
opt EFresamp=l		#disable resampling
opt EFvlpf=d		#disable VLPF
opt anti-alias=d	#disable sample anti-aliasing
opt EFns=0
opt p64a
dir /usr/share/sounds/sf2		# path to your sf2 dir
soundfont "MuseScore_General_Full.sf2"	# FluidR3_GM.sf2 / MuseScore_General_Full.sf2
```

## Usage

### Step 1 start timidity, example (for low cpu usage):
```bash
timidity -iA -B4,8 -OsSu1 --resample=l -a --voice-lpf=d --noise-shaping=0 --default-program=2 -s 44kHz &
```

### Step 2 start the script
```bash
python3 ./split_keyboard.py
```
