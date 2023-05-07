import requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup


def get_images_with_request_headers():
    del params["ijn"]
    params["content-type"] = "image/png" 

    return [img["src"] for img in soup.select("img")]

def get_suggested_search_data():
    suggested_searches = []

    all_script_tags = soup.select("script")

    
    matched_images = "".join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))
    
    
    matched_images_data_fix = json.dumps(matched_images)
    matched_images_data_json = json.loads(matched_images_data_fix)

    
    suggested_search_thumbnails = ",".join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))

    
    suggested_search_thumbnail_encoded = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails)

    for suggested_search, suggested_search_fixed_thumbnail in zip(soup.select(".PKhmud.sc-it.tzVsfd"), suggested_search_thumbnail_encoded):
        suggested_searches.append({
            "name": suggested_search.select_one(".VlHyHc").text,
            "link": f"https://www.google.com{suggested_search.a['href']}",
           
            "chips": "".join(re.findall(r"&chips=(.*?)&", suggested_search.a["href"])),
            "thumbnail": bytes(suggested_search_fixed_thumbnail, "ascii").decode("unicode-escape")
        })

    return suggested_searches

def get_original_images():
    
    global count
    count_init = count
    """
    https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    if you try to json.loads() without json.dumps() it will throw an error:
    "Expecting property name enclosed in double quotes"
    """

    google_images = []

    all_script_tags = soup.select("script")

   
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)

    matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(", ")

    thumbnails = [
        bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
    ]

    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

    full_res_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
    ]
    
    for index, (metadata, thumbnail, original) in enumerate(zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
        google_images.append({
            "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
            "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
            "source": metadata.select_one(".fxgdke").text,
            "thumbnail": thumbnail,
            "original": original
        })

        
        print(f'Downloading {count} image Query {params["q"]} ...')
        
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(original, f'Bs4_Images/image {count}.jpg')
        except:
            pass
        # save a txt file with the same name as the image containing the image title
        with open(f'Bs4_Images/image {count}.txt', 'w+') as f:
            f.write(metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"])
        count = count + 1
        if count - count_init > 50 :
            break


    return google_images

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}



KEYWORD = "INTERIOR"



queries = [
    'Moroccan room design ideas',
    'Moroccan bedroom design ideas',
    'Living room decor ideas with Moroccan touch',
    'Moroccan style bathroom ideas',
    'How to decorate a room in Moroccan style',
    'Moroccan inspired living room ideas',
    'Moroccan decor ideas for small spaces',
    'Moroccan style furniture ideas',
    'Moroccan interior design tips',
    'Moroccan color scheme ideas for rooms',
    'DIY Moroccan room decor ideas',
    'Moroccan lighting ideas for rooms',
    'How to create a Moroccan-inspired outdoor space',
    'Moroccan rugs for rooms',
    'Moroccan style curtains and drapes',
    'Moroccan zellige tile design ideas', 
    'Beni Ourain rug decor ideas', 
    'Moroccan leather pouf design ideas', 
    'Moroccan brass lanterns for decor', 
    'Moroccan ceramic bowl decor ideas', 
    'Moroccan wood carving design ideas', 
    'Moroccan textile patterns for decor', 
    'Moroccan wrought iron furniture design ideas']
    


count = 1
for query in queries:
    params = {
        "q": query,                 
        "tbm": "isch",              
        "hl": "en",                 
        "gl": "ma",                 
        "ijn": "0"                  
    }
    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")
    get_original_images()
    


for file in os.listdir('Bs4_Images'):
    if file.endswith('.jpg'):
        print(file)
        if not os.path.exists(f'Bs4_Images/{file[:-4]}.txt'):
            print(f'Deleting {file}...')
            os.remove(f'Bs4_Images/{file}')


