import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adicionar o diretório do agente ao path para importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'tools')))

from environment_validator_agent import EnvironmentValidatorAgent

class TestEnvironmentValidatorAgent(unittest.TestCase):

    def setUp(self):
        self.agent = EnvironmentValidatorAgent()

    @patch('subprocess.run')
    def test_check_docker_success(self, mock_subprocess_run):
        # Configura o mock para simular o Docker instalado e em execução
        mock_subprocess_run.side_effect = [
            MagicMock(stdout='Docker version 20.10.7, build f0df350', returncode=0),
            MagicMock(stdout='Server:\n Version:      20.10.7', returncode=0)
        ]
        result = self.agent._check_docker()
        self.assertEqual(result['status'], 'OK')
        self.assertIn('Docker version 20.10.7', result['details'])

    @patch('subprocess.run')
    def test_check_docker_not_found(self, mock_subprocess_run):
        # Simula o comando 'which' falhando
        mock_subprocess_run.side_effect = FileNotFoundError
        result = self.agent._check_docker()
        self.assertEqual(result['status'], 'ERROR')
        self.assertEqual(result['details'], "Comando 'docker' não encontrado.")

    @patch('sys.version_info', (3, 10, 0))
    def test_check_python_success(self):
        result = self.agent._check_python()
        self.assertEqual(result['status'], 'OK')
        self.assertIn('Python 3.10.0', result['details'])

    @patch('sys.version_info', (3, 8, 0))
    def test_check_python_failure(self):
        result = self.agent._check_python()
        self.assertEqual(result['status'], 'ERROR')
        self.assertIn('necessário >= 3.9', result['details'])

    @patch('subprocess.run')
    def test_check_git_success(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(stdout='git version 2.30.1', returncode=0)
        result = self.agent._check_git()
        self.assertEqual(result['status'], 'OK')
        self.assertIn('git version 2.30.1', result['details'])

    @patch('os.geteuid', return_value=0)
    def test_check_permissions_root(self, mock_geteuid):
        result = self.agent._check_permissions()
        self.assertEqual(result['status'], 'OK')
        self.assertEqual(result['details'], 'Executando como root.')

    @patch('os.geteuid', return_value=1000)
    @patch('subprocess.run')
    def test_check_permissions_sudo(self, mock_subprocess_run, mock_geteuid):
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        result = self.agent._check_permissions()
        self.assertEqual(result['status'], 'OK')
        self.assertEqual(result['details'], "Privilégios de 'sudo' sem senha disponíveis.")

    @patch('socket.create_connection')
    def test_check_network_success(self, mock_create_connection):
        mock_create_connection.return_value = None
        result = self.agent._check_network()
        self.assertEqual(result['status'], 'OK')

    @patch('socket.create_connection', side_effect=OSError)
    def test_check_network_failure(self, mock_create_connection):
        result = self.agent._check_network()
        self.assertEqual(result['status'], 'ERROR')

if __name__ == '__main__':
    unittest.main()
