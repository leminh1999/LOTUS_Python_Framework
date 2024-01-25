from PIL import Image

headerPic   = Image.open("1234567890"+"_header.png")
commentPic1 = Image.open("1234567890"+"_commentPart1.png")
commentPic2 = Image.open("1234567890"+"_commentPart2.png")
commentFullPic = Image.open("commentFullPic.png")

print(commentFullPic.size)
print(headerPic.size)
print(commentPic1.size)
print(commentPic2.size)
print("Total size: ", headerPic.size[1]+commentPic1.size[1]+commentPic2.size[1] )

