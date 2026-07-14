def merge_page_windows(pages, window=1):
    merged = []
    print(len(pages))
    for i in range(len(pages)):
        texts = []

        for j in range(i - window, i + window + 1):
            if 0 <= j < len(pages):
                texts.append(pages[j])
        merged.append('\n'.join(texts))

    return merged