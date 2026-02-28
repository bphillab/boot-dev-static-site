from textnode import TextNode, TextType


def main():
    tn = TextNode("Hello", TextType.TEXT, "https://google.com")
    print(tn)

if __name__ == "__main__":
    main()