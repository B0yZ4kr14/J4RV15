import psycopg2
import requests
import time
import subprocess

class MonitoringAgent:
    def __init__(self, config):
        self.config = config

    def health_check(self):
        results = [
            self._check_postgres(),
            self._check_ollama(),
            self._check_litellm(),
            self._check_mcp_servers(),
        ]
        overall_status = "OK" if all(r["status"] == "OK" for r in results) else "NEEDS_ATTENTION"
        return {"overall_status": overall_status, "health_results": results}

    def _check_postgres(self):
        try:
            start_time = time.time()
            conn = psycopg2.connect(**self.config["postgres"])
            conn.close()
            latency = (time.time() - start_time) * 1000
            return {"service": "PostgreSQL", "status": "OK", "details": "Conexão estabelecida com sucesso.", "latency_ms": round(latency)}
        except psycopg2.Error as e:
            return {"service": "PostgreSQL", "status": "ERROR", "details": str(e)}

    def _check_ollama(self):
        try:
            start_time = time.time()
            response = requests.get(self.config["ollama"]["api_url"])
            latency = (time.time() - start_time) * 1000
            if response.status_code == 200:
                return {"service": "Ollama API", "status": "OK", "details": "API respondeu com status 200 OK.", "latency_ms": round(latency)}
            return {"service": "Ollama API", "status": "ERROR", "details": f"API respondeu com status {response.status_code}."}
        except requests.RequestException as e:
            return {"service": "Ollama API", "status": "ERROR", "details": str(e)}

    def _check_litellm(self):
        try:
            start_time = time.time()
            response = requests.get(self.config["litellm"]["gateway_url"])
            latency = (time.time() - start_time) * 1000
            if response.status_code == 200:
                return {"service": "LiteLLM Gateway", "status": "OK", "details": "Gateway respondeu com status 200 OK.", "latency_ms": round(latency)}
            return {"service": "LiteLLM Gateway", "status": "ERROR", "details": f"Gateway respondeu com status {response.status_code}."}
        except requests.RequestException as e:
            return {"service": "LiteLLM Gateway", "status": "ERROR", "details": str(e)}

    def _check_mcp_servers(self):
        success_count = 0
        total_latency = 0
        for server in self.config["mcp_servers"]:
            try:
                start_time = time.time()
                response = requests.get(server["url"])
                total_latency += (time.time() - start_time) * 1000
                if response.status_code == 200:
                    success_count += 1
            except requests.RequestException:
                pass
        if success_count == len(self.config["mcp_servers"]):
            return {"service": "MCP Servers", "status": "OK", "details": f"Todos os {success_count} servidores MCP configurados estão respondendo.", "latency_ms": round(total_latency / success_count)}
        return {"service": "MCP Servers", "status": "ERROR", "details": f"{success_count}/{len(self.config['mcp_servers'])} servidores MCP estão respondendo."}
