with open("day3.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    def compute_val(data):
        if not data:
            return None, None

        bits = []
        for _ in data[0]:
            bits.append({})
        for bit in data:
            for i in range(len(bit)):
                ch = bit[i]        
                bits[i][ch] = bits[i].get(ch, 0) + 1 

        most_common = ""
        least_common = ""
        for bit in bits:
            most_common += "1" if bit.get('1', 0) >= bit.get('0', 0) else "0"
            least_common += "0" if bit.get('0', 0) <= bit.get('1', 0) else "1"
        return most_common,least_common

    a,b = compute_val(data)
    print(f"p1 =",int(a,2)*int(b,2))

    # oxy gen
    oxy = None
    co2 = None
    oxygen_data = data.copy()
    co2_data = data.copy()
    most, least = compute_val(oxygen_data)
    for i in range(len(data[0])):
        oxygen_data = list(filter(lambda x: x[i] == most[i], oxygen_data))
        co2_data = list(filter(lambda x: x[i] == least[i], co2_data))
        if not oxy and len(oxygen_data) == 1:
            oxy = oxygen_data[0]
        if not co2 and len(co2_data) == 1:
            co2 = co2_data[0]
        if oxy and co2:
            break
        most, _ = compute_val(oxygen_data)
        _, least = compute_val(co2_data)
        
    print (f"p2 = {int(oxy,2) * int(co2, 2)}")