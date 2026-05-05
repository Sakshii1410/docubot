from rag import process_pdf_and_answer
import os

def main():
    print("=" * 40)
    print("     DocuBot — PDF Question Answering")
    print("=" * 40)
    
    pdf_path = input("\nEnter PDF filename (must be in uploads/ folder): ")
    full_path = os.path.join("uploads", pdf_path)
    
    if not os.path.exists(full_path):
        print(f"Error: File not found at {full_path}")
        return
    
    print("\nPDF loaded! You can now ask questions.")
    print("Type 'exit' to quit.\n")
    
    while True:
        query = input("Your question: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        answer = process_pdf_and_answer(full_path, query)
        print(f"\nDocuBot: {answer}\n")
        print("-" * 40)

if __name__ == "__main__":
    main()