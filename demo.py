# To scrap data from a website
# import requests
# from bs4 import BeautifulSoup

# url = "http://olympus.realpython.org/profiles/dionysus"
# html = requests.get(url)
# html_text = html.text
# print(html_text)
# soup = BeautifulSoup(html_text, "html.parser")

# for string in ["Name: ","Favorite Color: "]:
#     startString = html_text.find(string)
#     lenString = len(string)
#     startIndex = startString + lenString
#     nextTag = html_text[startIndex:].find("<")
#     lastIndex = startIndex + nextTag
#     print(f"{string} {html_text[startIndex:lastIndex]}")






# To scrap prices from a website
# import requests
# from bs4 import BeautifulSoup

# url = "http://books.toscrape.com/"
# headers = {"User Agent": "Mozilla/5.0"}
# response = requests.get(url)
# html = response.text
# soup = BeautifulSoup(html, "html.parser")

# prices = soup.find_all("p", class_="price_color")

# i = 0
# for p in prices:
#     print(p.text)
#     i+=1
# print(i)    


# Find Missing numbers
# arr = [1,2,4,5,6]
# for i in range(1,7):
#     if i not in arr:
#         print("Missing number is ",i) #3

# Reverse word, but keep order
# s = "I love python"
# print("Reverse of s is ",s[::-1]) # nohtyp evol I
# lst1 = s.split()
# print(lst1) # ['I', 'love', 'python']
# rev = []
# for i in lst1:
#     i = i[::-1]
#     rev.append(i)
# print(' '.join(rev))  # I evol nohtyp  


# First non-repeating character
# s = "swiss"
# for i in s:
#     c = 0
#     for j in s:
#         if i==j:
#            c+=1
#     if c == 1:
#         print("First non-repeating character is ",i) # w
#         break   

# or   
# from collections import Counter
# s = 'swiss'
# count = Counter(s)
# for ch in s:
#     if count[ch] == 1:
#         print("First non-repeating character is ",ch) # w
#         break


# Count Frequency Without collections
# l = [1,2,2,3,3,3]
# dict = {}
# for i in l:
#     s = 0
#     for j in l:
#         if j == i:
#             s+=1
#     dict[i] = s
# print("Count frquency of the list is ",dict)   # {1: 1, 2: 2, 3: 3} 


# Check Anagram (Without sort)
# w1 = "sileNt"
# w2 = "listen"
# w3 = w2

# for i in w1.lower():
#     c = 0
#     for j in w2.lower():
#         if i == j:
#             w3 = w3.replace(j,'')
#         else:
#             pass  
#     c+=1
# print(w3)    
# if len(w3) == 0:
#     print("Yes, It's Anagram") # will come 
# else:
#     print("No, It's not")    


# Flatten nested list
# l1 = [1, [2, [3, 4], 5], 6]
# l2 = []

# def flatten_list(lst):
#     for i in lst:
#         if isinstance(i, list):
#             flatten_list(i)
#         else:
#             l2.append(i)
# flatten_list(l1)
# print(l2)  # [1, 2, 3, 4, 5, 6]


# Find duplicate elements
# l1 = [1, 2, 3, 2, 4, 5, 1]
# l2 = []

# for i in l1:
#     c = 0
#     for j in l1:
#         if i==j:
#             c+=1
#     if c > 1:
#         if i not in l2:
#             l2.append(i)        
# print(l2)  # [1,2] 


# Longest Word in Sentence
# sen = "Python is very powerful languages"
# longest_word = max(sen.split(), key=len)
# print(longest_word) # languages


# Rotate list (two step)
# l1 = [1, 2, 3, 4, 5]
# k = 2
# (with slicing)
# rotated = l1[-k:] + l1[:-k]
# print(rotated) # [4, 5, 1, 2, 3] 
# without slicing
# for _ in range(k):
#     l1.insert(0,l1.pop())
# print(l1)  # [4, 5, 1, 2, 3]


# Find Second Largest (Without sort)
# l1 = [10, 20, 4, 45, 99]
# l1.remove(max(set(l1)))
# print(max(l1)) # 45

# Group Anagrams
# l1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
# anagrams = {}

# for word in l1:
#     key = ''.join(sorted(word))
#     if key in anagrams:
#         anagrams[key].append(word)
#     else:
#         anagrams[key] = [word]  
# l2 = list(anagrams.values())
# print("grouped anagram lists are ",l2) # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]  

