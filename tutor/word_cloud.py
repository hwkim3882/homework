import matplotlib.pyplot as plt
from wordcloud import WordCloud

font_path = '/Library/Fonts/NanumBarunGothic.ttf'

wordcloud = WordCloud(
    font_path=font_path,
    width=800,
    height=800
   )

t = open('test.txt')
text = t.read()

wordcloud = wordcloud.generate(text)

fig = plt.figure(figsize=(12,12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
fig.savefig('wordcloud_without_axisoff.png')
