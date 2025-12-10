import subprocess
import sys
import os
import requests

class EnvironmentValidatorAgent:
    def validate(self):
        results = [
            self._validate_docker(),
            self._validate_python(),
            self._validate_git(),
            self._validate_permissions(),
            self._validate_network(),
        ]
        overall_status = "OK" if all(r["status"] == "OK" for r in results) else "NEEDS_ATTENTION"
        return {"overall_status": overall_status, "validation_results": results}

    def _run_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            return str(e)

    def _validate_docker(self):
        version = self._run_command("docker --version")
        if "Docker version" in version:
            return {"component": "Docker", "status": "OK", "details": version}
        return {"component": "Docker", "status": "ERROR", "details": "Docker não encontrado ou não está em execução."}

    def _validate_python(self):
        version = sys.version.split(" ")[0]
        if sys.version_info >= (3, 9):
            return {"component": "Python", "status": "OK", "details": f"Python {version} encontrado."}
        return {"component": "Python", "status": "ERROR", "details": f"Versão do Python ({version}) é incompatível. Requer >= 3.9."}

    def _validate_git(self):
        version = self._run_command("git --version")
        if "git version" in version:
            return {"component": "Git", "status": "OK", "details": version}
        return {"component": "Git", "status": "ERROR", "details": "Git não encontrado."}

    def _validate_permissions(self):
        if os.geteuid() == 0:
            return {"component": "Permissões", "status": "OK", "details": "Usuário possui privilégios de root."}
        return {"component": "Permissões", "status": "WARNING", "details": "Usuário não é root. Alguns comandos podem exigir 'sudo'."}

    def _validate_network(self):
        try:
            requests.get("http://www.google.com", timeout=5)
            return {"component": "Rede", "status": "OK", "details": "Conectividade com a internet estabelecida."}
        except requests.ConnectionError:
            return {"component": "Rede", "status": "ERROR", "details": "Sem conectividade com a internet."}
