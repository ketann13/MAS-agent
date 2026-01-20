from agents.planner_agent import handle_student_input

print("\n🎓 AI Learning Memory Agent\n")

while True:
    text = input("Enter your doubt or mistake (or type exit): ")
    if text.lower() == "exit":
        break

    concept = input("Which concept is this related to? ")

    result = handle_student_input(text, concept, correct=False)

    print("\n🧠 Similar Past Mistakes:")
    for e in result["similar_mistakes"]:
        print("-", e["text"])

    print("\n📌 Weak Concepts:", result["weak_concepts"])
    print("\n🔍 Why this was suggested:")
for e in result["similar_mistakes"]:
    print(f"- Past mistake related to: {e['concept']}")


    print("\n📚 Recommended Resources:")
    for r in result["resources"]:
        print("-", r["text"])

    print("\n🎯 Advice:")
    for a in result["advice"]:
        print("-", a)

    print("\n" + "="*50 + "\n")
