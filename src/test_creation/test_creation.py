#!/usr/bin/env python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def main():
    """This is the CLI entry point."""
    # TODO: Flesh out this! This is working on the older branch and refactoring had not been taken placed yet.
    # TODO: Calls to analyze/export should be written here via Fire.

    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a world class Machine Learning engineer."),
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    output_str = chain.invoke({"input": "Hello LLM World! I can't wait to use you to write a test suite for my ML pipeline!"})

    print(output_str)
