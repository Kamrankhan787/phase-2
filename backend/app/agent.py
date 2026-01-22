"""
OpenAI Agent Configuration for Todo Chatbot
Implements agent behavior rules and MCP tool integration
"""
from openai import OpenAI
from typing import List, Dict, Any, Optional
import json
import os
import logging
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from absolute path to ensure root .env is used
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

def get_openai_client() -> OpenAI:
    """
    Factory function to ensure OpenAI client is always initialized with a key.
    Supports OpenRouter, Groq, or OpenAI keys.
    """
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if openrouter_key:
        logger.info("Initializing client with OpenRouter API key")
        return OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Evolution Todo Chatbot",
            }
        )
    elif groq_key:
        logger.info("Initializing client with Groq API key")
        return OpenAI(
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1"
        )
    elif openai_key:
        logger.info("Initializing client with OpenAI API key")
        return OpenAI(api_key=openai_key)
    else:
        logger.error("No API key found (OPENROUTER, GROQ, or OPENAI)")
        raise ValueError("No compatible API key found in environment variables")


# Agent system instructions (Behavior Rules)
AGENT_INSTRUCTIONS = """You are a helpful AI assistant for managing todo tasks. Follow these rules strictly:

1. **Intent Inference**: Always understand the user's intent before responding.
2. **Tool Usage**: Never manipulate tasks directly. Always use the provided MCP tools.
3. **Parameter Validation**: If required parameters are missing, ask a clarifying question.
4. **Confirmation**: After every tool call, confirm the action in natural language.
5. **Error Handling**: On errors (e.g., task not found), respond politely and suggest next steps.

Available Tools:
- add_task: Create a new task (triggers: create/add/remember)
- list_tasks: Retrieve tasks (triggers: list/show/see)
- complete_task: Mark task as complete (triggers: done/complete/finished)
- delete_task: Remove a task (triggers: delete/remove/cancel)
- update_task: Modify task title or description (triggers: update/change/rename)

Always be friendly, concise, and helpful."""

# MCP Tool definitions for OpenAI function calling
MCP_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional)"
                    }
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve tasks from the user's list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by status (default: all)"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Remove a task from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Modify task title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]

async def run_agent(messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
    """
    Run the OpenAI agent with conversation history
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        user_id: User identifier for tool calls
    
    Returns:
        {
            "response": str,
            "tool_calls": List[Dict],
            "finish_reason": str
        }
    
    Raises:
        Exception: If OpenAI API call fails or tool execution fails
    """
    # Validate inputs
    if not messages:
        raise ValueError("Messages list cannot be empty")
    
    if not user_id:
        raise ValueError("user_id is required")
    
    # Prepend system message
    full_messages = [
        {"role": "system", "content": AGENT_INSTRUCTIONS}
    ] + messages
    
    logger.info(f"Running agent with {len(messages)} messages for user {user_id}")
    
    # Robust Initialization: Get client specifically for this run
    try:
        openai_client = get_openai_client()
    except ValueError as e:
        logger.critical(f"Agent failed to start: {str(e)}")
        raise e

    # Determine model name based on which provider is active
    using_openrouter = os.getenv("OPENROUTER_API_KEY") is not None
    using_groq = os.getenv("GROQ_API_KEY") is not None
    
    if using_openrouter:
        model_name = "google/gemini-2.0-flash-001"
    elif using_groq:
        model_name = "llama-3.3-70b-versatile"
    else:
        model_name = "gpt-4o"
    
    # Initial agent call with error handling
    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=full_messages,
            tools=MCP_TOOLS,
            tool_choice="auto"
        )
    except Exception as openai_error:
        logger.error(f"OpenAI API call failed: {str(openai_error)}")
        raise Exception(f"OpenAI API error: {str(openai_error)}")
    
    assistant_message = response.choices[0].message
    tool_calls_made = []
    
    # Handle tool calls with individual error boundaries
    if assistant_message.tool_calls:
        # Import MCP tools
        from .mcp_server import (
            add_task, list_tasks, complete_task, delete_task, update_task
        )
        
        tool_map = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task
        }
        
        # Execute each tool call with error boundary
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            
            try:
                function_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as json_error:
                logger.error(f"Failed to parse tool arguments: {str(json_error)}")
                # Add error to messages
                full_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps({
                        "error": "INVALID_ARGUMENTS",
                        "message": "Failed to parse tool arguments"
                    })
                })
                continue
            
            # Ensure user_id is included
            if "user_id" not in function_args:
                function_args["user_id"] = user_id
            
            # Execute tool with error boundary
            try:
                logger.info(f"Executing tool: {function_name} with args: {function_args}")
                tool_function = tool_map.get(function_name)
                
                if not tool_function:
                    raise ValueError(f"Unknown tool: {function_name}")
                
                result = await tool_function(**function_args)
                
                logger.info(f"Tool {function_name} executed successfully")
                
                tool_calls_made.append({
                    "tool": function_name,
                    "input": function_args,
                    "output": result,
                    "status": "success"
                })
                
                # Add tool response to messages
                full_messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call.model_dump()]
                })
                full_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
                
            except ValueError as tool_error:
                # Tool-specific error (e.g., task not found)
                logger.warning(f"Tool {function_name} failed: {str(tool_error)}")
                
                error_response = {
                    "error": "TOOL_EXECUTION_FAILED",
                    "message": str(tool_error),
                    "recoverable": True
                }
                
                tool_calls_made.append({
                    "tool": function_name,
                    "input": function_args,
                    "output": error_response,
                    "status": "failed"
                })
                
                full_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(error_response)
                })
                
            except Exception as unexpected_error:
                # Unexpected error in tool execution
                logger.exception(f"Unexpected error in tool {function_name}: {str(unexpected_error)}")
                
                error_response = {
                    "error": "UNEXPECTED_TOOL_ERROR",
                    "message": f"Tool execution failed: {str(unexpected_error)}",
                    "recoverable": True
                }
                
                tool_calls_made.append({
                    "tool": function_name,
                    "input": function_args,
                    "output": error_response,
                    "status": "error"
                })
                
                full_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(error_response)
                })
        
        # Get final response after tool execution
        try:
            using_openrouter = os.getenv("OPENROUTER_API_KEY") is not None
            using_groq = os.getenv("GROQ_API_KEY") is not None
            
            if using_openrouter:
                model_name = "google/gemini-2.0-flash-001"
            elif using_groq:
                model_name = "llama-3.3-70b-versatile"
            else:
                model_name = "gpt-4o"
                
            final_response = openai_client.chat.completions.create(
                model=model_name,
                messages=full_messages
            )
            final_message = final_response.choices[0].message.content
        except Exception as final_error:
            logger.error(f"Failed to get final response: {str(final_error)}")
            raise Exception(f"Failed to generate final response: {str(final_error)}")
    else:
        final_message = assistant_message.content
    
    if not final_message:
        logger.warning("Agent returned empty response")
        final_message = "I'm sorry, I couldn't process your request. Please try again."
    
    logger.info(f"Agent execution completed with {len(tool_calls_made)} tool calls")
    
    return {
        "response": final_message,
        "tool_calls": tool_calls_made,
        "finish_reason": response.choices[0].finish_reason
    }
