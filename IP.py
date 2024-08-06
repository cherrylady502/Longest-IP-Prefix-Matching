class TrieNode:
    def __init__(self):
        self.child = [None, None]
        self.interface = -1


def create_node():
    return TrieNode()


def insert(root, a, b, c, d, m, interf_nr):
    current = root
    subnet = [a, b, c, d]
    nr_bits = 0
    for i in range(4):
        for j in range(7, -1, -1):
            bit = (subnet[i] >> j) & 1
            nr_bits += 1
            if current.child[bit] is None and nr_bits <= m:
                current.child[bit] = create_node()
                if nr_bits != 32:
                    current = current.child[bit]
            else:
                if nr_bits > m:
                    current.interface = interf_nr
                if current.child[bit] is not None and nr_bits <= m and nr_bits != 32:
                    current = current.child[bit]
        if nr_bits == 32:
            current.interface = interf_nr


def free_trie(root):
    if root is None:
        return
    for i in range(2):
        free_trie(root.child[i])


def main():
    n = int(input())
    root = create_node()
    mask_zero = -1

    for _ in range(n):
        ip_mask_interface = input().strip().split()
        ip_part, mask = ip_mask_interface[0].split('/')
        ip = list(map(int, ip_part.split('.')))
        ip1, ip2, ip3, ip4 = ip
        mask = int(mask)
        interface = int(ip_mask_interface[1])
        if mask == 0:
            mask_zero = interface
        else:
            insert(root, ip1, ip2, ip3, ip4, mask, interface)

    m = int(input())
    for _ in range(m):
        ip2 = input().strip()
        copy = root
        length = len(ip2)
        index = 0
        match = 0
        ip = 0
        result = 0
        last_interface = -2

        while index <= length:
            if index == length or ip2[index] == '.':
                for k in range(7, -1, -1):
                    bit = (ip >> k) & 1
                    if copy.child[bit] is not None:
                        match += 1
                        if copy.interface != -1:
                            last_interface = copy.interface
                        if match != 32:
                            copy = copy.child[bit]
                    else:
                        if match == 0:
                            result = mask_zero
                        else:
                            if copy.interface != -1:
                                result = copy.interface
                            else:
                                result = last_interface
                        index = length
                        break
                if match == 32:
                    result = copy.interface
                ip = 0
                index += 1
            else:
                ip = ip * 10 + int(ip2[index])
                index += 1
        print(result)

    free_trie(root)


if __name__ == "__main__":
    main()
