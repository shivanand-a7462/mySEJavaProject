import re
from nltk import FreqDist
from nltk.corpus import stopwords

sample_titles = [
    "PM Narendra Modi heads to Seychelles, Mauritius, Lanka; tour begins on March 10",
    "PM Modi visits Ganga Talao in Mauritius, prays at temple",
    "India, Sri Lanka sign 4 pacts during Modi visit",
    "PM Narendra Modi's Singapore visit",
    "PM Modi dines with Lee Hsien Loong at Indian restaurant in Singapore, NOV 23",
    "Modi takes selfie with Indian students in France, April 11",
    "PM Modi to visit Germany in April, Jan 19",
    "Scripting a west side story: Modi’s visits to France, Germany and Canada adapt lessons learnt from China’s economic miracle, april 20(blog)",
    "PM Modi in Ottawa: Canada will supply uranium to India for next five years,  april 15",
    "Deals worth $22 billion signed during PM Narendra Modi’s China visit, May 17",
    "Modi to be first Indian PM to visit Mongolia, May 12",
    "Why PM Modi left 'Kanthaka' in Mongolia, May 28",
    "Joint statement by PM Modi during his visit to Seoul, May 18",
    "Narendra Modi in Seoul: India and South Korea sign 7 pacts; bilateral ties raised to 'strategic partnership'",
    "Great expectations in Dhaka: Modi has an opportunity to reboot India-Bangladesh relations after many erratic flip-flops, June 5(blog)",
    "India, Bangladesh ratify historic land deal, Narendra Modi announces new $2 billion line of credit to Dhaka, june 6",
    "Full text of PM Modi's joint statement in Dhaka, June 6",
    "As it happened: PM Modi's Bangladesh visit — Day 2, June 7",
    "Modi’s Dhaka visit can galvanise Indo-Bangla ties through Teesta and connectivity deals, May 30(blog)",
    "PM Narendra Modi on two-day Bangladesh visit from June 6, May 26",
    "PM Modi visits Uzbekistan, july 7",
    "Modi pays tribute to Lal Bahadur Shastri in Tashkent, July 7",
    "PM Modi in Tashkent, holds talks with Uzbek President Karimov, JULY 6",
    "Live Blog: PM Modi in Russia, Dec 24",
    "Narendra Modi will be first Indian PM to visit Israel and Palestine, June 1",
    "PM Narendra Modi’s foreign travel in 2015-16 has cost Air India Rs 117cr, may 6",
    "PM Modi hails 'long-standing' ties between Turkmenistan, India, June 11",
    "As it happened: PM Modi's UAE visit— Day 1, aug 16",
    "This is why PM Modi visited Masdar City in UAE, Aug 17",
    "As it happened: PM Narendra Modi in Ireland, Sep 23",
    "PM Modi connects with Indian diaspora in Ireland, promises more visits, Sep 23",
    "PM Modi arrives in Ireland, first Indian PM to visit country in 60 years, Sep 23",
    "Reform security council to maintain its credibility, PM Modi urges at UN meet, sep 26",
    "PM Narendra Modi in New York for his second US visit, sep 25",
    "Top 10 quotes of PM Modi at UN summit, sep 25",
    "As it happened: PM Narendra Modi in UK, Nov 14",
    "Narendra Modi confirms his maiden visit to Britain, july 3(world)",
    "Mossad, MI5 roped in to shield Prime Minister Narendra Modi in Turkey?, Nov 15",
    "Prime Minister Narendra Modi to visit Malaysia, Singapore from November 21, Nov 18",
    "Little India' in Malaysia preparing for PM Modi's visit, Nov 19",
    "Modi gifts Singapore PM reproduction of 1849 map, Nov 24",
    "India, Singapore to sign strategic partnership agreement during Modi's visit, Oct 13",
    "Prime Minister Narendra Modi arrives in Paris, April 10",
    "Prime Minister Narendra Modi to attend inaugural of Paris climate summit, Oct 28",
    "At Paris climate summit, PM Modi to unveil India's grand plans on renewables, Nov 29",
    "PM Narendra Modi arrives in Paris to attend climate summit, Nov 29",
    "PM Narendra Modi address to Afghanistan parliament: Read full speech/ dec 25",
    "PM Narendra Modi arrives in Kabul, Dec 25",
    "CPI(M) welcomes Modi's visit to Pakistan, Dec 25",
    "As it happened: PM Modi in Lahore, dec 25",
    "This is how PM Modi arranged his surprise visit to Pakistan, dec 25",
    "PM Modi meets Nawaz Sharif in surprise Lahore visit, Pak hails 'goodwill gesture', Dc 25",
    "Ahead of Modi visit, two warships reach Mauritian waters, March 11",
    "Narendra Modi may visit Sri Lanka in March, jan 20",
    "Modi in Colombo, announces slew of steps 'to steer Sri Lanka away from China', march 13",
    "Modi pays homage at war memorial for Indian soldiers in France, April 11"

]


all_word_list = []
freq_count = {}
for title in sample_titles:
    title = title.lower()
    title = re.sub('[,.]', '', title)
    title = re.sub('\d+', '', title)
    word_list = title.split()
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    all_word_list.extend(filtered_words) 


for words in all_word_list:
    try:
        counter = freq_count[words]
        freq_count[words] = counter + 1
    except KeyError:
        freq_count[words] = 1

sorted_key = sorted(freq_count, key=freq_count.__getitem__, reverse=True)[:10]
for item in sorted_key:
    print (item, freq_count[item])