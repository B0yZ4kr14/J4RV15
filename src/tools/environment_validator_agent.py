import subprocess
import sys
import os
import socket

class EnvironmentValidatorAgent:
    def __init__(self):
        pass

    def run_task(self, task: dict):
        action = task.get("action")
        if action == "validate_environment":
            return self.validate_environment()
        else:
            return {"status": "ERROR", "message": f"Ação desconhecida: {action}"}

    def _check_command_exists(self, cmd):
        try:
            subprocess.run(["which", cmd], check=True, capture_output=True, text=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _check_docker(self):
        if not self._check_command_exists("docker"):
            return {"component": "Docker", "status": "ERROR", "details": "Comando 'docker' não encontrado."}
        try:
            result = subprocess.run(["docker", "--version"], check=True, capture_output=True, text=True)
            version = result.stdout.strip()
            # Check if the docker daemon is running
            info_result = subprocess.run(["docker", "info"], check=True, capture_output=True, text=True, stderr=subprocess.PIPE)
            if "Server:" not in info_result.stdout:
                 return {"component": "Docker", "status": "ERROR", "details": "Docker Engine não está em execução."}
            return {"component": "Docker", "status": "OK", "details": f"{version} está em execução."}
        except subprocess.CalledProcessError as e:
            return {"component": "Docker", "status": "ERROR", "details": f"Docker Engine não está em execução: {e.stderr.strip()}"}

    def _check_python(self):
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 9:
                return {"component": "Python", "status": "OK", "details": f"Python {version.major}.{version.minor}.{version.micro} encontrado."}
            else:
                return {"component": "Python", "status": "ERROR", "details": f"Versão do Python é {version.major}.{version.minor}, mas é necessário >= 3.9."}
        except Exception as e:
            return {"component": "Python", "status": "ERROR", "details": str(e)}

    def _check_git(self):
        if not self._check_command_exists("git"):
            return {"component": "Git", "status": "ERROR", "details": "Comando 'git' não encontrado."}
        try:
            result = subprocess.run(["git", "--version"], check=True, capture_output=True, text=True)
            version = result.stdout.strip()
            return {"component": "Git", "status": "OK", "details": f"{version} encontrado."}
        except subprocess.CalledProcessError as e:
            return {"component": "Git", "status": "ERROR", "details": str(e)}

    def _check_permissions(self):
        if os.geteuid() == 0:
            return {"component": "Permissões", "status": "OK", "details": "Executando como root."}
        try:
            # Check for passwordless sudo
            subprocess.run(["sudo", "-n", "true"], check=True, capture_output=True, stderr=subprocess.DEVNULL)
            return {"component": "Permissões", "status": "OK", "details": "Privilégios de 'sudo' sem senha disponíveis."}
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {"component": "Permissões", "status": "NEEDS_ATTENTION", "details": "Executando como usuário não-root. Privilégios de 'sudo' podem ser necessários."}

    def _check_network(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return {"component": "Rede", "status": "OK", "details": "Conectividade com a internet estabelecida."}
        except OSError:
            return {"component": "Rede", "status": "ERROR", "details": "Sem conectividade com a internet."}

    def validate_environment(self):
        results = [
            self._check_docker(),
            self._check_python(),
            self._check_git(),
            self._check_permissions(),
            self._check_network(),
        ]
        
        overall_status = "OK"
        has_error = any(res["status"] == "ERROR" for res in results)
        has_attention = any(res["status"] == "NEEDS_ATTENTION" for res in results)

        if has_error:
            overall_status = "ERROR"
        elif has_attention:
            overall_status = "NEEDS_ATTENTION"

        return {
            "overall_status": overall_status,
            "validation_results": results
        }
