# testing the nautical almanac values
import ST as ST
p = [0.0231, 0.3058, -0.4001]
Z = [267.2721, 151.6809, 358.9823]

ans = []

[ans.append(p[i]*ST.sind(Z[i])) for i in range(0, len(p))]
ans = sum(ans)
print ans
