from collections import deque

class DonutMaze:
    def __init__(self, fname):
        with open(fname, "r") as f:
            mazelines = [line.rstrip('\n') for line in f.readlines()]
        self.oportals = {}
        #outer portals
        for i, ch in enumerate(mazelines[0]):
            if 'A' <= ch <= 'Z':
                self.oportals[ch + mazelines[1][i]] = (2,i)
        for j, row in enumerate(mazelines):
            if 'A' <= row[0] <= 'Z':
                self.oportals[row[0] + row[1]] = (j,2)
            if 'A' <= row[-2] <= 'Z':
                self.oportals[row[-2] + row[-1]] = (j,len(row)-3)
        for i, ch in enumerate(mazelines[-2]):
            if 'A' <= ch <= 'Z':
                self.oportals[ch + mazelines[-1][i]] = (len(mazelines)-3,i)

        #find inside
        istart = 3
        while mazelines[istart][istart] == '#' or mazelines[istart][istart] == '.':
            istart += 1

        self.iportals = {}
        for i, ch in enumerate(mazelines[istart][istart:-istart]):
            if 'A' <= ch <= 'Z':
                self.iportals[ch + mazelines[istart + 1][istart + i]] = (istart - 1, istart + i)
        for j, row in enumerate(mazelines[istart:-istart]):
            if 'A' <= row[istart] <= 'Z':
                self.iportals[row[istart] + row[istart + 1]] = (istart + j, istart - 1)
            if 'A' <= row[-(istart + 1)] <= 'Z':
                self.iportals[row[-(istart + 2)] + row[-(istart + 1)]] = (istart + j, len(row) - istart)
        for i, ch in enumerate(mazelines[-(istart + 1)][istart:-istart]):
            if 'A' <= ch <= 'Z':
                self.iportals[mazelines[-(istart + 2)][istart + i] + ch] = (len(mazelines) - istart, istart + i)

        self.mazemap = mazelines

    def search(self):
        bfs = deque()
        visited = set()

        dirs = [(0,1), (1,0), (0,-1), (-1,0)]

        if "AA" in self.oportals:
            bfs.append((*self.oportals["AA"], 0))
        else:
            bfs.append((*self.iportals["AA"], 0))

        if "ZZ" in self.oportals:
            tgt = self.oportals["ZZ"]
        else:
            tgt = self.iportals["ZZ"]

        while len(bfs) > 0:
            j, i, dist = bfs.popleft()
            if (j, i) == tgt:
                return dist
            visited.add((j,i))
            for direc in dirs:
                nj, ni = j + direc[0], i + direc[1]
                if (nj, ni) in visited:
                    continue
                mazechar = self.mazemap[nj][ni]
                if mazechar == '.':
                    bfs.append((nj,ni,dist+1))
                elif 'A' <= mazechar <= 'Z':
                    if direc == (0,-1) or direc == (-1,0):
                        pkey = self.mazemap[nj + direc[0]][ni + direc[1]] + mazechar
                    else:
                        pkey = mazechar + self.mazemap[nj + direc[0]][ni + direc[1]]
                    if pkey == "AA" or pkey == "ZZ":
                        continue
                    if (j, i) == self.oportals[pkey]:
                        bfs.append((*self.iportals[pkey], dist + 1))
                    else:
                        bfs.append((*self.oportals[pkey], dist + 1))
        return -1

maze = DonutMaze("inputday20.txt")
print(maze.oportals)
print(maze.iportals)

print(maze.search())