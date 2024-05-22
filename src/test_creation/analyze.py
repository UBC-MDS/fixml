import json
import pprint
from collections import defaultdict

import fire
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
from langchain_community.document_loaders import DirectoryLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
import os
import pypandoc

from modules.checklist.checklist import Checklist, ChecklistFormat
from modules.code_analyzer.repo import Repository

load_dotenv()


class TestEvaluator:
    def __init__(self, repo_path=None):
        self.repo = None
        self.test_fps = []  # test file paths
        self.test_dir_path = ''  # test dir path # FIXME: required by `load_test_dir`
        self.py_splits = []

        # FIXME: Tony's "Checklist - After Engineering" version
        self.checklist = """
            Each test function should have a clear, descriptive name that accurately reflects the test's purpose and the specific functionality or scenario it examines.
            Each test should focus on a single scenario, using only one set of mock data and testing one specific behavior or outcome to ensure clarity and isolate issues.
            Assertions within tests should be focused and narrow. Ensure you are only testing relevant behaviors of complex objects and not including unrelated assertions.
            Keep any modifications to objects and the corresponding assertions close together in your tests to maintain readability and clearly show the cause-and-effect relationship.
            Ensure that data-loading functions correctly load files when they exist and match the expected format, handle non-existent files appropriately, and return the expected results.
            Verify that functions for saving data and figures perform write operations correctly, checking that the operation succeeds and the content matches the expected format.
            Ensure all data files are non-empty and contain the necessary data required for further analysis or processing tasks.
            Verify that the data to be ingested matches the format expected by processing algorithms (like pd.DataFrame for CSVs or np.array for images) and adheres to the expected schema.
            Check that data files are free from unexpected null values and identify any outliers that could affect the analysis. Tests should explicitly state if null values are part of expected data.
            Test that a fixed input to a function or model produces the expected output, focusing on one verification per test to ensure predictable behavior.
            Confirm that the model accepts inputs of the correct shapes and types and produces outputs that meet the expected shapes and types without any errors.
            For parametric models, ensure that the model's weights update correctly per training iteration. For non-parametric models, verify that the data fits correctly into the model.
            Ensure the shape of the model's output aligns with the expected structure based on the task, such as matching the number of labels in a classification task.
            Verify that the model's output values are appropriate for its task, such as outputting probabilities that sum to 1 for classification tasks.
            If using gradient descent for training, verify that a single gradient step on a batch of data results in a decrease in the model's training loss.
            Confirm that there is no leakage of data between training, validation, and testing sets, or across cross-validation folds, to ensure the integrity of the splits.
        """
        self.system_message = []
        self.model = 'gpt-3.5-turbo'
        self.temperature = 0
        self.chain = None

        # self.evaluation_message = """
        #     Your task is to answer each question in the checklist using only the provided test functions.
        #     If an answer to the question is provided, it must be annotated with a citation of the test function(s) in the Observation session.
        #     Then, decide the completion score in a fraction format based on your answers. The denominator should be the number of checklist items.
        #     Desired format:
        #         Checklist Evaluation:
        #             ID:
        #             Title:
        #             Requirement:
        #             Observation:
        #             Evaluation: Satisfied/Partially Satisfied/Not Satisfied
        #             Score: (1 for Satisfied / 0.5 for Partially Satisfied / 0 for Not Satisfied)
        #         Completion Score: Number of satisfied requirements/Number of requirements
        #             Number of satisfied requirements:
        #             Number of partially satisfied requirements:
        #             Number of not satisfied requirements:
        # """
        self.evaluation_message = """
            Your task is to answer each question in the checklist using only the provided test functions.
            If an answer to the question is provided, it must be annotated with a citation of the test function(s) in the Observation session.
            Output a JSON format:
                [{
                    "ID": 
                    "Title":
                    "Requirement":
                    "Observation":
                    "Functions": [ ... ]
                    "Evaluation": Satisfied/Partially Satisfied/Not Satisfied
                    "Score": (1 for Satisfied / 0.5 for Partially Satisfied / 0 for Not Satisfied)
                }]
        """

        self.evaluation_result = None
        self.evaluation_report = None

        if repo_path is not None:
            self.load_repo(repo_path)

    def load_repo(self, repo_path):
        self.repo = Repository(repo_path)
        self.test_fps = self.repo.list_test_files()['Python']

    def load_test_file(self, file_path, overwrite=True):
        loader = PythonLoader(file_path)
        py = loader.load()
        py_splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(py)

        if overwrite:
            self.py_splits = py_splits

        return py_splits

    # def load_all_test_files(self):
    #     self.py_splits = []
    #     for fp in self.test_fps:
    #         self.py_splits += self.load_test_file(fp, overwrite=False)

    def load_test_dir(self, dir_path):
        self.test_dir_path = dir_path

        loader = DirectoryLoader(
            dir_path,
            glob="**/*.py",
            show_progress=True,
            loader_cls=PythonLoader
        )
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        self.py_splits = text_splitter.split_documents(docs)

    def load_checklist(self, checklist_path):
        raw_checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)

        checklist = []
        for item in raw_checklist.get_all_tests():
            checklist.append({
                'ID': item['ID'],
                'Title': item['Title'],
                'Requirement': item['Requirement']
            })

        self.checklist = json.dumps(checklist).replace('{', '[').replace('}', ']')

    def init_system_message(self):
        if len(self.checklist) == 0:
            # self.load_checklist()
            raise ValueError("Checklist is empty, make sure you have configured the checklist loader right!")

        self.system_message = [
            ("system",
             "You are a senior machine learning engineer who specializes in performing Machine Learning system testing. Extract and analyze the test functions from the codes:\n\n{context}"),
            ("system",
             f"Here is the Machine Learning system testing checklist delimited by triple quotes '''{self.checklist}'''")
        ]

    def init_chain(self, system_message=None, model=None):
        if system_message is None:
            if len(self.system_message) == 0:
                self.init_system_message()
            system_message = self.system_message
        else:
            self.system_message = system_message

        if model is None:
            model = self.model
        else:
            self.model = model

        prompt = ChatPromptTemplate.from_messages(
            system_message + [
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        chat = ChatOpenAI(model=model, temperature=self.temperature)

        chain = create_stuff_documents_chain(chat, prompt)
        self.chain = chain
        return chain

    def get_ai_response(self, message, context, history=None):
        if self.chain is None:
            self.init_chain()

        if history is None:
            history = ChatMessageHistory()

        history.add_user_message(message)

        response = self.chain.invoke({
            "context": context,
            "messages": history.messages
        })
        history.add_ai_message(response)

        return response, history

    def get_evaluation_response(self, py_splits=None):
        if py_splits is None:
            py_splits = self.py_splits

        return self.get_ai_response(
            message=self.evaluation_message,
            context=py_splits
        )

    # FIXME: combine evaluation
    # to be tested
    def extract_json(self, response, start='[', end=']'):
        start_idx = response.index(start)
        end_idx = response[::-1].index(end)
        if end_idx == 0:
            string = response[start_idx:]
        else:
            string = response[start_idx:-end_idx]
        return json.loads(string)

    def evaluate(self, on_file=True, verbose=False):
        result = []
        if on_file:
            for fp in tqdm(self.test_fps):
                if verbose:
                    print(fp)
                self.load_test_file(fp)
                if verbose:
                    print(f"# splits: {len(self.test_fps)}")
                response, history = self.get_evaluation_response()  # FIXME: it sometimes tests only part of the checklist items
                report = self.extract_json(response)
                for item in report:
                    item['file'] = fp
                result += [{
                    'file': fp,
                    'report': report,
                    'history': history
                }]
        else:
            self.load_test_dir(self.test_dir_path)
            response, history = self.get_evaluation_response()
            report = self.extract_json(response)
            for item in report:
                item['file'] = self.test_dir_path
            result += [{
                'file': self.test_dir_path,
                'report': report,
                'history': history
            }]

        self.evaluation_result = result
        return

    def get_completeness_score(self, score_format='fraction', verbose=False):
        report_df = pd.DataFrame(self.evaluation_result)['report'].explode('report').apply(pd.Series)
        report_df = report_df.rename(columns={"file": "File Path"})
        report_df['Function References'] = report_df[['File Path', 'Functions']].to_dict(orient='records')
        report_df['Observation'] = '(' + report_df['File Path'].apply(lambda x: os.path.split(x)[-1]) + ') ' + report_df['Observation']
        report_df = report_df.groupby(['ID', 'Title']).agg({
            'Requirement': ['max'],
            'Score': ['max', 'count'],
            'Observation': [list],
            'Function References': [list],
        })
        report_df.columns = ['Requirement', 'is_Satisfied', 'n_files_tested', 'Observations', 'Function References']
        self.evaluation_report = report_df.reset_index()

        if score_format == 'fraction':
            score = f"{report_df['is_Satisfied'].sum()}/{report_df['is_Satisfied'].count()}"
        elif score_format == 'number':
            score = report_df['is_Satisfied'].sum()/report_df['is_Satisfied'].count()

        if verbose:
            print("Report:")
            print(report_df)
            print()
            print(f'Score: {score}')
            print()
        return score

    # TBC_FIXME From checklist.py. To be refactored 
    def _get_md_representation(self, content: dict, curr_level: int):
        repeated_col = [k for k, v in content.items() if isinstance(v, list)]

        # print out header for each item
        md_repr = '#' * curr_level
        if 'ID' in content.keys():
            md_repr += f" {content['ID']}"
        if 'Title' in content.keys():
            md_repr += f" {content['Title']}\n\n"
        elif 'Topic' in content.keys():
            md_repr += f" {content['Topic']}\n\n"

        # print out non-title, non-repeated items
        for k, v in content.items():
            if k not in repeated_col and k not in ['Title', 'Topic', 'ID']:
                md_repr += f'**{k}**: {v.replace("'", "\\'")}\n\n'

        # handle repeated columns and references
        point_form_col = ['References', 'Function References', 'Observations']
        for k in repeated_col:
            if k not in point_form_col:
                for item in content[k]:
                    md_repr += self._get_md_representation(item, curr_level=curr_level + 1)
            else:
                md_repr += f'**{k}:**\n\n' + '\n'.join(f'  - {item}' for item in content[k]) + '\n\n'

        return md_repr
    
    # TBC_FIXME From checklist.py. To be refactored 
    @staticmethod
    def __filedump_check(output_path: str, exist_ok: bool):
        if not exist_ok and os.path.exists(output_path):
            raise FileExistsError("Output file already exists. Use `exist_ok=True` to overwrite.")
        return True

    # TBC_FIXME From checklist.py. To be refactored 
    def export_html(self, content: str, output_path: str, exist_ok: bool = False):
        self.__filedump_check(output_path, exist_ok)
        pypandoc.convert_text(content, 'html', format='md', outputfile=output_path)

    # TBC_FIXME From checklist.py. To be refactored 
    def export_pdf(self, content: str, output_path: str, exist_ok: bool = False):
        self.__filedump_check(output_path, exist_ok)
        pypandoc.convert_text(content, 'pdf', format='md', outputfile=output_path,
                              extra_args=['--pdf-engine=tectonic'])

    def export_evaluation_report(self, output_path, format='html', exist_ok: bool = False):
        """
        Export the test evaluation report
        """
        if self.evaluation_report is None:
            raise NotImplementedError(
                # TBC_FIXME
                "Evaluation report is not yet created. Please make sure the function `get_completeness_score` is run before calling this export function"
            )

        score = self.get_completeness_score(score_format='fraction')
        summary_df = self.evaluation_report[['ID', 'Title', 'is_Satisfied', 'n_files_tested']]
        details = self.evaluation_report[['ID', 'Title', 'Requirement', 'Observations', 'Function References']].to_dict(orient='records')

        export_content = dict()
        export_content['Title'] = 'Test Evaluation Report'
        export_content['Report Areas'] = []
        export_content['Report Areas'].append({'Title': 'Summary', 'Completeness Score': score, 'Completeness Score per Checklist Item': '\n\n' + summary_df.to_markdown(index=False)})
        export_content['Report Areas'].append({'Title': 'Details', 'Report Detail': details})
        if format=='html':
            self.export_html(self._get_md_representation(export_content, curr_level=1), output_path, exist_ok)
        elif format=='pdf':
            self.export_pdf(self._get_md_representation(export_content, curr_level=1), output_path, exist_ok)
        return

if __name__ == '__main__':
    def main(checklist_path, repo_path):
        test = TestEvaluator(repo_path)
        test.load_checklist(checklist_path)
        test.evaluate()
        test.get_completeness_score()

    fire.Fire(main)
