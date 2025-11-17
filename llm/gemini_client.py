import logging
from typing import Any, Dict, List
import google.generativeai as genai

class GeminiClient:
    """Client for Google Gemini API with function calling support"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.logger = logging.getLogger("gemini_client")
    
    async def generate_with_tools(
        self,
        prompt: str,
        tools: List[Any],
        context: Dict[str, Any],
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate response with tool calling capability
        
        Args:
            prompt: The main prompt
            tools: List of available tools
            context: Additional context
            temperature: Generation temperature
        
        Returns:
            Dict with 'text', 'tool_calls', and other metadata
        """
        try:
            # Convert tools to Gemini function declarations
            tool_declarations = self._convert_tools_to_functions(tools)
            
            # Generate with function calling
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                ),
                tools=tool_declarations if tool_declarations else None
            )
            
            # Parse response
            result = {
                "text": response.text if hasattr(response, 'text') else "",
                "tool_calls": [],
                "finish_reason": response.candidates[0].finish_reason if response.candidates else None
            }
            
            # Handle function calls
            if hasattr(response, 'parts'):
                for part in response.parts:
                    if hasattr(part, 'function_call'):
                        fc = part.function_call
                        result["tool_calls"].append({
                            "name": fc.name,
                            "args": dict(fc.args)
                        })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Gemini API error: {str(e)}")
            return {
                "text": f"Error: {str(e)}",
                "tool_calls": [],
                "error": str(e)
            }
    
    def _convert_tools_to_functions(self, tools: List) -> List:
        """Convert tool objects to Gemini function declarations"""
        declarations = []
        
        for tool in tools:
            if hasattr(tool, 'to_gemini_function'):
                declarations.append(tool.to_gemini_function())
        
        return declarations
