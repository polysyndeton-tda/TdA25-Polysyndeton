a = """ "n": [rowIndex - dist, columnIndex]
            "ne":[rowIndex - dist, columnIndex + dist]
            "e": [rowIndex, columnIndex + dist]
            "se": [rowIndex + dist, columnIndex + dist]
            "s": [rowIndex + dist, columnIndex]
            "sw":[rowIndex + dist, columnIndex - dist]
            "w": [rowIndex, columnIndex - dist]
            "nw": [rowIndex - dist, columnIndex -dist]""".split("\n")

k = [x.split(":")[0].strip().replace('"', "") for x in a]
print(k)
