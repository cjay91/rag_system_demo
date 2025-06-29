from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
from state import State
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
import ast
from db import get_database

db = get_database()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # or "gpt-4o", "gpt-4-turbo", etc.
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

class UserInput(BaseModel):
    """Schema for parsing user-provided account information."""
    identifier: str = Field(description="Identifier, which can be a customer ID, email, or phone number.")

# Create a structured LLM that outputs responses conforming to the UserInput schema
structured_llm = llm.with_structured_output(schema=UserInput)

# System prompt for extracting customer identifier information
structured_system_prompt = """You are a customer service representative responsible for extracting customer identifier.
Only extract the customer's account information from the message history. 
If they haven't provided the information yet, return an empty string for the identifier."""

from typing import Optional 

# Helper function for customer identification
def get_customer_id_from_identifier(identifier: str) -> Optional[int]:
    """
    Retrieve Customer ID using an identifier, which can be a customer ID, email, or phone number.
    
    This function supports three types of identifiers:
    1. Direct customer ID (numeric string)
    2. Phone number (starts with '+')
    3. Email address (contains '@')
    
    Args:
        identifier (str): The identifier can be customer ID, email, or phone number.
    
    Returns:
        Optional[int]: The CustomerId if found, otherwise None.
    """
    # Check if identifier is a direct customer ID (numeric)
    if identifier.isdigit():
        return int(identifier)
    
    # Check if identifier is a phone number (starts with '+')
    elif identifier[0] == "+":
        query = f"SELECT CustomerId FROM Customer WHERE Phone = '{identifier}';"
        result = db.run(query)
        formatted_result = ast.literal_eval(result)
        if formatted_result:
            return formatted_result[0][0]
    
    # Check if identifier is an email address (contains '@')
    elif "@" in identifier:
        query = f"SELECT CustomerId FROM Customer WHERE Email = '{identifier}';"
        result = db.run(query)
        formatted_result = ast.literal_eval(result)
        if formatted_result:
            return formatted_result[0][0]
    
    # Return None if no match found
    return None 

def verify_info(state: State, config: RunnableConfig):
    """
    Verify the customer's account by parsing their input and matching it with the database.
    
    This node handles customer identity verification as the first step in the support process.
    It extracts customer identifiers (ID, email, or phone) from user messages and validates
    them against the database.
    
    Args:
        state (State): Current state containing messages and potentially customer_id
        config (RunnableConfig): Configuration for the runnable execution
        
    Returns:
        dict: Updated state with customer_id if verified, or request for more info
    """
    # Only verify if customer_id is not already set
    if state.get("customer_id") is None: 
        # System instructions for prompting customer verification
        system_instructions = """You are a music store agent, where you are trying to verify the customer identity 
        as the first step of the customer support process. 
        Only after their account is verified, you would be able to support them on resolving the issue. 
        In order to verify their identity, one of their customer ID, email, or phone number needs to be provided.
        If the customer has not provided their identifier, please ask them for it.
        If they have provided the identifier but cannot be found, please ask them to revise it."""

        # Get the most recent user message
        user_input = state["messages"][-1] 
    
        # Use structured LLM to parse customer identifier from the message
        parsed_info = structured_llm.invoke([SystemMessage(content=structured_system_prompt)] + [user_input])
    
        # Extract the identifier from parsed response
        identifier = parsed_info.identifier
    
        # Initialize customer_id as empty
        customer_id = ""
        
        # Attempt to find the customer ID using the provided identifier
        if (identifier):
            customer_id = get_customer_id_from_identifier(identifier)
    
        # If customer found, confirm verification and set customer_id in state
        if customer_id != "":
            intent_message = SystemMessage(
                content= f"Thank you for providing your information! I was able to verify your account with customer id {customer_id}."
            )
            return {
                  "customer_id": customer_id,
                  "messages" : [intent_message]
                  }
        else:
            # If customer not found, ask for correct information
            response = llm.invoke([SystemMessage(content=system_instructions)]+state['messages'])
            return {"messages": [response]}

    else: 
        # Customer already verified, no action needed
        pass

from langgraph.types import interrupt

def human_input(state: State, config: RunnableConfig):
    """
    Human-in-the-loop node that interrupts the workflow to request user input.
    
    This node creates an interruption point in the workflow, allowing the system
    to pause and wait for human input before continuing. It's typically used
    for customer verification or when additional information is needed.
    
    Args:
        state (State): Current state containing messages and workflow data
        config (RunnableConfig): Configuration for the runnable execution
        
    Returns:
        dict: Updated state with the user's input message
    """
    # Interrupt the workflow and prompt for user input
    user_input = interrupt("Please provide input.")
    
    # Return the user input as a new message in the state
    return {"messages": [user_input]}

# Conditional edge: should_interrupt
def should_interrupt(state: State, config: RunnableConfig):
    """
    Determines whether the workflow should interrupt and ask for human input.
    
    If the customer_id is present in the state (meaning verification is complete),
    the workflow continues. Otherwise, it interrupts to get human input for verification.
    """
    if state.get("customer_id") is not None:
        return "continue" # Customer ID is verified, continue to the next step (supervisor)
    else:
        return "interrupt" # Customer ID is not verified, interrupt for human input