import heapq

with open("input.txt") as f:
    n, m = map(int, f.readline().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, f.readline().split())
        adj[u].append((v, w))
        adj[v].append((u, w))

INF = 10**30
dist = [INF] * (n + 1)
dist[1] = 0

heap = [(0, 1)]

while heap:
    d, v = heapq.heappop(heap)
    if d > dist[v]:
        continue
    if v == n:
        break
    for to, w in adj[v]:
        nd = d + w
        if nd < dist[to]:
            dist[to] = nd
            heapq.heappush(heap, (nd, to))
with open("output.txt", "w") as f:
    f.write(str(dist[n]))
