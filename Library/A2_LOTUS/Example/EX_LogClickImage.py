import __init
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS

print(LOTUS.log.clickImage(450,900,"/HShare/Library/A2_LOTUS/Components/PIC/1920_1080_sample.jpg",savePath="EX1_circularImage.png"))

print(LOTUS.log.clickImage(450,900,"/HShare/Library/A2_LOTUS/Components/PIC/1920_1080_sample.jpg",printPosInside=False,savePath="EX2_circularImage.png"))

print(LOTUS.log.clickImage(50,50,savePath="EX3_circularImage.png"))