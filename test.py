with open("data.tsv", "r", encoding="utf-8") as f, open("url.txt", "w", encoding="utf-8") as g:
    d = f.readline()
    cnt = 0
    while d:
        line = d.replace('\n', '').split('\t')
        data = line[-1]
        g.write("http://222.186.42.181:8084/file?url=" + data + "&topk=10\n")
        cnt += 1
        d = f.readline()

    f.close()
    g.close()
