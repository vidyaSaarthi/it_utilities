from pdf_to_jpg import start_pdf_to_jpg
from jpg_to_pdf import start_jpg_to_pdf
from compress_jpg import start_compress_jpg
from compress_pdf import start_compress_pdf
def main_menu():
    while True:
        print("\n" + "=" * 30)
        print("   PYTHON PDF/IMAGE TOOLKIT   ")
        print("=" * 30)
        print("1. Convert PDF -> JPG")
        print("2. Convert JPG -> PDF")
        print("3. Compress JPG")
        print("4. Compress PDF")
        print("5. Quit")

        choice = input("\nEnter your choice: ").lower()

        if choice == '1':
            start_pdf_to_jpg()
        elif choice == '2':
            start_jpg_to_pdf()
        elif choice == '3':
            start_compress_jpg()
        elif choice == '4':
            start_compress_pdf()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()