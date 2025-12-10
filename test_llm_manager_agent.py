
import unittest
from unittest.mock import MagicMock, patch
from llm_manager_agent import LLMManagerAgent

class TestLLMManagerAgent(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente de teste antes de cada teste."""
        self.mock_db_params = {
            'dbname': 'test_db',
            'user': 'test_user',
            'password': 'test_password',
            'host': 'localhost',
            'port': '5432'
        }

    @patch('llm_manager_agent.psycopg2.connect')
    def test_get_hardware_tier_cpu_only(self, mock_connect):
        """Testa a detecção de tier para um ambiente somente com CPU."""
        mock_system_context = {
            "hardware": {
                "cpu": {"cores": 8}
            }
        }
        agent = LLMManagerAgent(db_params=self.mock_db_params, system_context=mock_system_context)
        self.assertEqual(agent._get_hardware_tier(), "CPU")

    @patch('llm_manager_agent.psycopg2.connect')
    def test_get_hardware_tier_gpu_small(self, mock_connect):
        """Testa a detecção de tier para uma GPU pequena (VRAM < 16GB)."""
        mock_system_context = {
            "hardware": {
                "gpu": {"vram_gb": 12}
            }
        }
        agent = LLMManagerAgent(db_params=self.mock_db_params, system_context=mock_system_context)
        self.assertEqual(agent._get_hardware_tier(), "GPU_SMALL")

    @patch('llm_manager_agent.psycopg2.connect')
    def test_get_hardware_tier_gpu_large(self, mock_connect):
        """Testa a detecção de tier para uma GPU grande (VRAM >= 16GB)."""
        mock_system_context = {
            "hardware": {
                "gpu": {"vram_gb": 24}
            }
        }
        agent = LLMManagerAgent(db_params=self.mock_db_params, system_context=mock_system_context)
        self.assertEqual(agent._get_hardware_tier(), "GPU_LARGE")

    @patch('llm_manager_agent.psycopg2.connect')
    def test_get_models_for_tier_cpu(self, mock_connect):
        """Testa se os modelos corretos são retornados para o tier CPU."""
        agent = LLMManagerAgent(db_params=self.mock_db_params, system_context={})
        models = agent._get_models_for_tier("CPU")
        self.assertIn({"name": "llama3.1:8b-instruct-q4_K_M", "family": "llama", "size": 5, "type": "local"}, models)

    @patch('llm_manager_agent.psycopg2.connect')
    def test_get_models_for_tier_gpu_small(self, mock_connect):
        """Testa se os modelos corretos são retornados para o tier GPU_SMALL."""
        agent = LLMManagerAgent(db_params=self.mock_db_params, system_context={})
        models = agent._get_models_for_tier("GPU_SMALL")
        self.assertIn({"name": "codellama:13b", "family": "codellama", "size": 7.4, "type": "local"}, models)

    @patch('llm_manager_agent.psycopg2.connect')
    def test_get_models_for_tier_gpu_large(self, mock_connect):
        """Testa se os modelos corretos são retornados para o tier GPU_LARGE."""
        agent = LLMManagerAgent(db_params=self.mock_db_params, system_context={})
        models = agent._get_models_for_tier("GPU_LARGE")
        self.assertIn({"name": "llama3.1:70b-instruct-q4_K_M", "family": "llama", "size": 42, "type": "local"}, models)

if __name__ == '__main__':
    unittest.main()
