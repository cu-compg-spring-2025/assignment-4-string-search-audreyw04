def get_shift_match_table(P):
    m = len(P)
    shift_match_table = {}

    for shift in range(m - 1, 0, -1):
        p_1 = m - 1
        p_2 = m - shift - 1

        while p_2 >= 0:
            if P[p_2] == P[p_1]:
                p_1 -= 1
                p_2 -= 1
                if p_2 < 0:
                    shift_match_table[shift] = m - shift
                    break
            else:
                shift_match_table[shift] = m - shift - p_2 - 1
                break
    shift_match_table[m] = 0
    return shift_match_table

def get_good_suffix_table(P):
    m = len(P)

    good_suffix_table = {}
    good_suffix_table[0] = 1

    shift_match_table = get_shift_match_table(P)

    for i in range(1, m + 1):
        good_suffix_table[i] = i + m

    for i in range(m, 0, -1):
        if shift_match_table[i] > 0:
            good_suffix_table[shift_match_table[i]] = i + shift_match_table[i]

    for i in range(m, 0, -1):
        if shift_match_table[i] + i == m:
            for j in range(shift_match_table[i] + 1, m+1):
                good_suffix_table[j] = min(good_suffix_table[j], j + i)
    return good_suffix_table

def get_bad_char_table(P):
    bad_char_table = {}
   
    m = len(P)

    #make table with  -1 for all values 
    for i in range(256):
        bad_char_table[chr(i)] = -1
    
    #populate with the furtheest right occurence of each character in P
    for i in range(m):
        bad_char_table[P[i]] = i

    return bad_char_table


def boyer_moore_search(T, P):
    occurrences = []
    n = len(T)
    m = len(P)

    #process tables
    bct = get_bad_char_table(P)
    gst = get_good_suffix_table(P)

    #store shift
    s = 0

    while s <= n-m:
        j = m-1

        #compare right to left
        while j>= 0 and P[j] == T[s+j]:
            j-=1 #shift left

        if j <0:
            #use good suffix rule when match found
            occurrences.append(s)
            s+=gst[0]

        else:
            bcshift = j - bct.get(T[s+j], -1)
            gsshift = gst[j] if j<m else 1
            
            #move by max shift
            s += max(bcshift, gsshift) 

    return occurrences
