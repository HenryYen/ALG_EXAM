def lcs(s1, s2):
    n = len(s1)
    m = len(s2)
    dp = [ [0] * (m+1) for i in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])      
    return dp
        
def trace(dp, ans, path, link,  s1, s2, i, j):
    link.add(i-1, j-1)
    if dp[i][j] == 1:
        ans.add(link.clone())
        return 
    for e in path[i][j]:
        trace(dp, ans, path, link,  s1, s2, e[0], e[1])
        link.pop()
        
        
class Link:
    def __init__(self):
        self.record = []
    def add(self, i, j):
        self.record.append((i, j))
    def pop(self):
        self.record.pop()
    def is_equal(self, link):
        if len(link.record) != len(self.record):
            return False
        for i in self.record:
            idx = self.record.index(i)
            if i != link.record[idx]:
                return False
        return True
    def clone(self):
        tmp = Link()
        tmp.record = self.record[:]
        return tmp
    def print_link(self):
        print(self.record)
            
            
class Answer:
    def __init__(self):
        self.record = []
    def add(self, link):
        for i in self.record:
            if i.is_equal(link):
                return
        self.record.append(link)
    def print_ans(self, s1):
        out = []
        for l in self.record:
            tmp_s = ''
            for pos in l.record:
                tmp_s += s1[pos[0]]
            out.append(tmp_s[::-1])
        out.sort()
        out.insert(0, str(len(out[0])) +' '+ str(len(out)))
        for e in out:
            print(e)
        return out
        
def write_result(out, name):
    with open(name, 'w') as f:
        for line in out:
            f.write(line+'\n')
        
def get_tracepath(dp, s1, s2):
    n = len(s1)
    m = len(s2)
    path = [[[] for g in range(m+1)] for _ in range(n+1)]
    select = [[False]*(m+1) for _ in range(n+1)]
    
    for i in range(n+1):
        for j in range(m+1):
            if s1[i-1] == s2[j-1] and dp[i][j] == dp[n][m]:
                 select[i][j] = True

    for i in range(n, 0, -1):
        for j in range(m, 0, -1):
            if select[i][j]:
                for x in range(1, i):
                    for y in range(1, j):
                        if s1[x-1] == s2[y-1] and dp[x][y] == dp[i][j] - 1:
                            path[i][j].append((x, y))
                            select[x][y] = True
    return path
    
def read_file(name):
    out = []
    with open(name, 'r') as f:
        for line in f:
            out.append(line.rstrip('\n'))
    return (out[0], out[1])
    
def validate(name, result):
    out = []
    with open(name, 'r') as f:
        for line in f:
            out.append(line.rstrip('\n'))
    print(result == out)
    
            
if __name__ == '__main__':
    (s1, s2) = read_file('./LCS-5.txt')
    n = len(s1)
    m = len(s2)
    
    ans = Answer()
        
    dp = lcs(s1, s2)
    path = get_tracepath(dp, s1, s2)
    for i in range(n+1):
        for j in range(m+1):
            if dp[i][j] == dp[n][m]:
                trace(dp, ans, path, Link(), s1, s2, i, j)
    result = ans.print_ans(s1)
    write_result(result, "./LCS5.txt")
    #validate('./298068_Midterm Test Cases-20161104T051253Z/output/LCS-5.txt', result)
    

    
    
"""

    s1 = 'PWZGIFE'
    s2 = 'IPPHE'

範例輸入 1

PUWBVNUCUUESSJUNSVHE

CIHSIIDWCSUTOSWJHTOB

 範例輸出 1

6 8

CSSUSH

WCSSJH

WCSUSH

WCSUSH

WCUSJH

WCUSJH

WCUSJH

WCUSJH



 範例輸入 2

QHCCDETMFPPWZGIFEFUA

GZXPAWWOOCZEMBIPHECM

 範例輸出 2

5 10

CEMIE

CEMIE

CEMPE

CEMPE

CEMPE

CEMPE

PWZIE

PWZIE

PWZIE

PWZIE
"""