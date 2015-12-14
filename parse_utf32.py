import fileinput
import ujson as json
import pickle
from collections import defaultdict

emoji_dict_utf32 = pickle.load(open("emoji_dict_utf-32.pkl","r"))

# Initialize counters and results dicts
used_emojis = defaultdict(int)
tweets_with_this_emoji = defaultdict(int)
total_emoji_used = 0
total_tweets_with_emoji = 0
total_tweets = 0
emoji_per_tweet = defaultdict(int)

# Start reading in Tweets and counting Emoji!!!!!!!------------------------------------
for line in fileinput.FileInput():
    try:
        body = json.loads(line)["body"].encode('utf-32')
    except (ValueError, KeyError):
        continue
    len_body = len(body) 
    body_chars = [body[i:i+4] for i in range(0,len_body,4)] 
    j = 0
    emoji_in_tweet = []
    len_body_chars = len(body_chars)
    while j < len_body_chars:
        char = body_chars[j]
        # if it's an emoji and it's in the dict
        if char in emoji_dict_utf32:
            # set emoji_found to the character we just read
            emoji_found = char
            # get the info from the emoji dict
            char_info = emoji_dict_utf32[char]
            look_for_modifiers = char_info["look_for_modifiers"]
            found_a_modifier = False
            # see if it has modifiers around it so we can count both chars as one
            if look_for_modifiers:
                modifiers_possible_before = char_info["modifiers_possible_before"]
                modifiers_possible_after = char_info["modifiers_possible_after"]
                # check for after modifiers
                if (j != len_body_chars - 1) and len(modifiers_possible_after) > 0:
                    if body_chars[j+1] in modifiers_possible_after:
                        emoji_found = char + body_chars[j+1]
                        # Debugging
                        #print char, [char]
                        #print body_chars[j+1], [body_chars[j+1]]
                        #print emoji_found
                        #print "***************"
                        j += 1 # skip the next character because we found it
                        look_for_modifiers = False
                        found_a_modifier = True
                # check for before modifiers
                if (j != 0) and look_for_modifiers and len(modifiers_possible_before) > 0:
                    if body_chars[j-1] in modifiers_possible_before:
                        emoji_found = body_chars[j-1] + char
                        found_a_modifier = True
                        # Debugging
                        #print body_chars[j-1], [body_chars[j-1]]
                        #print char, [char]
                        #print emoji_found
                        #print "***************"
            if char_info["can_stand_alone"] or found_a_modifier:    
                emoji_in_tweet.append(emoji_found)
        j += 1
    len_emoji_in_tweet = len(emoji_in_tweet)
    for emoji in emoji_in_tweet:
        used_emojis[emoji] += 1
    for emoji in set(emoji_in_tweet):
        tweets_with_this_emoji[emoji] += 1
    emoji_per_tweet[len_emoji_in_tweet] += 1
    total_emoji_used += len_emoji_in_tweet
    total_tweets_with_emoji += int(bool(len_emoji_in_tweet))
    total_tweets += 1
    
    # Debugging
    #if len(emoji_in_tweet) == 0:
    #    print body
    #print body
    #for x,y in used_emojis.items():
    #    print x, y
    #print total_emoji_used
    #print total_tweets_with_emoji
    #print total_tweets
    #print "************************************************************"

print "************************************************************"
print "used_emojis"
for emoji,count in sorted(used_emojis.items(), key = lambda x:x[1], reverse = True)[0:10]:
    print emoji.decode("utf-32").encode("utf-8"), count
print ".\n.\n.\n"
for emoji,count in sorted(used_emojis.items(), key = lambda x:x[1], reverse = True)[-10:]:
    print emoji.decode("utf-32").encode("utf-8"), count
print "tweets_with_this_emoji"
for emoji,count in sorted(tweets_with_this_emoji.items(), key = lambda x:x[1], reverse = True)[0:10]:
    print emoji.decode("utf-32").encode("utf-8"), count
print ".\n.\n.\n"
for emoji,count in sorted(tweets_with_this_emoji.items(), key = lambda x:x[1], reverse = True)[-10:]:
    print emoji.decode("utf-32").encode("utf-8"), count
print "emoji_per_tweet"
for count, num_tweets in sorted(emoji_per_tweet.items())[0:10]:
    print count, num_tweets
print "Total emoji used: {}".format(total_emoji_used)
print "Total Tweets with emoji: {}".format(total_tweets_with_emoji)
print "Total Tweets processed: {}".format(total_tweets)
print "************************************************************"