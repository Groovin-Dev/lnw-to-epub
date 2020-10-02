from parsers import LightNovelWorld

def main():
    lnw_parser = LightNovelWorld()

    #print(lnw_parser.get_updates())
    print(lnw_parser.get_novel('sss-class-suicide-hunter').get_info())


if __name__ == '__main__':
    main()