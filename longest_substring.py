#Practice Problem 1 (Sliding Window • Strings)

#Longest substring with at most k distinct characters.
#Input: s: str, k: int. Output: length (int).
#Edge cases: k=0 → 0; repeated chars; unicode OK.

#Solution (O(n))

from collections import Counter


def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    if k == 0: 
        return 0
    left = 0
    freq = Counter()
    print (f"initial size of counter: {len(freq)}")
    #print (len(freq))
    best = 0
    for right, ch in enumerate(s):
        freq[ch] += 1
        print(f"current size of counter: {len(freq)}")
        #print (len(freq)) 
        while len(freq) > k:
            freq[s[left]] -= 1
            if freq[s[left]] == 0:
                del freq[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best

print(length_of_longest_substring_k_distinct("abc",3))


