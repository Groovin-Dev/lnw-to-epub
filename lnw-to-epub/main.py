from parsers import LightNovelWorld

def main():
    lnw_parser = LightNovelWorld()

    #print(lnw_parser.get_updates())
    print(lnw_parser.get_chapters('trash-of-the-counts-family-wn'))


if __name__ == '__main__':
    main()