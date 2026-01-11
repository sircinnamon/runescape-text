rm -r ./testoutput
mkdir testoutput

# Colors
python3 runescape_text/runescape_text.py -o testoutput/1_1_yellow.png yellow:This text should be yellow
python3 runescape_text/runescape_text.py -o testoutput/1_2_white.png white:This text should be white
python3 runescape_text/runescape_text.py -o testoutput/1_3_cyan.png cyan:This text should be cyan
python3 runescape_text/runescape_text.py -o testoutput/1_4_red.png red:This text should be red
python3 runescape_text/runescape_text.py -o testoutput/1_5_green.png green:This text should be green
python3 runescape_text/runescape_text.py -o testoutput/1_6_purple.png purple:This text should be purple

# Adv Colors
python3 runescape_text/runescape_text.py -o testoutput/2_1_flash1.gif flash1:This text should be flash1
python3 runescape_text/runescape_text.py -o testoutput/2_2_flash2.gif flash2:This text should be flash2
python3 runescape_text/runescape_text.py -o testoutput/2_3_flash3.gif flash3:This text should be flash3
python3 runescape_text/runescape_text.py -o testoutput/2_4_glow1.gif glow1:This text should be glow1
python3 runescape_text/runescape_text.py -o testoutput/2_5_glow2.gif glow2:This text should be glow2
python3 runescape_text/runescape_text.py -o testoutput/2_6_glow3.gif glow3:This text should be glow3

# Animations
python3 runescape_text/runescape_text.py -o testoutput/3_1_scroll.gif scroll:This text should be scroll
python3 runescape_text/runescape_text.py -o testoutput/3_2_slide.gif slide:This text should be slide
python3 runescape_text/runescape_text.py -o testoutput/3_3_wave.gif wave:This text should be wave
python3 runescape_text/runescape_text.py -o testoutput/3_4_wave2.gif wave2:This text should be wave2
python3 runescape_text/runescape_text.py -o testoutput/3_5_shake.gif shake:This text should be shake

# Ascender/descender tests
python3 runescape_text/runescape_text.py -o testoutput/4_01_wave.png wave
python3 runescape_text/runescape_text.py -o testoutput/4_02_wave.gif wave:wave
python3 runescape_text/runescape_text.py -o testoutput/4_03_wave_glow.gif wave:glow1:wave
python3 runescape_text/runescape_text.py -o testoutput/4_04_teen.png teen
python3 runescape_text/runescape_text.py -o testoutput/4_05_teen.gif wave:teen
python3 runescape_text/runescape_text.py -o testoutput/4_06_teen_glow.gif wave:glow1:teen
python3 runescape_text/runescape_text.py -o testoutput/4_07_jean.png jean
python3 runescape_text/runescape_text.py -o testoutput/4_08_jean.gif wave:jean
python3 runescape_text/runescape_text.py -o testoutput/4_09_jean_glow.gif wave:glow1:jean
python3 runescape_text/runescape_text.py -o testoutput/4_10_Omg.png Omg
python3 runescape_text/runescape_text.py -o testoutput/4_11_Omg.gif wave:Omg
python3 runescape_text/runescape_text.py -o testoutput/4_12_Omg_glow.gif wave:glow1:Omg

# Large file test
python3 runescape_text/runescape_text.py -o testoutput/5_1_large.gif scroll:glow1:This will have many frames

cat test.html > testoutput/index.html
python -m http.server -d testoutput 8001