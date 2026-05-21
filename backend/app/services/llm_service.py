"""LLM service for generating grounded answers from retrieved context."""

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class LLMService:
    """Generate answers using a local Ollama LLM with grounded context."""

    def __init__(self, ollama_base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        """Initialize LLM service with Ollama endpoint and model name.
        
        Args:
            ollama_base_url: Base URL of Ollama API (default: http://localhost:11434)
            model: Model name to use (default: llama3.2)
        """
        self.ollama_base_url = ollama_base_url
        self.model = model
        self.generate_endpoint = f"{ollama_base_url}/api/generate"
        self._is_available = None

    def _build_prompt(self, question: str, context: str) -> str:
        """Build the prompt with system instruction and grounded context.
        
        Args:
            question: User's question
            context: Retrieved document context
            
        Returns:
            Formatted prompt for the LLM
        """
        system_instruction = (
            "You are a grounded document question-answering assistant. "
            "Use only the provided context. "
            "Do not use outside knowledge. "
            "If the context is insufficient to answer, say: "
            '"I don\'t have enough information in the uploaded documents to answer that." '
            "Keep your answer concise and technically accurate."
        )

        prompt = f"""System Instruction:
{system_instruction}

Question:
{question}

Context:
{context}

Answer:"""
        return prompt

    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible.
        
        Returns:
            True if Ollama is available, False otherwise
        """
        if self._is_available is not None:
            return self._is_available

        try:
            response = requests.get(
                f"{self.ollama_base_url}/api/tags",
                timeout=2
            )
            self._is_available = response.status_code == 200
            return self._is_available
        except (requests.RequestException, Exception):
            self._is_available = False
            return False

    def generate_answer(self, question: str, context: str) -> Optional[str]:
        """Generate an answer from question and context using Ollama LLM.
        
        Args:
            question: User's question
            context: Retrieved document context (chunks concatenated)
            
        Returns:
            Generated answer, or None if Ollama is unavailable
        """
        if not context or not context.strip():
            return None

        if not self._check_ollama_available():
            logger.warning(
                f"Ollama not available at {self.ollama_base_url}. "
                "Falling back to retrieved context."
            )
            return None

        prompt = self._build_prompt(question, context)

        try:
            response = requests.post(
                self.generate_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,  # Low temperature for consistency
                },
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            generated_text = result.get("response", "").strip()

            if generated_text:
                return generated_text
            else:
                logger.warning("Ollama returned empty response")
                return None

        except requests.exceptions.Timeout:
            logger.warning(f"Ollama request timeout for model {self.model}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Ollama HTTP error: {e}")
            return None
        except (requests.RequestException, ValueError) as e:
            logger.warning(f"Ollama request failed: {e}")
            return None

    def is_available(self) -> bool:
        """Check if Ollama service is available.
        
        Returns:
            True if Ollama is accessible, False otherwise
        """
        return self._check_ollama_available()
