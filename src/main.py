from textnode import TextNode, TextType
from file_utils import remove_dir, create_dir, copy_tree


def main():
    tn = TextNode("Hello", TextType.TEXT, "https://google.com")
    print(tn)
    remove_dir("public")
    copy_tree("static","public")

if __name__ == "__main__":
    main()