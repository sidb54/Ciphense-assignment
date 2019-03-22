import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
#import matplotlib.pyplot as plt
#from PIL import Image
from io import BytesIO
import urllib
import json
from gtts import gTTS
import os
# Replace <Subscription Key> with your valid subscription key.
subscription_key = "fb9d9f3e929c4e4aa7740b0db0c6e896"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the "westus" region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

analyze_url = vision_base_url + "analyze"

# Set image_path to the local path of an image that you want to analyze.
image_path = "C:/Users/Siddharth/Desktop/Ciphense/image1.jpg"

# Read the image into a byte array

image_data = open(image_path, "rb").read()
headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}


parameters     = {'visualFeatures': 'Categories,Description,Color,ImageType,Objects,Tags,Adult,Brands,Faces'}
response = requests.post(
    analyze_url, headers=headers, params=parameters, data=image_data)
response.raise_for_status()

# The 'analyze' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.

analyze = json.loads(json.dumps(response.json()))
print()
print(analyze)

'''if 'detail' in analyze['categories'][0]:
        print("yes")
        if 'celebrities' in analyze['categories'][0]['detail']:
                print("yes")
'''

#image_caption = analyze["description"]["captions"][0]["text"].capitalize()
#print(image_caption)

s = ""
cat = ""
l=analyze["description"]["tags"]
k=analyze["categories"]
for i in l:
        s = s + i +", "

#print(s)

res = 0;
maxscore = {}; #finding the dict. which has maximum score/ confidence

for word in k:
        if res<float(word["score"]):
                res=float(word["score"])
                maxscore = word

#print(maxscore)

ans=""
ans=ans+"The category is "+maxscore['name']+"\n"

if 'detail' in maxscore:
        #print("yes")
        if 'celebrities' in maxscore['detail']:
                #print("yes")
                ll=""
                for l in maxscore['detail']['celebrities']:
                        ll = ll + l['name']+" "        
                ans=ans+"The celebs are "+ll+"\n"

        if 'landmarks' in maxscore['detail']:
                #print("yes")
                ll=""
                for l in maxscore['detail']['landmarks']:
                        ll = ll + l['name']+" "        
                ans=ans+"The landmarks are "+maxscore['landmarks']+"\n"


if analyze['adult']['isRacyContent']:
        ans = ans+"Racy content present\n"
else:
        ans = ans+"Racy content absent\n"

ans = ans  + "The foreground color is "+ analyze['color']['dominantColorForeground']+"\n"
ans = ans  + "The background color is "+ analyze['color']['dominantColorBackground']+"\n"

if analyze['color']['isBWImg']:
        ans = ans+"black and white image\n"
else:
        ans = ans+"Color Image\n"


ans = ans+"Tags are "+ s+"\n"

ans = ans+"Description of the image is "+analyze['description']['captions'][0]['text']+"\n"

ctr = 1

for i in analyze['faces']:
        ans = ans + "object "+ str(ctr)+" age is "+str(i['age'])+" , gender is "+i['gender']+"\n"
        ctr=ctr+1

if analyze['adult']['isAdultContent']:
        ans = ans+"Adult content present\n"
else:
        ans = ans+"Adult content absent\n"

file = open("out.txt","w")
file.write(ans)
file.close()

# Language in which you want to convert 
language = 'en'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=ans, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  

myobj.save("welcome.mp3") 
