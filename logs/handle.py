def handle_log():
    log = open("server.log","r")
    content = log.readlines()
    l = len(content)
    ans = []
    for i in range(2, l):
        if ("2023" in content[i]):
            info = {}
            info['time'] = content[i][:23]
            object = content[i][23:].split()
            info['type'] = object[0][1:-1]
            t = ""
            for j in range(1, len(object)):
                t = t + " " + object[j]
            info['text'] = t
            ans.append(info)
        else:
            continue
    log.close()
    print(ans)
    return ans
handle_log()