
from src.main import load_product_config
from src.prd_generator import generate_prd, save_prd


def main():
    product = load_product_config()

    content = generate_prd(product)
    output_path = save_prd(content)

    print("PRD 初稿生成成功！")
    print(f"文件位置：{output_path}")


if __name__ == "__main__":
    main()
