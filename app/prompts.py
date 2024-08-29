from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import OpenAIEmbeddings
from decouple import config
import tiktoken

from app.schemas import ExperienceSchema


def get_number_of_tokens(documents):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoding.encode(documents)
    number_tokens = len(encoding.encode(documents))
    return number_tokens


async def rewrite_experience(responsibilities, job_position):
    experience_output_parser = PydanticOutputParser(pydantic_object=ExperienceSchema)
    experience_format_instructions = experience_output_parser.get_format_instructions()
    experience_template = """
        This is a list of responsibility in {responsibilities}. For each responsibility in {responsibilities}, 
        rewrite the responsibility to align with the {job_position}. 

        The list of responsibilities is: {responsibilities}
        The job_position is: {job_position}

        Format instructions: {format_instructions}

        """
    experience_prompt = PromptTemplate(
        template=experience_template,
        input_variables=["responsibilities", "job_position"],
        partial_variables={"format_instructions": experience_format_instructions}
    )
    llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), temperature=0.0,
                     model_name='gpt-4-0125-preview')
    the_experience = experience_prompt | llm | experience_output_parser
    response = the_experience.invoke({"responsibilities": responsibilities, "job_position": job_position})

    return response


async def write_responsibilities_for_experience(job_position):
    experience_output_parser = PydanticOutputParser(pydantic_object=ExperienceSchema)
    experience_format_instructions = experience_output_parser.get_format_instructions()
    experience_template = """
        Based on this experience in {job_position}, write the responsibilities 
        
        The job_position is: {job_position}  

        Format instructions: {format_instructions}

        """
    experience_prompt = PromptTemplate(
        template=experience_template,
        input_variables=["job_position"],
        partial_variables={"format_instructions": experience_format_instructions}
    )
    llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), temperature=0.0,
                     model_name='gpt-4-0125-preview')
    the_experience = experience_prompt | llm | experience_output_parser
    response = the_experience.invoke({"job_position": job_position})

    return response


