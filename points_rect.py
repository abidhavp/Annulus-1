def sum(a, b):
    return a + b

class Rect:

    def __init__(self, pts_list):
        
        self.mx = int(1e6 + 10)

        self.vals = []
        self.L = []
        self.R = []
        self.root = self.create(self.mx)
        pts_map = {}
        for (x, y) in pts_list:

            if x not in pts_map:
                pts_map[x] = []

            pts_map[x].append(y)

        prev_ind = self.root

        self.ind_map = {}

        for x in range(int(1e6 + 1)):
            if (x in pts_map):
                pts_map[x].sort()
                for y in pts_map[x]:
                    prev_val = self.sum_query(prev_ind, y, y + 1, self.mx)
                    prev_ind = self.setter(prev_ind, y, prev_val + 1, self.mx)
            self.ind_map[x] = prev_ind

    
    def get_pts(self, x, y):
        if (x <= 0 or y <= 0):
            return 0
        ans = self.sum_query(self.ind_map[x], 0, y + 1, self.mx)
        return ans

    def get_rect(self, x1, y1, x2, y2):

        return ((self.get_pts(x2, y2) - self.get_pts(x1 - 1, y2) - self.get_pts(x2, y1 - 1) + self.get_pts(x1 - 1, y1 - 1)))


    def create(self, n):
        """create a persistant segment tree of size n"""

        ind = len(self.vals)
        self.vals.append(0)

        self.L.append(-1)
        self.R.append(-1)

        if n == 1:
            self.L[ind] = -1
            self.R[ind] = -1
        else:
            mid = n // 2
            self.L[ind] = self.create(mid)
            self.R[ind] = self.create(n - mid)
        return ind


    def setter(self, ind, i, val, n):
        """set set[i] = val for segment tree ind, of size n"""

        ind2 = len(self.vals)
        self.vals.append(0)

        self.L.append(-1)
        self.R.append(-1)

        if n == 1:
            # print(ind2, ind, i, n, "ind ind2")
            self.vals[ind2] += val
            return ind2

        mid = n // 2
        if i < mid:
            self.L[ind2] = self.setter(self.L[ind], i, val, mid)
            self.R[ind2] = self.R[ind]
        else:
            self.L[ind2] = self.L[ind]
            self.R[ind2] = self.setter(self.R[ind], i - mid, val, n - mid)
        self.vals[ind2] = sum(self.vals[self.L[ind2]], self.vals[self.R[ind2]])
        return ind2


    def sum_query(self, ind, l, r, n):
        """find mimimum of set[l:r] for segment tree ind, of size n"""

        if l == 0 and r == n:
            # print(l, r, n, ind, self.vals[ind], "l r n ind")
            return self.vals[ind]
        mid = n // 2
        if r <= mid:
            return self.sum_query(self.L[ind], l, r, mid)
        elif mid <= l:
            return self.sum_query(self.R[ind], l - mid, r - mid, n - mid)
        else:
            return sum(self.sum_query(self.L[ind], l, mid, mid), self.sum_query(self.R[ind], 0, r - mid, n - mid))


if __name__ == "__main__":
    pts_list = [(1, 5), (2, 5), (4, 5), (2, 2), (1, 1), (6, 7)]
    obj = Rect(pts_list)
    while (True):
        x1 = int(input())
        y1 = int(input())
        x2 = int(input())
        y2 = int(input())
        print(obj.get_rect(x1, y1, x2, y2))