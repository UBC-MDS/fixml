from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def main():
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a world class Machine Learning engineer."),
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    output_str = chain.invoke({"input": "Hello LLM World! I can't wait to use you to write a test suite for my ML pipeline!"})

    print(output_str)


if __name__ == "__main__":
    main()
